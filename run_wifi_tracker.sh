#!/bin/bash

# Step 1: Detect wireless interface
iface=$(iw dev | awk '$1=="Interface"{print $2}')

if [ -z "$iface" ]; then
    echo "❌ No wireless interface found. Please check your Wi-Fi adapter."
    exit 1
fi

echo "✅ Wireless interface detected: $iface"

# Step 2: Enable monitor mode
echo "🔄 Switching $iface to monitor mode..."
sudo ip link set $iface down
sudo iwconfig $iface mode monitor
sudo ip link set $iface up
echo "✅ Monitor mode enabled on $iface"

# Step 3: Run the Python tracker script
echo "🚀 Starting Wi-Fi tracker for target BSSID..."
sudo python3 wifi_tracker.py

# Step 4: Revert to managed mode after tracking
echo "🔁 Reverting $iface back to managed mode..."
sudo ip link set $iface down
sudo iwconfig $iface mode managed
sudo ip link set $iface up
echo "✅ Interface restored. You're back online."