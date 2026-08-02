# Disable debug packages
%define debug_package %{nil}

Name:           wolf-os-virtualization
Version:        1.0.0
Release:        2%{?dist}
Summary:        User-Enabled Virtualization Stack for Wolf-OS
License:        GPLv3
URL:            https://github.com/jonathonp3/wolf-os-virtualization
BuildArch:      noarch

# --- SOURCES ---
Source0:        wolf-os-virtualization.sysusers
Source1:        wolf-os-virtualization.tmpfiles
Source2:        wolf-os-virtualization-libvirt.xml

# --- DEPENDENCIES ---
Requires:       libvirt-daemon-config-network
Requires:       libvirt-daemon-kvm
Requires:       qemu-kvm
Requires:       virt-install
Requires:       virt-manager
Requires:       virt-viewer
Requires:       firewalld

%description
Provides the full libvirt/virtnetworkd runtime foundation for Wolf-OS. Includes a custom firewalld zone (wolf-libvirt) 
User intervention is required where services are enabled in the new deployment.

%setup -c -T

%build
# No build needed

%install
# Create vendor-layer directories (/usr/lib) instead of /etc
mkdir -p %{buildroot}/usr/lib/sysusers.d
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
mkdir -p %{buildroot}/usr/lib/firewalld/zones
mkdir -p %{buildroot}/usr/lib/wolf-os

# Install files to the vendor layer
install -p -m 644 %{_sourcedir}/wolf-os-virtualization.sysusers %{buildroot}/usr/lib/sysusers.d/wolf-os-virtualization.conf
install -p -m 644 %{_sourcedir}/wolf-os-virtualization.tmpfiles %{buildroot}/usr/lib/tmpfiles.d/wolf-os-virtualization.conf
install -p -m 644 %{_sourcedir}/wolf-os-virtualization-libvirt.xml %{buildroot}/usr/lib/firewalld/zones/wolf-libvirt.xml
install -p -m 644 %{_sourcedir}/wolf-os-default-net.xml %{buildroot}/usr/lib/wolf-os/default-net.xml

%files
/usr/lib/sysusers.d/wolf-os-virtualization.conf
/usr/lib/tmpfiles.d/wolf-os-virtualization.conf
/usr/lib/firewalld/zones/wolf-libvirt.xml
/usr/lib/wolf-os/default-net.xml

%changelog
* Sun Aug 02 2026 Jonathon <jonathon@sirius-os> - 1.1.0-2
- Implement declarative firewalld zone (wolf-libvirt) in the vendor layer
- Shift default virtual network to 192.168.100.0/24 to prevent nested VM conflicts
- Add tmpfiles.d logic for zero-touch network autostart on first boot
- Verified successful bridge initialization on Atomic deployments

* Sun Aug 2 2026 Jonathon <jonathon@sirius-os> - 1.0.0-1
- First Stable Release for wolf-os-virtualization
- Verified compatibility with modular libvirt architecture
- Custom wolf-libvirt firewalld zone for virbr0
