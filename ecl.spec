Name:           ecl
Version:        0.9h
Release:        5%{?dist}
Summary:        Embeddable Common-Lisp

Group:          Development/Languages
License:        LGPL
URL:            http://ecls.sourceforge.net
Source0:	http://switch.dl.sourceforge.net/sourceforge/ecls/ecl-0.9h.tgz
Patch0:		ecl-gcc41.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libX11-devel
BuildRequires:	m4
BuildRequires:	texinfo
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info

%description
ECL (Embeddable Common-Lisp) is an interpreter of the Common-Lisp
language as described in the X3J13 Ansi specification, featuring CLOS
(Common-Lisp Object System), conditions, loops, etc, plus a translator
to C, which can produce standalone executables.

# no -devel package for header files is split off
# since they are required by the main package

%prep
%setup0 -q
%patch0 -p1
# wrong character in texinfo file
perl -pi -e 's|\xc7||' src/doc/user.txi


%build
%configure --enable-boehm=included --enable-threads=yes --with-cxx
make -k
(cd build/doc; make all html)


%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}/ecl \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	docdir=$RPM_BUILD_ROOT%{_docdir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	install
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -fr $RPM_BUILD_ROOT%{_docdir}

find $RPM_BUILD_ROOT%{_libdir}/ecl -name '*.lsp' | xargs chmod 0644


%post
/sbin/install-info %{_infodir}/ecldev.info %{_infodir}/dir 2>/dev/null || :
/sbin/install-info %{_infodir}/ecl.info %{_infodir}/dir 2>/dev/null || :

 
%postun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/ecldev.info %{_infodir}/dir 2>/dev/null || :
  /sbin/install-info --delete %{_infodir}/ecl.info %{_infodir}/dir 2>/dev/null || :
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/ecl
%{_bindir}/ecl-config
%{_libdir}/ecl
%{_mandir}/man*/*
%{_infodir}/*
%doc ANNOUNCEMENT Copyright LGPL README.1st build/doc/*.html build/doc/ecl build/doc/ecldev


%changelog
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
