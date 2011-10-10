Name:           ecl
Version:        11.1.1
Release:        1%{?dist}.1
Summary:        Embeddable Common-Lisp

Group:          Development/Languages
License:        LGPLv2+ and BSD and MIT and Public Domain
URL:            http://ecls.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/ecls/ecls/11.1/ecl-%{version}.tar.gz
# The manual has not yet been released.  Use the following commands to generate
# the manual tarball:
#   git clone git://ecls.git.sourceforge.net/gitroot/ecls/ecl-doc
#   cd ecl-doc
#   git checkout 04798a28d55c5ec096af5976f0ceef663f4d717b
#   rm -fr .git
#   cd ..
#   tar cf ecl-doc.tar ecl-doc
#   xz ecl-doc.tar
Source1:        ecl-doc.tar.xz
Source2:        ecl.desktop
# A modified version of src/util/ecl.svg with extra whitespace removed.  The
# extra whitespace made the icon appear very small and shoved into a corner.
Source3:        ecl.svg
# This patch was accepted upstream on 9 Jan 2011.  It fixes a few autoconf
# constructs that are broken for Fedora, and also avoids building
# libatomic_ops from source.
Patch0:         ecl-11.1.1-configure.patch
# This patch was accepted upstream on 21 Jan 2011.  It fixes a few warnings
# from the C compiler that indicate situations that might be dangerous at
# runtime.
Patch1:         ecl-11.1.1-warnings.patch

BuildRequires:  libX11-devel
BuildRequires:  pkgconfig
BuildRequires:  gmp-devel
BuildRequires:  gc-devel
BuildRequires:  libffi-devel
BuildRequires:  libatomic_ops-devel
BuildRequires:  emacs-common
BuildRequires:  docbook-dtds
BuildRequires:  xmlto
BuildRequires:  desktop-file-utils
Requires:       gcc
Requires(post): coreutils, desktop-file-utils, gtk2
Requires(postun): coreutils, desktop-file-utils, gtk2

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
%patch1 -p1

# Remove spurious executable bits
chmod a-x src/CHANGELOG
find src/c -type f -perm /0111 | xargs chmod a-x
find src/h -type f -perm /0111 | xargs chmod a-x


%build
%configure --enable-unicode --enable-c99complex --enable-rpath=no \
  --enable-threads=yes --with-__thread --with-clx \
%ifarch x86_64
  --with-sse \
%endif
  CPPFLAGS=`pkg-config --cflags libffi` CFLAGS="${RPM_OPT_FLAGS}"
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

# Install the desktop file
desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE2}

# Install the desktop icon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps


%post
update-desktop-database -q >&/dev/null ||:
touch --no-create %{_datadir}/icons/hicolor

 
%postun
/sbin/ldconfig
update-desktop-database -q >&/dev/null ||:
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null ||:
fi


%posttrans
/sbin/ldconfig
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null ||:


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/ecl
%{_bindir}/ecl-config
%{_datadir}/applications/ecl.desktop
%{_datadir}/icons/hicolor/scalable/apps/ecl.svg
%{_libdir}/ecl*
%{_libdir}/libecl.so*
%{_includedir}/ecl
%{_mandir}/man1/*
%doc ANNOUNCEMENT Copyright LGPL examples src/CHANGELOG
%doc ecl-doc/ecl.css ecl-doc/html src/doc/amop.txt src/doc/types-and-classes


%changelog
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
