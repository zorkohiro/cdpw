#
# Build our plugin to Orthanc
#
MAJORV  ?= 1
MINORV  ?= 3
RLEASE  ?= 0
BUILDV	?= -1
BASE    := cdpw-report
RELEASE := $(MAJORV).$(MINORV)-$(RLEASE)${BUILDV}
PKGNAME := $(BASE)-$(RELEASE)

ARTIFACTS ?= ../artifacts

INSTALL_ROOT = $(CURDIR)/$(PKGNAME)
CDPW_LIB = ${INSTALL_ROOT}/usr/lib/cdpw
TDIR = Templates

CMAKE_ARGS= .. -DCMAKE_INSTALL_PREFIX=$(INSTALL_ROOT)/usr -DALLOW_DOWNLOADS=ON -DCMAKE_BUILD_TYPE=Release

NTHREAD := $(shell getconf _NPROCESSORS_ONLN)

all:	.setup .setup_cmake .built

.setup:
	mkdir Build
	mkdir -p ${INSTALL_ROOT}
	touch $@

.setup_cmake:
	cd Build && cmake $(CMAKE_ARGS)
	touch $@

.built:
	cd Build && $(MAKE) -j $(NTHREAD)
	touch .built

.sub_install:
	cd Build && $(MAKE) install
	mkdir -p ${CDPW_LIB}/${TDIR}
	for c in ${CURDIR}/${TDIR}/*.json; do cp -f $$c ${CDPW_LIB}/${TDIR}; done
	mkdir -p ${INSTALL_ROOT}/usr/bin
	for c in ${CURDIR}/Scripts/*; do cp -f $$c ${INSTALL_ROOT}/usr/bin/`basename $$c`; done
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
