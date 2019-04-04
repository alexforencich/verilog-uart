
# FPGA settings
FPGA_PART = xc7a35t-csg324-1
FPGA_TOP = fpga
FPGA_ARCH = artix7

# Files for synthesis
SYN_FILES = rtl/fpga.v
SYN_FILES += rtl/fpga_core.v
SYN_FILES += rtl/debounce_switch.v
SYN_FILES += rtl/sync_reset.v
SYN_FILES += rtl/sync_signal.v
SYN_FILES += lib/uart/rtl/uart.v
SYN_FILES += lib/uart/rtl/uart_rx.v
SYN_FILES += lib/uart/rtl/uart_tx.v

# XDC files
XDC_FILES = fpga.xdc

include ../common/vivado.mk

program: $(FPGA_TOP).bit
	echo "open_hw" > program.tcl
	echo "connect_hw_server" >> program.tcl
	echo "open_hw_target" >> program.tcl
	echo "current_hw_device [lindex [get_hw_devices] 0]" >> program.tcl
	echo "refresh_hw_device -update_hw_probes false [lindex [get_hw_devices] 0]" >> program.tcl
	echo "set_property PROGRAM.FILE {$(FPGA_TOP).bit} [lindex [get_hw_devices] 0]" >> program.tcl
	echo "program_hw_devices [lindex [get_hw_devices] 0]" >> program.tcl
	echo "exit" >> program.tcl
	vivado -mode batch -source program.tcl

