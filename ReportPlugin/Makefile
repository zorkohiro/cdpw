#
# Build our plugin to Orthanc
#
MAJORV  ?= 1
MINORV  ?= 1
RLEASE  ?= Dev-1.0
BUILDV	?= -7
BASE    := kp-report
RELEASE := $(MAJORV).$(MINORV)-$(RLEASE)${BUILDV}
PKGNAME := $(BASE)-$(RELEASE)

ARTIFACTS ?= ../artifacts

INSTALL_ROOT = $(CURDIR)/$(PKGNAME)
KPLIB = ${INSTALL_ROOT}/usr/lib/${BASE}
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
	mkdir -p ${KPLIB}/${TDIR}
	for c in ${CURDIR}/${TDIR}/*.json; do cp -f $$c ${KPLIB}/${TDIR}; done
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
