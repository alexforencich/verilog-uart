#!/usr/bin/env python
"""

Copyright (c) 2014-2016 Alex Forencich

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

try:
    from queue import Queue
except ImportError:
    from Queue import Queue

import axis_ep
import uart_ep

module = 'uart_rx'

srcs = []

srcs.append("../rtl/%s.v" % module)
srcs.append("test_%s.v" % module)

src = ' '.join(srcs)

build_cmd = "iverilog -o test_%s.vvp %s" % (module, src)

def dut_uart_rx(clk,
                 rst,
                 current_test,

                 output_axis_tdata,
                 output_axis_tvalid,
                 output_axis_tready,

                 rxd,

                 busy,
                 overrun_error,
                 frame_error,

                 prescale):

    if os.system(build_cmd):
        raise Exception("Error running build command")
    return Cosimulation("vvp -m myhdl test_%s.vvp -lxt2" % module,
                clk=clk,
                rst=rst,
                current_test=current_test,

                output_axis_tdata=output_axis_tdata,
                output_axis_tvalid=output_axis_tvalid,
                output_axis_tready=output_axis_tready,

                rxd=rxd,

                busy=busy,
                overrun_error=overrun_error,
                frame_error=frame_error,

                prescale=prescale)

def bench():

    # Inputs
    clk = Signal(bool(0))
    rst = Signal(bool(0))
    current_test = Signal(intbv(0)[8:])

    output_axis_tready = Signal(bool(0))
    rxd = Signal(bool(1))
    prescale = Signal(intbv(0)[16:])

    # Outputs
    output_axis_tdata = Signal(intbv(0)[8:])
    output_axis_tvalid = Signal(bool(0))

    busy = Signal(bool(0))
    overrun_error = Signal(bool(0))
    frame_error = Signal(bool(0))

    # sources and sinks
    source_queue = Queue()
    sink_queue = Queue()
    sink_pause = Signal(bool(0))

    source = uart_ep.UARTSource(clk,
                                rst,
                                txd=rxd,
                                prescale=prescale,
                                fifo=source_queue,
                                name='source')

    sink = axis_ep.AXIStreamSink(clk,
                                rst,
                                tdata=output_axis_tdata,
                                tvalid=output_axis_tvalid,
                                tready=output_axis_tready,
                                fifo=sink_queue,
                                pause=sink_pause,
                                name='sink')

    # DUT
    dut = dut_uart_rx(clk,
                        rst,
                        current_test,

                        output_axis_tdata,
                        output_axis_tvalid,
                        output_axis_tready,

                        rxd,

                        busy,
                        overrun_error,
                        frame_error,

                        prescale)

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

        source_queue.put(bytearray(b'\x00\x01\x02\x04\x08\x10\x20\x40\x80'))
        yield clk.posedge

        yield delay(5000)

        yield delay(1000)

        yield clk.posedge

        rx_data = b''
        while not sink_queue.empty():
            rx_data += bytearray(sink_queue.get())
        assert rx_data == b'\x00\x01\x02\x04\x08\x10\x20\x40\x80'

        yield clk.posedge
        print("test 2: walk 2")
        current_test.next = 2

        source_queue.put(bytearray(b'\x00\x01\x03\x07\x0F\x1F\x3F\x7F\xFF'))
        yield clk.posedge

        yield delay(5000)

        yield delay(1000)

        yield clk.posedge

        rx_data = b''
        while not sink_queue.empty():
            rx_data += bytearray(sink_queue.get())
        assert rx_data == b'\x00\x01\x03\x07\x0F\x1F\x3F\x7F\xFF'

        yield delay(100)

        raise StopSimulation

    return dut, source, sink, clkgen, check

def test_bench():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sim = Simulation(bench())
    sim.run()

if __name__ == '__main__':
    print("Running test...")
    test_bench()

