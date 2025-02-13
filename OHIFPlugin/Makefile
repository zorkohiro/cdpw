#
# Overmakefile for orthanc-ohif source
#
ifeq ($(INSTALL_ROOT),)
$(error INSTALL_ROOT not set)
endif
CMAKE_ARGS= .. -DCMAKE_INSTALL_PREFIX=$(INSTALL_ROOT) -DSTATIC_BUILD=ON -DCMAKE_BUILD_TYPE=Release
NTHREAD := $(shell getconf _NPROCESSORS_ONLN)

all:	.built_ohif .cmake_setup .built_binary

.built_ohif:
	mkdir -p Build
	cd Build && ../Resources/CreateOHIFDist.sh
	touch $@

.cmake_setup:
	cd Build && cmake $(CMAKE_ARGS)
	touch $@

.built_binary:
	cd Build && make -j $(NTHREAD)
	touch $@

install:	all
	cd Build && make install

clean:
	@rm -rf Build

.PHONY: all install clean
