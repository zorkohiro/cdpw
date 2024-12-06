MAJORV  ?= 0
MINORV  ?= 9
MICROV  ?= 1
RELEASE := $(MAJORV).$(MINORV).$(MICROV)

BASE    := kp-report
PKGNAME := $(BASE)-$(RELEASE)
BINS    := spawn_ol

all:    dist

.PHONY: dist
dist:
	rm -rf ${BASE}-*
	for c in $(BINS); do install -D -m 755 $$c $(PKGNAME)/usr/bin/$$c; done
	install -D -m 644 ../Build/libReport.so.1.0 ${PKGNAME}/usr/lib/kp-report/libReport.so.1.0
	mkdir -p ${PKGNAME}/usr/share/orthanc/templates
	cp Templates/*.odt ${PKGNAME}/usr/share/orthanc/templates
	mkdir -p -m 755 $(PKGNAME)/DEBIAN
	sed -e "s,%VERSION%,$(RELEASE)," control > $(PKGNAME)/DEBIAN/control
	cp postinst prerm ${PKGNAME}/DEBIAN
	dpkg-deb --build $(PKGNAME)

clean:
	@rm -rf $(BASE)-*

