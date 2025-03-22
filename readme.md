## Overview 📚

pySync is a versatile, modular Python script designed to synchronize files and directories using rsync. It supports both remote and local sources, leveraging watchdog for real-time monitoring (when available) and falling back to periodic sync for remote directories. The tool is highly configurable, offering options like exclusion patterns, custom SSH ports, backup/versioning, dynamic configuration reload, and detailed logging.

---

## Features ✨

- **Rsync Sync:**  
  Synchronizes files using rsync with robust options such as `--delete`, `--inplace`, and `--partial`.

- **Itemized Changes:**  
  Uses rsync’s `--itemize-changes` to provide a concise summary of files that were transferred, updated, or deleted.

- **Watchdog Integration:**  
  Monitors local directories in real-time to trigger sync operations immediately.

- **Periodic Syncing:**  
  Supports periodic checks (configurable via `CHECK_INTERVAL`) for remote directories where live monitoring isn’t feasible.

- **Dynamic Configuration Reload:**  
  Automatically reloads configuration changes without needing to restart the tool.

- **Dry-Run Mode:**  
  Allows simulation of sync operations (via `--dry-run`) without applying any changes.

- **Backup/Versioning Options:**  
  Optional backup mode that saves previous versions of files to prevent accidental data loss.

- **Enhanced Logging & Notifications:**  
  Utilizes Python’s logging module for detailed output and supports notifications for sync errors.

- **Additional SSH Options:**  
  Customize SSH parameters (custom key files, non-standard ports, etc.) for secure remote connections.

---

## Installation 🛠

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/pySync.git
    cd pySync
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

---