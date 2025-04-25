from scapy.all import *
from datetime import datetime

# Store discovered networks
networks = {}

# Target BSSID (you can change this to the MAC you want to track)
TARGET_BSSID = "c8:cd:55:72:27:7c"

def callback(packet):
    if packet.haslayer(Dot11Beacon):
        bssid = packet[Dot11].addr2.lower()
        ssid = packet[Dot11Elt].info.decode(errors="ignore") or "<Hidden>"
        dbm_signal = packet.dBm_AntSignal
        channel = int(ord(packet[Dot11Elt:3].info))
        timestamp = datetime.now().strftime('%H:%M:%S')

        if bssid == TARGET_BSSID:
            if bssid not in networks:
                networks[bssid] = (ssid, dbm_signal, channel, timestamp)
                print(f"[{timestamp}] BSSID: {bssid} | SSID: {ssid} | Signal: {dbm_signal} dBm | Channel: {channel}")
            else:
                print(f"[{timestamp}] Update - Signal: {dbm_signal} dBm")

print("🛜 Tracking target BSSID (Press Ctrl+C to stop)...")
print(f"🎯 Target: {TARGET_BSSID}")
sniff(iface="wlan0mon", prn=callback, store=0)