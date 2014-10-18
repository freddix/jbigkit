Summary:	JBIG1 lossless image compression library
Name:		jbigkit
Version:	2.1
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://www.cl.cam.ac.uk/~mgk25/download/%{name}-%{version}.tar.gz
# Source0-md5:	ebcf09bed9f14d7fa188d3bd57349522
Patch0:		%{name}-shared.patch
Patch1:		%{name}-warnings.patch
URL:		http://www.cl.cam.ac.uk/~mgk25/jbigkit/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JBIG-KIT is a software implementation of the JBIG1 data compression
standard (ITU-T T.82), which was designed for bi-level image data,
such as scanned documents. This library is available in portable C
code. It is widely used in fax products, printer firmware, printer
drivers, document management systems and imaging software.

%package devel
Summary:	Development files for JBIG1
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file needed to build programs using JBIG1 library.

%package progs
Summary:	JBIG1 utilities
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description progs
Utilities converting JBIG1 and PBM images.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} -j1 \
	CC="%{__cc}"				\
	OPTFLAGS="%{rpmcflags} %{rpmcppflags}"	\
	LDFLAGS="%{rpmldflags}"

%check
%{__make} -j1 test

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir},%{_mandir}/man1}

install libjbig/libjbig.so.%{version} $RPM_BUILD_ROOT%{_libdir}
install libjbig/libjbig85.so.%{version} $RPM_BUILD_ROOT%{_libdir}
ln -sf libjbig.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/libjbig.so
ln -sf libjbig85.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/libjbig85.so

install libjbig/{jbig.h,jbig85.h,jbig_ar.h} $RPM_BUILD_ROOT%{_includedir}
install pbmtools/???to??? $RPM_BUILD_ROOT%{_bindir}
install pbmtools/???to???85 $RPM_BUILD_ROOT%{_bindir}

install pbmtools/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
# INSTALL is about "installing and using" jbigkit
%doc ANNOUNCE CHANGES INSTALL TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

