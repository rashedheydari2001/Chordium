#!/bin/bash

set -e

echo "=========================================="
echo "   Installing Chordium Music Player..."
echo "=========================================="

# Ensure script is NOT run as root
if [ "$EUID" -eq 0 ]; then
  echo "[-] Please do NOT run this script with sudo or as root."
  echo "    Run it normally: ./installer.sh"
  exit 1
fi

# Step 1: Install System Dependencies (asks for password only if needed for package manager)
# Step 2: Ensure pipx path is set up for the user
echo "[+] Configuring pipx..."
pipx ensurepath

# Step 3: Install the application locally via pipx (No root)
echo "[+] Installing Chordium locally via pipx..."
pipx install --system-site-packages --force .

# Step 4: Register Desktop Application Menu Entry locally
echo "[+] Registering desktop application menu entry..."
INSTALL_DIR="$HOME/.local/share/applications"
mkdir -p "$INSTALL_DIR"

if [ -f "chordium.desktop" ]; then
  cp chordium.desktop "$INSTALL_DIR/chordium.desktop"
  update-desktop-database "$INSTALL_DIR" 2>/dev/null || true
  echo "[+] Desktop shortcut successfully installed!"
else
  echo "[!] Warning: chordium.desktop file not found, skipping menu shortcut registration."
fi

echo "=========================================="
echo "   Installation Completed Successfully!"
echo "   You can now launch Chordium from your"
echo "   desktop menu or by typing 'chordium' in terminal."
echo "=========================================="
