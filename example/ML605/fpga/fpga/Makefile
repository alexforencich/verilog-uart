
# FPGA settings
FPGA_PART = xc6vlx130t-1ff1156
FPGA_TOP = fpga
FPGA_ARCH = spartan6

# PROM settings
#PROM = xc18v04
#SPI_PROM_SIZE = (in bytes)

# Files for synthesis
SYN_FILES = rtl/fpga.v
SYN_FILES += rtl/fpga_core.v
SYN_FILES += rtl/debounce_switch.v
SYN_FILES += rtl/sync_reset.v
SYN_FILES += rtl/sync_signal.v
SYN_FILES += lib/uart/rtl/uart.v
SYN_FILES += lib/uart/rtl/uart_rx.v
SYN_FILES += lib/uart/rtl/uart_tx.v

# UCF files
UCF_FILES = fpga.ucf

# NGC paths for ngdbuild
#NGC_PATHS = coregen/dcm_i100_o125

# Bitgen options
BITGEN_OPTIONS = -g StartupClk:Cclk -g ConfigRate:26

include ../common/xilinx.mk

program: $(FPGA_TOP).bit
	echo "setmode -bscan" > program.cmd
	echo "setcable -p auto" >> program.cmd
	echo "identify" >> program.cmd
	echo "assignfile -p 2 -file $(FPGA_TOP).bit" >> program.cmd
	echo "program -p 2" >> program.cmd
	echo "quit" >> program.cmd
	impact -batch program.cmd

