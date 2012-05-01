%global __strip %{_mingw32_strip}
%global __objdump %{_mingw32_objdump}


%global specversion 5
%global upstream_version 0b41287

# Keep around for when/if required
#global alphatag #{upstream_version}.git

%global mh_release %{?alphatag:0.}%{specversion}%{?alphatag:.%{alphatag}}%{?dist}

Name:		mingw32-matahari
Version:	0.4.0
Release:	%{mh_release}
Summary:	Matahari QMF Agents for Windows guests

Group:		Applications/System
License:	GPLv2
URL:		https://github.com/matahari/matahari/wiki

# wget --no-check-certificate -O matahari-{upstream_version}.tgz https://github.com/beekhof/matahari/tarball/{upstream_version}
Source0:	matahari-%{upstream_version}.tgz
Patch1:		matahari-2798d52.patch
Patch2:		matahari-0.4.1.patch
Patch3:		matahari-no-qpidd.patch
Patch4:		matahari-lsb.patch
Patch5:		matahari-qmf-lib.patch
Patch6:		matahari-windows.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

BuildRequires:	redhat-rpm-config cmake make qmf-devel
BuildRequires:	mingw32-filesystem >= 57
BuildRequires:	mingw32-gcc-c++ mingw32-nsis genisoimage
BuildRequires:	mingw32-pcre mingw32-qpid-cpp mingw32-srvany mingw32-glib2 mingw32-sigar

%description

Matahari provides a QMF Agent that can be used to control and manage
various pieces of functionality for an ovirt node, using the AMQP protocol.

The Advanced Message Queuing Protocol (AMQP) is an open standard application
layer protocol providing reliable transport of messages.

QMF provides a modeling framework layer on top of qpid (which implements
AMQP).  This interface allows you to manage a host and its various components
as a set of objects with properties and methods.

MinGW cross-compiled Windows application.

%prep
%setup -q -n beekhof-matahari-%{upstream_version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
PATH=%{_mingw32_bindir}:$PATH

ls -al /usr/i686-pc-mingw32/sys-root/mingw/lib/pkgconfig
%{_mingw32_cmake} --debug-output -DCMAKE_BUILD_TYPE=Release -DCMAKE_VERBOSE_MAKEFILE=on
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make VERBOSE=1 %{?_smp_mflags} package
genisoimage -o matahari-%{version}-win32.iso matahari-%{version}-win32.exe src/windows/autorun.inf

%{__install} -d $RPM_BUILD_ROOT/%{_mingw32_datadir}/matahari
%{__install} matahari-%{version}-win32.iso $RPM_BUILD_ROOT/%{_mingw32_datadir}/matahari

%clean
test "x%{buildroot}" != "x" && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_mingw32_datadir}/matahari

%doc AUTHORS COPYING

%changelog
* Wed Apr 20 2011 Andrew Beekhof <abeekhof@redhat.com> - 0.4.0-5
- Bump the version to sync with Linux package
- Related: rhbz#698370

* Wed Apr 20 2011 Andrew Beekhof <abeekhof@redhat.com> - 0.4.0-4
- Bump the version to sync with Linux package
- Related: rhbz#698370

* Fri Apr 15 2011 Andrew Beekhof <abeekhof@redhat.com> - 0.4.0-3
- Bump the version to sync with Linux package
- Related: rhbz#696810

* Fri Apr  1 2011 Andrew Beekhof <abeekhof@redhat,com> - 0.4.0-1
- Convert agents to the QMFv2 API
- Removed empty debug package
  Related: rhbz#658840

* Wed Mar 30 2011 Lon Hohberger <lhh@redhat.com> 0.4.0-0.3.0b41287.git
- Rebuilt against latest version of QPid and QMF libraries
  Related: rhbz#658840

* Fri Feb  4 2011 Andrew Beekhof <andrew@beekhof.net> - 0.4.0-0.2.0b41287.git
- Update to upstream version 2798d52.git
  + Support password authentication to qpid
  + Prevent errors when matahari is started at boot
  Related: rhbz#658840

* Thu Jan 13 2011 Andrew Beekhof <andrew@beekhof.net> - 0.4.0-0.1.0b41287.git
- Initial import

