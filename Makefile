#
# Top makefile for cdpw
#

all:
	$(MAKE) -C ReportPlugin install
	$(MAKE) -C OHIFPlugin install
	@echo Missing CDPW Constraints/scripts build

.PHONY: sub_build clean
