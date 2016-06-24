# XDC constraints for the Digilent Nexys Video board
# part: xc7a200tsbg484-1

# General configuration
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]

# 100 MHz clock
set_property -dict {LOC R4   IOSTANDARD LVCMOS33} [get_ports clk]
create_clock -name clk -period 10.000 [get_ports clk]

# LEDs
set_property -dict {LOC T14  IOSTANDARD LVCMOS25 SLEW SLOW DRIVE 12} [get_ports led[0]]
set_property -dict {LOC T15  IOSTANDARD LVCMOS25 SLEW SLOW DRIVE 12} [get_ports led[1]]
set_property -dict {LOC T16  IOSTANDARD LVCMOS25 SLEW SLOW DRIVE 12} [get_ports led[2]]
set_property -dict {LOC U16  IOSTANDARD LVCMOS25 SLEW SLOW DRIVE 12} [get_ports led[3]]
set_property -dict {LOC V15  IOSTANDARD LVCMOS25 SLEW SLOW DRIVE 12} [get_ports led[4]]
set_property -dict {LOC W16  IOSTANDARD LVCMOS25 SLEW SLOW DRIVE 12} [get_ports led[5]]
set_property -dict {LOC W15  IOSTANDARD LVCMOS25 SLEW SLOW DRIVE 12} [get_ports led[6]]
set_property -dict {LOC Y13  IOSTANDARD LVCMOS25 SLEW SLOW DRIVE 12} [get_ports led[7]]

# Reset button
set_property -dict {LOC G4   IOSTANDARD LVCMOS15} [get_ports reset_n]

# Push buttons
set_property -dict {LOC F15  IOSTANDARD LVCMOS12} [get_ports btnu]
set_property -dict {LOC C22  IOSTANDARD LVCMOS12} [get_ports btnl]
set_property -dict {LOC D22  IOSTANDARD LVCMOS12} [get_ports btnd]
set_property -dict {LOC D14  IOSTANDARD LVCMOS12} [get_ports btnr]
set_property -dict {LOC B22  IOSTANDARD LVCMOS12} [get_ports btnc]

# Toggle switches
set_property -dict {LOC E22  IOSTANDARD LVCMOS12} [get_ports sw[0]]
set_property -dict {LOC F21  IOSTANDARD LVCMOS12} [get_ports sw[1]]
set_property -dict {LOC G21  IOSTANDARD LVCMOS12} [get_ports sw[2]]
set_property -dict {LOC G22  IOSTANDARD LVCMOS12} [get_ports sw[3]]
set_property -dict {LOC H17  IOSTANDARD LVCMOS12} [get_ports sw[4]]
set_property -dict {LOC J16  IOSTANDARD LVCMOS12} [get_ports sw[5]]
set_property -dict {LOC K13  IOSTANDARD LVCMOS12} [get_ports sw[6]]
set_property -dict {LOC M17  IOSTANDARD LVCMOS12} [get_ports sw[7]]

# UART
set_property -dict {LOC AA19 IOSTANDARD LVCMOS33 SLEW SLOW DRIVE 12} [get_ports uart_txd]
set_property -dict {LOC V18  IOSTANDARD LVCMOS33} [get_ports uart_rxd]
