#
# Install/packaging step for kp-report
#
ifeq ($(INSTALL_ROOT),)
$(error INSTALL_ROOT not set)
endif

BINS    := spawn_editor CheckOrthancDataMount CDW_Configure restart_orthanc code_dark_rptgen GetModality

KPLIB	:= ${INSTALL_ROOT}/usr/lib/kp-report

install:
	for c in $(BINS); do install -D -m 755 $$c $(INSTALL_ROOT)/usr/bin/$$c; done
	install -D -m 640 orthanc_datamount_checker.service ${INSTALL_ROOT}/lib/systemd/system/orthanc_datamount_checker.service
	install -D -m 640 cdw_configure.service ${INSTALL_ROOT}/lib/systemd/system/cdw_configure.service
	install -D -m 640 dbmount.conf ${INSTALL_ROOT}/lib/systemd/system/orthanc.service.d/dbmount.conf
	install -D -m 640 configure.conf ${INSTALL_ROOT}/lib/systemd/system/orthanc.service.d/configure.conf
	install -D -m 440 orthanc.sudo ${INSTALL_ROOT}/etc/sudoers.d/orthanc
	for i in Templates/*.json; do install -D -m 555 $$i ${KPLIB}/$$i; done
	mkdir -p ${INSTALL_ROOT}/usr/bin
	mkdir -p -m 755 $(INSTALL_ROOT)/DEBIAN
	sed -e "s,%VERSION%,$(RELEASE)," control > $(INSTALL_ROOT)/DEBIAN/control
	cp copyright preinst postinst postrm ${INSTALL_ROOT}/DEBIAN
all:

clean:

.PHONY: all install clean
