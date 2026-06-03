#!/bin/bash
# --- VANGUARD DEPLOYMENT SEQUENCE: app_antivirus ---
# Generated: 2026-06-03 12:00
# Target: /home/heavenly/Resteer_Projects/python-army/app_antivirus

set -e # Exit on error

echo "[+] Step 1: System dependency sync..."
sudo apt update
sudo apt install -y build-essential python3-dev python3-pip python3-venv

echo "[+] Step 2: Virtual Environment isolation..."
# Clear existing to ensure clean state
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate

echo "[+] Step 3: Core Module installation..."
pip install --upgrade pip
pip install psutil

echo "------------------------------------------------"
echo "SEQUENCE COMPLETE. ENVIRONMENT IS READY."
echo "------------------------------------------------"
echo "To activate: source .venv/bin/activate"
echo "To run:      python <script_name>.py"
