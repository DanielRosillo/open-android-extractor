# OpenExtractor – Companion App

The **OpenExtractor Companion App** is an Android helper application designed to work alongside the OpenAndroidExtractor desktop tool.  
Its purpose is to facilitate data extraction operations that are restricted or limited when performed directly via ADB.

The app temporarily runs on the target device, requests the required permissions, performs local data export, and stores the results in accessible storage paths so they can be retrieved safely using ADB.

---

## Disclaimer

This application is intended for **authorized and lawful use only**.  
You must have explicit permission to access data on any device where this app is installed.

The developer assumes no responsibility for misuse.

---

## Purpose

Due to Android security restrictions (especially Android 11+), certain data such as SMS, call logs, and contacts cannot be fully accessed via ADB alone.

The companion app:
- Handles privileged data access using granted runtime permissions
- Exports data in structured formats
- Stores output in known, ADB-accessible locations
- Is installed temporarily and removed after extraction

---

## Features

- SMS export to text format
- Call log export to CSV format
- Contacts export to VCF format
- Automatic permission handling
- Android version–aware behavior
- No user interaction required
- Automatic launch via ADB
- Safe uninstall after completion

---

## Permissions Used

The application requests only the permissions required for extraction:

- `READ_SMS`
- `READ_CALL_LOG`
- `WRITE_CALL_LOG`
- `READ_CONTACTS`
- `READ_PHONE_NUMBERS`

All permissions are granted temporarily via ADB.

---

## Android Compatibility

- Android 6(23) to Android 16(36) supported
- Android 15+ supported using install bypass logic
- Scoped storage compliant

---

## Typical Workflow

1. Desktop app detects Android version
2. Companion APK is installed via ADB
3. Required permissions are granted
4. App is launched automatically
5. Data is exported locally on the device
6. Files are pulled via ADB
7. Companion app is uninstalled

---

## License

This project is licensed under the **MIT License**.

---

## Info
- Flutter 3.3.10
- Android SDK version 35.0.1

## Contact

Developed by  **Duxgor25**(VHS_DREAMS25) - danielrosillo@outlook.es
