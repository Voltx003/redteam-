# Red Team Environment Setup

This repository provides scripts to set up a security research environment on Ubuntu 24.04.

## Setup Kali Linux Tools

> **WARNING:** The setup script adds Kali Linux repositories to your Ubuntu system. This "mixed" configuration can lead to system instability if not handled carefully. Use a dedicated environment.

To install the essential Kali Linux security tools, run the provided setup script:

```bash
chmod +x setup_kali.sh
./setup_kali.sh
```

### Included Tools
The script installs the following tools:
- **Recon:** `nmap`, `netdiscover`, `onesixtyone`, `hping3`, `masscan`
- **Exploitation:** `metasploit-framework`, `sqlmap`, `aircrack-ng`, `reaver`
- **Bruteforce/Wordlists:** `hashcat`, `crunch`, `cewl`
- **Utilities:** `proxychains4`, `macchanger`, `dirb`, `xxd`, `chntpw`, `sslscan`

## Reconnaissance Rules
Refer to `RECCE.md` for target-specific information (e.g., Zendesk Bug Bounty).