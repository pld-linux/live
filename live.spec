Summary:	LIVE555 libraries for streaming media
Summary(pl.UTF-8):	Biblioteki LIVE555 do strumieni multimedialnych
Name:		live
Version:	2009.07.09
Release:	2.6
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

%define		specflags	-fno-strict-aliasing

%description
LIVE555 libraries for streaming media.

%description -l pl.UTF-8
Biblioteki LIVE555 do strumieni multimedialnych.

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
Requires:       %{name} = %{epoch}:%{version}-%{release}

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
	COMPILE_OPTS="\$(INCLUDES) -I. %{rpmcflags} -DSOCKLEN_T=socklen_t"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/liveMedia/{liveMedia,groupsock,UsageEnvironment,BasicUsageEnvironment} \
	$RPM_BUILD_ROOT%{_includedir}/liveMedia

cd %{name}-static
install liveMedia/libliveMedia.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/liveMedia
install groupsock/libgroupsock.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/groupsock
install UsageEnvironment/libUsageEnvironment.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/UsageEnvironment
install BasicUsageEnvironment/libBasicUsageEnvironment.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/BasicUsageEnvironment

install liveMedia/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
install UsageEnvironment/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
install BasicUsageEnvironment/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
install groupsock/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia

cd ../%{name}-shared
install liveMedia/libliveMedia.so $RPM_BUILD_ROOT%{_libdir}/liveMedia/liveMedia
install groupsock/libgroupsock.so $RPM_BUILD_ROOT%{_libdir}/liveMedia/groupsock
install UsageEnvironment/libUsageEnvironment.so $RPM_BUILD_ROOT%{_libdir}/liveMedia/UsageEnvironment
install BasicUsageEnvironment/libBasicUsageEnvironment.so $RPM_BUILD_ROOT%{_libdir}/liveMedia/BasicUsageEnvironment

cd ..
install %{SOURCE1} ChangeLog.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%dir %{_libdir}/liveMedia
%dir %{_libdir}/liveMedia/UsageEnvironment
%attr(755,root,root) %{_libdir}/liveMedia/UsageEnvironment/libUsageEnvironment.so
%dir %{_libdir}/liveMedia/BasicUsageEnvironment
%attr(755,root,root) %{_libdir}/liveMedia/BasicUsageEnvironment/libBasicUsageEnvironment.so
%dir %{_libdir}/liveMedia/liveMedia
%attr(755,root,root) %{_libdir}/liveMedia/liveMedia/libliveMedia.so
%dir %{_libdir}/liveMedia/groupsock
%attr(755,root,root) %{_libdir}/liveMedia/groupsock/libgroupsock.so

%files devel
%defattr(644,root,root,755)
%doc ChangeLog.txt
%{_includedir}/liveMedia

%files static
%defattr(644,root,root,755)
%{_libdir}/liveMedia/BasicUsageEnvironment/libBasicUsageEnvironment.a
%{_libdir}/liveMedia/UsageEnvironment/libUsageEnvironment.a
%{_libdir}/liveMedia/groupsock/libgroupsock.a
%{_libdir}/liveMedia/liveMedia/libliveMedia.a
