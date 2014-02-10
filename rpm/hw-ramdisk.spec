Name:       hw-ramdisk
Summary:    Ramdisk for booting root
Version:    0.0.2
Release:    1
Group:      System/Boot
License:    GPLv2
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  findutils
BuildRequires:  gzip
BuildRequires:  cpio
BuildRequires:  busybox-static


%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}


%build
ROOTFS_DIR=rootfs
# Copy busybox to rootfs
rm -rf ${ROOTFS_DIR}
mkdir -p ${ROOTFS_DIR}

mkdir -p ${ROOTFS_DIR}/bin/ ${ROOTFS_DIR}/usr/bin/ ${ROOTFS_DIR}/sbin/
cp /bin/busybox-static ${ROOTFS_DIR}/bin/busybox

# Some links to apps that the init needs.
ln -s /bin/busybox ${ROOTFS_DIR}/bin/cat
ln -s /bin/busybox ${ROOTFS_DIR}/bin/chmod
ln -s /bin/busybox ${ROOTFS_DIR}/bin/cpio
ln -s /bin/busybox ${ROOTFS_DIR}/bin/echo
ln -s /bin/busybox ${ROOTFS_DIR}/bin/find
ln -s /bin/busybox ${ROOTFS_DIR}/bin/ls
ln -s /bin/busybox ${ROOTFS_DIR}/bin/mkdir
ln -s /bin/busybox ${ROOTFS_DIR}/bin/mknod
ln -s /bin/busybox ${ROOTFS_DIR}/bin/mount
ln -s /bin/busybox ${ROOTFS_DIR}/bin/mv
ln -s /bin/busybox ${ROOTFS_DIR}/bin/ps
ln -s /bin/busybox ${ROOTFS_DIR}/bin/sh
ln -s /bin/busybox ${ROOTFS_DIR}/bin/sleep
ln -s /bin/busybox ${ROOTFS_DIR}/bin/sort
ln -s /bin/busybox ${ROOTFS_DIR}/bin/touch
ln -s /bin/busybox ${ROOTFS_DIR}/bin/true
ln -s /bin/busybox ${ROOTFS_DIR}/bin/umount
ln -s /bin/busybox ${ROOTFS_DIR}/bin/vi
ln -s /bin/busybox ${ROOTFS_DIR}/bin/env
ln -s /bin/busybox ${ROOTFS_DIR}/bin/ln
ln -s /bin/busybox ${ROOTFS_DIR}/bin/dmesg
ln -s /bin/busybox ${ROOTFS_DIR}/bin/sync

ln -s /bin/busybox ${ROOTFS_DIR}/usr/bin/rpm2cpio
ln -s /bin/busybox ${ROOTFS_DIR}/usr/bin/tail
ln -s /bin/busybox ${ROOTFS_DIR}/usr/bin/tee
ln -s /bin/busybox ${ROOTFS_DIR}/usr/bin/telnet
ln -s /bin/busybox ${ROOTFS_DIR}/usr/bin/telnetd
ln -s /bin/busybox ${ROOTFS_DIR}/usr/bin/top

ln -s /bin/busybox ${ROOTFS_DIR}/sbin/ifconfig
ln -s /bin/busybox ${ROOTFS_DIR}/sbin/losetup
ln -s /bin/busybox ${ROOTFS_DIR}/sbin/switch_root

# Copy our init to the rootfs dir.
install -D -m 755 init ${ROOTFS_DIR}/init
install -D -m 755 root-mount ${ROOTFS_DIR}/sbin/root-mount

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/boot/
# Make the ramdisk file from the rootfs directory.
pushd rootfs/
find . | cpio -o -H newc --quiet | gzip > %{buildroot}/boot/%{name}.gz
popd

%files
%defattr(-,root,root,-)
/boot/%{name}.gz
%doc LICENSE README



