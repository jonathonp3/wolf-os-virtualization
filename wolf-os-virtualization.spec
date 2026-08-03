# Disable debug packages
%define debug_package %{nil}

Name:           wolf-os-virtualization
Version:        1.0.0
Release:        5%{?dist}
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

Overrides the system libvirt firewalld zone with a development-friendly version:
- DHCP/DNS/TFTP/SSH services
- HTTP/HTTPS for web development
- Container services: 8080, 8443, 8090
- Quick-share ports: 8000, 5000, 3000
- Masquerade for internet access
- Reject rule for host protection
- Laptop-friendly - works on WiFi/Ethernet/hotspots

%setup -c -T

%build
# No build needed

%install
# Create vendor-layer directories (/usr/lib) instead of /etc
mkdir -p %{buildroot}/usr/lib/sysusers.d
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
mkdir -p %{buildroot}/usr/lib/firewalld/zones
mkdir -p %{buildroot}/etc/firewalld/services
mkdir -p %{buildroot}/usr/lib/wolf-os

# Install sysusers and tmpfiles
install -p -m 644 %{_sourcedir}/wolf-os-virtualization.sysusers %{buildroot}/usr/lib/sysusers.d/wolf-os-virtualization.conf
install -p -m 644 %{_sourcedir}/wolf-os-virtualization.tmpfiles %{buildroot}/usr/lib/tmpfiles.d/wolf-os-virtualization.conf

# Install firewalld zone
install -p -m 644 %{_sourcedir}/wolf-os-virtualization-libvirt.xml %{buildroot}/etc/firewalld/zones/libvirt.xml  

# Install firewalld services
install -p -m 644 %{_sourcedir}/wolf-os-virtualization-container-http.xml %{buildroot}/etc/firewalld/services/container-http.xml
install -p -m 644 %{_sourcedir}/wolf-os-virtualization-container-https.xml %{buildroot}/etc/firewalld/services/container-https.xml
install -p -m 644 %{_sourcedir}/wolf-os-virtualization-container-https-alt.xml %{buildroot}/etc/firewalld/services/container-https-alt.xml
install -p -m 644 %{_sourcedir}/wolf-os-virtualization-quick-share.xml %{buildroot}/etc/firewalld/services/quick-share.xml

# Default system network configuration
install -p -m 644 %{_sourcedir}/wolf-os-virtualization-default-net.xml %{buildroot}/usr/lib/wolf-os/default-net.xml

%files
/usr/lib/sysusers.d/wolf-os-virtualization.conf
/usr/lib/tmpfiles.d/wolf-os-virtualization.conf
/etc/firewalld/zones/libvirt.xml 
/usr/lib/wolf-os/default-net.xml
/etc/firewalld/services/container-http.xml
/etc/firewalld/services/container-https.xml
/etc/firewalld/services/container-https-alt.xml
/etc/firewalld/services/quick-share.xml

%changelog
* Mon Aug 03 2026 Jonathon <jonathon@sirius-os> - 1.0.0-5
- Fix: Install zone to /etc/firewalld/zones/ instead of /usr/lib
- This allows override without conflicting with base firewalld package
- Add %post and %postun to reload firewalld

* Mon Aug 03 2026 Jonathon <jonathon@sirius-os> - 1.0.0-4
- Override system libvirt zone with wolf-libvirt configuration
- Add: Quick-share service (ports 8000, 5000, 3000)
- Add: Container services (8080, 8443, 8090)
- Add: HTTP/HTTPS services for web development
- Add: Reject rule for host protection
- Works with libvirt default network on 192.168.100.0/24

* Mon Aug 03 2026 Jonathon <jonathon@sirius-os> - 1.1.0-3
- Implement authoritative libvirt zone masking in the vendor layer
- Fix virbr0 overwrite /usr/lib/firewalld/zones/libvirt.xml
- Enforce Workstation-accurate permissions (0700/0600) for network configs via tmpfiles
- Finalized nested virtualization with 192.168.100.0/24 subnet
- Ensure zero-touch bridge initialization on initial deployment boot

* Mon Aug 03 2026 Jonathon <jonathon@sirius-os> - 1.1.0-2
- Implement declarative firewalld zone (wolf-libvirt) in the vendor layer
- Shift default virtual network to 192.168.100.0/24 to prevent nested VM conflicts
- Add tmpfiles.d logic for zero-touch network autostart on first boot
- Verified successful bridge initialization on Atomic deployments

* Sun Aug 2 2026 Jonathon <jonathon@sirius-os> - 1.0.0-1
- First Stable Release for wolf-os-virtualization
- Verified compatibility with modular libvirt architecture
- Custom wolf-libvirt firewalld zone for virbr0
