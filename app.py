#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# OpenAndroidExtractor
# Android data extraction and backup tool using ADB
# Danielrosillo@outlook.es
# Copyright (c) 2025 Duxgor25 (VHS_DREAMS25)
# SPDX-License-Identifier: MIT
# Python 3.11.2
# =============================================================================
# ***
# ** ***
# *** *** *** MB
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import time
import uuid
from pathlib import Path
import os
import subprocess
import sys
from datetime import datetime
from tkinter import filedialog

BG = "#f2f4f8"
SIDEBAR_BG = "#ffffff"
CARD_BG = "#ffffff"
ACCENT = "#3DDC84"
TEXT = "#1f2937"
MUTED = "#6b7280"
class ADBTool(tk.Tk):

    DEVICE_ID = ""
    SERIAL = ""
    PKG = "com.duxgor25.systems.open_extractor"
    APK = "extractor.apk"
    APP_VERSION = "1.0.1"
    APP_NAME = "Open Android Extractor"

    def __init__(self):
        super().__init__()

        self.card_col = 0
        self.card_row = 0
        self.max_cols = 4

        self.title(ADBTool.APP_NAME)
        self.geometry("1500x870")
        self.configure(bg=BG)
        self.resizable(False, False)

        self._layout()
        self.devices_connected = False
        
        self.show_section("My Phone")
        self.after(500, self.check_devices)

    def _layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._sidebar()
        self._content()
        self._console()

    def _sidebar(self):
        self.sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=220)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

        title = tk.Label(
            self.sidebar,
            text="OAE",
            bg=SIDEBAR_BG,
            fg=ACCENT,
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(pady=(20, 5))

        version = tk.Label(
            self.sidebar,
            text=ADBTool.APP_VERSION,
            bg=SIDEBAR_BG,
            fg="#9ca3af",   
            font=("Segoe UI", 9),
        )
        version.pack(pady=(0, 15))

        sections = [
            ("MY PHONE", "My Phone"),
            ("FOLDERS", "Folders"),
            ("CONTACTS", "Contacts"),
            ("MESSAGES", "Messages"),
            ("CALLS", "Calls"),
            ("MORE", "More"),
            ("INSTALL","Install"),
            ("RELOAD","Reload")
        ]

        for text, section in sections:
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=lambda s=section: self.show_section(s),
                bg=SIDEBAR_BG,
                fg=TEXT,
                relief="flat",
                anchor="w",
                padx=25,
                pady=12,
                font=("Segoe UI", 11),
                activebackground="#eef2ff",
            )
            btn.pack(fill="x")

        spacer = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        spacer.pack(expand=True, fill="both")


    def _content(self):
        self.content = tk.Frame(self, bg=BG)
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.status = tk.Label(
            self.content,
            text="Finding devices...",
            bg="#e5e7eb",
            fg="#111827",
            font=("Segoe UI", 11),
            padx=15,
            pady=8,
        )
        self.status.pack(fill="x", pady=(0, 15))

        self.title_label = tk.Label(
            self.content,
            text="",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 22, "bold"),
        )
        self.title_label.pack(anchor="w")

        self.cards_container = tk.Frame(self.content, bg=BG)
        self.cards_container.pack(fill="both", expand=True)

    def _console(self):
        frame = tk.Frame(self, bg="#111827")
        frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=(0, 15))

        self.console = tk.Text(
            frame,
            height=7,
            bg="#020617",
            fg="#3DDC84",
            font=("Consolas", 10),
            relief="flat",
        )
        self.console.pack(fill="both", expand=True, padx=10, pady=10)

    def clear_cards(self):
        for w in self.cards_container.winfo_children():
            w.destroy()
        self.card_col = 0
        self.card_row = 0

    def card(self, title, desc, command):
        shadow = tk.Frame(self.cards_container, bg="#d1d5db")
        shadow.grid(
            row=self.card_row,
            column=self.card_col,
            padx=15,
            pady=15,
            sticky="n",
        )

        card = tk.Frame(
            shadow,
            bg=CARD_BG,
            padx=20,
            pady=15,
        )
        card.pack(padx=3, pady=3)

        tk.Label(
            card,
            text=title,
            bg=CARD_BG,
            fg=TEXT,
            font=("Segoe UI", 13, "bold"),
            wraplength=200,
            justify="left",
        ).pack(anchor="w")

        tk.Label(
            card,
            text=desc,
            bg=CARD_BG,
            fg=MUTED,
            font=("Segoe UI", 10),
            wraplength=220,
            justify="left",
        ).pack(anchor="w", pady=8)

        ttk.Button(
            card,
            text="Execute",
            command=command if callable(command) else lambda: self.run_adb(command),
        ).pack(anchor="e", pady=(10, 0))

        self.card_col += 1
        if self.card_col >= self.max_cols:
            self.card_col = 0
            self.card_row += 1

    def run_adb(self, cmd):
        if not self.devices_connected:
            self.status.config(
                text="Connect an Android device first.",
                bg="#fef3c7",
                fg="#92400e",
            )
            return
        def task():
            self.console.insert(tk.END, f"$ {cmd}\n")
            self.console.see(tk.END)
            try:
                p = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    text=True,
                )
                for line in p.stdout:
                    self.console.insert(tk.END, line)
                    self.console.see(tk.END)
            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def show_section(self, name):
        self.clear_cards()
        self.title_label.config(text=ADBTool.DEVICE_ID)

        if (name == "Install"):
            self.install_apk_dialog()
            return

        if (name == "Reload"):
            self.check_devices()
            return

        if name == "My Phone":
            self.max_cols = 5
            if not self.devices_connected:
                self.info_card("Estado", "Device not connected")
                return

            info = self.get_device_info()

            # --- Android / Build ---
            self.info_card(
                "Android",
                f"{info['android_version']} (SDK {info['sdk']})"
            )

            self.info_card(
                "Security Patch",
                info["security_patch"]
            )

            self.info_card(
                "Build ID",
                info["build_id"]
            )

            # --- Device ---
            self.info_card(
                "Manufacturer",
                info["manufacturer"]
            )

            self.info_card(
                "Brand",
                info["brand"]
            )

            self.info_card(
                "Model",
                info["model"]
            )

            self.info_card(
                "Device",
                info["device"]
            )

            self.info_card(
                "Hardware",
                info["hardware"]
            )

            # --- Identifiers ---
            self.info_card(
                "Serial",
                info["serial"]
            )

            # --- Display ---
            self.info_card(
                "Resolution",
                info["resolution"]
            )

            self.info_card(
                "Density",
                info["density"]
            )

            # --- Memory / CPU ---
            self.info_card(
                "RAM",
                info["ram"]
            )

            self.info_card(
                "CPU / SoC",
                info["cpu"]
            )

            # --- Security ---
            self.info_card(
                "SELinux",
                info["selinux"]
            )

            self.info_card(
                "Encryption",
                info["encryption"]
            )

            self.info_card(
                "IP Address",
                info["ip"]
            )

            level = None
            for line in info["battery"].splitlines():
                if line.strip().startswith("level:"):
                    level = int(line.split(":")[1].strip())
                    
                    break

            self.info_card("Battery", str(level)+"%")



        if name == "Folders":
            self.max_cols = 4
            self.card(
                "Dump All",
                "Create a full backup of the device storage using ADB.",
                self.backup_full_storage
            )

            self.card(
                "Download Folder",
                "Backup files from the system Download directory.",
                self.backup_downloads_auto
            )

            self.card(
                "Camera Folder",
                "Extract photos and videos captured by the device camera.",
                self.backup_camera
            )

            self.card(
                "Pictures Folder",
                "Backup images stored in the Pictures directory.",
                self.backup_pictures
            )

            self.card(
                "Screenshots Folder",
                "Backup screenshots stored in the Pictures directory.",
                self.backup_screenshots
            )

            self.card(
                "Documents Folder",
                "Copy documents and files from the Documents folder.",
                self.backup_documents
            )

            self.card(
                "Music Folder",
                "Backup audio and music files from the device.",
                self.backup_music
            )

            self.card(
                "Video Folder",
                "Extract videos stored on the device.",
                self.backup_movies
            )

            self.card(
                "Recordings Folder",
                "Backup voice recordings and audio notes.",
                self.backup_recordings
            )

            self.card(
                "Facebook & Messenger Folder",
                "Copy pictures from Facebook and Messenger apps.",
                self.backup_facebook_messenger_pictures
            )

            self.card(
                "WhatsApp Folder",
                "Backup WhatsApp media, documents, and databases.",
                self.backup_whatsapp_images
            )

            self.card(
                "Instagram Folder",
                "Backup media files from Instagram.",
                self.backup_instagram
            )


        elif name == "Contacts":
            self.card(
                "Export Contacts",
                "Extract and export all contacts stored on the device.",
                self.export_contacts_full
            )

        elif name == "Messages":
            self.card(
                "Export SMS",
                "Retrieve and export SMS messages from the device inbox.",
                self.export_sms_full
            )

        elif name == "More":
            self.card(
                "Screenshot Device",
                "Capture a screenshot of the device screen via ADB.",
                self.adb_screenshot
            )
            self.card(
                "Screenrecord Device",
                "Record the device screen and save it as a video file(60s).",
                self.record_screen
            )
            self.card(
                "Restart ADB",
                "Restart the ADB server and refresh device connections.",
                "adb kill-server && adb start-server"
            )

        
        elif name == "Calls":
            self.card(
                "Export Call History",
                "Extract and export all call history stored on the device.",
                self.export_call_logs_full
            )

    def check_devices(self):
        def task():
            self.console.insert(tk.END, "$ adb devices\n")
            self.console.see(tk.END)

            try:
                p = subprocess.Popen(
                    "adb devices",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    text=True,
                )

                output = p.stdout.read().strip()
                self.console.insert(tk.END, output + "\n\n")
                self.console.see(tk.END)

                lines = output.splitlines()[1:] 
                self.devices_connected = False

                if not lines:
                    self.status.config(
                        text="No ADB devices connected",
                        bg="#fee2e2",
                        fg="#991b1b",
                    )
                    self.clear_cards()
                    self.info_card("Estado", "Device not connected")
                    return

                for line in lines:
                    if "\tdevice" in line:
                        
                        if ADBTool.SERIAL != line.split()[0]:
                            ADBTool.SERIAL = line.split()[0]
                            info = self.get_device_info()
                            random_uuid = uuid.uuid4()
                            ADBTool.DEVICE_ID = info["model"] + "-" + str(random_uuid)

                            directory_path = Path(ADBTool.DEVICE_ID)
                            directory_path.mkdir(parents=True, exist_ok=True)

                        self.status.config(
                        text=f"Device connected: {ADBTool.SERIAL }",
                        bg="#dcfce7",
                        fg="#166534",
                        )
                        
                        self.devices_connected = True
                        self.after(0, lambda: self.show_section("My Phone"))

                        return

                    elif "\tunauthorized" in line:
                        self.clear_cards()
                        self.info_card("Estado", "Device not connected")
                        self.status.config(
                            text="Device not authorized (accept the USB permission)",
                            bg="#fef3c7",
                            fg="#92400e",
                        )
                        return

                    elif "\toffline" in line:
                        self.clear_cards()
                        self.info_card("Estado", "Device not connected")
                        self.status.config(
                            text="Device offline",
                            bg="#fef3c7",
                            fg="#92400e",
                        )
                        return

                self.clear_cards()
                self.info_card("Estado", "Device not connected")
                self.status.config(
                    text="Unknown Device",
                    bg="#fef3c7",
                    fg="#92400e",
                )

            except Exception as e:
                self.devices_connected = False
                self.status.config(
                    text="Error from adb",
                    bg="#fee2e2",
                    fg="#991b1b",
                )
                self.console.insert(tk.END, f"{e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def info_card(self, title, value):
        shadow = tk.Frame(self.cards_container, bg="#d1d5db")
        shadow.grid(
            row=self.card_row,
            column=self.card_col,
            padx=15,
            pady=15,
            sticky="n",
        )

        card = tk.Frame(
            shadow,
            bg=CARD_BG,
            width=220,
            height=100,
            padx=15,
            pady=10,
        )
        card.pack(padx=3, pady=3)
        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            bg=CARD_BG,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        tk.Label(
            card,
            text=value,
            bg=CARD_BG,
            fg=TEXT,
            font=("Segoe UI", 15, "bold"),
            wraplength=190,
            justify="left",
        ).pack(anchor="w", pady=(5, 0))

        self.card_col += 1
        if self.card_col >= self.max_cols:
            self.card_col = 0
            self.card_row += 1
            
    def get_device_info(self):
        info = {}

        commands = {
            # Android / Build
            "android_version": "adb shell getprop ro.build.version.release",
            "sdk": "adb shell getprop ro.build.version.sdk",
            "security_patch": "adb shell getprop ro.build.version.security_patch",
            "build_id": "adb shell getprop ro.build.display.id",
            "fingerprint": "adb shell getprop ro.build.fingerprint",

            # Device
            "manufacturer": "adb shell getprop ro.product.manufacturer",
            "brand": "adb shell getprop ro.product.brand",
            "model": "adb shell getprop ro.product.model",
            "device": "adb shell getprop ro.product.device",
            "hardware": "adb shell getprop ro.hardware",

            # Identifiers
            "serial": "adb get-serialno",

            # Display
            "resolution": "adb shell wm size",
            "density": "adb shell wm density",

            # Battery 
            "battery": "adb shell dumpsys battery",

            # CPU / RAM
            "cpu": "adb shell getprop ro.hardware",
            "ram": "adb shell cat /proc/meminfo | head -n 1",

            # Security
            "selinux": "adb shell getenforce",
            "encryption": "adb shell getprop ro.crypto.state",

            # Network
            "wifi_state": "adb shell dumpsys wifi | grep 'Wi-Fi is'",
            "ip": "adb shell ip addr show wlan0 | grep 'inet '",

        }

        for key, cmd in commands.items():
            try:
                result = subprocess.check_output(
                    cmd,
                    shell=True,
                    stderr=subprocess.DEVNULL,
                    text=True
                ).strip()

                if key == "resolution":
                    result = result.replace("Physical size:", "").strip()

                elif key == "density":
                    result = result.replace("Physical density:", "").strip()

                elif key == "ram":
                    result = result.split(":")[-1].strip()

                elif key == "ip":
                    result = result.split()[1] if result else "N/A"

                info[key] = result if result else "N/A"

            except Exception:
                info[key] = "N/A"

        return info

    def open_filde_browser(self):
        if sys.platform.startswith("win"):
            os.startfile(ADBTool.DEVICE_ID)
        elif sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", ADBTool.DEVICE_ID])
    
    def run(self,cmd, sleep_time=0):
        self.console.insert(tk.END, f"$ {cmd}\n")
        self.console.see(tk.END)
        subprocess.run(cmd, shell=True)
        if sleep_time:
            self.console.insert(tk.END, f"...waiting {sleep_time}s\n")
            self.console.see(tk.END)
            time.sleep(sleep_time)

    def export_sms_full(self):
        def task():
            OUT = f"/storage/emulated/0/Android/data/{ADBTool.PKG}/files/sms_export_full.txt"
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)

            try:
                android_version = subprocess.check_output(
                    "adb shell getprop ro.build.version.release",
                    shell=True,
                    text=True
                ).strip()

                self.console.insert(
                    tk.END, f"Android version detected: {android_version}\n\n"
                )

                if int(android_version.split(".")[0]) >= 15:
                    self.run(f"adb install --bypass-low-target-sdk-block -r {ADBTool.APK}")
                else:
                    self.run(f"adb install -r {ADBTool.APK}")

                perms = [
                    "android.permission.READ_PHONE_NUMBERS",
                    "android.permission.WRITE_CALL_LOG",
                    "android.permission.READ_CALL_LOG",
                    "android.permission.READ_SMS",
                    "android.permission.READ_CONTACTS",
                ]

                for perm in perms:
                    self.run(f"adb shell pm grant {ADBTool.PKG} {perm}")

                self.run(
                    f"adb shell monkey -p {ADBTool.PKG} -c android.intent.category.LAUNCHER 1",
                    sleep_time=10
                )
                self.run('adb pull "'+OUT+'" "{}"'.format(DEST),)

                self.run(f"adb uninstall {ADBTool.PKG}")

                self.console.insert(
                    tk.END, "\nSMS export completed successfully\n"
                )
                
                self.notify_success(f"SMS export completed successfully")
                self.open_filde_browser()

            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def notify_success(self, message):
        self.status.config(
            text=f"{message}",
            bg="#dcfce7",
            fg="#166534",
        )

    def notify_error(self, message):
        self.status.config(
            text=f"{message}",
            bg="#fee2e2",
            fg="#991b1b",
        )

    def export_contacts_full(self):
        def task():
            OUT = f"/storage/emulated/0/Android/data/{ADBTool.PKG}/files/contacts.vcf"
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            try:
                android_version = subprocess.check_output(
                    "adb shell getprop ro.build.version.release",
                    shell=True,
                    text=True
                ).strip()

                self.console.insert(
                    tk.END, f"Android version detected: {android_version}\n\n"
                )

                major_version = int(android_version.split(".")[0])

                if major_version >= 15:
                    self.run(f"adb install --bypass-low-target-sdk-block -r {ADBTool.APK}")
                else:
                    self.run(f"adb install -r {ADBTool.APK}")

                permissions = [
                    "android.permission.READ_PHONE_NUMBERS",
                    "android.permission.WRITE_CALL_LOG",
                    "android.permission.READ_CALL_LOG",
                    "android.permission.READ_SMS",
                    "android.permission.READ_CONTACTS",
                ]

                for perm in permissions:
                    self.run(f"adb shell pm grant {ADBTool.PKG} {perm}")

                self.run(
                    f"adb shell monkey -p {ADBTool.PKG} -c android.intent.category.LAUNCHER 1",
                    sleep_time=10
                )

                self.run('adb pull "'+OUT+'" "{}"'.format(DEST),)

                self.run(f"adb uninstall {ADBTool.PKG}")

                self.notify_success(
                    "Contacts export completed successfully (VCF file saved)."
                )
                self.open_filde_browser()

            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def export_call_logs_full(self):
        def task():
            OUT = f"/storage/emulated/0/Android/data/{ADBTool.PKG}/files/call_export_full.csv"
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)

            try:
                android_version = subprocess.check_output(
                    "adb shell getprop ro.build.version.release",
                    shell=True,
                    text=True
                ).strip()

                self.console.insert(
                    tk.END, f"Android version detected: {android_version}\n\n"
                )

                major_version = int(android_version.split(".")[0])

                if major_version >= 15:
                    self.run(f"adb install --bypass-low-target-sdk-block -r {ADBTool.APK}")
                else:
                    self.run(f"adb install -r {ADBTool.APK}")

                permissions = [
                    "android.permission.READ_PHONE_NUMBERS",
                    "android.permission.WRITE_CALL_LOG",
                    "android.permission.READ_CALL_LOG",
                    "android.permission.READ_SMS",
                    "android.permission.READ_CONTACTS",
                ]

                for perm in permissions:
                    self.run(f"adb shell pm grant {ADBTool.PKG} {perm}")

                self.run(
                    f"adb shell monkey -p {ADBTool.PKG} -c android.intent.category.LAUNCHER 1",
                    sleep_time=10
                )

                self.run('adb pull "'+OUT+'" "{}"'.format(DEST),)

                self.run(f"adb uninstall {ADBTool.PKG}")

                self.notify_success(
                    "Call logs exported successfully (CSV file saved)."
                )
                self.open_filde_browser()
            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def backup_full_storage(self):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            DATA_DIR = os.path.join(DEST, "data")

            try:

                self.console.insert(tk.END, "Copying device storage...\n")
                self.console.see(tk.END)

                subprocess.run(
                    'adb pull "/storage/emulated/0/" "{}"'.format(DATA_DIR),
                    shell=True
                )

                self.console.insert(
                    tk.END, "\nBackup completed successfully.\n"
                )
                self.console.see(tk.END)

                self.notify_success("Full device storage backup completed.")
                self.open_filde_browser()
            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def backup_screenshots(self):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            DATA_DIR = os.path.join(DEST, "Screenshots")

            possible_paths = [
                "/storage/emulated/0/Pictures/Screenshots",
                "/storage/emulated/0/DCIM/Screenshots",
            ]

            try:
                os.makedirs(DATA_DIR, exist_ok=True)

                self.console.insert(
                    tk.END, "Detecting screenshots folder on device...\n"
                )
                self.console.see(tk.END)

                source_path = None
                for path in possible_paths:
                    if self.adb_path_exists(path):
                        source_path = path
                        break

                if not source_path:
                    raise Exception("Screenshots folder not found on device.")

                self.console.insert(
                    tk.END, f"Using source path: {source_path}\n"
                )
                self.console.see(tk.END)

                subprocess.run(
                    f'adb pull "{source_path}" "{DATA_DIR}"',
                    shell=True,
                    check=True
                )

                self.console.insert(
                    tk.END, "\nScreenshots backup completed successfully.\n"
                )
                self.console.see(tk.END)

                self.notify_success("Screenshots backup completed.")
                self.open_filde_browser()

            except Exception as e:
                self.notify_error(f"Screenshots backup failed: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def adb_path_exists(self,path):
        result = subprocess.run(
            f'adb shell "[ -d {path} ] && echo OK"',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return "OK" in result.stdout
        
    def backup_recordings(self):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            DATA_DIR = os.path.join(DEST, "data")

            try:
                os.makedirs(DATA_DIR, exist_ok=True)

                self.console.insert(tk.END, "Copying recordings from device...\n")
                self.console.see(tk.END)

                subprocess.run(
                    'adb pull "/storage/emulated/0/Recordings" "{}"'.format(DATA_DIR),
                    shell=True
                )

                self.console.insert(
                    tk.END, "\nRecordings backup completed successfully.\n"
                )
                self.console.see(tk.END)

                self.notify_success("Recordings backup completed.")
                self.open_filde_browser()

            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def backup_downloads_auto(self):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            DATA_DIR = os.path.join(DEST, "data")

            possible_paths = [
                "/storage/emulated/0/Download",
                "/storage/emulated/0/Downloads",
            ]

            try:
                os.makedirs(DATA_DIR, exist_ok=True)

                self.console.insert(tk.END, "Detecting Downloads folder...\n")
                self.console.see(tk.END)

                source_path = None
                for path in possible_paths:
                    if self.adb_path_exists(path):
                        source_path = path
                        break

                if not source_path:
                    raise Exception("Downloads folder not found on device.")

                self.console.insert(
                    tk.END, f"Using source path: {source_path}\n"
                )

                subprocess.run(
                    f'adb pull "{source_path}" "{DATA_DIR}"',
                    shell=True
                )

                self.console.insert(
                    tk.END, "\nDownloads backup completed successfully.\n"
                )
                self.console.see(tk.END)

                self.notify_success("Downloads backup completed.")
                self.open_filde_browser()

            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def backup_facebook_messenger_pictures(self):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)

            try:
                os.makedirs(DEST, exist_ok=True)

                # ---------- FACEBOOK ----------
                self.console.insert(tk.END, "\nBacking up Facebook pictures...\n")
                self.console.see(tk.END)

                subprocess.run(
                    f'adb pull "/storage/emulated/0/Pictures/Facebook" "{DEST}/Facebook"',
                    shell=True
                )

                # ---------- MESSENGER ----------
                self.console.insert(tk.END, "\nBacking up Messenger pictures...\n")
                self.console.see(tk.END)

                subprocess.run(
                    f'adb pull "/storage/emulated/0/Pictures/Messenger" "{DEST}/Messenger"',
                    shell=True
                )

                self.console.insert(
                    tk.END, "\nFacebook + Messenger backup completed.\n"
                )
                self.console.see(tk.END)

                self.notify_success("Facebook and Messenger backup completed.")
                self.open_filde_browser()

            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def backup_documents(self):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            DATA_DIR = os.path.join(DEST, "data")

            try:

                os.makedirs(DATA_DIR, exist_ok=True)

                self.console.insert(tk.END, "Copying documents from device...\n")
                self.console.see(tk.END)

                subprocess.run(
                    'adb pull "/storage/emulated/0/Documents" "{}"'.format(DATA_DIR),
                    shell=True
                )

                self.console.insert(
                    tk.END, "\nDocuments backup completed successfully.\n"
                )
                self.console.see(tk.END)

                self.notify_success("Documents backup completed.")
                self.open_filde_browser()

            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def backup_camera(self):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            DCIM_DIR = os.path.join(DEST, "data")

            try:
                os.makedirs(DCIM_DIR, exist_ok=True)

                self.console.insert(tk.END, "Copying DCIM (Camera) photos...\n")
                self.console.see(tk.END)

                subprocess.run(
                    'adb pull "/storage/emulated/0/DCIM/Camera" "{}"'.format(DCIM_DIR),
                    shell=True
                )

                self.console.insert(
                    tk.END, "\nCamera/DCIM backup completed successfully.\n"
                )
                self.console.see(tk.END)

                self.notify_success("Camera (DCIM) backup completed.")
                self.open_filde_browser()

            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def backup_music(self):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            DATA_DIR = os.path.join(DEST, "data")

            try:
                os.makedirs(DATA_DIR, exist_ok=True)

                self.console.insert(tk.END, "Copying music from device...\n")
                self.console.see(tk.END)

                subprocess.run(
                    'adb pull "/storage/emulated/0/Music" "{}"'.format(DATA_DIR),
                    shell=True
                )

                self.console.insert(
                    tk.END, "\nMusic backup completed successfully.\n"
                )
                self.console.see(tk.END)

                self.notify_success("Music backup completed.")
                self.open_filde_browser()
            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def backup_whatsapp_images(self):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            SRC = "/storage/emulated/0/Pictures/WhatsApp/"
            DATA_DIR = os.path.join(DEST, "data")

            try:

                os.makedirs(DATA_DIR, exist_ok=True)

                self.console.insert(tk.END, "Copying from:\n")
                self.console.insert(tk.END, f"   {SRC}\n")
                self.console.insert(tk.END, "To:\n")
                self.console.insert(tk.END, f"   {DEST}\n\n")
                self.console.see(tk.END)

                subprocess.run(
                    f'adb pull "{SRC}" "{DEST}"',
                    shell=True
                )

                self.console.insert(
                    tk.END, "\nWhatsApp images backup completed.\n"
                )
                self.console.see(tk.END)

                self.notify_success("WhatsApp images backup completed.")
                self.open_filde_browser()

            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def backup_pictures(self):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            DATA_DIR = os.path.join(DEST, "data")

            try:

                os.makedirs(DATA_DIR, exist_ok=True)

                self.console.insert(tk.END, "Copying pictures from device...\n")
                self.console.see(tk.END)

                subprocess.run(
                    'adb pull "/storage/emulated/0/Pictures" "{}"'.format(DATA_DIR),
                    shell=True
                )

                self.console.insert(
                    tk.END, "\nPictures backup completed successfully.\n"
                )
                self.console.see(tk.END)

                self.notify_success("Pictures backup completed.")
                self.open_filde_browser()

            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def backup_movies(self):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            DATA_DIR = os.path.join(DEST, "data")

            try:

                os.makedirs(DATA_DIR, exist_ok=True)

                self.console.insert(tk.END, "Copying videos from device...\n")
                self.console.see(tk.END)

                subprocess.run(
                    'adb pull "/storage/emulated/0/Movies" "{}"'.format(DATA_DIR),
                    shell=True
                )

                self.console.insert(
                    tk.END, "\nMovies backup completed successfully.\n"
                )
                self.console.see(tk.END)

                self.notify_success("Movies backup completed.")
                self.open_filde_browser()

            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def backup_instagram(self):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            DATA_DIR = os.path.join(DEST, "data")

            DOWNLOAD_DIR = os.path.join(DATA_DIR, "Download")
            PICTURES_DIR = os.path.join(DATA_DIR, "Pictures")

            try:
                os.makedirs(DOWNLOAD_DIR, exist_ok=True)
                os.makedirs(PICTURES_DIR, exist_ok=True)

                self.console.insert(
                    tk.END, "Copying Instagram downloads...\n"
                )
                self.console.see(tk.END)

                subprocess.run(
                    'adb pull "/storage/emulated/0/Download/Instagram" "{}"'.format(DOWNLOAD_DIR),
                    shell=True
                )

                self.console.insert(
                    tk.END, "Copying saved Instagram posts...\n"
                )
                self.console.see(tk.END)

                subprocess.run(
                    'adb pull "/storage/emulated/0/Download/Instagram" "{}"'.format(PICTURES_DIR),
                    shell=True
                )

                self.console.insert(
                    tk.END, "\nInstagram backup completed successfully.\n"
                )
                self.console.see(tk.END)

                self.notify_success("Instagram backup completed.")
                self.open_filde_browser()


            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def record_screen(self, duration=60):
        def task():
            DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            remote_file = f"/storage/emulated/0/screenrecord_{timestamp}.mp4"
            local_file = os.path.join(DEST, f"screenrecord_{timestamp}.mp4")

            try:
                self.console.insert(
                    tk.END, f"Recording screen ({duration}s)...\n"
                )
                self.console.see(tk.END)

                subprocess.run(
                    f'adb shell screenrecord --time-limit {duration} --verbose "{remote_file}"',
                    shell=True,
                    check=True
                )

                self.console.insert(
                    tk.END, "Recording finished. Pulling file...\n"
                )
                self.console.see(tk.END)

                subprocess.run(
                    f'adb pull "{remote_file}" "{local_file}"',
                    shell=True,
                    check=True
                )

                subprocess.run(
                    f'adb shell rm "{remote_file}"',
                    shell=True
                )

                self.console.insert(
                    tk.END, f"Saved: {local_file}\n"
                )
                self.console.see(tk.END)

                self.notify_success("Screen recording completed successfully.")
                self.open_filde_browser()

            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def adb_screenshot(self):
        DEST = os.path.join(os.getcwd(), ADBTool.DEVICE_ID)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot__{timestamp}.png"
        filepath = os.path.join(DEST, filename)

        with open(filepath, "wb") as f:
            subprocess.run(
                ["adb", "exec-out", "screencap", "-p"],
                stdout=f,
                stderr=subprocess.DEVNULL,
                check=True
            )
            self.open_filde_browser()

    def install_apk(self, apk_path):
        def task():
            try:
                if not os.path.exists(apk_path):
                    raise Exception("APK file not found")

                android_version = subprocess.check_output(
                    "adb shell getprop ro.build.version.release",
                    shell=True,
                    text=True
                ).strip()

                major = int(android_version.split(".")[0])

                self.console.insert(
                    tk.END,
                    f"Android detected: {android_version}\n"
                    f"Installing APK:\n{apk_path}\n\n"
                )
                self.console.see(tk.END)

                if major >= 15:
                    cmd = f'adb install --bypass-low-target-sdk-block -r "{apk_path}"'
                else:
                    cmd = f'adb install -r "{apk_path}"'

                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )

                for line in process.stdout:
                    self.console.insert(tk.END, line)
                    self.console.see(tk.END)

                process.wait()

                if process.returncode != 0:
                    raise Exception("ADB install failed")

                self.console.insert(
                    tk.END, "\nAPK installed successfully.\n"
                )
                self.console.see(tk.END)

                self.notify_success("APK installed successfully")
                self.show_section("My Phone")

            except Exception as e:
                self.notify_error(f"ADB error: {e}")
                self.console.insert(tk.END, f"\nError: {e}\n")
                print( f"\nError: {e}\n")

        threading.Thread(target=task, daemon=True).start()

    def install_apk_dialog(self):

        apk_path = filedialog.askopenfilename(
            title="Select APK to install",
            filetypes=[("Android APK", "*.apk")]
        )

        if not apk_path:
            self.show_section("My Phone")
            return

        self.install_apk(apk_path)

if __name__ == "__main__":
    ADBTool().mainloop()
