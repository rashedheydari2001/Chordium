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
echo "[+] Checking and installing system dependencies..."
if command -v apt &>/dev/null; then
  sudo apt update
  sudo apt install -y python3-pip python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-gst-1.0 gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly pipx desktop-file-utils

elif command -v dnf &>/dev/null; then
  sudo dnf install -y python3 python3-gobject gtk4 gstreamer1-plugins-good gstreamer1-plugins-bad-free gstreamer1-plugins-ugly-free pipx desktop-file-utils

elif command -v pacman &>/dev/null; then
  sudo pacman -Sy --noconfirm python python-gobject gtk4 gst-plugins-good gst-plugins-bad gst-plugins-ugly pipx desktop-file-utils

elif command -v zypper &>/dev/null; then
  sudo zypper refresh
  sudo zypper install -y python3-gobject Gtk4 gstreamer-plugins-good gstreamer-plugins-bad gstreamer-plugins-ugly pipx desktop-file-utils

else
  echo "[-] Unsupported package manager. Please ensure Python 3, GTK4, GStreamer, and pipx are installed."
  exit 1
fi

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
