Name:           ecl
Version:        0.9l
Release:        1%{?dist}
Summary:        Embeddable Common-Lisp

Group:          Development/Languages
License:        LGPLv2+
URL:            http://ecls.sourceforge.net
Source0:	http://switch.dl.sourceforge.net/sourceforge/ecls/ecl-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libX11-devel
BuildRequires:	m4
BuildRequires:	texinfo
BuildRequires:  texi2html
BuildRequires:  gmp-devel
Requires:       gcc
Requires(post): policycoreutils /sbin/install-info
Requires(postun): policycoreutils /sbin/install-info
ExcludeArch:    ppc64

%description
ECL (Embeddable Common-Lisp) is an interpreter of the Common-Lisp
language as described in the X3J13 Ansi specification, featuring CLOS
(Common-Lisp Object System), conditions, loops, etc, plus a translator
to C, which can produce standalone executables.

# no -devel package for header files is split off
# since they are required by the main package


%prep
%setup0 -q
# wrong character in texinfo file
sed -i 's|\xc7||' src/doc/user.txi
# set rpath to the final path
sed -i's|-Wl,--rpath,~A|-Wl,--rpath,%{_libdir}/ecl|' src/configure
find -name CVS | xargs rm -rf


%build
%configure --enable-boehm=included --enable-threads=yes --with-clx
make
(cd build/doc; make all html)


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
(cd build/doc; make DESTDIR=$RPM_BUILD_ROOT install)
rm -fr $RPM_BUILD_ROOT%{_infodir}/dir
rm -fr $RPM_BUILD_ROOT%{_docdir}

find $RPM_BUILD_ROOT%{_libdir}/ecl -name '*.lsp' | xargs chmod 0644

%post
/usr/sbin/semanage fcontext -a -t textrel_shlib_t "%{_libdir}/libecl.so" 2>/dev/null || :
/sbin/restorecon "%{_libdir}/libecl.so" 2> /dev/null || :
/sbin/install-info %{_infodir}/ecl.info %{_infodir}/dir 2>/dev/null || :
/sbin/install-info %{_infodir}/ecldev.info %{_infodir}/dir 2>/dev/null || :
/sbin/install-info %{_infodir}/clx.info %{_infodir}/dir 2>/dev/null || :
/sbin/ldconfig

 
%postun
if [ $1 = 0 ]; then
  /usr/sbin/semanage fcontext -d -t textrel_shlib_t "%{_libdir}/libecl.so" 2>/dev/null || :
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
%{_libdir}/ecl
%{_libdir}/libecl.so
%{_includedir}/ecl
%{_mandir}/man*/*
%{_infodir}/*
%doc ANNOUNCEMENT Copyright LGPL
%doc examples


%changelog
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
