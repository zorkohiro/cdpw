#
# Install/packaging step for cdpw
#
MAJORV  ?= 1
MINORV  ?= 1
RLEASE  ?= 1
BUILDV  ?= -2
BASE    := cdpw
RELEASE := $(MAJORV).$(MINORV).$(RLEASE)$(BUILDV)
PKGNAME := $(BASE)-$(RELEASE)
#
# LEVEL is syntactic suger. It is $(RELEASE) which must be unique.
# When it's truly a release, LEVEL should be null.
#
LEVEL   := Beta

ARTIFACTS ?= ../artifacts

INSTALL_ROOT = $(CURDIR)/$(PKGNAME)
CDPW_LIB = $(INSTALL_ROOT)/usr/share/$(BASE)
SYSTEMD = ${INSTALL_ROOT}/lib/systemd/system

all:

install:
	install -D -m 640 cdpw_data_present.service ${SYSTEMD}/cdpw_data_present.service
	install -D -m 640 cdpw.service ${SYSTEMD}/cdpw.service
	install -D -m 644 configurator.json ${CDPW_LIB}/configurator.json
	rm -f ${CDPW_LIB}/cdpw_version.txt
	echo $(RELEASE) ${LEVEL| > ${CDPW_LIB}/cdpw_version.txt
	install -D -m 644 cdpw.json ${CDPW_LIB}/cdpw.json
	install -D -m 644 dicom_aet_port.json ${CDPW_LIB}/dicom_aet_port.json
	install -D -m 644 images/code_dark_label_nv.gif $(CDPW_LIB)/code_dark_label_nv.gif
	install -D -m 644 images/KaiserRedSmall.png $(CDPW_LIB)/KaiserRedSmall.png
	install -D -m 755 code_dark_configurator.desktop ${INSTALL_ROOT}/usr/share/applications/code_dark_configurator.desktop
	install -D -m 755 code_dark_study_tool.desktop ${INSTALL_ROOT}/usr/share/applications/code_dark_study_tool.desktop
	install -D -m 755 code_dark_about.desktop ${INSTALL_ROOT}/usr/share/applications/code_dark_about.desktop
	install -D -m 755 code_dark_configurator ${INSTALL_ROOT}/usr/bin/code_dark_configurator
	install -D -m 755 code_dark_study_tool ${INSTALL_ROOT}/usr/bin/code_dark_study_tool
	install -D -m 755 about_code_dark ${INSTALL_ROOT}/usr/bin/about_code_dark
	install -D -m 755 orthanc_checker ${INSTALL_ROOT}/usr/sbin/orthanc_checker
	install -D -m 440 orthanc.sudo ${INSTALL_ROOT}/etc/sudoers.d/orthanc
	mkdir -p -m 755 $(INSTALL_ROOT)/DEBIAN
	sed -e "s,%VERSION%,$(RELEASE)," control > $(INSTALL_ROOT)/DEBIAN/control
	cp copyright preinst postinst prerm postrm ${INSTALL_ROOT}/DEBIAN
	rm -rf ${INSTALL_ROOT}/usr/include
	dpkg-deb --build $(INSTALL_ROOT)
	mkdir -p $(ARTIFACTS)
	cp $(PKGNAME).deb $(ARTIFACTS)
	echo $(RELEASE) > ${ARTIFACTS}/RELEASE

clean:

.PHONY: all install clean
