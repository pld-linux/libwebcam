Summary:	The Webcam Library
#Summary(pl.UTF-8):	-
Name:		libwebcam
Version:	0.2.1
Release:	1
License:	LGPL
Group:		Libraries
# svn co http://svn.quickcamteam.net/svn/qct/webcam-tools/trunk/
Source0:	%{name}-%{version}.tar.xz
# Source0-md5:	2046d9a568d0a2b989f9d218ff04ad78
Patch0:		%{name}-uvcvideo_h.patch
Patch1:		%{name}-pkgconfig.patch
URL:		http://www.quickcamteam.net/software/libwebcam/
BuildRequires:	cmake >= 2.6.0
BuildRequires:	libxml2-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Webcam Library libwebcam is designed to simplify
the development of webcam applications, primarily on Linux but
with an option to be ported to other platforms, in particular
Solaris. It realizes part of what the unwritten Video4Linux user
space library was always supposed to be: an easy to use library
that shields its users from many of the difficulties and problems
of using the V4L2 API directly.

#%description -l pl.UTF-8

%package devel
Summary:	Header files for the Webcam Library
#Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FOO
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for the Webcam Library library.

#%description devel -l pl.UTF-8
#Pliki nagłówkowe biblioteki FOO.

%package -n uvcdynctrl
Summary:	Command line tool to control v4l2 devices
#Summary(pl.UTF-8):	Dokumentacja API biblioteki FOO
License:	GPL
Group:		Applications/Multimedia

%description -n uvcdynctrl
This package provides the tools needed to add vendor specific
controls to uvc devices.

#%description -n uvcdynctrl -l pl.UTF-8
#Dokumentacja API biblioteki FOO.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake \
	-DCMAKE_INCLUDE_PATH=../common/include \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/libwebcam

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a common/include/*.h $RPM_BUILD_ROOT%{_includedir}/libwebcam

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc libwebcam/README
%attr(755,root,root) %{_libdir}/libwebcam.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libwebcam.so
%{_includedir}/libwebcam
%{_pkgconfigdir}/libwebcam.pc

%files -n uvcdynctrl
%defattr(644,root,root,755)
%doc uvcdynctrl/README
%attr(755,root,root) %{_bindir}/*
#%{_sysconfdir}/udev/data/046d/logitech.xml
%{_sysconfdir}/udev/data
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/80-uvcdynctrl.rules
%attr(755,root,root) /lib/udev/uvcdynctrl
