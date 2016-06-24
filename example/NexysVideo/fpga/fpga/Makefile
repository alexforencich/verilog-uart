
# FPGA settings
FPGA_PART = xc7a200t-sbg484-1
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
	djtgcfg prog -d NexysVideo --index 0 --file $(FPGA_TOP).bit

