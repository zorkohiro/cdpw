#
# Install/packaging step for kp-report
#
ifeq ($(INSTALL_ROOT),)
$(error INSTALL_ROOT not set)
endif

BINS    := spawn_editor CheckOrthancDataMount CDPW_Configure restart_orthanc code_dark_rptgen code_dark_configurator GetModality GetStudyDate age_in_years orthanc_reconfigure

DOCS	:= Code_Dark_PACS_Workstion_Configuration_Notes.pdf What_is_a_Code_Dark_PACS_Workstation.pdf
DOCDIR	:= $(CURDIR)/../Documentation

KPLIB	:= ${INSTALL_ROOT}/usr/lib/kp-report

install:
	for c in $(BINS); do install -D -m 755 $$c $(INSTALL_ROOT)/usr/bin/$$c; done
	install -D -m 640 orthanc_datamount_checker.service ${INSTALL_ROOT}/lib/systemd/system/orthanc_datamount_checker.service
	install -D -m 640 cdpw_configure.service ${INSTALL_ROOT}/lib/systemd/system/cdpw_configure.service
	install -D -m 640 dbmount.conf ${INSTALL_ROOT}/lib/systemd/system/orthanc.service.d/dbmount.conf
	install -D -m 640 configure.conf ${INSTALL_ROOT}/lib/systemd/system/orthanc.service.d/configure.conf
	install -D -m 440 orthanc.sudo ${INSTALL_ROOT}/etc/sudoers.d/orthanc
	mkdir -p ${KPLIB}
	cp images/* ${KPLIB}
	for i in Templates/*.json; do install -D -m 555 $$i ${KPLIB}/$$i; done
	install -D -m 600 configurator.json ${KPLIB}
	install -D -m 640 code_dark_configurator.desktop ${KPLIB}
	for i in $(DOCS); do cp ${DOCDIR}/$$i $(KPLIB)/$$i; done
	mkdir -p -m 755 $(INSTALL_ROOT)/DEBIAN
	echo $(RELEASE) > ${KPLIB}/version
	sed -e "s,%VERSION%,$(RELEASE)," control > $(INSTALL_ROOT)/DEBIAN/control
	cp copyright preinst postinst prerm postrm ${INSTALL_ROOT}/DEBIAN

all:

clean:

.PHONY: all install clean
