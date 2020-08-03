#!/usr/bin/env python

import visa
import argparse

rm=0 #VISA resource manager
ps=0 #power supply instance

def check_inst():
    global ps
    x = ps.query('*IDN?')
    print(x)
    y = x.split(", ")
    if y[0] != "Keithley instruments" or y[1] != "2231A-30-3":
        raise Exception("This is not Keithley 2231A")

def connect():
    global rm, ps
    rm = visa.ResourceManager()
    #print rm.list_resources()
    ps = rm.open_resource('ASRL/dev/ttyUSB0::INSTR', baud_rate=9600, data_bits=8)
    ps.write_termination = '\n'
    ps.read_termination = '\n'
    ps.write('SYST:REM') #Enable remote Contol

def disconnect():
    global rm, ps
    ps.write("SYST:LOC")
    ps.close
    rm.close

def channel(ch):
    global ps
    print("Select channel %s" % ch)
    ps.write("INST:NSEL %s" % ch)

def voltage(volt):
    global ps
    print("Set voltage %f" % volt)
    ps.write("VOLT %f" % volt)

def current(amp):
    global ps
    print("Set current %f" % amp)
    ps.write("CURR %f" % amp)

def output(onoff):
    global ps
    print("Set output %d" % onoff)
    ps.write("OUTP %d" % onoff)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--channel", help="Select Channel", choices=["1", "2", "3"], required=True)
    parser.add_argument("-v", "--voltage", help="Set Voltage", type=float)
    parser.add_argument("-a", "--ampere", help="Set Current limit", type=float)
    parser.add_argument("-o", "--output", help="Output on/off", choices=["0", "1"])
    args = parser.parse_args()
    #print args
    connect()
    check_inst()
    channel(args.channel)

    if args.voltage is not None:
        voltage(args.voltage)
    if args.ampere is not None:
        current(args.ampere)
    if args.output is not None:
        output(args.output)

    disconnect()
