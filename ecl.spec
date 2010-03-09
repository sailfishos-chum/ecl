Name:           ecl
Version:        10.3.1
Release:        1%{?dist}
Summary:        Embeddable Common-Lisp

Group:          Development/Languages
License:        LGPLv2+ and BSD and MIT and Public Domain
URL:            http://ecls.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/ecls/ecls/10.3/ecl-%{version}.tgz
# This patch was sent upstream on 9 Mar 2010.  (Actually, the equivalent patch
# to src/aclocal.m4 was sent upstream; this patch is to src/configure.)  The
# patch fixes a malformed test for sem_init() that causes the test to fail
# spuriously.
Patch0:         ecl-10.3.1-semaphore.patch
# This patch has not yet been sent upstream.  The code assumes that all libffi
# headers are in a directory named "ffi".  On Fedora, they are not.
Patch1:         ecl-10.3.1-ffi.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libX11-devel
BuildRequires:  pkgconfig
BuildRequires:  texinfo
BuildRequires:  gmp-devel
BuildRequires:  gc-devel
BuildRequires:  libffi-devel
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
%patch0
%patch1

# Remove spurious executable bits
chmod a-x src/CHANGELOG
find src/c -type f -perm /0111 | xargs chmod a-x
find src/h -type f -perm /0111 | xargs chmod a-x


%build
%configure --enable-boehm=system --enable-gengc --enable-unicode \
  --enable-longdouble --enable-c99complex \
  --enable-threads=yes --with-__thread --with-clx \
  CPPFLAGS=`pkg-config --cflags libffi` \
  CFLAGS="${RPM_OPT_FLAGS} -fno-strict-aliasing"
make
(cd build/doc; make all )


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
(cd build/doc; make DESTDIR=$RPM_BUILD_ROOT install)
rm -fr $RPM_BUILD_ROOT%{_infodir}/dir
rm -fr $RPM_BUILD_ROOT%{_docdir}

# Add missing executable bits
chmod a+x $RPM_BUILD_ROOT%{_libdir}/ecl-%{version}/dpp
chmod a+x $RPM_BUILD_ROOT%{_libdir}/ecl-%{version}/ecl_min


%post
/sbin/install-info %{_infodir}/ecl.info %{_infodir}/dir 2>/dev/null || :
/sbin/install-info %{_infodir}/ecldev.info %{_infodir}/dir 2>/dev/null || :
/sbin/install-info %{_infodir}/clx.info %{_infodir}/dir 2>/dev/null || :
/sbin/ldconfig

 
%postun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/ecl.info %{_infodir}/dir 2>/dev/null || :
  /sbin/install-info --delete %{_infodir}/ecldev.info %{_infodir}/dir 2>/dev/null || :
  /sbin/install-info --delete %{_infodir}/clx.info %{_infodir}/dir 2>/dev/null || :
fi
/sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/ecl
%{_bindir}/ecl-config
%{_libdir}/ecl*
%{_libdir}/libecl.so*
%{_includedir}/ecl
%{_mandir}/man*/*
%{_infodir}/*
%doc ANNOUNCEMENT Copyright LGPL examples
%doc src/CHANGELOG src/doc/todo.txt src/doc/tutorial.txt


%changelog
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
