# Vanguard Shield (V1)

Vanguard Shield is an ultra-lightweight, dark-themed Tkinter GUI wrapper for the ClamAV (`clamscan`) malware detection engine. Designed specifically for resource-constrained GNU/Linux systems, it provides a safe interface to run deep scans on targeted files, monitor active RAM impact, and automatically isolate threats.

### Disclaimer

CRITICAL NOTICE: Vanguard Shield V1 is an open-source graphical interface overlay for the third-party ClamAV scanning engine. It is provided "as is" without warranties of any kind, explicit or implied.

- This tool does not provide real-time kernel-level file protection (AMSI/fanotify monitoring).
- The developer assumes zero liability for system damages, data corruption, or undetected threats ("false negatives").
- Always handle files inside the quarantine/ directory with extreme caution.

## Features
* **Threaded Execution:** Scans run in background threads to keep the UI fully responsive.
* **Automatic Quarantine:** Relocates infected binaries, appends a `.locked` extension, and breaks execution capabilities.
* **Live Metrics:** Embedded low-overhead RAM utilization tracker.
* **Clean Architecture:** Generates individual execution log reports under a local directory structure.

## Prerequisites

This tool requires Python 3, `psutil`, and the ClamAV backend engine installed on your Linux system.

```bash
# Update package lists and install ClamAV
sudo apt update && sudo apt install clamav clamav-daemon -y

# Update ClamAV virus signatures
sudo freshclam

# Install Python requirements
pip install psutil
