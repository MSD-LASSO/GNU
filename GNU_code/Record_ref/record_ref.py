#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Record Ref
# GNU Radio version: 3.7.13.5
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time


class record_ref(gr.top_block):

    def __init__(self, center_freq=162000000, channel_freq=162400000, file_loc='', num_samples=10000000, samp_rate=20000000):
        gr.top_block.__init__(self, "Record Ref")

        ##################################################
        # Parameters
        ##################################################
        self.center_freq = center_freq
        self.channel_freq = channel_freq
        self.file_loc = file_loc
        self.num_samples = num_samples
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.channel_width = channel_width = 200e3

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'hackrf=0,bias=1' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(0, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, num_samples)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, file_loc, False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, center_freq - channel_freq, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_head_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_multiply_xx_0, 0))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
        self.analog_sig_source_x_0.set_frequency(self.center_freq - self.channel_freq)

    def get_channel_freq(self):
        return self.channel_freq

    def set_channel_freq(self, channel_freq):
        self.channel_freq = channel_freq
        self.analog_sig_source_x_0.set_frequency(self.center_freq - self.channel_freq)

    def get_file_loc(self):
        return self.file_loc

    def set_file_loc(self, file_loc):
        self.file_loc = file_loc
        self.blocks_file_sink_1.open(self.file_loc)

    def get_num_samples(self):
        return self.num_samples

    def set_num_samples(self, num_samples):
        self.num_samples = num_samples
        self.blocks_head_0.set_length(self.num_samples)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_channel_width(self):
        return self.channel_width

    def set_channel_width(self, channel_width):
        self.channel_width = channel_width


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--center-freq", dest="center_freq", type="intx", default=162000000,
        help="Set center_freq [default=%default]")
    parser.add_option(
        "", "--channel-freq", dest="channel_freq", type="intx", default=162400000,
        help="Set channel_freq [default=%default]")
    parser.add_option(
        "", "--file-loc", dest="file_loc", type="string", default='',
        help="Set file_loc [default=%default]")
    parser.add_option(
        "", "--num-samples", dest="num_samples", type="intx", default=10000000,
        help="Set num_samples [default=%default]")
    parser.add_option(
        "", "--samp-rate", dest="samp_rate", type="intx", default=20000000,
        help="Set samp_rate [default=%default]")
    return parser


def main(top_block_cls=record_ref, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(center_freq=options.center_freq, channel_freq=options.channel_freq, file_loc=options.file_loc, num_samples=options.num_samples, samp_rate=options.samp_rate)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()