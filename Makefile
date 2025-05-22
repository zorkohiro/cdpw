#
# Top makefile for kp-report
#
MAJORV  ?= 1
MINORV  ?= 0
RLEASE  ?= Alpha-1.0
BUILDV  ?= -1
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
	@rm -rf $(BASE)-*
	$(MAKE) -C orthanc-packages INSTALL_ROOT=$(INSTALL_ROOT) clean

.PHONY: all sub_build clean
