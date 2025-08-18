#
# Install/packaging step for cdpw
#
MAJORV  ?= 1
MINORV  ?= 2
RLEASE  ?= 0-Dev
BUILDV  ?= -1
BASE    := cdpw
RELEASE := $(MAJORV).$(MINORV).$(RLEASE)$(BUILDV)
PKGNAME := $(BASE)-$(RELEASE)

ARTIFACTS ?= ../artifacts

INSTALL_ROOT = $(CURDIR)/$(PKGNAME)
CDPW_LIB = $(INSTALL_ROOT)/usr/share/$(BASE)
SYSTEMD = ${INSTALL_ROOT}/lib/systemd/system

all:

install:
	install -D -m 640 cdpw_data_present.service ${SYSTEMD}/cdpw_data_present.service
	install -D -m 640 cdpw.service ${SYSTEMD}/cdpw.service
	install -D -m 644 configurator.json ${CDPW_LIB}/configurator.json
	install -D -m 644 cdpw.json ${CDPW_LIB}/cdpw.json
	install -D -m 644 dicom_aet_port.json ${CDPW_LIB}/dicom_aet_port.json
	install -D -m 755 code_dark_configurator ${INSTALL_ROOT}/usr/bin/code_dark_configurator
	install -D -m 755 orthanc_checker ${INSTALL_ROOT}/usr/sbin/orthanc_checker
	install -D -m 440 orthanc.sudo ${INSTALL_ROOT}/etc/sudoers.d/orthanc
	mkdir -p -m 755 $(INSTALL_ROOT)/DEBIAN
	sed -e "s,%VERSION%,$(RELEASE)," control > $(INSTALL_ROOT)/DEBIAN/control
	cp copyright preinst postinst prerm postrm ${INSTALL_ROOT}/DEBIAN
	dpkg-deb --build $(INSTALL_ROOT)
	mkdir -p $(ARTIFACTS)
	cp $(PKGNAME).deb $(ARTIFACTS)

clean:

.PHONY: all install clean
