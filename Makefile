PREFIX ?= /usr

default: all

include initfs/tools/Makefile

initfs.tar.bz2: tools
	tar -cjf initfs.tar.bz2 initfs/skeleton/ sbin/evkey \
		 sbin/reboot2 sbin/rtc-clear initfs/tools/gen_init_cpio

all: initfs.tar.bz2

install: all
	install -d $(DESTDIR)$(PREFIX)/sbin/
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -m 755 initfs/scripts/*.sh $(DESTDIR)$(PREFIX)/sbin/
	install -m 755 sbin/* $(DESTDIR)$(PREFIX)/sbin/
	install -m 755 tools/* $(DESTDIR)$(PREFIX)/bin/
	install -m 644 -D initfs.tar.bz2 $(DESTDIR)$(PREFIX)/share/hw-ramdisk/initfs.tar.bz2

clean: tools_clean
	rm -f initfs.tar.bz2

