Name:       hw-ramdisk
Summary:    Ramdisk for booting root
Version:    1.0.0
Release:    1
Group:      System/Boot
License:    GPLv2
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  findutils
BuildRequires:  gzip
BuildRequires:  cpio
Requires:  busybox-static


%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}


%build
make

%install

%make_install

%files
%defattr(-,root,root,-)
%{_sbindir}/*.sh
%dir %{_datadir}/hw-ramdisk
%{_datadir}/hw-ramdisk/initfs.tar.bz2
