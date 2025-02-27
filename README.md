# Verilog UART Readme

[![Build Status](https://github.com/alexforencich/verilog-uart/workflows/Regression%20Tests/badge.svg?branch=master)](https://github.com/alexforencich/verilog-uart/actions/)

For more information and updates: http://alexforencich.com/wiki/en/verilog/uart/start

GitHub repository: https://github.com/alexforencich/verilog-uart

## Deprecation Notice

This repository is superseded by https://github.com/fpganinja/taxi.  All new features and bug fixes will be applied there, and commercial support is also available.  As a result, this repo is deprecated and will not receive any future maintenance or support.

## Introduction

This is a basic UART to AXI Stream IP core, written in Verilog with cocotb
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

Running the included testbenches requires [cocotb](https://github.com/cocotb/cocotb), [cocotbext-axi](https://github.com/alexforencich/cocotbext-axi), and [Icarus Verilog](http://iverilog.icarus.com/).  The testbenches can be run with pytest directly (requires [cocotb-test](https://github.com/themperek/cocotb-test)), pytest via tox, or via cocotb makefiles.
