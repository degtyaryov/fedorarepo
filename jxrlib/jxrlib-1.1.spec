Name:           jxrlib
Epoch:          1
Version:        1.1
Release:        1%{?dist}

Summary:        JPEG XR is an approved ISO/IEC International standard (its official designation is ISO/IEC 29199-2).
Group:          Applications/Multimedia
License:        Microsoft License
URL:            http://jxrlib.codeplex.com/

Source0:        jxrlib-%{version}.tar.gz
Source1:        jxrlib-copyright
Source2:        JxrDecApp.1
Source3:        JxrEncApp.1

Patch0:         jxrlib-usecmake.patch
Patch1:         jxrlib-bug748590.patch
Patch2:         jxrlib-typos.patch

BuildRequires:  cmake >= 2.8

%description
JPEG XR is an approved ISO/IEC International standard (its official designation is ISO/IEC 29199-2).

JPEG XR started its life in Microsoft Research. It publicly first appeared as the HD Photo format in Windows Vista.

For web developers, JPEG XR has a large number of interesting features, see the table below. Some of these are big advantages over other image formats like JPEG, PNG, OpenEXR, and TIFF.

 - Better Compression (40% smaller than JPEG)
 - Lossless Mode (better compression than PNG)
 - Alpha Channel (compress color lossy and alpha losslessly)
 - Extended Bitdepth (supports 8-, 16-, and 32-bit/channel)
 - Progressive Decode
 - Advanced Decoding Features (tile-based layout, for efficient
   region-of-interest access.)

%package devel
Summary:        Library links and header files for jxrlib app development
Group:		Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description devel
jxrlib-devel contains the library links and header files you'll
need to develop jxrlib applications.

If you want to create applications that will use jxrlib code or
APIs, you need to install jxrlib-devel as well as jxrlib.
You do not need to install it if you just want to use jxrlib,
however.

%package libs
Summary:	jxrlib libraries to link with
Group:		Applications/Multimedia

%description libs
This packages contains a shared libraries to use within other applications.


%prep
%setup -q -n jxrlib-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
mkdir -p build
pushd build
%cmake CMAKE_VERBOSE=1 \
%ifnarch x86_64 ia64
 -DENABLE_SSE=0 \
 -DENABLE_SSE2=0 \
%endif
 %{!?_with_sse3:-DENABLE_SSE3=0} \
 -DCMAKE_BUILD_TYPE=ReleaseWithDebInfo \
 -DBUILD_TEST=1 \
%ifarch %{ix86} x86_64 ia64
 -DJXRLIB_INSTALL_LIB_DIR=%{_libdir} \
%endif
 -DBUILD_TESTS=0 \
 ..

make VERBOSE=1 %{?_smp_mflags}

popd

%install
pushd build
make install DESTDIR=%{buildroot} INSTALL="install -p" CPPROG="cp -p"

find %{buildroot} -type f -empty -exec rm -f '{}' \;
find %{buildroot} -type f -iname '*.so' -exec chmod 0755 '{}' \;

%{__install} -Dp -m 644 %{SOURCE1} %{buildroot}%{_docdir}/%{name}-%{version}/copyright
%{__install} -Dp -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man1/JxrDecApp.1
%{__install} -Dp -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man1/JxrEncApp.1

popd

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc doc/*
%{_bindir}/JxrDecApp
%{_bindir}/JxrEncApp
%{_mandir}/man1/JxrDecApp.*
%{_mandir}/man1/JxrEncApp.*


%files libs
%defattr(-,root,root,-)
%{_libdir}/libjpegxr.so
%{_libdir}/libjpegxr.so.*
%{_libdir}/libjxrglue.so
%{_libdir}/libjxrglue.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*

%changelog
* Thu Apr 9 2015 Degtyaryov Dmitriy <degtyaryov@gmail.com> - 1:1.1-1
- jxrlib version 1.1
- build for fedora based on debian libjxr0
