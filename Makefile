#
# Top makefile for kp-report
#
MAJORV  ?= 1
MINORV  ?= 1
RLEASE  ?= Dev-1.0
BUILDV  ?= -2
BASE    := kp-report
RELEASE := $(MAJORV).$(MINORV)-$(RLEASE)${BUILDV}
PKGNAME := $(BASE)-$(RELEASE)
INSTALL_ROOT = $(CURDIR)/$(PKGNAME)

export INSTALL_ROOT
export RELEASE

NTHREAD := $(shell getconf _NPROCESSORS_ONLN)

all:	sub_build
	$(MAKE) -C Installation
	dpkg-deb --build $(INSTALL_ROOT)

sub_build:
	$(MAKE) -C ReportPlugin install
	$(MAKE) -C OHIFPlugin install

clean:
	$(MAKE) -C ReportPlugin clean
	$(MAKE) -C OHIFPlugin clean
	rm -rf $(BASE)-*

.PHONY: all sub_build clean
