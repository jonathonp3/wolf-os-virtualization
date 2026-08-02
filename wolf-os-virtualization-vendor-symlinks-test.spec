# Disable debug packages
%define debug_package %{nil}

Name:           wolf-os-virtualization
Version:        1.1.0
Release:        1%{?dist}
Summary:        User-Enabled Virtualization Stack for Wolf-OS
License:        GPLv3
URL:            https://github.com/jonathonp3/wolf-os-virtualization
BuildArch:      noarch

# --- SOURCES ---
Source0:        wolf-os-virtualization.sysusers
Source1:        wolf-os-virtualization.tmpfiles
Source2:        wolf-os-libvirt.xml

# --- DEPENDENCIES ---
Requires:       libvirt-daemon-config-network
Requires:       libvirt-daemon-kvm
Requires:       qemu-kvm
Requires:       virt-install
Requires:       virt-manager
Requires:       virt-viewer
Requires:       firewalld

%description
Provides the full libvirt/virtnetworkd runtime foundation for Wolf-OS.
Includes declarative firewall rules to ensure virbr0 networking works on Atomic deployments.
User intervention is required to enable services unless using the vendor-symlinks variant.

%prep
%setup -c -T

%build
# No build needed

%install
# 1. Create target directories
mkdir -p %{buildroot}/usr/lib/sysusers.d
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
mkdir -p %{buildroot}/usr/lib/firewalld/zones

# 2. Install configurations
install -p -m 644 %{_sourcedir}/wolf-os-virtualization.sysusers %{buildroot}/usr/lib/sysusers.d/wolf-os-virtualization.conf
install -p -m 644 %{_sourcedir}/wolf-os-virtualization.tmpfiles %{buildroot}/usr/lib/tmpfiles.d/wolf-os-virtualization.conf
install -p -m 644 %{_sourcedir}/wolf-os-libvirt.xml %{buildroot}/usr/lib/firewalld/zones/libvirt.xml

%files
# Base files
/usr/lib/sysusers.d/wolf-os-virtualization.conf
/usr/lib/tmpfiles.d/wolf-os-virtualization.conf
# Declarative Firewall Zone
/usr/lib/firewalld/zones/libvirt.xml

%changelog
* Sun Aug 02 2026 Jonathon <jonathon@sirius-os> - 1.1.0-1
- Add declarative firewalld zone for libvirt
- Ensure virbr0 is automatically assigned to libvirt zone
- Fix DHCP/DNS timeout issues on Atomic deployments
* Thu Jul 16 2026 Jonathon <jonathon@sirius-os> - 1.0.0-1
- First Stable Release for wolf-os-virtualization
- Verified compatibility with modular libvirt architecture

