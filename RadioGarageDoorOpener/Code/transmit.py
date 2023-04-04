import os
import time
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio import digital
from gnuradio import uhd

# Set the parameters for the USRP
samp_rate = 2e6
center_freq = 315e6
gain = 30
tx_freq = 315e6
tx_gain = 30

# Create a USRP source and set the parameters
src = uhd.usrp_source(device_addr="", stream_args=uhd.stream_args(cpu_format="fc32", channels=range(1)))
src.set_samp_rate(samp_rate)
src.set_center_freq(center_freq, 0)
src.set_gain(gain, 0)
# Create a USRP sink and set the parameters
tx = uhd.usrp_sink(device_addr="", stream_args=uhd.stream_args(cpu_format="fc32", channels=range(1)))
tx.set_samp_rate(samp_rate)
tx.set_center_freq(tx_freq, 0)
tx.set_gain(tx_gain, 0)

# Create a digital modulator
decoder = digital.gfsk_demod(samples_per_symbol=2, sensitivity=0.5)

tx_data = blocks.file_source(gr.sizeof_char, "/Recordings/")
tx_mod = digital.gfsk_mod(samples_per_symbol=2, sensitivity=0.5, bt=0.5)

tb = gr.top_block()

tb.connect(src, decoder)
tb.connect(decoder, tx)
tb.connect(tx_data, tx_mod, tx)

tb.start()

time.sleep(1)

tb.stop()

tb.wait()
