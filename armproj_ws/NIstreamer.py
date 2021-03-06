#!/usr/bin/env python

import nidaqmx as daq
import time
import warnings
class ni_stream(object):
    def __init__(self,name=None):
        try:
            self.daqtask=daq.Task(name)
        except:
            raise ValueError('Unable to connect to DAQ device')      
    def start_streaming(self,channels,callback,ni_fs=1000): 
        """
        defines channels to read, write a callback function to do signal processing
        default frame rate =1k Hz

        channels: list of strings eg. ["Dev1/ai0","Dev1/ai1"]
        callback: can take multiple callback functions as list
        ni_fs: sample rate
        """

        
        for chn in channels:
            self.daqtask.ai_channels.add_ai_voltage_chan(chn)
        self.daqtask.timing.cfg_samp_clk_timing(ni_fs)
        while True:
            # now=time.time()
            
            raw_sig=self.daqtask.read()
            callback(raw_sig)

            # elapsed=time.time()-now
            # try:
            #     time.sleep(period-elapsed)
            # except:
            #     warnings.warn('System cannot handle such high frame rate, lower the desired frequency or simplify your callback fucntion')
            #     continue
    def stop_streaming(self):
        self.daqtask.close()

def fake_streaming(channels,callback,ni_fs=1000):
    from math import sin
    import numpy as np
    period=1.0/ni_fs
    i=0
    while True:
        now=time.time()
        raw_sig=sin(2*np.pi*3*i)+sin(2*np.pi*0.5*i)
        callback([raw_sig,raw_sig])

        i+=period

        elapsed=time.time()-now
        try:
            time.sleep(period-elapsed)
        except:
            warnings.warn('System cannot handle such high frame rate, lower the desired frequency or simplify your callback fucntion')
            continue

        
