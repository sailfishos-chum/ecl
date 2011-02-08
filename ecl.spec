Name:           ecl
Version:        10.4.1
Release:        2%{?dist}
Summary:        Embeddable Common-Lisp

Group:          Development/Languages
License:        LGPLv2+ and BSD and MIT and Public Domain
URL:            http://ecls.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/ecls/ecls/10.4/ecl-%{version}.tar.gz
# The manual has not yet been released.  Use the following commands to generate
# the manual tarball:
#   git clone git://ecls.git.sourceforge.net/gitroot/ecls/ecl-doc
#   cd ecl-doc
#   git checkout a70a56aedbfad1cc26ffe6f4783e37c2a4e5c0b4
#   rm -fr .git
#   cd ..
#   tar cf ecl-doc.tar ecl-doc
#   xz ecl-doc.tar
Source1:        ecl-doc.tar.xz
# This patch has not yet been sent upstream.  The code assumes that all libffi
# headers are in a directory named "ffi".  On Fedora, they are not.
Patch0:         ecl-10.4.1-ffi.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libX11-devel
BuildRequires:  pkgconfig
BuildRequires:  gmp-devel
BuildRequires:  gc-devel
BuildRequires:  libffi-devel
BuildRequires:  emacs-common
BuildRequires:  docbook-dtds
BuildRequires:  xmlto
Requires:       gcc
Requires(post): info
Requires(postun): info

%description
ECL (Embeddable Common Lisp) is an implementation of the Common Lisp
language as defined by the ANSI X3J13 specification.  ECL features a
bytecode compiler and interpreter, the ability to build standalone
executables and libraries, and extensions such as ASDF, sockets, and
Gray streams.

# no -devel package for header files is split off
# since they are required by the main package


%prep
%setup -q
%setup -q -T -D -a 1
%patch0

# Remove spurious executable bits
chmod a-x src/CHANGELOG
find src/c -type f -perm /0111 | xargs chmod a-x
find src/h -type f -perm /0111 | xargs chmod a-x


%build
%configure --enable-boehm=system --enable-unicode --enable-longdouble \
  --enable-c99complex --enable-threads=yes --with-__thread --with-clx \
  CPPFLAGS=`pkg-config --cflags libffi` \
  CFLAGS="${RPM_OPT_FLAGS} -fno-strict-aliasing"
make
make -C ecl-doc


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove installed files that are in the wrong place
rm -fr $RPM_BUILD_ROOT%{_docdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/Copyright
rm -f $RPM_BUILD_ROOT%{_libdir}/LGPL

# Install the man pages
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
sed -e "s|@bindir@|%{_bindir}|" src/doc/ecl.man.in > \
  $RPM_BUILD_ROOT%{_mandir}/man1/ecl.1
cp -p src/doc/ecl-config.man.in $RPM_BUILD_ROOT%{_mandir}/man1/ecl-config.1

# Add missing executable bits
chmod a+x $RPM_BUILD_ROOT%{_libdir}/ecl-%{version}/dpp
chmod a+x $RPM_BUILD_ROOT%{_libdir}/ecl-%{version}/ecl_min


%post -p /sbin/ldconfig

 
%postun -p /sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/ecl
%{_bindir}/ecl-config
%{_libdir}/ecl*
%{_libdir}/libecl.so*
%{_includedir}/ecl
%{_mandir}/man1/*
%doc ANNOUNCEMENT Copyright LGPL examples src/CHANGELOG
%doc ecl-doc/ecl.css ecl-doc/html


%changelog
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
