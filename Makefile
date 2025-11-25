#
# Top makefile for cdpw
#

all:
	$(MAKE) -C cdpw-report install
	$(MAKE) -C cdpw-ohif install
	$(MAKE) -C cdpw-dicomweb install
	$(MAKE) -C cdpw-orthanc install
	$(MAKE) -C cdpw install
	cd artifacts && rel=`cat RELEASE` && tar cf ../cdpw-$$rel.tar *.deb

.PHONY: clean
