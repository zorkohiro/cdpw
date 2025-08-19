#
# Top makefile for cdpw
#

all:
	$(MAKE) -C cdpw-report install
	$(MAKE) -C cdpw-ohif install
	$(MAKE) -C cdpw-dicomweb install
	$(MAKE) -C cdpw-orthanc install
	$(MAKE) -C cdpw install

.PHONY: clean
