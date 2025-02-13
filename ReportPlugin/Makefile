#
# Overmakefile for our report plugin
#
ifeq ($(INSTALL_ROOT),)
$(error INSTALL_ROOT not set)
endif
CMAKE_ARGS= .. -DCMAKE_INSTALL_PREFIX=$(INSTALL_ROOT) -DALLOW_DOWNLOADS=ON -DCMAKE_BUILD_TYPE=Release
NTHREAD=$(shell getconf _NPROCESSORS_ONLN)

#
# Note that the submake usage explicitly uses make- not $(MAKE)
#
all:
	mkdir -p Build
	cd Build && cmake $(CMAKE_ARGS)
	cd Build && make -j $(NTHREAD)

install:	all
	cd Build && make install

clean:
	@rm -rf Build
