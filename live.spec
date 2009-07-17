Summary:	LIVE555 libraries for streaming media
Summary(pl.UTF-8):	Biblioteki LIVE555 do strumieni multimedialnych
Name:		live
Version:	2009.06.02
Release:	1
Epoch:		2
License:	LGPL v2.1+
Group:		Development/Libraries
Source0:	http://www.live555.com/liveMedia/public/%{name}.%{version}.tar.gz
# Source0-md5:	088f848b64cef1d54034bc24cfa3c156
Source1:	http://www.live555.com/liveMedia/public/changelog.txt
# Source1-md5:	c79bc6acd34e2593f2e98332652ad95c
URL:		http://www.live555.com/liveMedia/
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

%description
LIVE555 libraries for streaming media.

%description -l pl.UTF-8
Biblioteki LIVE555 do strumieni multimedialnych.

%prep
%setup -q -n live

%build
./genMakefiles linux
sed -i -e 's#$(TESTPROGS_APP)##g' Makefile Makefile.tail
%{__make} \
	C_COMPILER="%{__cc}" \
	CPLUSPLUS_COMPILER="%{__cxx}" \
	COMPILE_OPTS="\$(INCLUDES) -I. %{rpmcflags} -DSOCKLEN_T=socklen_t"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/liveMedia/{liveMedia,groupsock,UsageEnvironment,BasicUsageEnvironment} \
	$RPM_BUILD_ROOT%{_includedir}/liveMedia

install liveMedia/libliveMedia.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/liveMedia
install groupsock/libgroupsock.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/groupsock
install UsageEnvironment/libUsageEnvironment.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/UsageEnvironment
install BasicUsageEnvironment/libBasicUsageEnvironment.a $RPM_BUILD_ROOT%{_libdir}/liveMedia/BasicUsageEnvironment

install liveMedia/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
install UsageEnvironment/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
install BasicUsageEnvironment/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
install groupsock/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia

install %{SOURCE1} ChangeLog.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog.txt
%{_libdir}/liveMedia
%{_includedir}/liveMedia
