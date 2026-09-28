### Compress File
A Python and Qt6-based desktop application designed to simplify the process of compressing photos locally. It is built to be easy for anyone to use, without requiring specialized technical knowledge. Key features:
- **Secure Local Compression**: The entire process takes place on your device, eliminating the need to upload files.
- **Modern Interface**: Built with Qt6 to deliver a lightweight, responsive, and user-friendly UI.
- **High Performance**: Optimized with parallel processing for rapid compression.
- **Cross-Platform**: Runs seamlessly on Windows and Linux operating systems.

### Project Identity
- License: ![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)
- Status: ![Status](https://img.shields.io/badge/status-stable-brightgreen.svg) ![Status](https://img.shields.io/badge/status-actively%20developed-green.svg)

### Used Technologies
- Python 3.14 ![tech](https://img.shields.io/badge/code-Python%203.14-blue?logo=python&logoColor=white)
- Qt6 via PySide6 ![Qt6](https://img.shields.io/badge/framework-Qt6-41CD52?logo=qt&logoColor=white)
- Pillow Library ![Pillow](https://img.shields.io/badge/library-Pillow-3776AB?logo=python&logoColor=white)

### Binary Releases
![Download Ubuntu](https://img.shields.io/badge/download-Ubuntu%2026.04-brightgreen?logo=ubuntu&logoColor=white&style=for-the-badge) ![Download Windows](https://img.shields.io/badge/Download-Windows_10/11-blue?logo=windows&logoColor=white&style=for-the-badge)

Releases available for Windows and Ubuntu/Debian-based Operating System. Check [Releases](https://github.com/Hattaakim/Compress-Photo/releases) for more information about the latest version. 

### Note (For Binary Releases)
This application is built using the Qt6 (PySide6) framework, so it requires the following minimum OS specification:
- **Windows:** Windows 10 (version 1809 or later) or Windows 11 (64-bit). Windows 7, 8, and 8.1 are not supported.
- **Linux (Ubuntu Only):** Ubuntu 26.04 LTS (Resolute Racoon)

## Installation & Usage

### For Windows Users
1. Download the latest `Installer.exe` file from the [Releases](https://github.com/Hattaakim/Compress-Photo/releases) page.
2. Run the installer and follow the on-screen instructions.
3. Open the application via the shortcut on your Desktop or Start Menu.

### For Linux Users (AppImage)
This application is distributed as a portable `.AppImage` file, so no special installation is required. This AppImage was compiled on Ubuntu 26.04. If you are using an older version of Linux (such as Ubuntu 24.04 or 22.04), the application may not run due to glibc version differences.

**Usage via GUI:**
1. Download the latest `.AppImage` file from the [Releases](https://github.com/Hattaakim/Compress-Photo/releases) page.
2. Right-click the downloaded file > select **Properties**.
3. Go to the **Permissions** tab, then check the box **"Allow executing file as program"**.
4. Double-click the `.AppImage` file to launch the application.

**Usage via Terminal:**
Open a terminal in your downloads folder, then run the following commands:
```bash
# Grant execution permissions
chmod +x app-file-name.AppImage

# Run the application
./app-file-name.AppImage
