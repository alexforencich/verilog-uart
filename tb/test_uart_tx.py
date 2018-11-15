#!/usr/bin/env python
"""

Copyright (c) 2014-2017 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from myhdl import *
import os

import axis_ep
import uart_ep

module = 'uart_tx'
testbench = 'test_%s' % module

srcs = []

srcs.append("../rtl/%s.v" % module)
srcs.append("%s.v" % testbench)

src = ' '.join(srcs)

build_cmd = "iverilog -o %s.vvp %s" % (testbench, src)

def bench():

    # Inputs
    clk = Signal(bool(0))
    rst = Signal(bool(0))
    current_test = Signal(intbv(0)[8:])

    s_axis_tdata = Signal(intbv(0)[8:])
    s_axis_tvalid = Signal(bool(0))
    s_axis_tlast = Signal(bool(0))
    prescale = Signal(intbv(0)[16:])

    # Outputs
    s_axis_tready = Signal(bool(0))
    txd = Signal(bool(1))

    busy = Signal(bool(0))

    # sources and sinks
    source_pause = Signal(bool(0))

    source = axis_ep.AXIStreamSource()

    source_logic = source.create_logic(
        clk,
        rst,
        tdata=s_axis_tdata,
        tvalid=s_axis_tvalid,
        tready=s_axis_tready,
        pause=source_pause,
        name='source'
    )

    sink = uart_ep.UARTSink()

    sink_logic = sink.create_logic(
        clk,
        rst,
        rxd=txd,
        prescale=prescale,
        name='sink'
    )

    # DUT
    if os.system(build_cmd):
        raise Exception("Error running build command")
    
    dut = Cosimulation(
        "vvp -m myhdl %s.vvp -lxt2" % testbench,
        clk=clk,
        rst=rst,
        current_test=current_test,

        s_axis_tdata=s_axis_tdata,
        s_axis_tvalid=s_axis_tvalid,
        s_axis_tready=s_axis_tready,

        txd=txd,

        busy=busy,

        prescale=prescale
    )

    @always(delay(4))
    def clkgen():
        clk.next = not clk

    @instance
    def check():
        yield delay(100)
        yield clk.posedge
        rst.next = 1
        yield clk.posedge
        rst.next = 0
        yield clk.posedge
        yield delay(100)
        yield clk.posedge

        yield clk.posedge

        yield clk.posedge

        prescale.next = 1;

        yield clk.posedge

        yield clk.posedge
        print("test 1: walk")
        current_test.next = 1

        source.write(b'\x00\x01\x02\x04\x08\x10\x20\x40\x80')
        yield clk.posedge

        yield s_axis_tvalid.negedge

        yield delay(1000)

        yield clk.posedge

        rx_data = bytearray(sink.read())
        print(rx_data)
        assert rx_data == b'\x00\x01\x02\x04\x08\x10\x20\x40\x80'

        yield clk.posedge
        print("test 2: walk 2")
        current_test.next = 2

        source.write(b'\x00\x01\x03\x07\x0F\x1F\x3F\x7F\xFF')
        yield clk.posedge

        yield s_axis_tvalid.negedge

        yield delay(1000)

        yield clk.posedge

        rx_data = bytearray(sink.read())
        print(rx_data)
        assert rx_data == b'\x00\x01\x03\x07\x0F\x1F\x3F\x7F\xFF'

        yield delay(100)

        raise StopSimulation

    return instances()

def test_bench():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sim = Simulation(bench())
    sim.run()

if __name__ == '__main__':
    print("Running test...")
    test_bench()

