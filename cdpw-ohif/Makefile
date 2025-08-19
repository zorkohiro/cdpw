#
# Makefile added for OHIF plugin, version 1.4.1
#
MAJORV  ?= 1
MINORV  ?= 7
BUILDV	?=
BASE    := cdpw-ohif
RELEASE := $(MAJORV).$(MINORV)
PKGNAME := $(BASE)-$(RELEASE)
DLCACHE := $(HOME)/Downloads

ORTHANC_BASE  := https://orthanc.uclouvain.be/downloads/sources/orthanc-ohif
ORTHANC_TBALL ?= OrthancOHIF-$(RELEASE).tar.gz
ORTHANC_FETCH = $(ORTHANC_BASE)/$(ORTHANC_TBALL)
ORTHANC_LOCAL = $(DLCACHE)/$(ORTHANC_TBALL)

VIEWER_BASE := https://orthanc.uclouvain.be/downloads/third-party-downloads/OHIF
VIEWER_TBALL ?= Viewers-3.11.0.tar.gz 
VIEWER_FETCH = ${VIEWER_BASE}/${VIEWER_TBALL}
VIEWER_LOCAL = ${DLCACHE}/${VIEWER_TBALL}

INSTALL_ROOT = $(CURDIR)/$(PKGNAME)
CMAKE_ARGS= .. -DCMAKE_INSTALL_PREFIX=$(INSTALL_ROOT)/usr -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
NTHREAD := $(shell getconf _NPROCESSORS_ONLN)

ARTIFACTS ?= ../artifacts

all:	.setup_source .setup_ohif .setup_cmake .built

.setup_source: ThirdPartyDownloads ${ORTHANC_LOCAL}
	tar --strip-components=1 -xf $(ORTHANC_LOCAL)
	mkdir -p Build
	touch $@

ThirdPartyDownloads: ${ORTHANC_LOCAL}
	ln -s ${DLCACHE} $@

$(ORTHANC_LOCAL):
	mkdir -p $(DLCACHE)
	wget -q -O $(ORTHANC_LOCAL) $(ORTHANC_FETCH)

.setup_ohif: ${DLCACHE} ${VIEWER_LOCAL}
	mkdir -p Build
	cd Build && ../Resources/CreateOHIFDist.sh
	touch $@

${VIEWER_LOCAL}:
	wget -q -o ${VIEWER_LOCAL} ${VIEWER_FETCH}
	mkdir -p OHIF && cd OHIF && if [ ! -e ${VIEWER} ]; then ln -s ${VIEWER_LOCAL}; fi

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
	cp copyright ${INSTALL_ROOT}/DEBIAN
	dpkg-deb --build $(INSTALL_ROOT)
	mkdir -p ${ARTIFACTS}
	cp ${PKGNAME}.deb ${ARTIFACTS}

clean:
	rm -rf Build

.PHONY: all install clean
