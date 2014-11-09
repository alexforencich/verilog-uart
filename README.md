# Verilog UART Readme

For more information and updates: http://alexforencich.com/wiki/en/verilog/uart/start

GitHub repository: https://github.com/alexforencich/verilog-uart

## Introduction

This is a basic UART to AXI Stream IP core, written in Verilog with MyHDL
testbenches.

## Documentation

The main code for the core exists in the rtl subdirectory.  The uart_rx.v and
uart_tx.v files are the actual implementation, uart.v simply instantiates both
modules and makes a couple of internal connections.

The UART transmitter and receiver both use a single transmit or receive pin.
The modules take one parameter, DATA_WIDTH, that specifies the width of both
the data bus and the length of the actual data words communicated.  The
default value is 8 for an 8 bit interface.  The prescale input determines the
data rate - it should be set to Fclk / (baud * 8).  This is an input instead
of a parameter so it can be changed at run time, though it is not buffered
internally so care should be used to avoid corrupt data.  The main interface
to the user design is an AXI4-Stream interface that consists of the tdata,
tvalid, and tready signals.  tready flows in the opposite direction.  tdata
is considered valid when tvalid is high.  The destination will accept data
only when tready is high.  Data is transferred from the source to the
destination only when both tvalid and tready are high, otherwise the bus is
stalled.

Both interfaces also present a 'busy' signal that is high when an operation is
taking place.  The receiver also presents overrun error and frame error strobe
outputs.  If the data word currently in the tdata output register is not read
before another word is received, then a single cycle pulse will be emitted
from overrun_error and the word is discarded.  If the receiver does not get a
stop bit of the right level, then a single pulse will be emitted from the
frame_error output and the received word will be discarded.

### Source Files

    rtl/uart.v     : Wrapper for complete UART
    rtl/uart_rx.v  : UART receiver implementation
    rtl/uart_tx.v  : UART transmitter implementation

### AXI Stream Interface Example

two byte transfer with sink pause after each byte

              __    __    __    __    __    __    __    __    __
    clk    __/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__/  \__
                    _____ _________________
    tdata  XXXXXXXXX_D0__X_D1______________XXXXXXXXXXXXXXXXXXXXXXXX
                    _______________________
    tvalid ________/                       \_______________________
           ______________             _____             ___________
    tready               \___________/     \___________/


## Testing

Running the included testbenches requires MyHDL and Icarus Verilog.  Make sure
that myhdl.vpi is installed properly for cosimulation to work correctly.  The
testbenches can be run with a Python test runner like nose or py.test, or the
individual test scripts can be run with python directly.

### Testbench Files

    tb/axis_ep.py        : MyHDL AXI Stream endpoints
    tb/test_uart_rx.py   : MyHDL testbench for uart_rx module
    tb/test_uart_rx.v    : Verilog toplevel file for uart_rx cosimulation
    tb/test_uart_tx.py   : MyHDL testbench for uart_tx module
    tb/test_uart_tx.v    : Verilog toplevel file for uart_tx cosimulation
    tb/uart_ep.py        : MyHDL UART endpoints

## Example design

The included example design is targeted to a Digilent Atlys board.  To build
it, cd into example/ATLYS/fpga, make sure the Xilinx settings file has been
sourced correctly, and run make.
