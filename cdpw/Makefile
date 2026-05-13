#
# Install/packaging step for cdpw
#
MAJORV  ?= 2
MINORV  ?= 0
RLEASE  ?= 0
BUILDV  ?= -deb13-2
BASE    := cdpw
RELEASE := $(MAJORV).$(MINORV).$(RLEASE)$(BUILDV)
PKGNAME := $(BASE)-$(RELEASE)
#
# LEVEL is syntactic suger. It is $(RELEASE) which must be unique.
# When it's truly a release, LEVEL should be null.
#
LEVEL   := Dev0

ARTIFACTS ?= ../artifacts

INSTALL_ROOT = $(CURDIR)/$(PKGNAME)
CDPW_LIB = $(INSTALL_ROOT)/usr/share/$(BASE)
TDIR = Templates

all:

install:
	install -D -m 644 configurator.json ${CDPW_LIB}/configurator.json
	rm -f ${CDPW_LIB}/cdpw_version.txt
	echo $(RELEASE) $(LEVEL) > ${CDPW_LIB}/cdpw_version.txt
	install -D -m 644 cdpw.json ${CDPW_LIB}/cdpw.json
	install -D -m 644 dicom_aet_port.json ${CDPW_LIB}/dicom_aet_port.json
	install -D -m 644 images/code_dark_label.gif $(CDPW_LIB)/code_dark_label.gif
	install -D -m 644 images/KaiserRedSmall.png $(CDPW_LIB)/KaiserRedSmall.png
	install -D -m 755 code_dark_configurator.desktop ${INSTALL_ROOT}/usr/share/applications/code_dark_configurator.desktop
	install -D -m 755 code_dark_study_tool.desktop ${INSTALL_ROOT}/usr/share/applications/code_dark_study_tool.desktop
	install -D -m 755 code_dark_about.desktop ${INSTALL_ROOT}/usr/share/applications/code_dark_about.desktop
	install -D -m 755 code_dark_configurator ${INSTALL_ROOT}/usr/bin/code_dark_configurator
	install -D -m 755 code_dark_study_tool ${INSTALL_ROOT}/usr/bin/code_dark_study_tool
	install -D -m 755 about_code_dark ${INSTALL_ROOT}/usr/bin/about_code_dark
	install -D -m 440 orthanc.sudo ${INSTALL_ROOT}/etc/sudoers.d/orthanc

	for c in ${CURDIR}/Scripts/*; do cp -f $$c ${INSTALL_ROOT}/usr/bin; done
	mkdir -p ${CDPW_LIB}/${TDIR}
	for c in ${CURDIR}/${TDIR}/*.json; do cp -f $$c ${CDPW_LIB}/${TDIR}; done

	mkdir -p -m 755 $(INSTALL_ROOT)/DEBIAN
	sed -e "s,%VERSION%,$(RELEASE)," control > $(INSTALL_ROOT)/DEBIAN/control
	cp copyright postinst postrm ${INSTALL_ROOT}/DEBIAN
	rm -rf ${INSTALL_ROOT}/usr/include
	dpkg-deb --build $(INSTALL_ROOT)
	mkdir -p $(ARTIFACTS)
	cp $(PKGNAME).deb $(ARTIFACTS)
	echo $(RELEASE) > ${ARTIFACTS}/RELEASE

clean:

.PHONY: all install clean
