# Wolf-OS Virtualization Stack

Installs the libvirt/virtnetworkd runtime foundation for Fedora Atomic desktops so virt-manager networking works correctly out of the box (including users/groups, permissions, and tmpfiles).

This RPM adds the libvirt networking runtime foundation needed for virt-manager on Fedora Atomic-style images (including Bazzite). It installs /usr/lib/tmpfiles.d/ rules and creates the required virtnetwork/libvirt-qemu groups plus the filesystem layout for libvirt networking state—such as /var/lib/libvirt/dnsmasq, /var/lib/libvirt/network, and /var/log/libvirt/qemu—with correct ownership and write permissions at boot.

With these changes, virtnetworkd.service starts cleanly and runs dnsmasq, so libvirt networking behaves as it should. For my use case, manually creating a bridge is no longer necessary.

This project is built and hosted via [Fedora COPR](https://copr.fedorainfracloud.org/coprs/jonathonp3/sirius-os/). 

📦 Installation

1. On an existing system (Sirius-OS, Silverblue, Bazzite)

Add the COPR repository, then layer the package:

```bash
sudo curl -Lo /etc/yum.repos.d/_copr_jonathonp3-sirius-os.repo https://copr.fedorainfracloud.org/coprs/jonathonp3/sirius-os/repo/fedora-44/jonathonp3-sirius-os-fedora-44.repo
```

## Option A: Virtualization Stack (requires user action after install)

```bash
rpm-ostree install wolf-os-virtualization
```

Reboot to apply changes
```bash
systemctl reboot
```

After reboot, enable and start the services/socket:
```bash
sudo systemctl enable --now virtqemud.service
sudo systemctl enable --now virtlogd.service
sudo systemctl enable --now virtnetworkd.service
sudo systemctl enable --now virtstoraged.service
sudo systemctl enable --now virtnodedevd.socket
```

## Option B: Virtualization Stack (auto via vendor-layer symlinks)

This package uses hard-coded vendor-layer systemd symlinks and declared systemd dependencies to ensure the required services start on boot.

Note: `systemctl is-enabled virtqemud.service virtlogd.service virtstoraged.service virtnetworkd.service virtnodedevd.socket` may not report enabled because the enablement is implemented in the vendor layer rather than via symlinks under /etc.

Install:
```bash
rpm-ostree install wolf-os-virtualization-vendor-symlinks
```

Reboot to apply changes:
```bash
systemctl reboot
```


## Via BlueBuild / Custom Image (Bazzite, Aurora, etc.)

If you’re building your own image with BlueBuild, add the COPR repository in your recipe.yml or in your config directory, then add the package(s) you want in the packages section.

Repository URL:
```bash
https://copr.fedorainfracloud.org/coprs/jonathonp3/sirius-os/repo/fedora-44/jonathonp3-sirius-os-fedora-44.repo
```

Option A: User-enable after install
yaml
```bash
  - type: rpm-ostree
    install:
      - wolf-os-virtualization
```

Option B: Auto via vendor-layer symlinks


```bash
  - type: rpm-ostree
    install:
      - wolf-os-virtualization-vendor-symlinks
```

Choose Option A if you prefer enabling services manually during the build or after the image is deployed , or Option B if you want them started on boot via vendor-layer systemd enablement.
