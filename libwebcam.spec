Summary:	The Webcam Library
Summary(pl.UTF-8):	Biblioteka Webcam
Name:		libwebcam
Version:	0.2.5
Release:	1
License:	LGPL v3+ (libwebcam), GPL v3+ (uvcdynctrl)
Group:		Libraries
Source0:	https://downloads.sourceforge.net/libwebcam/%{name}-src-%{version}.tar.gz
# Source0-md5:	454123bbcc2497fb74a7542b48dd96b4
Patch1:		%{name}-pkgconfig.patch
URL:		https://sourceforge.net/projects/libwebcam/
BuildRequires:	cmake >= 2.6.0
# for vcs checkouts (uvcdynctrl/cmdline.* generation)
#BuildRequires:	gengetopt
# <linux/uvcvideo.h> uapi header
BuildRequires:	linux-libc-headers >= 7:3.7
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Webcam Library libwebcam is designed to simplify
the development of webcam applications, primarily on Linux but
with an option to be ported to other platforms, in particular
Solaris. It realizes part of what the unwritten Video4Linux user
space library was always supposed to be: an easy to use library
that shields its users from many of the difficulties and problems
of using the V4L2 API directly.

%description -l pl.UTF-8
Biblioteka Webcam została zaprojektowana w celu uproszczenia
tworzenia aplikacji wykorzystujących kamery internetowe, głównie pod
Linuksem, ale z możliwością portowania na inne platformy, w
szczególności Solaris. Spełnia część zadań, które powinna realizować
nienapisana biblioteka przestrzeni użytkownika Video4Linux: łatwej w
użyciu biblioteki oddzielającej wiele trudności i problemów przy
korzystaniu bezpośrednio z interfejsu API V4L2.

%package devel
Summary:	Header files for the Webcam library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Webcam
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for the Webcam library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Webcam.

%package static
Summary:	Static Webcam library
Summary(pl.UTF-8):	Statyczna biblioteka Webcam
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Webcam library.

%description static -l pl.UTF-8
Statyczna biblioteka Webcam.

%package -n uvcdynctrl
Summary:	Command line tool to control V4L2 devices
Summary(pl.UTF-8):	Narzędzie linii poleceń do sterowania urządzeniami V4L2
License:	GPL v3+
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description -n uvcdynctrl
This package provides the tools needed to add vendor specific controls
to UVC devices.

%description -n uvcdynctrl -l pl.UTF-8
Ten pakiet dostarcza narzędzie potrzebne do dodania do urządzeń UVC
sterowania urządzeń zależnego od producenta.

%prep
%setup -q
%patch -P1 -p1

# junk in dist tarball
%{__rm} common/build/cmake_try_v4l2_ctrl_type_string.c~
%{__rm} uvcdynctrl/data/046d/logitech.xml~

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md libwebcam/README
%attr(755,root,root) %{_libdir}/libwebcam.so.*.*.*
%ghost %{_libdir}/libwebcam.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libwebcam.so
%{_includedir}/dynctrl-logitech.h
%{_includedir}/webcam.h
%{_pkgconfigdir}/libwebcam.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libwebcam.a

%files -n uvcdynctrl
%defattr(644,root,root,755)
%doc uvcdynctrl/README
%attr(755,root,root) %{_bindir}/uvcdynctrl*
%attr(755,root,root) /lib/udev/uvcdynctrl
/lib/udev/rules.d/80-uvcdynctrl.rules
%{_datadir}/uvcdynctrl
%{_mandir}/man1/uvcdynctrl*.1*
