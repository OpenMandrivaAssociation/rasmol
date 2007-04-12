#
# spec file for rasmol
#

# Basic macros
%define name     rasmol
%define version  2.7.2.1.1
%define release  %mkrel 6
%define abstract Molecular Graphics Visualization Tool

Name:         %name
Summary:      %abstract
Version:      %version
Release:      %release
License:      Distributable
Group:        Sciences/Chemistry
URL:          http://www.bernstein-plus-sons.com/software/rasmol/
Autoreqprov:  off
BuildRoot:    %{_tmppath}/%{name}-buildroot
Provides:     RasMol

BuildRequires: X11-devel
BuildRequires: imake
BuildRequires: gccmakedep

Source:       http://www.bernstein-plus-sons.com/software/rasmol/RasMol-%{version}.tar.bz2

%description
RasMol is an X Window System tool intended for the visualization of
proteins and nucleic acids. It reads Brookhaven Protein Database (PDB)
files and interactively renders them in a variety of formats on either
an 8-bit or 24/32-bit color display.

Authors:
--------
    Roger Sayle <ras32425@ggr.co.uk>

%prep

%setup -n RasMol-%{version}

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
ln -sf %_bindir/%name  %buildroot/%_bindir/%name
mkdir -p %buildroot%{_mandir}/man1/
mv %buildroot/usr/man/man1/* %buildroot%{_mandir}/man1/
# Menu icons
install -D -m 644 Icons/%{name}48.png %buildroot/%_liconsdir/%name.png
install -D -m 644 Icons/%{name}32.png %buildroot/%_iconsdir/%name.png
install -D -m 644 Icons/%{name}16.png %buildroot/%_miconsdir/%name.png

# Menu entries
mkdir -p %buildroot/%_menudir
cat > %buildroot/%_menudir/%name << EOF
?package(%name): command="/usr/X11R6/bin/rasmol" \
needs="text" icon="%name.png" section="More applications/Sciences/Chemistry" \
title="RasMol" longtitle="%abstract" \
xdg="true"
EOF

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
%doc NOTICE PROJECTS TODO* README* ChangeLog.html history.html index.shtml html_graphics
%doc doc/*.gz doc/*.html doc/*.hlp
%doc %{_mandir}/man1/*
%{_libdir}/rasmol
%_bindir/*
%_liconsdir/*.png
%_miconsdir/*.png
%_iconsdir/*.png
%_menudir/*
%{_datadir}/applications/mandriva-%{name}.desktop

%clean
rm -rf %buildroot

%post
%update_menus

%postun
%clean_menus



