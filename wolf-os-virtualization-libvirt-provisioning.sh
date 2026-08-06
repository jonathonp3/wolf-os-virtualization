#!/bin/bash
# Wolf-OS: libvirt provisioning with dynamic subnet
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

# --- 4. Enable libvirt services FIRST ---
echo "🔧 Enabling libvirt services..."
systemctl enable --now virtqemud.service 2>/dev/null || :
systemctl enable --now virtlogd.service 2>/dev/null || :
systemctl enable --now virtnetworkd.service 2>/dev/null || :
systemctl enable --now virtstoraged.service 2>/dev/null || :
systemctl enable --now virtnodedevd.socket 2>/dev/null || :

# --- 5. Wait for libvirt to be ready ---
echo "⏳ Waiting for libvirt to be ready..."
for i in {1..10}; do
    if virsh net-list --all &>/dev/null; then
        echo "✅ libvirt is ready"
        break
    fi
    echo "⏳ Waiting... ($i/10)"
    sleep 2
done

# --- 6. Remove existing default network if present ---
if virsh net-list --all 2>/dev/null | grep -q "default"; then
    echo "🧹 Removing existing default network..."
    virsh net-destroy default 2>/dev/null || :
    virsh net-undefine default 2>/dev/null || :
fi

# --- 7. Setup libvirt network directories ---
echo "📦 Configuring libvirt network..."
mkdir -p /etc/libvirt/qemu/networks
chmod 700 /etc/libvirt/qemu/networks

# --- 8. Dynamic Subnet Selection (Auto-Pivot) ---
echo "🔍 Searching for available subnet..."
SUBNET=100
# Look for a subnet that is NOT in the host's route table
while ip route | grep -q "192.168.${SUBNET}.0/24"; do
    echo "⚠️  Subnet 192.168.${SUBNET}.x is in use. Pivoting..."
    SUBNET=$((SUBNET + 1))
    if [ $SUBNET -gt 150 ]; then
        echo "❌ Error: No free subnets found in range 100-150."
        exit 1
    fi
done

echo "✅ Selected Subnet: 192.168.${SUBNET}.0/24"

# --- 9. Install custom default network with dynamic subnet ---
echo "🌐 Generating dynamic network configuration..."
sed "s/100/${SUBNET}/g" /usr/share/wolf-os/default-net.xml > /etc/libvirt/qemu/networks/default.xml
chmod 600 /etc/libvirt/qemu/networks/default.xml

# --- 10. Define and start network ---
echo "🌐 Defining default network..."
virsh net-define /etc/libvirt/qemu/networks/default.xml
virsh net-autostart default
virsh net-start default

# --- 11. Create provisioning marker ---
mkdir -p /etc/wolf-os
touch /etc/wolf-os/libvirt-provisioned

# --- 12. Log the selected subnet ---
echo "📝 Subnet selected: 192.168.${SUBNET}.0/24"
echo "192.168.${SUBNET}.0/24" > /etc/wolf-os/default-subnet.txt

# --- 13. Provision the uninstall service ---
echo "📦 Provisioning uninstall service..."
if [ -f /usr/libexec/wolf-os-virtualization-uninstall-provision.sh ]; then
    /usr/libexec/wolf-os-virtualization-uninstall-provision.sh
else
    echo "⚠️  Uninstall provision script not found!"
fi

echo "✅ Wolf-OS libvirt provisioning complete!"
echo "ℹ️  VM Network: 192.168.${SUBNET}.0/24"
