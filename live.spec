# TODO:
# - mediaServer should have init-scripts, user, etc, etc...
Summary:	LIVE555 streaming media server
Summary(pl.UTF-8):	LIVE555 - serwer strumieni multimedialnych
Name:		live
Version:	2013.10.25
Release:	1
Epoch:		2
License:	LGPL v2.1+
Group:		Applications/Multimedia
Source0:	http://www.live555.com/liveMedia/public/%{name}.%{version}.tar.gz
# Source0-md5:	43a8d3a622db8a4582174fa2ddc7461b
Source1:	http://www.live555.com/liveMedia/public/changelog.txt
# Source1-md5:	a6558728ef766075a53d6e94ab7bcc31
Source2:	%{name}-shared.config
Patch0:		%{name}-link.patch
URL:		http://www.live555.com/liveMedia/
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_livedir		%{_libdir}/liveMedia
%define		specflags		-fno-strict-aliasing
# Should be changed on every ABI change
# Alexis Ballier <aballier@gentoo.org>:
%define		LIVE_ABI_VERSION	1
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
%setup -q -c -n %{name}
%patch0 -p0
install %{SOURCE2} %{name}/config.linux-shared
cp -pPR %{name} %{name}-shared
mv %{name} %{name}-static
cp -af %{SOURCE1} ChangeLog.txt

%build
cd %{name}-static
./genMakefiles linux
sed -i -e 's#$(TESTPROGS_APP)##g' Makefile Makefile.tail
%{__make} \
	C_COMPILER="%{__cc}" \
	CPLUSPLUS_COMPILER="%{__cxx}" \
	COMPILE_OPTS="\$(INCLUDES) -I. %{rpmcppflags} %{rpmcflags} -DSOCKLEN_T=socklen_t -DRTSPCLIENT_SYNCHRONOUS_INTERFACE=1 -fPIC"

cd ../%{name}-shared
./genMakefiles linux-shared
sed -i -e 's#$(TESTPROGS_APP)##g' Makefile Makefile.tail
%{__make} \
	C_COMPILER="%{__cc}" \
	CPLUSPLUS_COMPILER="%{__cxx}" \
	LIB_SUFFIX="so.%{LIVE_ABI_VERSION}" \
	COMPILE_OPTS="\$(INCLUDES) -I. %{rpmcppflags} %{rpmcflags} -DSOCKLEN_T=socklen_t -DRTSPCLIENT_SYNCHRONOUS_INTERFACE=1"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/liveMedia,%{_bindir}}

for i in liveMedia groupsock UsageEnvironment BasicUsageEnvironment; do
	install -p %{name}-static/$i/lib$i.a $RPM_BUILD_ROOT%{_libdir}
	install -p %{name}-shared/$i/lib$i.so.%{LIVE_ABI_VERSION} $RPM_BUILD_ROOT%{_libdir}
	ln -s lib$i.so.%{LIVE_ABI_VERSION} $RPM_BUILD_ROOT%{_libdir}/lib$i.so
	install -p %{name}-shared/$i/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
done

# We provide shared version:
install -p %{name}-shared/mediaServer/live555MediaServer $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/live555MediaServer

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libBasicUsageEnvironment.so.*
%attr(755,root,root) %{_libdir}/libUsageEnvironment.so.*
%attr(755,root,root) %{_libdir}/libgroupsock.so.*
%attr(755,root,root) %{_libdir}/libliveMedia.so.*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog.txt
%attr(755,root,root) %{_libdir}/libBasicUsageEnvironment.so
%attr(755,root,root) %{_libdir}/libUsageEnvironment.so
%attr(755,root,root) %{_libdir}/libgroupsock.so
%attr(755,root,root) %{_libdir}/libliveMedia.so
%{_includedir}/liveMedia

%files static
%defattr(644,root,root,755)
%{_libdir}/libBasicUsageEnvironment.a
%{_libdir}/libUsageEnvironment.a
%{_libdir}/libgroupsock.a
%{_libdir}/libliveMedia.a
