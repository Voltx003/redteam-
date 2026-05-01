#!/bin/bash

# Exit on error
set -e

echo "[*] Adding Kali Linux GPG key..."
wget -qO - https://archive.kali.org/archive-key.asc | gpg --dearmor | sudo tee /usr/share/keyrings/kali-archive-keyring.gpg > /dev/null

echo "[*] Adding Kali Linux repository..."
echo "Types: deb
URIs: http://http.kali.org/kali
Suites: kali-rolling
Components: main contrib non-free
Signed-By: /usr/share/keyrings/kali-archive-keyring.gpg" | sudo tee /etc/apt/sources.list.d/kali.sources > /dev/null

echo "[*] Updating package lists..."
sudo apt-get update

echo "[*] Holding base-files to prevent critical system conflicts..."
sudo apt-mark hold base-files

echo "[*] Installing security tools..."
# We install tools individually to avoid breaking Ubuntu 24.04 dependencies
# Metasploit and Nmap
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y nmap metasploit-framework sqlmap

# Other essential tools
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    aircrack-ng \
    chntpw \
    crunch \
    dirb \
    hashcat \
    hping3 \
    masscan \
    onesixtyone \
    reaver \
    sslscan \
    xxd \
    cewl \
    macchanger \
    netdiscover \
    proxychains4 \
    --no-install-recommends

echo "[+] Setup complete! Tools are ready."
