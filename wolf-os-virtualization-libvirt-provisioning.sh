#!/bin/bash
# Wolf-OS: libvirt provisioning
set -euo pipefail

echo "🔧 Wolf-OS libvirt provisioning starting..."

# --- 1. Install firewalld services ---
echo "📦 Installing firewalld services..."
mkdir -p /etc/firewalld/services
cp /usr/share/wolf-os/container-http.xml /etc/firewalld/services/
cp /usr/share/wolf-os/container-https.xml /etc/firewalld/services/
cp /usr/share/wolf-os/container-https-alt.xml /etc/firewalld/services/
cp /usr/share/wolf-os/quick-share.xml /etc/firewalld/services/

# --- 2. Install firewalld zone ---
echo "📦 Installing firewalld zone..."
mkdir -p /etc/firewalld/zones
cp /usr/share/wolf-os/libvirt.xml /etc/firewalld/zones/

# --- 3. Reload firewalld ---
echo "🔄 Reloading firewalld..."
firewall-cmd --reload

# --- 4. Setup libvirt network directories ---
echo "📦 Configuring libvirt network..."
mkdir -p /etc/libvirt/qemu/networks
chmod 700 /etc/libvirt/qemu/networks

# --- 5. Remove existing default network ---
if virsh net-list --all | grep -q "default"; then
    virsh net-destroy default 2>/dev/null || :
    virsh net-undefine default 2>/dev/null || :
fi

# --- 6. Install custom default network ---
cp /usr/share/wolf-os/default-net.xml /etc/libvirt/qemu/networks/default.xml
chmod 600 /etc/libvirt/qemu/networks/default.xml

# --- 7. Enable libvirt services ---
echo "🔧 Enabling libvirt services..."
systemctl enable --now virtqemud.service 2>/dev/null || :
systemctl enable --now virtlogd.service 2>/dev/null || :
systemctl enable --now virtnetworkd.service 2>/dev/null || :
systemctl enable --now virtstoraged.service 2>/dev/null || :
systemctl enable --now virtnodedevd.socket 2>/dev/null || :

# --- 8. Define and start network ---
echo "🌐 Defining default network..."
virsh net-define /etc/libvirt/qemu/networks/default.xml
virsh net-autostart default
virsh net-start default

# --- 9. Create provisioning marker ---
mkdir -p /etc/wolf-os
touch /etc/wolf-os/libvirt-provisioned

# --- 10. Provision the uninstall service ---
echo "📦 Provisioning uninstall service..."
/usr/libexec/wolf-os-virtualization-uninstall-provision.sh

echo "✅ Wolf-OS libvirt provisioning complete!"
