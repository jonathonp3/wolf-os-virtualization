# Disable debug packages
%define debug_package %{nil}

Name:           wolf-os-virtualization
Version:        1.0.0
Release:        11%{?dist}
Summary:        User-Enabled Virtualization Stack for Wolf-OS
License:        GPLv3
URL:            https://github.com/jonathonp3/wolf-os-virtualization
BuildArch:      noarch

# --- SOURCES ---
Source0:        wolf-os-virtualization.sysusers
Source1:        wolf-os-virtualization.tmpfiles
Source2:        wolf-os-virtualization-libvirt.xml
Source3:        wolf-os-virtualization-default-net.xml
Source4:        wolf-os-virtualization-container-http.xml
Source5:        wolf-os-virtualization-container-https.xml
Source6:        wolf-os-virtualization-container-https-alt.xml
Source7:        wolf-os-virtualization-quick-share.xml
Source8:        wolf-os-virtualization-libvirt-provisioning.sh
Source9:        wolf-os-virtualization-libvirt-provision.service
Source10:       wolf-os-virtualization-uninstall-provision.sh
Source11:       wolf-os-virtualization-uninstall-provision.service

# --- DEPENDENCIES ---
Requires:       libvirt-daemon-config-network
Requires:       libvirt-daemon-kvm
Requires:       qemu-kvm
Requires:       virt-install
Requires:       virt-manager
Requires:       virt-viewer
Requires:       firewalld
Requires:       systemd

%description
Provides the full libvirt/virtnetworkd runtime foundation for Wolf-OS.

%setup -c -T

%build
# No build needed

%install
# Create directories
mkdir -p %{buildroot}/usr/lib/sysusers.d
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
mkdir -p %{buildroot}/usr/share/wolf-os
mkdir -p %{buildroot}/usr/libexec
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/usr/lib/systemd/system/multi-user.target.wants

# Install sysusers and tmpfiles
install -p -m 644 %{SOURCE0} %{buildroot}/usr/lib/sysusers.d/wolf-os-virtualization.conf
install -p -m 644 %{SOURCE1} %{buildroot}/usr/lib/tmpfiles.d/wolf-os-virtualization.conf

# Install source templates to /usr/share/wolf-os/
install -p -m 644 %{SOURCE2} %{buildroot}/usr/share/wolf-os/libvirt.xml
install -p -m 644 %{SOURCE3} %{buildroot}/usr/share/wolf-os/default-net.xml
install -p -m 644 %{SOURCE4} %{buildroot}/usr/share/wolf-os/container-http.xml
install -p -m 644 %{SOURCE5} %{buildroot}/usr/share/wolf-os/container-https.xml
install -p -m 644 %{SOURCE6} %{buildroot}/usr/share/wolf-os/container-https-alt.xml
install -p -m 644 %{SOURCE7} %{buildroot}/usr/share/wolf-os/quick-share.xml

# Install provisioning scripts
install -p -m 755 %{SOURCE8} %{buildroot}/usr/libexec/wolf-os-virtualization-libvirt-provisioning.sh
install -p -m 755 %{SOURCE10} %{buildroot}/usr/libexec/wolf-os-virtualization-uninstall-provision.sh

# Install systemd services
install -p -m 644 %{SOURCE9} %{buildroot}/usr/lib/systemd/system/wolf-os-virtualization-libvirt-provision.service
install -p -m 644 %{SOURCE11} %{buildroot}/usr/lib/systemd/system/wolf-os-virtualization-uninstall-provision.service

# Enable Services via Symlinks
ln -sf ../wolf-os-virtualization-libvirt-provision.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/wolf-os-virtualization-libvirt-provision.service
ln -sf ../wolf-os-virtualization-uninstall-provision.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/wolf-os-virtualization-uninstall-provision.service

%post
# Reload systemd to pick up new services
systemctl daemon-reload 2>/dev/null || :

%postun
# Reload systemd after removal
systemctl daemon-reload 2>/dev/null || :

%files
/usr/lib/sysusers.d/wolf-os-virtualization.conf
/usr/lib/tmpfiles.d/wolf-os-virtualization.conf
/usr/share/wolf-os/libvirt.xml
/usr/share/wolf-os/default-net.xml
/usr/share/wolf-os/container-http.xml
/usr/share/wolf-os/container-https.xml
/usr/share/wolf-os/container-https-alt.xml
/usr/share/wolf-os/quick-share.xml
/usr/libexec/wolf-os-virtualization-libvirt-provisioning.sh
/usr/libexec/wolf-os-virtualization-uninstall-provision.sh
/usr/lib/systemd/system/wolf-os-virtualization-libvirt-provision.service
/usr/lib/systemd/system/wolf-os-virtualization-uninstall-provision.service
/usr/lib/systemd/system/multi-user.target.wants/wolf-os-virtualization-libvirt-provision.service
/usr/lib/systemd/system/multi-user.target.wants/wolf-os-virtualization-uninstall-provision.service

%changelog
%changelog
* Thu Aug 06 2026 Jonathon <jonathon@sirius-os> - 1.0.0-11
- Complete rewrite using systemd provisioning (Silverblue/Atomic compatible)
  - Main provision service runs at boot to copy configs from /usr/share/wolf-os/ to /etc
  - Uninstall provision service creates dormant uninstall service at runtime
  - Clean uninstall removes all traces when package is removed
  
- Custom firewalld zone with development-friendly services:
  - HTTP/HTTPS for web development
  - Container services: 8080, 8443, 8090
  - Quick-share port: 8000
  - Masquerade for internet access
  - Reject rule for host protection

- Virtual network configuration:
  - Dynamic subnet selection (auto-pivot) avoids conflicts with host networks
  - Default virtual network configured on first available 192.168.100-150.0/24 subnet
  - Network autostart enabled at boot

- Automatic service enablement at boot:
  - virtqemud.service
  - virtlogd.service
  - virtnetworkd.service
  - virtstoraged.service
  - virtnodedevd.socket

* Sun Aug 2 2026 Jonathon <jonathon@sirius-os> - 1.0.0-1
- First Stable Release for wolf-os-virtualization
- Verified compatibility with modular libvirt architecture
- Custom wolf-libvirt firewalld zone for virbr0


* Sun Aug 2 2026 Jonathon <jonathon@sirius-os> - 1.0.0-1
- First Stable Release for wolf-os-virtualization
- Verified compatibility with modular libvirt architecture
- Custom wolf-libvirt firewalld zone for virbr0
