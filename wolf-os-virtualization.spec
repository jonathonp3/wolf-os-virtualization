# Disable debug packages
%define debug_package %{nil}

Name:           wolf-os-virtualization
Version:        1.0.0
Release:        3%{?dist}
Summary:        User-Enabled Virtualization Stack for Wolf-OS
License:        GPLv3
URL:            https://github.com/jonathonp3/wolf-os-virtualization
BuildArch:      noarch

# --- SOURCES ---
Source0:        wolf-os-virtualization.sysusers
Source1:        wolf-os-virtualization.tmpfiles

# --- DEPENDENCIES ---
# Explicit systemd requirement (Matches your working PIA build)
Requires:       libvirt-daemon-config-network
Requires:       libvirt-daemon-kvm
Requires:       qemu-kvm
Requires:       virt-install
Requires:       virt-manager
Requires:       virt-viewer

%description
Provides the full libvirt/virtnetworkd runtime foundation for Wolf-OS.
User intervention is required where services are enabled in the new deployment.

%setup -c -T

%build
# No build needed

%install
# 1. Create target directories
mkdir -p %{buildroot}/usr/lib/sysusers.d
mkdir -p %{buildroot}/usr/lib/tmpfiles.d

# 2. Install configurations
install -p -m 644 %{_sourcedir}/wolf-os-virtualization.sysusers %{buildroot}/usr/lib/sysusers.d/wolf-os-virtualization.conf
install -p -m 644 %{_sourcedir}/wolf-os-virtualization.tmpfiles %{buildroot}/usr/lib/tmpfiles.d/wolf-os-virtualization.conf


%files
# Base files
/usr/lib/sysusers.d/wolf-os-virtualization.conf
/usr/lib/tmpfiles.d/wolf-os-virtualization.conf

%changelog
* Thu Jul 16 2026 Jonathon <jonathon@sirius-os> - 1.0.0-3
- refactor(sysusers): remove redundant kvm group definition

* Sun Jul 19 2026 Jonathon <jonathon@sirius-os> - 1.0.0-2
- fix: define kvm group to enable declarative user membership

* Thu Jul 16 2026 Jonathon <jonathon@sirius-os> - 1.0.0-1
- First Stable Release for wolf-os-virtualization
- Verified compatibility with modular libvirt architecture

