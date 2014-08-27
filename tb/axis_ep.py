"""

Copyright (c) 2014 Alex Forencich

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

def words2list(f, N=1, WL=8):
    frame = []
    while len(f) > 0:
        data = 0
        keep = 0
        for i in range(N):
            data = data | (f.pop(0) << (i*WL))
            keep = keep | (1 << i)
            if len(f) == 0: break
        frame.append((data, keep))
    return frame

def list2words(f, N=1, WL=8):
    frame = []
    mask = 2**WL-1
    for data in f:
        keep = -1
        if type(data) is tuple:
            data, keep = data
        for i in range(N):
            if keep & (1 << i):
                frame.append((data >> (i*WL)) & mask)
    return frame

def AXIStreamSource(clk, rst,
                    tdata=None,
                    tkeep=None,
                    tvalid=Signal(bool(False)),
                    tready=Signal(bool(True)),
                    tlast=Signal(bool(False)),
                    fifo=None,
                    pause=0):

    tready_int = Signal(bool(False))
    tvalid_int = Signal(bool(False))

    @always_comb
    def pause_logic():
        tready_int.next = tready and not pause
        tvalid.next = tvalid_int and not pause

    @instance
    def logic():
        frame = []
        N = len(tdata)
        M = 1
        b = False
        if tkeep is not None:
            M = len(tkeep)
        WL = (len(tdata)+M-1)/M
        if WL == 8:
            b = True

        while True:
            yield clk.posedge, rst.posedge

            if rst:
                tdata.next = 0
                if tkeep is not None:
                    tkeep.next = 0
                tvalid_int.next = False
                tlast.next = False
            else:
                if tready_int and tvalid:
                    if len(frame) > 0:
                        data, keep = frame.pop(0)
                        tdata.next = data
                        if tkeep is not None:
                            tkeep.next = keep
                        tvalid_int.next = True
                        tlast.next = len(frame) == 0
                    else:
                        tvalid_int.next = False
                        tlast.next = False
                if (tlast and tready_int and tvalid) or not tvalid_int:
                    if not fifo.empty():
                        frame = fifo.get()
                        if type(frame) is bytes:
                            frame = bytearray(frame)
                        if type(frame) is bytearray:
                            frame = words2list(frame, M, WL)
                        data, keep = frame.pop(0)
                        tdata.next = data
                        if tkeep is not None:
                            tkeep.next = keep
                        tvalid_int.next = True
                        tlast.next = len(frame) == 0

    return logic, pause_logic


def AXIStreamSink(clk, rst,
                  tdata=None,
                  tkeep=None,
                  tvalid=Signal(bool(True)),
                  tready=Signal(bool(True)),
                  tlast=Signal(bool(True)),
                  fifo=None,
                  pause=0):

    tready_int = Signal(bool(False))
    tvalid_int = Signal(bool(False))

    @always_comb
    def pause_logic():
        tready.next = tready_int and not pause
        tvalid_int.next = tvalid and not pause

    @instance
    def logic():
        frame = []
        N = len(tdata)
        M = 1
        b = False
        if tkeep is not None:
            M = len(tkeep)
        WL = (len(tdata)+M-1)/M
        if WL == 8:
            b = True

        while True:
            yield clk.posedge, rst.posedge

            if rst:
                tready_int.next = False
                frame = []
            else:
                tready_int.next = True

                if tvalid_int:
                    if tkeep is not None:
                        frame.append((int(tdata), int(tkeep)))
                    else:
                        frame.append(int(tdata))
                    if tlast:
                        if b:
                            frame = list2words(frame, M, WL)
                        if fifo is not None:
                            fifo.put(frame)
                        print("Got frame %s" % repr(frame))
                        frame = []

    return logic, pause_logic

