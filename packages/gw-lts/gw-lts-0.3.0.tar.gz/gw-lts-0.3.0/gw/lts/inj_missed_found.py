#!/usr/bin/env python3

from optparse import OptionParser
import os
import sys
import json
import yaml
import logging

from collections import defaultdict, deque

from confluent_kafka import Producer
from cronut import App
from cronut.utils import uriparse

from ligo.lw import lsctables

from lal import GPSTimeNow

from ligo.scald.io import influx, kafka

from gw.lts import utils

def parse_command_line():
	parser = utils.add_general_opts()

	parser.add_option('--far-threshold', default=2.314e-5, help = 'far threshold for missed vs found injections. Default is 2 per day.')
	parser.add_option("--scald-config", metavar = "file", help = "sets ligo-scald options based on yaml configuration.")
	opts, args = parser.parse_args()

	return opts, args


class InjMissedFound(object):
	def __init__(self, options):
		self.tag = options.tag
		self.kafka_server = options.kafka_server
		self.topics = options.input_topic
		self.datasource = options.data_source
		self.far_threshold = float(options.far_threshold)

		# set up producer
		self.client = kafka.Client(f'kafka://{self.tag}@{self.kafka_server}')
		self.output_topics = (
			"H1_injsnr", "L1_injsnr", "V1_injsnr",
			"H1_recsnr", "L1_recsnr", "V1_recsnr",
			"inj_snr", "decisive_snr",
			"injchi_eff", "recchi_eff", "injchi_p",
			"combined_far", "likelihood", "snr"
		)
		trigger = self.new_trigger()
		for topic in self.output_topics:
			if not topic in trigger.keys():
				raise ValueError("Output topics must be a subset of keys stored in the trigger object.")

		# set up dicts to store trigger information
		self.routes = ['triggers', 'missed_triggers']
		self.triggers = {route: defaultdict(lambda: {'time': deque(maxlen = 1000), 'fields': defaultdict(lambda: deque(maxlen=1000))}) for route in self.routes}
		self.last_trigger_snapshot = None

		# set up influx configuration
		with open(options.scald_config, 'r') as f:
			config = yaml.safe_load(f)

		self.influx_sink = influx.Aggregator(**config["backends"]["default"])
		self.influx_sink.load(path=options.scald_config)

		# create a job service using cronut
		self.app = App('inj_missed_found', broker=f'kafka://{self.tag}_inj_missed_found@{self.kafka_server}')

		# subscribes to a topic
		@self.app.process(self.topics)
		def process(message): 
			mtopic = message.topic().split('.')[-1]
			mpipeline = message.topic().split('.')[0]
			mkey = utils.parse_msg_key(message)

			# these are injections that were never associated
			# with an event from the search
			if mtopic == 'missed_inj':
				# unpack information from the message
				injection = json.loads(message.value())
				sim_file = utils.load_xml(injection['sim'])
				on_ifos = self.sort_ifos(injection['onIFOs'])

				# the event is automatically missed and 
				# there are no participating IFOs
				is_recovered = 'missed'
				part_ifos = 'None'

				# process injection information from 
				# the sim inspiral table
				time, source, trigger_dict = self.process_injection(sim_file, on_ifos)
				logging.debug(f'{mpipeline}: {source} injection from time {time} {is_recovered.upper()}: no associated event message received.')

				# send time series data to kafka
				self.produce_output(time, trigger_dict, prefix = f'{mpipeline}.{self.tag}.testsuite', tags = [source, is_recovered])

				# store trigger data to influx
				self.store_triggers(time, trigger_dict, route='missed_triggers', tags = (on_ifos, part_ifos))

			# these are injections that were associated with
			# a recovered event from the search on gracedb
			elif mtopic == 'events':
				# unpack information from the message
				event = json.loads(message.value())
				coinc_file = utils.load_xml(event['coinc'])
				far = event['far']
				time = event['time'] + event['time_ns'] * 10**-9.
				on_ifos = self.sort_ifos(event['onIFOs'])

				# determine if the injection was missed or found
				# by getting the far of the recovered event
				is_recovered = 'found' if far < self.far_threshold else 'missed'

				# process the injection and recovered event information
				# from the tables in the coinc file
				source, part_ifos, trigger_dict = self.process_event(coinc_file, on_ifos)
				logging.debug(f'{mpipeline}: {source} event from time {time} {is_recovered.upper()}: far = {far}.')

				# send time series data to kafka
				self.produce_output(time, trigger_dict, prefix = f'{mpipeline}.{self.tag}.testsuite', tags=[source, is_recovered])

				# store trigger data to influx
				self.store_triggers(time, trigger_dict, route='triggers', tags = (on_ifos, part_ifos))


	def start(self):
		# start up
		logging.info('Starting up...')
		self.app.start()


	def produce_output(self, time, dict, prefix = '', tags = []):
		output = defaultdict(lambda: {'time': [], 'data': []})

		for topic in self.output_topics:
			if dict[topic] is not None:
				output[topic] = {
					'time': [ time ],
					'data': [ dict[topic] ]
				}

		for topic, data in output.items():
			self.client.write(f'{prefix}.{topic}', data, tags = tags)
			logging.info(f'Sent msg to: {prefix}.{topic} with tags: {tags}')

		return


	def process_injection(self, xmldoc, on_ifos):
		trigger_dict = self.new_trigger()
		inj_snrs = defaultdict(lambda: None)

		# load sim inspiral table
		simtable = lsctables.SimInspiralTable.get_table(xmldoc)

		# get info from sim table
		time = simtable[0].geocent_end_time + 10.**-9 * simtable[0].geocent_end_time_ns
		trigger_dict["end"] = time
		inj_snrs['H1'] = simtable[0].alpha4
		inj_snrs['L1'] = simtable[0].alpha5
		inj_snrs['V1'] = simtable[0].alpha6

		for ifo in ('H1', 'L1', 'V1'):
			trigger_dict[f'{ifo}_injsnr'] = inj_snrs[ifo]

		net_snr = utils.network_snr(inj_snrs.values())
		trigger_dict["inj_snr"] = net_snr

		# add injection parameters to trigger dict
		for attr in ("mass1", "mass2", "spin1x", "spin1y", "spin1z", "spin2x", "spin2y", "spin2z"):
			try:
				trigger_dict[f'sim_{attr}'] = float(simtable.getColumnByName(attr)[0])
			except TypeError:
				pass

		source = utils.source_tag(simtable)

		# add decisive snr to trigger dict
		dec_snr = utils.decisive_snr(inj_snrs, on_ifos)
		trigger_dict['decisive_snr'] = dec_snr

		# add effective spin parameters
		chi_eff = utils.effective_spin(trigger_dict['sim_mass1'], trigger_dict['sim_mass2'], trigger_dict['sim_spin1z'], trigger_dict['sim_spin2z'])
		chi_p = utils.effective_precession_spin(trigger_dict['sim_mass1'], trigger_dict['sim_mass2'], trigger_dict['sim_spin1x'], trigger_dict['sim_spin1y'], trigger_dict['sim_spin2x'], trigger_dict['sim_spin2y'])

		trigger_dict[f"injchi_eff"] = chi_eff
		trigger_dict[f"injchi_p"] = chi_p

		return time, source, trigger_dict


	def process_event(self, coinc_file, on_ifos):
		# get inj SNR information
		time, source, trigger_dict = self.process_injection(coinc_file, on_ifos)

		part_ifos = ''

		# load tables
		coinctable = lsctables.CoincInspiralTable.get_table(coinc_file)
		sngltable = lsctables.SnglInspiralTable.get_table(coinc_file)
		coinceventtable = lsctables.CoincTable.get_table(coinc_file)

		# get info from coinc table
		trigger_dict["end"] = coinctable[0].end_time + 10.**-9 * coinctable[0].end_time_ns
		for attr in ("combined_far", "snr", "false_alarm_rate"):
			try:
				trigger_dict[attr] = float(coinctable.getColumnByName(attr)[0])
			except TypeError:
				pass

		# get likelihood from coinc event table
		try:
			trigger_dict["likelihood"] = float(coinceventtable.getColumnByName("likelihood")[0])
		except TypeError:
			pass

		# get info from sngl inspiral table
		for r in sngltable:
			if r.snr:
				trigger_dict[f'{r.ifo}_recsnr'] = float(r.snr)

			# keep track of participating IFOs
			if r.snr >= 4.:
				part_ifos += r.ifo

			for attr in ("chisq", "mass1", "mass2", "spin1x", "spin1y", "spin1z", "spin2x", "spin2y", "spin2z", "coa_phase"):
				if getattr(r, attr):
					if not trigger_dict[f'sngl_{attr}']:
						trigger_dict[f'sngl_{attr}'] = float(getattr(r, attr))

		part_ifos = self.sort_ifos(part_ifos)

		rec_chi_eff = utils.effective_spin(trigger_dict['sngl_mass1'], trigger_dict['sngl_mass2'], trigger_dict['sngl_spin1z'], trigger_dict['sngl_spin2z'])
		trigger_dict["recchi_eff"] = rec_chi_eff

		return source, part_ifos, trigger_dict

	def store_triggers(self, time, data, route=None, tags=None):
		self.triggers[route][tags]['time'].append(time)
		this_triggers = self.triggers[route][tags]['fields']
		for key, value in data.items():
			this_triggers[key].append(value)

		# output data to influx every 100 seconds
		if not self.last_trigger_snapshot or (float(GPSTimeNow()) - self.last_trigger_snapshot >= 100.):
			self.last_reduce_time = float(GPSTimeNow())

			# cast data from deques to lists to output
			outdata = {}
			for key in self.triggers:
				outdata[key] = {}
				for tag in self.triggers[key]:
					outdata[key][tag] = {
						'time': list(self.triggers[key][tag]['time']),
						'fields': {
							dataname: list(datadeq) for dataname, datadeq in self.triggers[key][tag]['fields'].items()
						}
					}

			## First store triggers, these get aggregated by combined_far
			if outdata["triggers"]:
				logging.debug("Writing triggers to influx...")
				self.influx_sink.store_columns("triggers", outdata["triggers"], aggregate = "min")

			## Then store missed_triggers, these do not get aggregated
			if outdata["missed_triggers"]:
				logging.debug("Writing missed triggers to influx...")
				self.influx_sink.store_columns("missed_triggers", outdata["missed_triggers"], aggregate = None)

	@staticmethod
	def sort_ifos(string):
		if not string:
			return 'None'
		else:
			# return the sorted string of IFOs in alphabetical order
			list = string.split(',')
			list.sort()
			return ','.join(list)

	@staticmethod
	def new_trigger():
		dict = {}
		columns = (
			'combined_far',
			'likelihood',
			'snr',
			'inj_snr',
			'decisive_snr',
			'H1_injsnr',
			'L1_injsnr',
			'V1_injsnr',
			'H1_recsnr',
			'L1_recsnr',
			'V1_recsnr',
			'chisq',
			'end',
			'sim_mass1',
			'sim_mass2',
			'sim_spin1x',
			'sim_spin1y',
			'sim_spin1z',
			'sim_spin2x',
			'sim_spin2y',
			'sim_spin2z',
			'sngl_mass1',
			'sngl_mass2',
			'sngl_spin1x',
			'sngl_spin1y',
			'sngl_spin1z',
			'sngl_spin2x',
			'sngl_spin2y',
			'sngl_spin2z',
			'sngl_chisq',
			'sngl_coa_phase',
			'injchi_p',
			'injchi_eff',
			'recchi_eff',
		)
		for col in columns:
			dict[col] = None

		return dict


def main():
	# parse options from command line
	opts, args = parse_command_line()

	# set up logging
	utils.set_up_logger(opts.verbose)

	# initialize the processor
	processor = InjMissedFound(opts)
	processor.start()

if __name__ == '__main__':
	main()
