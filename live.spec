Summary:	LIVE.COM libraries for streaming media
Name:		live
Version:	20021221
Release:	0.1
Epoch:		1
License:	LGPL
Group:		Libraries
Source0:	http://www.live.com/liveMedia/public/%{name}.2002.12.21.tar.gz
URL:		http://live.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
LIVE.COM libraries for streaming media

%prep
%setup -q -n live

%build
./genMakefiles linux
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
rm -Rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/liveMedia/liveMedia
install -d $RPM_BUILD_ROOT%{_libdir}/liveMedia/groupsock
install -d $RPM_BUILD_ROOT%{_libdir}/liveMedia/UsageEnvironment
install -d $RPM_BUILD_ROOT%{_libdir}/liveMedia/BasicUsageEnvironment
cp liveMedia/libliveMedia.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/liveMedia/
cp groupsock/libgroupsock.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/groupsock/
cp UsageEnvironment/libUsageEnvironment.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/UsageEnvironment/
cp BasicUsageEnvironment/libBasicUsageEnvironment.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/BasicUsageEnvironment/

install -d $RPM_BUILD_ROOT%{_includedir}/liveMedia

cp liveMedia/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
cp UsageEnvironment/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
cp BasicUsageEnvironment/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
cp groupsock/include/* $RPM_BUILD_ROOT/%{_includedir}/liveMedia

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%dir %{_includedir}/liveMedia
%dir %{_libdir}/liveMedia
%attr(755,root,root) %{_libdir}/liveMedia/liveMedia/libliveMedia.a
%attr(755,root,root) %{_libdir}/liveMedia/groupsock/libgroupsock.a
%attr(755,root,root) %{_libdir}/liveMedia/UsageEnvironment/libUsageEnvironment.a
%attr(755,root,root) %{_libdir}/liveMedia/BasicUsageEnvironment/libBasicUsageEnvironment.a
%attr(755,root,root) %{_includedir}/liveMedia/*
