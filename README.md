# DsoMiti

**DsoMiti** (Drakensang Online Migration Tool) is a utility that automates the safe migration of a standalone Drakensang Online installation to the Steam version.

<img width="812" height="355" alt="image" src="https://github.com/user-attachments/assets/983d9ce2-3d08-40c3-884b-4006b109a93f" />

---

## Features

* Auto Login so you don't need to put your password when you login
* Automated migration from standalone to Steam installation
* Recursive file copying with error handling
* Safe cleanup of obsolete files and shortcuts
* Informative logging with timestamps and log levels
* Structured, extensible operation system for clean task orchestration

---

## Requirements

* **Windows 10 or later**
* **Python 3.8+**
* Drakensang Online installed both from the **official website** and **Steam**

---

## Usage

1. Make sure Drakensang Online is installed:

   * Install and log in once via the **official website** version
   * Install and launch it once via **Steam**, then close it

2. Run the migration script:

   ```
   python DsoMiti.py
   ```

3. Follow the on-screen instructions. The tool will:

   * Copy files from the standalone installation
   * Remove the old installation
   * Clean up any old shortcuts
