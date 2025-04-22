#
# Overmakefile for orthanc-ohif source
#
ifeq ($(INSTALL_ROOT),)
$(error INSTALL_ROOT not set)
endif
CMAKE_ARGS= .. -DCMAKE_INSTALL_PREFIX=$(INSTALL_ROOT)/usr -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
NTHREAD := $(shell getconf _NPROCESSORS_ONLN)

all:	.built_ohif .cmake_setup build

.built_ohif:
	mkdir -p Build
	cd Build && ../Resources/CreateOHIFDist.sh
	touch $@

.cmake_setup:
	cd Build && cmake $(CMAKE_ARGS)
	touch $@

build:
	cd Build && make -j $(NTHREAD)

install:	all
	cd Build && make install

clean:
	@rm -rf Build

.PHONY: all install clean
