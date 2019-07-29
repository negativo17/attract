Name:       attract
Version:    2.5.1
Release:    1%{?dist}
Summary:    A graphical front-end for command line emulators
License:    GPLv3
URL:        http://attractmode.org 

Source0:    https://github.com/mickelson/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libavresample)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(sfml-audio)
BuildRequires:  pkgconfig(sfml-graphics)
BuildRequires:  pkgconfig(sfml-system)
BuildRequires:  pkgconfig(sfml-window)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xinerama)

#Requires:       

%description
A graphical front-end for command line emulators that hides the underlying
operating system and is intended to be controlled with a joystick or game pad.

%prep
%autosetup -p1
sed -i -e 's|^prefix=.*|prefix=%{_prefix}|g' Makefile

%build
export FE_HWACCEL_VDPAU=1
export FE_HWACCEL_VAAPI=1
export FE_DEBUG=1
export VERBOSE=1
# Disable temporarily as it makes attract crash:
# export EXTRA_CFLAGS="%{optflags}"
%make_build

%install
%make_install

# Menu icon
install -D -p -m 644 util/linux/attract-mode.desktop %{buildroot}%{_datadir}/applications/attract-mode.desktop
sed -i -e 's|%{_datadir}/icons/hicolor/512x512/apps/|%{_datadir}/pixmaps/|g' %{buildroot}%{_datadir}/applications/attract-mode.desktop
install -D -p -m 644 util/linux/attract-mode.png %{buildroot}%{_datadir}/pixmaps/attract-mode.png

# Install AppData
%if 0%{?fedora}
install -D -p -m 0644 util/linux/attract-mode.appdata.xml %{buildroot}%{_metainfodir}/attract-mode.appdata.xml
%endif

# rpmlint issues
find . -name "*.h" -exec chmod 644 {} \;
find . -name "*.cpp" -exec chmod 644 {} \;

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/attract-mode.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/attract-mode.appdata.xml

%files
%license License.txt
%doc Readme.md Layouts.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/attract-mode.desktop
%{_metainfodir}/attract-mode.appdata.xml
%{_datadir}/pixmaps/attract-mode.png

%changelog
* Mon Jul 29 2019 Simone Caronni <negativo17@gmail.com> - 2.5.1-1
- First build.
