Summary:	LIVE555 for streaming media
Summary(pl.UTF-8):	LIVE555 do strumieni multimedialnych
Name:		live
Version:	2009.07.09
Release:	3.2
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
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_livedir		%{_libdir}/liveMedia
%define		specflags		-fno-strict-aliasing
# Should be changed on every ABI change
# Alexis Ballier <aballier@gentoo.org>:
%define		LIVE_ABI_VERSION	1

%description
LIVE555 for streaming media.

%description -l pl.UTF-8
LIVE555 do strumieni multimedialnych.

%package libs
Summary:        Shared LIVE555 libraries for streaming media
Group:          Development/Libraries

%description libs
Shared LIVE555 libraries for streaming media.

%package devel
Summary:        Header files for developing programs using LIVE555
Summary(pl.UTF-8):      Pliki nagłówkowe do biblioteki LIVE555
Group:          Development/Libraries
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}

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
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/liveMedia,%{_bindir}}

cd %{name}-static
for i in liveMedia groupsock UsageEnvironment BasicUsageEnvironment; do
	install $i/lib$i.a $RPM_BUILD_ROOT%{_libdir}
done

cd ../%{name}-shared

for i in liveMedia groupsock UsageEnvironment BasicUsageEnvironment; do
	install $i/lib$i.so.%{LIVE_ABI_VERSION} $RPM_BUILD_ROOT%{_libdir}
	ln -s lib$i.so.%{LIVE_ABI_VERSION} $RPM_BUILD_ROOT%{_libdir}/lib$i.so
	install $i/include/* $RPM_BUILD_ROOT%{_includedir}/liveMedia
done

# We provide shared version:
install mediaServer/live555MediaServer $RPM_BUILD_ROOT%{_bindir}

cd ..
install %{SOURCE1} ChangeLog.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post libs   -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/live555MediaServer

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libBasicUsageEnvironment.so*
%attr(755,root,root) %{_libdir}/libUsageEnvironment.so*
%attr(755,root,root) %{_libdir}/libgroupsock.so*
%attr(755,root,root) %{_libdir}/libliveMedia.so*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog.txt
%{_includedir}/liveMedia

%files static
%defattr(644,root,root,755)
%{_libdir}/libBasicUsageEnvironment.a
%{_libdir}/libUsageEnvironment.a
%{_libdir}/libgroupsock.a
%{_libdir}/libliveMedia.a
