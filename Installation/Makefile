MAJORV  ?= 0
MINORV  ?= 9
MICROV  ?= 8
BUILDV  ?= -1
RELEASE := $(MAJORV).$(MINORV).$(MICROV)${BUILDV}

BASE    := kp-report
PKGNAME := $(BASE)-$(RELEASE)
BINS    := spawn_editor SetSystemTime CheckOrthancDataMount CDW_Configure restart_orthanc

KPLIB	:= ${PKGNAME}/usr/lib/kp-report

all:    dist

.PHONY: dist
dist:
	rm -rf ${BASE}-*
	for c in $(BINS); do install -D -m 755 $$c $(PKGNAME)/usr/bin/$$c; done
	install -D -m 640 orthanc_datamount_checker.service ${PKGNAME}/lib/systemd/system/orthanc_datamount_checker.service
	install -D -m 640 cdw_configure.service ${PKGNAME}/lib/systemd/system/cdw_configure.service
	install -D -m 640 dbmount.conf ${PKGNAME}/lib/systemd/system/orthanc.service.d/dbmount.conf
	install -D -m 640 configure.conf ${PKGNAME}/lib/systemd/system/orthanc.service.d/configure.conf
	install -D -m 440 orthanc.sudo ${PKGNAME}/etc/sudoers.d/orthanc
	install -D -m 644 ../ReportPlugin/Build/libReport.so.1.0 ${KPLIB}/libReport.so.1.0
	install -D -m 644 ../OHIFPlugin/Build/libOrthancOHIF.so.1.4 ${KPLIB}/libOrthancOHIF.so.1.4
	install -D -m 555 SetSystemTime.desktop ${KPLIB}/SetSystemTime.desktop
	for i in Templates/*.json; do install -d -m 555 $$i ${KPLIB}/templates/$$i; done
	mkdir -p -m 755 $(PKGNAME)/DEBIAN
	sed -e "s,%VERSION%,$(RELEASE)," control > $(PKGNAME)/DEBIAN/control
	cp copyright preinst postinst postrm ${PKGNAME}/DEBIAN
	dpkg-deb --build $(PKGNAME)

clean:
	@rm -rf $(BASE)-*
