# OpenAndroidExtractor

OpenAndroidExtractor is a desktop application designed to extract and backup data from Android devices using Android Debug Bridge (ADB).  
It provides a clean, modern interface to perform structured data acquisition without requiring root access.

The tool is intended for digital forensics, technical analysis, data recovery, and Android device diagnostics.

![Demo](https://github.com/DanielRosillo/open-android-extractor/blob/main/preview.png)

---

## Disclaimer

This tool is intended for authorized use only.
You must have explicit permission to access and extract data from any device you connect.

The author is not responsible for misuse or unauthorized access.

## Features
- Plug and Play
- Automatic detection of connected Android devices
- Dashboard with device information:
  - Android version
  - Serial number
  - Screen resolution
  - Battery level
- Contacts export (VCF)
- SMS and call log extraction (CSV)
- Full and selective media backups:
  - Camera (DCIM)
  - Screenshots
  - Pictures
  - Videos
  - Music
  - Documents
  - Downloads
- Social media media extraction:
  - WhatsApp
  - Facebook
  - Messenger
  - Instagram
- Screen capture and screen recording with timestamp
- Android version–aware logic (Android 15+ supported)
- Organized local output structure
- No root required

---

## Interface Overview

OpenAndroidExtractor uses a card-based UI with clearly separated sections:

- **Dashboard** – Device information and status
- **Folders** – Media and storage extraction
- **Contacts** – Contacts export
- **Messages** – SMS extraction
- **Transfer** – Upload and restore files
- **Extras** – Screenshots, screen recording, ADB tools

A real-time console panel displays executed ADB commands and results.

---

## Requirements

- Python 3.9+
- Android Debug Bridge (ADB)
- USB debugging enabled on the Android device
- Android device connected via USB or Wifi

Ensure `adb` is available in your system PATH.

---

## Compatibility
- Any Android device.

---

## Available on Windows and Linux

---

## Installation

git clone https://github.com/danielrosillo/OpenAndroidExtractor.git
cd OpenAndroidExtractor
python app.py

---

## License

OpenAndroidExtractor is released under the MIT License.

---

## Contributions

- Contributions are welcome.

---

## Companion App

Some features may require the OpenExtractor Companion App
installed on the target Android device to enable extended data access
on newer Android versions.

---

## TODO
- Restore options.

---

## Contact

Developed by  **Duxgor25**(VHS_DREAMS25) - danielrosillo@outlook.es

If you find this project useful, consider giving it a ⭐ on GitHub.
