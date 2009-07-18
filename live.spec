Summary:	LIVE555 libraries for streaming media
Summary(pl.UTF-8):	Biblioteki LIVE555 do strumieni multimedialnych
Name:		live
Version:	2009.07.09
Release:	3
Epoch:		2
License:	LGPL v2.1+
Group:		Development/Libraries
Source0:	http://www.live555.com/liveMedia/public/%{name}.%{version}.tar.gz
# Source0-md5:	8085b7f75e55c91f15e96f375c80b9fb
Source1:	http://www.live555.com/liveMedia/public/changelog.txt
# Source1-md5:	9f962afca5e55ae76b84ad8cb365d805
Source2:	%{name}-shared.config
URL:		http://www.live555.com/liveMedia/
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_livedir		%{_libdir}/liveMedia
%define		specflags		-fno-strict-aliasing
# Should be changed on every ABI change
# Alexis Ballier <aballier@gentoo.org>:
%define		LIVE_ABI_VERSION	1

%description
LIVE555 libraries for streaming media.

%description -l pl.UTF-8
Biblioteki LIVE555 do strumieni multimedialnych.

%package libs
Summary:        Shared LIVE555 libraries
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description libs
Shared LIVE555 libraries

%package devel
Summary:        Header files for developing programs using LIVE555
Summary(pl.UTF-8):      Pliki nagłówkowe do biblioteki LIVE555
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for developing programs using LIVE555.

%description devel -l pl.UTF-8
Pliki nagłówkowe do biblioteki LIVE555

%package static
Summary:        Static version LIVE555 library
Summary(pl.UTF-8):      Biblioteka statyczna LIVE555
Group:          Development/Libraries
Requires:       %{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static LIVE555 library.

%description static -l pl.UTF-8
Statyczna biblioteka LIVE555.

%prep 
%setup -q -c -n %{name}
install %{SOURCE2} %{name}/config.linux-shared
cp -pPR %{name} %{name}-shared
mv %{name} %{name}-static

%build
cd %{name}-static
./genMakefiles linux
sed -i -e 's#$(TESTPROGS_APP)##g' Makefile Makefile.tail
%{__make} \
	C_COMPILER="%{__cc}" \
	CPLUSPLUS_COMPILER="%{__cxx}" \
	COMPILE_OPTS="\$(INCLUDES) -I. %{rpmcflags} -DSOCKLEN_T=socklen_t -fPIC"

cd ../%{name}-shared
./genMakefiles linux-shared
sed -i -e 's#$(TESTPROGS_APP)##g' Makefile Makefile.tail
%{__make} \
	C_COMPILER="%{__cc}" \
	CPLUSPLUS_COMPILER="%{__cxx}" \
	LIB_SUFFIX="so.%{LIVE_ABI_VERSION}" \
	COMPILE_OPTS="\$(INCLUDES) -I. %{rpmcflags} -DSOCKLEN_T=socklen_t"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_livedir}/{liveMedia,groupsock,UsageEnvironment,BasicUsageEnvironment} \
	$RPM_BUILD_ROOT%{_includedir}/liveMedia

cd %{name}-static
install liveMedia/libliveMedia.a $RPM_BUILD_ROOT%{_livedir}/liveMedia
install groupsock/libgroupsock.a $RPM_BUILD_ROOT%{_livedir}/groupsock
install UsageEnvironment/libUsageEnvironment.a $RPM_BUILD_ROOT%{_livedir}/UsageEnvironment
install BasicUsageEnvironment/libBasicUsageEnvironment.a $RPM_BUILD_ROOT%{_livedir}/BasicUsageEnvironment

install liveMedia/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
install UsageEnvironment/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
install BasicUsageEnvironment/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
install groupsock/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia

cd ../%{name}-shared
install liveMedia/libliveMedia.so.%{LIVE_ABI_VERSION} $RPM_BUILD_ROOT%{_livedir}/liveMedia
ln -s libliveMedia.so.%{LIVE_ABI_VERSION} $RPM_BUILD_ROOT%{_livedir}/liveMedia/libliveMedia.so
install groupsock/libgroupsock.so.%{LIVE_ABI_VERSION} $RPM_BUILD_ROOT%{_livedir}/groupsock
ln -s libgroupsock.so.%{LIVE_ABI_VERSION} $RPM_BUILD_ROOT%{_livedir}/groupsock/libgroupsock.so
install UsageEnvironment/libUsageEnvironment.so.%{LIVE_ABI_VERSION} $RPM_BUILD_ROOT%{_livedir}/UsageEnvironment
ln -s libUsageEnvironment.so.%{LIVE_ABI_VERSION} $RPM_BUILD_ROOT%{_livedir}/UsageEnvironment/libUsageEnvironment.so
install BasicUsageEnvironment/libBasicUsageEnvironment.so.%{LIVE_ABI_VERSION} $RPM_BUILD_ROOT%{_livedir}/BasicUsageEnvironment
ln -s libBasicUsageEnvironment.so.%{LIVE_ABI_VERSION} $RPM_BUILD_ROOT%{_livedir}/BasicUsageEnvironment/libBasicUsageEnvironment.so

cd ..
install %{SOURCE1} ChangeLog.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post libs   -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%dir %{_livedir}
%dir %{_livedir}/BasicUsageEnvironment
%dir %{_livedir}/UsageEnvironment
%dir %{_livedir}/groupsock
%dir %{_livedir}/liveMedia

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_livedir}/BasicUsageEnvironment/libBasicUsageEnvironment.so.*
%attr(755,root,root) %{_livedir}/UsageEnvironment/libUsageEnvironment.so.*
%attr(755,root,root) %{_livedir}/groupsock/libgroupsock.so.*
%attr(755,root,root) %{_livedir}/liveMedia/libliveMedia.so.*
# Temporary:
%attr(755,root,root) %{_livedir}/BasicUsageEnvironment/libBasicUsageEnvironment.so
%attr(755,root,root) %{_livedir}/UsageEnvironment/libUsageEnvironment.so
%attr(755,root,root) %{_livedir}/groupsock/libgroupsock.so
%attr(755,root,root) %{_livedir}/liveMedia/libliveMedia.so

%files devel
%defattr(644,root,root,755)
%doc ChangeLog.txt
%{_includedir}/liveMedia

%files static
%defattr(644,root,root,755)
%{_livedir}/BasicUsageEnvironment/libBasicUsageEnvironment.a
%{_livedir}/UsageEnvironment/libUsageEnvironment.a
%{_livedir}/groupsock/libgroupsock.a
%{_livedir}/liveMedia/libliveMedia.a
