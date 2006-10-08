Summary:	LIVE555 libraries for streaming media
Summary(pl):	Biblioteki LIVE555 do strumieni multimedialnych
Name:		live
Version:	2006.10.07
Release:	1
Epoch:		2
License:	LGPL
Group:		Libraries
Source0:	http://www.live555.com/liveMedia/public/%{name}.%{version}.tar.gz
# Source0-md5:	dc4b5b26d63d321727b7bc0cfa7912c0
Source1:	http://www.live555.com/liveMedia/public/changelog.txt
# Source1-md5:	5361fea03f65085261fb624ae6cbaa38
URL:		http://www.live555.com/liveMedia/
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

%description
LIVE555 libraries for streaming media.

%description -l pl
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

install %{SOURCE1} ChangeLog.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog.txt
%{_libdir}/liveMedia
%{_includedir}/liveMedia
