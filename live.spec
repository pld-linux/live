Summary:	LIVE.COM libraries for streaming media
Summary(pl):	Biblioteki LIVE.COM do strumieni multimedialnych
Name:		live
Version:	2003.03.14
Release:	0.1
Epoch:		2
License:	LGPL
Group:		Libraries
Source0:	http://www.live.com/liveMedia/public/%{name}.%{version}.tar.gz
# Source0-md5: a7f3ce90addbe7d868ce8d6ff97d1aa4
URL:		http://live.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LIVE.COM libraries for streaming media.

%description -l pl
Biblioteki LIVE.COM do strumieni multimedialnych.

%prep
%setup -q -n live

%build
./genMakefiles linux
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/liveMedia/liveMedia
install -d $RPM_BUILD_ROOT%{_libdir}/liveMedia/groupsock
install -d $RPM_BUILD_ROOT%{_libdir}/liveMedia/UsageEnvironment
install -d $RPM_BUILD_ROOT%{_libdir}/liveMedia/BasicUsageEnvironment

install liveMedia/libliveMedia.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/liveMedia
install groupsock/libgroupsock.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/groupsock
install UsageEnvironment/libUsageEnvironment.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/UsageEnvironment
install BasicUsageEnvironment/libBasicUsageEnvironment.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/BasicUsageEnvironment

install -d $RPM_BUILD_ROOT%{_includedir}/liveMedia

install liveMedia/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
install UsageEnvironment/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
install BasicUsageEnvironment/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
install groupsock/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/liveMedia
%{_includedir}/liveMedia
