#
# Install/packaging step for kp-report
#
ifeq ($(INSTALL_ROOT),)
$(error INSTALL_ROOT not set)
endif

IBINS	:= CDPW_Configure CheckOrthancDataMount orthanc_reconfigure restart_orthanc
BINS	:= age_in_years code_dark_configurator code_dark_rptgen code_dark_study_selector GetStudyDate spawn_editor

DOCS	:= Code_Dark_PACS_Workstion_Configuration_Notes.pdf What_is_a_Code_Dark_PACS_Workstation.pdf
DOCDIR	:= $(CURDIR)/../Documentation

KPLIB	:= ${INSTALL_ROOT}/usr/lib/kp-report

install:
	mkdir -p ${KPLIB}/Templates
	cp images/* ${KPLIB}

	for c in $(BINS); do install -D -m 755 ${CURDIR}/../Scripts/$$c $(INSTALL_ROOT)/usr/bin/$$c; done
	for c in $(IBINS); do install -D -m 755 $$c $(INSTALL_ROOT)/usr/bin/$$c; done
	for c in $(DOCS); do cp ${DOCDIR}/$$c $(KPLIB)/$$c; done

	for c in ${CURDIR}/../Templates/*.json; do cp $$c ${KPLIB}/Templates/`basename $$c`; done

	install -D -m 640 orthanc_datamount_checker.service ${INSTALL_ROOT}/lib/systemd/system/orthanc_datamount_checker.service
	install -D -m 640 cdpw_configure.service ${INSTALL_ROOT}/lib/systemd/system/cdpw_configure.service
	install -D -m 640 dbmount.conf ${INSTALL_ROOT}/lib/systemd/system/orthanc.service.d/dbmount.conf
	install -D -m 640 configure.conf ${INSTALL_ROOT}/lib/systemd/system/orthanc.service.d/configure.conf
	install -D -m 440 orthanc.sudo ${INSTALL_ROOT}/etc/sudoers.d/orthanc
	install -D -m 600 configurator.json ${KPLIB}
	install -D -m 640 code_dark_configurator.desktop ${KPLIB}

	mkdir -p -m 755 $(INSTALL_ROOT)/DEBIAN
	echo $(RELEASE) > ${KPLIB}/version
	sed -e "s,%VERSION%,$(RELEASE)," control > $(INSTALL_ROOT)/DEBIAN/control
	cp copyright preinst postinst prerm postrm ${INSTALL_ROOT}/DEBIAN

all:

clean:

.PHONY: all install clean
