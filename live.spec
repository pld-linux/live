# TODO:
# - mediaServer should have init-scripts, user, etc, etc...
# - package test apps (?)
#
# Conditional build:
%bcond_without	static_libs	# static libraries

Summary:	LIVE555 streaming media server
Summary(pl.UTF-8):	LIVE555 - serwer strumieni multimedialnych
Name:		live
Version:	2019.11.05
Release:	1
Epoch:		2
License:	LGPL v2.1+
Group:		Applications/Multimedia
Source0:	http://www.live555.com/liveMedia/public/%{name}.%{version}.tar.gz
# Source0-md5:	130f62ce9de7316cb60092d079989103
Source1:	http://www.live555.com/liveMedia/public/changelog.txt
# Source1-md5:	d4e99b1676759f9620cc32776e8fa9d0
Patch0:		%{name}-link.patch
# from debian
Patch1:		%{name}-pkgconfig.patch
URL:		http://www.live555.com/liveMedia/
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags		-fno-strict-aliasing
# circular symbol dependencies with libBasicUsageEnvironment
%define		skip_post_check_so	.*%{_libdir}/libUsageEnvironment\.so.*

%description
LIVE555 streaming media server.

%description -l pl.UTF-8
LIVE555 - serwer strumieni multimedialnych.

%package libs
Summary:	Shared LIVE555 libraries for streaming media
Summary(pl.UTF-8):	Biblioteki współdzielone LIVE555 do strumieni multimedialnych
Group:		Libraries

%description libs
Shared LIVE555 libraries for streaming media.

%description libs -l pl.UTF-8
Biblioteki współdzielone LIVE555 do strumieni multimedialnych.

%package devel
Summary:	Header files for developing programs using LIVE555
Summary(pl.UTF-8):	Pliki nagłówkowe do biblioteki LIVE555
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel
Obsoletes:	live < 2:2009.07.09-2.5

%description devel
Header files for developing programs using LIVE555.

%description devel -l pl.UTF-8
Pliki nagłówkowe do biblioteki LIVE555

%package static
Summary:	Static LIVE555 libraries for streaming media
Summary(pl.UTF-8):	Biblioteki statyczne LIVE555 do strumieni multimedialnych
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static LIVE555 libraries for streaming media.

%description static -l pl.UTF-8
Biblioteki statyczne LIVE555 do strumieni multimedialnych.

%prep
%setup -q -c
%patch0 -p0
cd live
%patch1 -p1
cd ..

# disable building test programs
%{__sed} -i -e '/cd \$(TESTPROGS_DIR)/d' live/Makefile.tail

# out-of-source builds not supported, so clone sources for shared and static build
%if %{with static_libs}
cp -pPR live live-static
%endif
%{__mv} live live-shared

cp -af %{SOURCE1} ChangeLog.txt

%build
%if %{with static_libs}
cd live-static
./genMakefiles linux
%{__make} \
	C_COMPILER="%{__cc}" \
	CPLUSPLUS_COMPILER="%{__cxx}" \
	CPPFLAGS="%{rpmcppflags}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcxxflags} -fPIC"
cd ..
%endif

cd live-shared
./genMakefiles linux-with-shared-libraries
%{__make} \
	C_COMPILER="%{__cc}" \
	CPLUSPLUS_COMPILER="%{__cxx}" \
	CPPFLAGS="%{rpmcppflags}" \
	CFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcxxflags}" \
	LIBRARY_LINK="%{__cxx} -o"

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
# static first so that binaries will be overwritten by shared version
%{__make} -C live-static install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT
%endif
	
%{__make} -C live-shared install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT
	
%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/live555MediaServer
%attr(755,root,root) %{_bindir}/live555ProxyServer

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libBasicUsageEnvironment.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libBasicUsageEnvironment.so.1
%attr(755,root,root) %{_libdir}/libUsageEnvironment.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libUsageEnvironment.so.3
%attr(755,root,root) %{_libdir}/libgroupsock.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgroupsock.so.8
%attr(755,root,root) %{_libdir}/libliveMedia.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libliveMedia.so.73

%files devel
%defattr(644,root,root,755)
%doc ChangeLog.txt
%attr(755,root,root) %{_libdir}/libBasicUsageEnvironment.so
%attr(755,root,root) %{_libdir}/libUsageEnvironment.so
%attr(755,root,root) %{_libdir}/libgroupsock.so
%attr(755,root,root) %{_libdir}/libliveMedia.so
%{_includedir}/BasicUsageEnvironment
%{_includedir}/UsageEnvironment
%{_includedir}/groupsock
%{_includedir}/liveMedia
%{_pkgconfigdir}/live555.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libBasicUsageEnvironment.a
%{_libdir}/libUsageEnvironment.a
%{_libdir}/libgroupsock.a
%{_libdir}/libliveMedia.a
%endif
