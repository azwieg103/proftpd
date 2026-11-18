%global _hardened_build 1
Name:           proftpd
Version:        %{proftpd_version}
Release:        %{?proftpd_release}%{!?proftpd_release:ZWIEGNET.1}
Summary:        Flexible, stable and highly configurable FTP server
License:        GPL-2.0-or-later
URL:            https://www.proftpd.org/
Source0:        %{name}-%{version}.tar.gz
Source1:        proftpd.conf
Source2:        proftpd.service
Source3:        sysconfig.proftpd
Source4:        proftpd.tmpfiles
Source5:        proftpd.logrotate
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconf-pkg-config
BuildRequires:  gettext-devel
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  zlib-devel
BuildRequires:  pcre2-devel
BuildRequires:  libacl-devel
BuildRequires:  libcap-devel
BuildRequires:  openldap-devel
BuildRequires:  sqlite-devel
BuildRequires:  libpq-devel
BuildRequires:  mariadb-connector-c-devel
BuildRequires:  systemd-rpm-macros

%description
ProFTPD is a highly configurable FTP server for Unix-like operating systems.
It supports virtual hosts, Unix and LDAP authentication, SQL authentication,
FTP over TLS, and the SFTP protocol through its modular architecture.

%prep
%setup -q -n proftpd-%{version}

%build
%configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_localstatedir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --enable-openssl \
    --enable-shadow \
    --enable-nls \
    --with-modules=mod_tls:mod_sftp:mod_ldap:mod_sql:mod_sql_sqlite:mod_sql_postgres:mod_sql_mysql
%make_build

%install
rm -rf %{buildroot}
%make_install

# The service is not enabled automatically. Administrators must configure
# TLS and firewall/passive-port policy before exposing FTP to a network.
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/proftpd.conf
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/proftpd.service
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/proftpd
install -Dpm 0644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}/proftpd.conf
install -Dpm 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/proftpd
install -d -m 0750 %{buildroot}%{_localstatedir}/log/proftpd

find %{buildroot} \( -type f -o -type l \) \
    ! -path '%{buildroot}%{_sysconfdir}/proftpd.conf' \
    ! -path '%{buildroot}%{_unitdir}/proftpd.service' \
    ! -path '%{buildroot}%{_sysconfdir}/sysconfig/proftpd' \
    ! -path '%{buildroot}%{_tmpfilesdir}/proftpd.conf' \
    ! -path '%{buildroot}%{_sysconfdir}/logrotate.d/proftpd' \
    ! -path '%{buildroot}%{_mandir}/man*' \
    | sed 's#^%{buildroot}##' | sort > %{_builddir}/proftpd-filelist

%pre
getent group proftpd >/dev/null || groupadd -r proftpd
getent passwd proftpd >/dev/null || \
    useradd -r -g proftpd -d /var/empty -s /sbin/nologin \
    -c "ProFTPD server" proftpd
exit 0

%post
%systemd_post proftpd.service

%preun
%systemd_preun proftpd.service

%postun
%systemd_postun_with_restart proftpd.service

%files -f %{_builddir}/proftpd-filelist
%license COPYING
%config(noreplace) %{_sysconfdir}/proftpd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/proftpd
%config(noreplace) %{_sysconfdir}/logrotate.d/proftpd
%{_unitdir}/proftpd.service
%{_tmpfilesdir}/proftpd.conf
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %attr(0750,root,proftpd) %{_localstatedir}/log/proftpd

%changelog
* Wed Nov 18 2026 Zwiegnet Packaging <packages@zwiegnet.com> - %{version}-%{release}
- Initial Enterprise Linux 10 rebuild.
