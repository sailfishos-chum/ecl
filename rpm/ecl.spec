%global major 24
%global minor 5
%global micro 10
Name:           ecl
Version:        %{major}.%{minor}.{micro}
Release:        3%{?dist}
Summary:        Embeddable Common-Lisp

License:        LGPLv2+ and BSD and MIT and Public Domain
URL:            https://common-lisp.net/project/ecl/
Source0:        %{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  gmp-devel
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(atomic_ops)
Requires:       %{name}-devel
Requires:       libgcc%{?_isa}
Requires:       glibc-devel%{?_isa}
Requires:       gmp-devel
Requires:       pkgconfig(libffi)
Requires:       pkgconfig(atomic_ops)
Requires(post): coreutils
Requires(postun): coreutils

%description
ECL (Embeddable Common Lisp) is an implementation of the Common Lisp
language as defined by the ANSI X3J13 specification.  ECL features a
bytecode compiler and interpreter, the ability to build standalone
executables and libraries, and extensions such as ASDF, sockets, and
Gray streams.

%if "%{?vendor}" == "chum"
Title: Embeddable Common-Lisp
Type: other
DeveloperName: Marius Gerbershagen
Categories:
- Library
Custom:
PackagingRepo: https://github.com/sailfishos-chum/ecl
Links:
Homepage: %{url}
%endif

%package -n lib%{name}
Summary:  Embeddable Common-Lisp -- shared library
Group:    System/Libraries

%description -n lib%{name}
This package contains the ECL shared library.

%package devel
Summary:  Embeddable Common-Lisp -- development files
Group:    Development/Libraries/C and C++
Requires: lib%{name} = %{version}

%description devel
ECL (Embeddable Common Lisp) is an implementation of the Common Lisp
language as defined by the ANSI X3J13 specification.  ECL features a
bytecode compiler and interpreter, the ability to build standalone
executables and libraries, and extensions such as ASDF, sockets, and
Gray streams.

This package contains development files for ECL.

%prep
%autosetup -p1 -n %{name}-%{version}/ecl

%build
%configure  --enable-boehm=included \
            --enable-libatomic=system --enable-gmp=system --with-dffi=system \
            --enable-c99complex --with-sse=yes --disable-manual \
            CFLAGS="%{optflags} -Wno-unused -Wno-return-type -Wno-unknown-pragmas"
make

%install
make DESTDIR=$RPM_BUILD_ROOT install

# Remove installed files that are in the wrong place
rm -fr $RPM_BUILD_ROOT%{_docdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/Copyright
rm -f $RPM_BUILD_ROOT%{_libdir}/LGPL

# Add missing executable bits
chmod a+x $RPM_BUILD_ROOT%{_libdir}/ecl-*/dpp
chmod a+x $RPM_BUILD_ROOT%{_libdir}/ecl-*/ecl_min

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%license COPYING LICENSE
%{_bindir}/%{name}
%{_libdir}/%{name}-*/
%{_mandir}/man1/%{name}.1.gz

%files -n lib%{name}
%license COPYING LICENSE
%{_libdir}/lib%{name}.so.*

%files devel
%license COPYING LICENSE
%{_bindir}/%{name}-config
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}/
%{_mandir}/man1/%{name}-config.1.gz

%changelog
* Tue Jul  1 2025 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 24.5.10-3
- Fix package dependencies

* Sun Jun 29 2025 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 24.5.10-2
- Remove static libraries
- Split into main/lib/devel packages

* Thu Jun 26 2025 Peter G. <sailfish@nephros.org> - 24.5.10-1
- Upstream update

* Sun Mar 21 2021 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 21.2.1-2
- Add static libraries

* Mon Feb 15 2021 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 21.2.1-1
- Upstream update

* Mon Feb 11 2019 Renaud Casenave-Péré <renaud@casenave-pere.fr> - 16.1.3-2
- Rebuilt for sailfishos 3.0.1.11

* Fri Feb 24 2017 Jerry James <loganjerry@gmail.com> - 16.1.3-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Mar  4 2016 Jerry James <loganjerry@gmail.com> - 16.1.2-1
- New upstream release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 16.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Oct  3 2015 Jerry James <loganjerry@gmail.com> - 16.0.0-1
- New upstream release
- Drop many upstreamed patches

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 20 2015 Jerry James <loganjerry@gmail.com> - 13.5.1-9
- Fix stack direction detection (broken with gcc 5)

* Fri Feb 13 2015 Jerry James <loganjerry@gmail.com> - 13.5.1-8
- Use license macro

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 18 2014 Rex Dieter <rdieter@fedoraproject.org> 13.5.1-5
- fix configure check for end-of-line when using -Werror=format-security

* Wed May 14 2014 Rex Dieter <rdieter@fedoraproject.org> 13.5.1-4
- backport GC_start_call_back fixes

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul  3 2013 Jerry James <loganjerry@gmail.com> - 13.5.1-2
- Update -warnings patch with more fixes from upstream

* Mon Jun  3 2013 Jerry James <loganjerry@gmail.com> - 13.5.1-1
- New upstream release
- Drop upstreamed -fixes patch
- Add -fenv-access patch to work around a GCC limitation

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Jerry James <loganjerry@gmail.com> - 12.12.1-3
- BR libatomic_ops-static instead of -devel (bz 889173)
- Pull in upstream patches for bugs discovered post-release
- Documentation needs docbook 5 schemas and XSL

* Sat Dec 08 2012 Rex Dieter <rdieter@fedoraproject.org> 12.12.1-2
- track libecl soname, so bumps aren't a surprise

* Fri Dec  7 2012 Jerry James <loganjerry@gmail.com> - 12.12.1-1
- New upstream release
- Drop upstreamed patches

* Wed Aug  8 2012 Jerry James <loganjerry@gmail.com> - 12.7.1-1
- New upstream release
- Add sighandler patch to fix thread-enabled build

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Rex Dieter <rdieter@fedoraproject.org> 12.2.1-4
- ecl missing Requires: libffi-devel (#837102)

* Wed Jun 13 2012 Jerry James <loganjerry@gmail.com> - 12.2.1-3
- Fix Requires so 32-bit gcc is not dragged into 64-bit platforms (bz 831383)
- Apply multiple fixes from bz 821183
- Rebuild to fix bz 822296

* Thu Apr 26 2012 Jerry James <loganjerry@gmail.com> - 12.2.1-2
- Add missing Requires (bz 816675)

* Sat Feb  4 2012 Jerry James <loganjerry@gmail.com> - 12.2.1-1
- New upstream release
- Fix source URL

* Fri Jan  6 2012 Jerry James <loganjerry@gmail.com> - 11.1.1-2
- Rebuild for GCC 4.7
- Drop unnecessary spec file elements (clean script, etc.)

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 11.1.1-1.2
- rebuild with new gmp without compat lib

* Mon Oct 10 2011 Peter Schiffer <pschiffe@redhat.com> - 11.1.1-1.1
- rebuild with new gmp

* Tue Mar  1 2011 Jerry James <loganjerry@gmail.com> - 11.1.1-1
- New release 11.1.1
- Drop libffi patch (fixed upstream)
- Add -configure and -warnings patches
- Add SSE2 support on x86_64
- Disable rpath explicitly, as it is now enabled by default
- Add desktop file and icon

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Apr 12 2010 Jerry James <loganjerry@gmail.com> - 10.4.1-1
- New release 10.4.1
- Drop upstreamed semaphore patch
- Add manual built from ecl-doc sources, replaces info documentation

* Tue Mar  9 2010 Jerry James <loganjerry@gmail.com> - 10.3.1-1
- New release 10.3.1

* Wed Feb 24 2010 Jerry James <loganjerry@gmail.com> - 10.2.1-1
- New release 10.2.1

* Sun Aug  9 2009 Gerard Milmeister <gemi@bluewin.ch> - 9.8.1-1
- new release 9.8.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Gerard Milmeister <gemi@bluewin.ch> - 9.6.1-1
- new release 9.6.1

* Mon Oct  6 2008 Gerard Milmeister <gemi@bluewin.ch> - 0.9l-2
- disable ppc64 (fails to build)

* Wed Aug  6 2008 Gerard Milmeister <gemi@bluewin.ch> - 0.9l-1
- new release 0.9l

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9j-2
- Autorebuild for GCC 4.3

* Sat Dec 29 2007 Gerard Milmeister <gemi@bluewin.ch> - 0.9j-1
- new release 0.9j

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 0.9i-3
- Rebuild for FE6

* Sun Jul 23 2006 Gerard Milmeister <gemi@bluewin.ch> - 0.9i-2
- release number fix

* Sat Jul  8 2006 Gerard Milmeister <gemi@bluewin.ch> - 0.9i-1
- new version 0.9i

* Wed Mar 15 2006 Gerard Milmeister <gemi@bluewin.ch> - 0.9h-5
- patch for gcc 4.1

* Tue Mar 14 2006 Gerard Milmeister <gemi@bluewin.ch> - 0.9h-4
- removed buildreq perl

* Fri Mar 10 2006 Gerard Milmeister <gemi@bluewin.ch> - 0.9h-3
- fixed permissions and texinfo problems

* Sun Dec  4 2005 Gerard Milmeister <gemi@bluewin.ch> - 0.9h-2
- buildreq m4, texinfo

* Mon Nov 21 2005 Gerard Milmeister <gemi@bluewin.ch> - 0.9h-1
- New Version 0.9h

* Sat Aug 20 2005 Gerard Milmeister <gemi@bluewin.ch> - 0.9g-1
- New Version 0.9g

* Sun Apr 10 2005 Gerard Milmeister <gemi@bluewin.ch> - 0.9e-1.cvs20050410
- CVS Version 20050410

* Sun Apr 10 2005 Gerard Milmeister <gemi@bluewin.ch> - 0.9e-1
- New Version 0.9e

* Sat Nov  6 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:0.9-0.fdr.1.d
- New Version 0.9d

* Sat Mar 27 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:0.9-0.fdr.1.c
- First Fedora release
