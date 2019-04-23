# TODO: -apidocs (doc++ or doxygen based?)
Summary:	The Universal Plug and Play (UPnP) SDK for Linux
Summary(pl.UTF-8):	Pakiet programistyczny Universal Plug and Play (UPnP) dla Linuksa
Name:		libupnp
Version:	1.8.4
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/pupnp/%{name}-%{version}.tar.bz2
# Source0-md5:	317ae98255cbabdb34cab8e4f8d20a50
Patch0:		%{name}-opt.patch
URL:		http://pupnp.sourceforge.net/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.8
BuildRequires:	libtool >= 2:1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux SDK for UPnP Devices (libupnp) provides developers with an
API and open source code for building control points, devices, and
bridges that are compliant with Version 1.0 of the Universal Plug and
Play Device Architecture Specification.

%description -l pl.UTF-8
Linuksowy pakiet programistyczny dla urządzeń UPnP (libupnp) dostarcza
programistom API i kod z otwartymi źródłami służące do tworzenia
punktów kontrolnych, urządzeń i mostków kompatybilnych z wersją 1.0
specyfikacji architektury urządzeń Universal Plug and Play.

%package devel
Summary:	Header files for libupnp
Summary(pl.UTF-8):	Pliki nagłówkowe libupnp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains header files for the Linux SDK for UPnP Devices
(libupnp).

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe dla linuksowego pakietu
programistycznego do urządzeń UPnP (libupnp).

%package static
Summary:	Static upnp libraries
Summary(pl.UTF-8):	Statyczne biblioteki upnp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static upnp libraries.

%description static -l pl.UTF-8
Statyczne biblioteki upnp.

%package apidocs
Summary:	API documentation for upnp libraries
Summary(pl.UTF-8):	Dokumentacja API bibliotek upnp
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for upnp libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek upnp.

%prep
%setup -q
%patch0 -p1

# LFS is required in library clients (including examples)
%{__sed} -i -e '/^Cflags/ s/$/ -D_FILE_OFFSET_BITS=64/' libupnp.pc.in
%{__sed} -i -e '/^AM_CPPFLAGS =/ s/= /= -D_FILE_OFFSET_BITS=64 /' upnp/sample/Makefile.am

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?debug:--enable-debug}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog THANKS
%attr(755,root,root) %{_libdir}/libixml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libixml.so.10
%attr(755,root,root) %{_libdir}/libupnp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libupnp.so.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libixml.so
%attr(755,root,root) %{_libdir}/libupnp.so
%{_libdir}/libixml.la
%{_libdir}/libupnp.la
%{_includedir}/upnp
%{_pkgconfigdir}/libupnp.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libixml.a
%{_libdir}/libupnp.a

%if 0
%files apidocs
%defattr(644,root,root,755)
%doc docs/dist/html/{ixml,upnp}
%endif
