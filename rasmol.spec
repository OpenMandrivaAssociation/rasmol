#
# spec file for rasmol
#

# Basic macros
%define name     rasmol
%define version  2.7.3
%define release  %mkrel 1
%define abstract Molecular Graphics Visualization Tool

Name:         %name
Summary:      %abstract
Version:      %version
Release:      %release
License:      GPL
Group:        Sciences/Chemistry
URL:          http://www.bernstein-plus-sons.com/software/rasmol/
Autoreqprov:  off
BuildRoot:    %{_tmppath}/%{name}-buildroot
Provides:     RasMol

BuildRequires: X11-devel
BuildRequires: imake
BuildRequires: gccmakedep

Source0:      http://www.bernstein-plus-sons.com/software/rasmol/RasMol_%{version}.tar.bz2
Source1:      rasmol16.png
Source2:      rasmol32.png
Source3:      rasmol48.png

%description
RasMol is an X Window System tool intended for the visualization of
proteins and nucleic acids. It reads Brookhaven Protein Database (PDB)
files and interactively renders them in a variety of formats on either
an 8-bit or 24/32-bit color display.

Authors:
--------
    Roger Sayle <ras32425@ggr.co.uk>

%prep

%setup -n RasMol_%{version}
rm -rf doc/RCS
find ./ -name ".DS_Store" -exec rm -f {} \;
chmod 644 NOTICE PROJECTS *.html *.shtml *.txt html_graphics/* data/* doc/*
# This script is mac-specific, we don't need it
rm -f data/RSML_fixup.csh

%build
cd src
xmkmf -a
%make

%install
rm -rf %buildroot
mkdir -p %buildroot/%_bindir
make -C src "DESTDIR=$RPM_BUILD_ROOT" install
make -C src "DESTDIR=$RPM_BUILD_ROOT" install.man
cp -a data %buildroot/usr/%{_lib}/rasmol
cp src/%name  %buildroot/%_bindir/%name
mkdir -p %buildroot%{_mandir}/man1/
#mv %buildroot/usr/share/man/man1/* %buildroot%{_mandir}/man1/
# Menu icons
install -D -m 644 %{SOURCE1} %buildroot/%_miconsdir/%name.png
install -D -m 644 %{SOURCE2} %buildroot/%_iconsdir/%name.png
install -D -m 644 %{SOURCE3} %buildroot/%_liconsdir/%name.png

# Menu entries

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=RasMol
Comment=Molecular Graphics Visualization Tool
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-MoreApplications-Sciences-Chemistry;Science;Chemistry;
EOF

%files
%defattr(-,root,root)
%doc NOTICE PROJECTS TODO* README* RASLIC ChangeLog.* history.html index.shtml html_graphics
%doc doc/*.gz doc/*.html doc/*.hlp
%doc %{_mandir}/man1/*
%{_libdir}/rasmol
%_bindir/*
%_liconsdir/*.png
%_miconsdir/*.png
%_iconsdir/*.png
%{_datadir}/applications/mandriva-%{name}.desktop

%clean
rm -rf %buildroot

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif



