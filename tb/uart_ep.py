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

class UARTSource(object):
    def __init__(self):
        self.has_logic = False
        self.queue = []

    def write(self, data):
        self.queue.extend(data)

    def count(self):
        return len(self.queue)

    def empty(self):
        return self.count() == 0

    def create_logic(self,
                clk,
                rst,
                txd=None,
                width=8,
                prescale=2,
                name=None
            ):

        assert not self.has_logic

        self.has_logic = True

        @instance
        def logic():
            frame = []
            temp_data = 0
            prescale_cnt = 0
            bit_cnt = 0

            while True:
                yield clk.posedge, rst.posedge

                if rst:
                    txd.next = 1
                    prescale_cnt = 0
                    bit_cnt = 0
                else:
                    if prescale_cnt > 0:
                        prescale_cnt = prescale_cnt-1
                    elif bit_cnt > 0:
                        bit_cnt = bit_cnt-1
                        prescale_cnt = (prescale << 3) - 1
                        if bit_cnt > 0:
                            txd.next = temp_data & 1 != 0
                            temp_data = temp_data >> 1
                        else:
                            txd.next = 1
                    elif len(self.queue) > 0:
                        temp_data = self.queue.pop(0)
                        if name is not None:
                            print("[%s] Sending data byte %d" % (name, temp_data))
                        prescale_cnt = (prescale << 3) - 1
                        bit_cnt = width+1
                        txd.next = 0

        return instances()


class UARTSink(object):
    def __init__(self):
        self.has_logic = False
        self.queue = []

    def read(self, count=-1):
        if count < 0:
            count = len(self.queue)
        data = self.queue[:count]
        del self.queue[:count]
        return data

    def count(self):
        return len(self.queue)

    def empty(self):
        return self.count() == 0

    def create_logic(self,
                clk, rst,
                rxd=None,
                width=8,
                prescale=2,
                name=None
            ):

        assert not self.has_logic

        self.has_logic = True

        @instance
        def logic():
            frame = []
            temp_data = 0
            prescale_cnt = 0
            bit_cnt = 0

            while True:
                yield clk.posedge, rst.posedge

                if rst:
                    frame = []
                    prescale_cnt = 0
                    bit_cnt = 0
                else:
                    if prescale_cnt > 0:
                        prescale_cnt = prescale_cnt-1
                    elif bit_cnt > 0:
                        bit_cnt = bit_cnt-1
                        prescale_cnt = (prescale << 3) - 1
                        if bit_cnt == width+1:
                            if rxd:
                                if name is not None:
                                    print("[%s] Bad start bit" % name)
                                prescale_cnt = 0
                                bit_cnt = 0
                        elif bit_cnt > 0:
                            temp_data = temp_data | (rxd << (width-bit_cnt))
                        else:
                            prescale_cnt = 0
                            if rxd:
                                if name is not None:
                                    print("[%s] Got data byte %d" % (name, temp_data))
                                self.queue.append(temp_data)
                            else:
                                if name is not None:
                                    print("[%s] Bad stop bit" % name)
                    elif rxd == 0:
                        prescale_cnt = (prescale << 2) - 2
                        bit_cnt = width+2
                        temp_data = 0

        return instances()

