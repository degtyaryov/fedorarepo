Name:           perl-EV
Version:        4.03
Release:        5%{?dist}
Summary:        Wrapper for the libev high-performance event loop library

Group:          Development/Libraries
# Note: The source archive includes a libev/ folder which contents are licensed
#       as "BSD or GPLv2+". However, those are removed at build-time and
#       perl-EV is instead built against the system-provided libev.
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/EV/
Source0:        http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/EV-%{version}.tar.gz
Patch0:         perl-EV-4.03-Don-t-ask-questions-at-build-time.patch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(common::sense)
BuildRequires:  gdbm-devel
BuildRequires:  libev-source == %{version}
BuildRequires:  perl(AnyEvent) => 2.6
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# As per review, a perl-EV-devel subpackage had at first been pushed to the
# repositories. It now has broken deps if it's not properly obsoleted/provided.
# TODO: Remove those two lines during the Fedora 17 development cycle.
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:      %{name}-devel < 4.03-5

%{?perl_default_filter}


%description
This module provides an interface to libev
(<http://software.schmorp.de/pkg/libev.html>). While the included documentation
is comprehensive, one might also consult the documentation of libev itself
(<http://cvs.schmorp.de/libev/ev.html>) for more subtle details on watcher
semantics or some discussion on the available backends, or how to force a
specific backend with "LIBEV_FLAGS", or just about in any case because it has
much more detailed information.


%prep
%setup -q -n EV-%{version}

# no questins during build
%patch0 -p1

# remove all traces of the bundled libev
rm -fr libev/*

# use the sources from the system libev
mkdir -p ./libev
cp -r /usr/share/libev-source/* ./libev/


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes COPYING README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/EV.pm
%{perl_vendorarch}/EV
%{perl_vendorarch}/EV/*.h
%{_mandir}/man3/*.3*


%changelog
* Tue Apr 12 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 4.03-5
- Add the correct Obsoletes/Provides to avoid broken deps from the -devel
  subpackage removal.

* Thu Apr 07 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 4.03-4
- Readded the header file to the main package, as per guidelines:
      -> http://fedoraproject.org/wiki/Packaging/Perl#.h_files_in_module_packages

* Tue Mar 08 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 4.03-3
- Some more fixes as part of the review process:
  - Fix the license tag to be only the license of perl-EV, and add a note about
    the included libev sources.
- Removed manual cleaning of the buildroot since it has been useless since
  Fedora 10 and even EPEL (>=6) doesn't need it now.

* Wed Feb 23 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 4.03-2
- Fixes asked during the review process:
  - Filter the private shared EV.so out of the automatic Provides
  - Put the header files in a -devel package
- Removed the Buildroot line since it's useless for newer versions of Fedora
  and this package can only go in Fedora >= 15 due to its libev dependency)

* Mon Jan 24 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 4.03-1
- Update to 4.03.
- Use the system libev instead of the bundled one.

* Sun Nov  8 2009 kwizart < kwizart at gmail.com > - 3.8-1
- Update to 3.8

* Tue Apr 28 2009 kwizart < kwizart at gmail.com > - 3.6-1
- Update to 3.6

* Mon Mar  2 2009 kwizart < kwizart at gmail.com > - 3.53-1
- Update to 3.53

* Tue Feb  3 2009 kwizart < kwizart at gmail.com > - 3.52-1
- Update to 3.52

* Tue Oct 14 2008 kwizart < kwizart at gmail.com > - 3.44-1
- Update to 3.44
- WIP conditional --with systemlibev

* Wed Jul 15 2008 kwizart < kwizart at gmail.com > - 3.431-1
- Update to 3.431
- Update License to (GPL+ or Artistic) and (BSD or GPLv2+)
- Add libev README and LICENSE

* Wed Jul  8 2008 kwizart < kwizart at gmail.com > - 3.43-1
- Update to 3.43

* Mon Jun  9 2008 kwizart < kwizart at gmail.com > - 3.42-2
- Disable filter AnyEvent

* Tue May 27 2008 kwizart < kwizart at gmail.com > - 3.42-1
- Update to 3.42

* Wed Apr 30 2008 kwizart < kwizart at gmail.com > - 3.31-1
- Initial package for Fedora

