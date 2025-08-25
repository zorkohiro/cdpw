#
# Makefile added for Orthanc, 1.12.9
#
MAJORV  ?= 1
MINORV  ?= 12
RLEASE  ?= 9
BUILDV	?= -1
BASE    := cdpw-orthanc
ORTHANC_RELEASE := ${MAJORV}.${MINORV}.${RLEASE}
RELEASE := $(MAJORV).$(MINORV).$(RLEASE)$(BUILDV)
PKGNAME := $(BASE)-$(RELEASE)
DLCACHE := $(HOME)/Downloads

ORTHANC_BASE  := https://orthanc.uclouvain.be/downloads/sources/orthanc
ORTHANC_TBALL ?= Orthanc-$(ORTHANC_RELEASE).tar.gz
ORTHANC_FETCH = $(ORTHANC_BASE)/$(ORTHANC_TBALL)
ORTHANC_LOCAL = $(DLCACHE)/$(ORTHANC_TBALL)

ARTIFACTS ?= ../artifacts

INSTALL_ROOT = $(CURDIR)/$(PKGNAME)
CMAKE_ARGS= cmake -DALLOW_DOWNLOADS=ON -DUSE_GOOGLE_TEST_DEBIAN_PACKAGE=ON -DUSE_SYSTEM_BOOST=OFF \
  -DUSE_SYSTEM_CIVETWEB=OFF -DUSE_SYSTEM_DCMTK=OFF -DUSE_SYSTEM_JSONCPP=OFF -DUSE_SYSTEM_LUA=OFF \
   -DCIVETWEB_OPENSSL_API=1.0 -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$(INSTALL_ROOT)/usr ../OrthancServer

NTHREAD := $(shell getconf _NPROCESSORS_ONLN)

all:	.setup_source .setup_cmake .built

.setup_source: OrthancServer/ThirdPartyDownloads
	mkdir -p Build
	touch $@

OrthancServer/ThirdPartyDownloads: ${ORTHANC_LOCAL}
	tar --strip-components=1 -xf $(ORTHANC_LOCAL)
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
	cp copyright preinst $(INSTALL_ROOT)/DEBIAN
	rm -rf ${INSTALL_ROOT}/usr/include
	dpkg-deb --build $(INSTALL_ROOT)
	mkdir -p $(ARTIFACTS)
	cp $(PKGNAME).deb $(ARTIFACTS)

clean:
	rm -rf Build

.PHONY: all install clean
