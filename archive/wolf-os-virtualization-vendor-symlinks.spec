# Disable debug packages
%define debug_package %{nil}

Name:           wolf-os-virtualization-vendor-symlinks
Version:        1.0.0
Release:        2%{?dist}
Summary:        Hard-Enabled Virtualization Stack for Wolf-OS
License:        GPLv3
URL:            https://github.com/jonathonp3/wolf-os-virtualization
BuildArch:      noarch

# --- SOURCES ---
Source0:        wolf-os-virtualization.sysusers
Source1:        wolf-os-virtualization.tmpfiles

# --- DEPENDENCIES ---
Requires:       systemd
Requires:       libvirt-daemon-config-network
Requires:       libvirt-daemon-kvm
Requires:       qemu-kvm
Requires:       virt-install
Requires:       virt-manager
Requires:       virt-viewer

%description
Provides the full libvirt/virtnetworkd runtime foundation for Wolf-OS.

This package uses hard-coded vendor-layer systemd symlinks and declared systemd dependencies to ensure the required services are started on boot.

Note: systemctl is-enabled virtqemud.service virtlogd.service virtstoraged.service virtnetworkd.service virtnodedevd.socket will not display “enabled” because the unit enablement is implemented in the vendor layer rather than via symlinks under /etc.

%prep
%setup -c -T

%build
# No build needed

%install
# --- THE CONSTRUCTION PHASE ---
# %install creates the physical files and symlinks inside a temporary "BuildRoot."
# This BuildRoot mimics the structure of the final Silverblue filesystem.

# %install is where files and symlinks are created
# If you put a file in %{buildroot}/usr/bin/, the RPM will install that file into the real /usr/bin/ on your target system.
# Uses mkdir -p to create the exact folder structure that Silverblue expects.

# 1. Create target directories
mkdir -p %{buildroot}/usr/lib/sysusers.d
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
mkdir -p %{buildroot}/usr/lib/systemd/system/multi-user.target.wants
mkdir -p %{buildroot}/usr/lib/systemd/system/sockets.target.wants

# 2. Install configurations
# %{_sourcedir} is the location where the GitHub files (the .sysusers and .tmpfiles) are sitting during the COPR build.
# %{buildroot} "blueprint" of the construction phase. %install section prepares the BuildRoot (a temporary fake filesystem), 
# so the RPM builder knows exactly what the finished product should look like before it gets packed into sirius-os-virtualization.

# 2. Deploy configurations from the GitHub Sources
# Copy the raw source files and set standard read permissions (644).
install -p -m 644 %{_sourcedir}/wolf-os-virtualization.sysusers %{buildroot}/usr/lib/sysusers.d/wolf-os-virtualization.conf
install -p -m 644 %{_sourcedir}/wolf-os-virtualization.tmpfiles %{buildroot}/usr/lib/tmpfiles.d/wolf-os-virtualization.conf

# 3. Enable services via Vendor-Layer Symlinks
# Vendor Links begin with /usr/lib/systemd/.... "System Design."
# Non-Vendor Links begin with /etc/systemd/.... "User Choices."
# Use relative paths (../service-name) so the links remain 
# valid even if the image is mounted in a different location during build.
ln -sf ../libvirtd.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/libvirtd.service
ln -sf ../virtnetworkd.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/virtnetworkd.service
ln -sf ../virtlogd.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/virtlogd.service
ln -sf ../virtstoraged.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/virtstoraged.service
ln -sf ../virtqemud.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/virtqemud.service
ln -sf ../virtnodedevd.socket %{buildroot}/usr/lib/systemd/system/sockets.target.wants/virtnodedevd.socket

%files
# %files is where the file is OWNED and REGISTERED.
# Instructs the RPM database: "This specific file is part of this package. I own it, I track its security hash, and I will clean it up if I am uninstalled."
# Base files
/usr/lib/sysusers.d/wolf-os-virtualization.conf
/usr/lib/tmpfiles.d/wolf-os-virtualization.conf

# Hard-wired symlinks
# The symlinks are to be registered and owned by the rpm. They're read only and can not be changed on Silverblue. 
# They're baked into the image. Services are set to start.   
/usr/lib/systemd/system/multi-user.target.wants/libvirtd.service
/usr/lib/systemd/system/multi-user.target.wants/virtnetworkd.service
/usr/lib/systemd/system/multi-user.target.wants/virtlogd.service
/usr/lib/systemd/system/multi-user.target.wants/virtstoraged.service
/usr/lib/systemd/system/multi-user.target.wants/virtqemud.service
/usr/lib/systemd/system/sockets.target.wants/virtnodedevd.socket


# Changelog must have a corresponding entry for that exact version and release
# Upgrade Path in COPR
# Open COPR: Go to your project dashboard.
# Builds > New Build > SCM >  Clone url: https://github.com/jonathonp3/sirius-os-virtualization > Committish: Main > 
# Spec File: > Chroots: fedora-44-x86_64 > Other options: Enable internet access during this build
# Build: Run a new build
%changelog
* Thu Jul 16 2026 Jonathon <jonathon@sirius-os> - 1.0.0-2
- First Stable Release for Sirius-OS Virtualization
- Implemented hard-wired vendor symlinks for zero-touch enablement
- Verified compatibility with modular libvirt architecture

