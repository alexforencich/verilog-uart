/*

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

*/

// Language: Verilog 2001

`timescale 1 ns / 1 ps

module test_uart_rx;

// Inputs
reg clk = 0;
reg rst = 0;
reg [7:0] current_test = 0;

reg m_axis_tready = 0;
reg rxd = 1;
reg [15:0] prescale = 0;

// Outputs
wire [7:0] m_axis_tdata;
wire m_axis_tvalid;

wire busy;
wire overrun_error;
wire frame_error;

initial begin
    // myhdl integration
    $from_myhdl(clk,
                rst,
                current_test,
                m_axis_tready,
                rxd,
                prescale);
    $to_myhdl(m_axis_tdata,
              m_axis_tvalid,
              busy,
              overrun_error,
              frame_error);

    // dump file
    $dumpfile("test_uart_rx.lxt");
    $dumpvars(0, test_uart_rx);
end

uart_rx #(
    .DATA_WIDTH(8)
)
UUT (
    .clk(clk),
    .rst(rst),
    // axi output
    .m_axis_tdata(m_axis_tdata),
    .m_axis_tvalid(m_axis_tvalid),
    .m_axis_tready(m_axis_tready),
    // input
    .rxd(rxd),
    // status
    .busy(busy),
    .overrun_error(overrun_error),
    .frame_error(frame_error),
    // configuration
    .prescale(prescale)
);

endmodule
