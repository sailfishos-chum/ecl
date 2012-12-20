Name:           ecl
Version:        12.12.1
Release:        3%{?dist}
Summary:        Embeddable Common-Lisp

Group:          Development/Languages
License:        LGPLv2+ and BSD and MIT and Public Domain
URL:            http://ecls.sourceforge.net/
Source0:        http://downloads.sourceforge.net/ecls/%{name}-%{version}.tgz
# The manual has not yet been released.  Use the following commands to generate
# the manual tarball:
#   git clone git://ecls.git.sourceforge.net/gitroot/ecls/ecl-doc
#   cd ecl-doc
#   git checkout 3af1c1eaec1a3cb590c0ce140f881f48be19995e
#   rm -fr .git
#   cd ..
#   tar cJf ecl-doc.tar.xz ecl-doc
Source1:        %{name}-doc.tar.xz
Source2:        %{name}.desktop
# A modified version of src/util/ecl.svg with extra whitespace removed.  The
# extra whitespace made the icon appear very small and shoved into a corner.
Source3:        %{name}.svg
# This patch was sent upstream on 4 Feb 2012.  It fixes a few warnings
# from the C compiler that indicate situations that might be dangerous at
# runtime.
Patch0:         %{name}-12.12.1-warnings.patch
# Do not use a separate thread to handle signals by default if built with
# boehm-gc support.
# This prevents a deadlock when building maxima with ecl support in
# fedora, and should handle by default these problems:
# http://trac.sagemath.org/sage_trac/ticket/11752
# http://www.mail-archive.com/ecls-list@lists.sourceforge.net/msg00644.html
Patch1:         %{name}-12.12.1-signal_handling_thread.patch
# Bug-fixing patches cherry picked from upstream's git.
Patch2:         %{name}-12.12.1-fixes.patch
# Work around xsltproc requiring namespace declarations for entities.
Patch3:         %{name}-12.12.1-xsltproc.patch

BuildRequires:  libX11-devel
BuildRequires:  pkgconfig
BuildRequires:  gmp-devel
BuildRequires:  gc-devel
BuildRequires:  libatomic_ops-static
BuildRequires:  libffi-devel
BuildRequires:  emacs-common
BuildRequires:  docbook5-schemas
BuildRequires:  docbook5-style-xsl
BuildRequires:  xmlto
BuildRequires:  desktop-file-utils
Requires:       gcc
Requires:       libgcc%{?_isa}
Requires:       glibc-devel%{?_isa}
Requires:       gc-devel%{?_isa}
Requires:       gmp-devel%{?_isa}
Requires:       libffi-devel%{?_isa}
Requires:       hicolor-icon-theme
Requires(post): coreutils
Requires(postun): coreutils

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
%patch1
%patch2 -p1
%patch3

# Remove spurious executable bits
chmod a-x src/CHANGELOG
find src/c -type f -perm /0111 | xargs chmod a-x
find src/h -type f -perm /0111 | xargs chmod a-x


%build
%configure --enable-unicode=yes --enable-c99complex --enable-threads=yes \
  --with-__thread --with-clx --disable-rpath \
%ifarch x86_64
  --with-sse \
%endif
  CPPFLAGS=`pkg-config --cflags libffi`
make
mkdir -p ecl-doc/tmp
make -C ecl-doc
rm ecl-doc/html/ecl2.proc


%install
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
/sbin/ldconfig
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
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null ||:


%files
%{_bindir}/ecl
%{_bindir}/ecl-config
%{_datadir}/applications/ecl.desktop
%{_datadir}/icons/hicolor/scalable/apps/ecl.svg
%{_libdir}/ecl*
%{_libdir}/libecl.so.12.12*
%{_libdir}/libecl.so.12
%{_libdir}/libecl.so
%{_includedir}/ecl
%{_mandir}/man1/*
%doc ANNOUNCEMENT Copyright LGPL examples src/CHANGELOG
%doc ecl-doc/html src/doc/amop.txt src/doc/types-and-classes


%changelog
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
