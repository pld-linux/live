Summary:	LIVE.COM libraries for streaming media
Summary(pl):	Biblioteki LIVE.COM do strumieni multimedialnych
Name:		live
Version:	2003.12.26
Release:	0.1
Epoch:		2
License:	LGPL
Group:		Libraries
Source0:	http://www.live.com/liveMedia/public/%{name}.%{version}.tar.gz
# Source0-md5:	2761f83e75994543d359e21124253b4a
URL:		http://live.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LIVE.COM libraries for streaming media.

%description -l pl
Biblioteki LIVE.COM do strumieni multimedialnych.

%prep
%setup -q -n live

# no <strstream.h> in gcc 3.3 - but... this API is not used anyway
echo > groupsock/strstream.h

%build
./genMakefiles linux
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/liveMedia
%{_includedir}/liveMedia
