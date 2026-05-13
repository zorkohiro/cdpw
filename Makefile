#
# Top makefile for cdpw
#

all:
	mkdir -p artifacts
	sudo $(MAKE) -C cdpw-ohif install
	$(MAKE) -C cdpw install
	cd artifacts && rel=`cat RELEASE` && tar cf ../cdpw-$$rel.tar *.deb

.PHONY: clean
