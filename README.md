# 🎵 Chordium

**Chordium** is a lightweight, modern desktop music player built for Linux using **Python**, **GTK 4**, and **GStreamer**. It features a clean, native user interface and a robust audio pipeline designed to handle everything from single audio files to full folder queues seamlessly.

---

## ✨ Features

- **Modern GTK 4 UI:** Native, clean, and responsive design that integrates beautifully with modern Linux desktop environments.
- **GStreamer Backend:** Powered by `playbin` for reliable and high-performance audio playback.
- **Flexible Playback Options:**
  - Open and play individual audio files (`.mp3`, `.flac`, `.wav`, `.ogg`, `.m4a`).
  - Load entire folders of music with automated batch playlist importing.
- **Interactive Playlist:** Easily view tracks, skip to next items, and jump straight to any track with double-click activation.
- **End-of-Stream (EOS) Autoplay:** Automatically transitions to the next track in your playlist when the current song finishes.
- **Precise Volume Controls:** Real-time volume slider integration.

---

## 🛠️ Prerequisites & Dependencies

First install pipx for your OS

Make sure you have Python 3 and the required system packages installed on your Linux distribution before running Chordium.

### 1. Install System Dependencies (Ubuntu / Debian / Linux Mint)
```bash
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-gst-1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad
```

### 2. Install System Dependencies (Fedora / RHEL)
```bash
sudo dnf install python3-gobject gtk4 gstreamer1-plugins-good gstreamer1-plugins-bad-free
```

### 3. Install System Dependencies (Arch Linux)
```bash
sudo pacman -S python-gobject gtk4 gst-plugins-good gst-plugins-bad 
```

---

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rashedheydari2001/Chordium.git
   cd Chordium
   ```

2. **Run the application:**
   ```bash
   python3 main.py
   ```
   *(Note: Replace `main.py` with your main script filename if it differs).*

---

## 💡 How to Use

- **Open File:** Click the **Open File** button to pick an individual track to play.
- **Open Folder:** Click the **Open Folder** button to load all supported audio tracks found within a directory into your queue.
- **Play/Pause:** Use the primary play toggle button to control playback.
- **Next Track:** Click **Next** to skip manually, or let the playlist progress automatically.
- **Playlist Navigation:** Click any song in the playlist view to play it instantly.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/rashedheydari2001/Chordium/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
