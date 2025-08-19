#
# Makefile added for OrthancDicomWeb
#
MAJORV  ?= 1
MINORV  ?= 21
BASE    := cdpw-dicomweb
RELEASE := $(MAJORV).$(MINORV)
PKGNAME := $(BASE)-$(RELEASE)
DLCACHE := $(HOME)/Downloads

ORTHANC_BASE  := https://orthanc.uclouvain.be/downloads/sources/orthanc-dicomweb
ORTHANC_TBALL ?= OrthancDicomWeb-$(RELEASE).tar.gz
ORTHANC_FETCH = $(ORTHANC_BASE)/$(ORTHANC_TBALL)
ORTHANC_LOCAL = $(DLCACHE)/$(ORTHANC_TBALL)

ARTIFACTS ?= ../artifacts

INSTALL_ROOT = $(CURDIR)/$(PKGNAME)
CMAKE_ARGS= cmake .. -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$(INSTALL_ROOT)/usr

NTHREAD := $(shell getconf _NPROCESSORS_ONLN)

all:	.setup_source .setup_cmake .built

.setup_source: ThirdPartyDownloads ${ORTHANC_LOCAL}
	tar --strip-components=1 -xf $(ORTHANC_LOCAL)
	mkdir -p Build
	touch $@

ThirdPartyDownloads: ${ORTHANC_LOCAL}
	ln -s ${DLCACHE} $@

$(ORTHANC_LOCAL):
	mkdir -p $(DLCACHE)
	wget -q -O $(ORTHANC_LOCAL) $(ORTHANC_FETCH)

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
	cp copyright $(INSTALL_ROOT)/DEBIAN
	dpkg-deb --build $(INSTALL_ROOT)
	mkdir -p $(ARTIFACTS)
	cp $(PKGNAME).deb $(ARTIFACTS)

clean:
	rm -rf Build

.PHONY: all install clean
