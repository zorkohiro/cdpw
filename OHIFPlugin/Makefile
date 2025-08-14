#
# Makefile added for OHIF plugin, version 1.4.1
#
MAJORV  ?= 1
MINORV  ?= 4
RLEASE  ?= 1
BUILDV	?=
BASE    := orthanc-ohif
RELEASE := $(MAJORV).$(MINORV).$(RLEASE)${BUILDV}
PKGNAME := $(BASE)-$(RELEASE)
INSTALL_ROOT = $(CURDIR)/$(PKGNAME)

ARTIFACTS ?= ../artifacts

CMAKE_ARGS= .. -DCMAKE_INSTALL_PREFIX=$(INSTALL_ROOT)/usr -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
NTHREAD := $(shell getconf _NPROCESSORS_ONLN)

all:	.setup_ohif .setup_cmake .built

.setup_ohif:
	mkdir -p Build
	cd Build && ../Resources/CreateOHIFDist.sh
	touch $@

.setup_cmake:
	cd Build && cmake $(CMAKE_ARGS)
	touch $@

.built:
	cd Build && $(MAKE) -j $(NTHREAD)
	touch .built

.sub_install:
	cd Build && $(MAKE) install
	touch $@

install:	all .sub_install
	mkdir -p -m 755 $(INSTALL_ROOT)/DEBIAN
	sed -e "s,%VERSION%,$(RELEASE)," control > $(INSTALL_ROOT)/DEBIAN/control
	cp copyright postinst prerm postrm ${INSTALL_ROOT}/DEBIAN
	dpkg-deb --build $(INSTALL_ROOT)
	mkdir -p ${ARTIFACTS}
	cp ${PKGNAME}.deb ${ARTIFACTS}

clean:
	rm -rf Build

.PHONY: all install clean
