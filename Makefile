#
# Top makefile for kp-report
#
MAJORV  ?= 0
MINORV  ?= 9
MICROV  ?= 7
BUILDV  ?= -1
BASE    := kp-report
RELEASE := $(MAJORV).$(MINORV).$(MICROV)${BUILDV}
PKGNAME := $(BASE)-$(RELEASE)
INSTALL_ROOT = $(CURDIR)/$(PKGNAME)

export INSTALL_ROOT
export RELEASE

NTHREAD := $(shell getconf _NPROCESSORS_ONLN)

all:	.build
	$(MAKE) -C Installation
	dpkg-deb --build $(INSTALL_ROOT)

.build:
	$(MAKE) -C ReportPlugin install
	$(MAKE) -C OHIFPlugin install
	touch $@

clean:
	@rm -rf $(BASE)-*
	$(MAKE) -C orthanc-packages INSTALL_ROOT=$(INSTALL_ROOT) clean

.PHONY: all clean
