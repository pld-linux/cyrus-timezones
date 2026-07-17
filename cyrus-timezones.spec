#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Timezone information for the Cyrus IMAP Server
Summary(pl.UTF-8):	Informacja o strefach czasowych dla serwera Cyrus IMAP
Name:		cyrus-timezones
Version:	1.0
%define	gitref	cyruslibs-fastmail-v86
%define	snap	20260610
%define	rel	1
Release:	0.%{snap}.%{rel}
License:	BSD (library), Public Domain (zoneinfo)
Group:		Libraries
#Source0Download: https://github.com/cyrusimap/cyrus-timezones/tags
Source0:	https://github.com/cyrusimap/cyrus-timezones/archive/%{gitref}/%{name}-%{gitref}.tar.gz
# Source0-md5:	366bbf62c24e93278fd6e5f8ad70fc02
Patch0:		%{name}-flags.patch
Patch1:		%{name}-link.patch
URL:		https://github.com/cyrusimap/cyrus-timezones
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	jansson-devel
BuildRequires:	libical-devel >= 4
BuildRequires:	libical-vzic
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides timezone information for the Cyrus IMAP Server.

%description -l pl.UTF-8
Ten pakiet dostarcza informacje o strefach czasowych dla serwera Cyrus
IMAP.

%package -n cyrus-guesstz
Summary:	Library to guess IANA timezone names from VTIMEZONE
Summary(pl.UTF-8):	Biblioteka do zgadywania nazw stref czasowych z VTIMEZONE
License:	BSD
Group:		Libraries

%description -n cyrus-guesstz
Library to guess IANA timezone names from VTIMEZONE.

%description -n cyrus-guesstz -l pl.UTF-8
Biblioteka do zgadywania nazw stref czasowych z VTIMEZONE.

%package -n cyrus-guesstz-devel
Summary:	Header files for guesstz library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki guesstz
License:	BSD
Group:		Development/Libraries
Requires:	cyrus-guesstz = %{version}-%{release}
Requires:	jansson-devel
Requires:	libical-devel >= 4

%description -n cyrus-guesstz-devel
Header files for guesstz library.

%description -n cyrus-guesstz-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki guesstz.

%package -n cyrus-guesstz-static
Summary:	Static guesstz library
Summary(pl.UTF-8):	Statyczna biblioteka guesstz
License:	BSD
Group:		Development/Libraries
Requires:	cyrus-guesstz-devel = %{version}-%{release}

%description -n cyrus-guesstz-static
Static guesstz library.

%description -n cyrus-guesstz-static -l pl.UTF-8
Statyczna biblioteka guesstz.

%prep
%setup -q -n %{name}-%{gitref}
%patch -P0 -p1
%patch -P1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libguesstz.la

%{__rm} $RPM_BUILD_ROOT%{_datadir}/cyrus-timezones/zoneinfo/zones.h

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n cyrus-guesstz -p /sbin/ldconfig
%postun	-n cyrus-guesstz -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%dir %{_datadir}/cyrus-timezones
%dir %{_datadir}/cyrus-timezones/zoneinfo
%{_datadir}/cyrus-timezones/zoneinfo/Africa
%{_datadir}/cyrus-timezones/zoneinfo/America
%{_datadir}/cyrus-timezones/zoneinfo/Antarctica
%{_datadir}/cyrus-timezones/zoneinfo/Arctic
%{_datadir}/cyrus-timezones/zoneinfo/Asia
%{_datadir}/cyrus-timezones/zoneinfo/Atlantic
%{_datadir}/cyrus-timezones/zoneinfo/Australia
%{_datadir}/cyrus-timezones/zoneinfo/Brazil
%{_datadir}/cyrus-timezones/zoneinfo/Canada
%{_datadir}/cyrus-timezones/zoneinfo/Chile
%{_datadir}/cyrus-timezones/zoneinfo/Etc
%{_datadir}/cyrus-timezones/zoneinfo/Europe
%{_datadir}/cyrus-timezones/zoneinfo/Indian
%{_datadir}/cyrus-timezones/zoneinfo/Mexico
%{_datadir}/cyrus-timezones/zoneinfo/Pacific
%{_datadir}/cyrus-timezones/zoneinfo/US
%{_datadir}/cyrus-timezones/zoneinfo/*.ics
%{_datadir}/cyrus-timezones/zoneinfo/version
%{_datadir}/cyrus-timezones/zoneinfo/zones.tab
%{_pkgconfigdir}/cyrus-timezones.pc

%files -n cyrus-guesstz
%defattr(644,root,root,755)
%doc guesstz/COPYING
%attr(755,root,root) %{_bindir}/cyr_guesstz
%{_libdir}/libguesstz.so.*.*.*
%ghost %{_libdir}/libguesstz.so.0
%dir %{_datadir}/cyrus-timezones
%dir %{_datadir}/cyrus-timezones/zoneinfo
%{_datadir}/cyrus-timezones/zoneinfo/guesstz.db

%files -n cyrus-guesstz-devel
%defattr(644,root,root,755)
%{_libdir}/libguesstz.so
%{_includedir}/guesstz.h
%{_pkgconfigdir}/guesstz.pc

%if %{with static_libs}
%files -n cyrus-guesstz-static
%defattr(644,root,root,755)
%{_libdir}/libguesstz.a
%endif
