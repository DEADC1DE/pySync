# config.py.example
#
# SOURCE: Remote source directory in the format "user@host:/path". 
#         For syncing only the content, include a trailing slash.
SOURCE = "/mnt/"
#
# SOURCE_SSH_PORT: SSH port for connecting to the remote source (non-standard port).
SOURCE_SSH_PORT = ""
#
# DESTINATION: Local destination directory.
DESTINATION = "/home/test"
#
# DESTINATION_SSH_PORT: SSH port for destination if needed; empty for local.
DESTINATION_SSH_PORT = ""
#
# SSH_OPTIONS: Additional SSH options (e.g. custom SSH key) to be appended.
SSH_OPTIONS = ""  # Example: "-i /path/to/ssh/key"
#
# EXCLUDEDIRS: A set of directory names or regex patterns to exclude from sync.
EXCLUDEDIRS = {
    r"GROUPS",
}
#
# EXCLUDED_FILE_PATTERNS: A list of regex patterns for filenames to exclude.
EXCLUDED_FILE_PATTERNS = [
    r".*NotWanted.py",
]
#
# RSYNC_FLAGS: Base flags for rsync.
# - "-avzP": Archive mode, verbose, compress data, show progress.
# - "--partial": Keep partially transferred files.
# - "--inplace": Update destination files in place.
# - "--delete": Delete destination files not present in source.
RSYNC_FLAGS = ["-avzP", "--partial", "--inplace", "--delete"]
#
# Backup/Versioning Options: (Optional) If ENABLE_BACKUP is True, rsync will keep backups.
ENABLE_BACKUP = False
BACKUP_DIR = "/home/test_backup"
if ENABLE_BACKUP:
    RSYNC_FLAGS += ["--backup", f"--backup-dir={BACKUP_DIR}"]
#
# CHECK_INTERVAL: Time interval in seconds for periodic rsync execution when live monitoring is not possible.
CHECK_INTERVAL = 10
#
# LOG_FILE: Path to the log file.
LOG_FILE = "/home/pySync/pySync.log"
#
# LOG_LEVEL: Logging level ("DEBUG", "INFO", "WARNING", "ERROR").
LOG_LEVEL = "INFO"
#
# DRY_RUN: If True, rsync will run in dry-run mode (no changes will be made).
DRY_RUN = False
#
# Notification settings (stub example, extend with actual email/webhook integration as needed).
NOTIFICATIONS_ENABLED = False
NOTIFICATION_RECIPIENT = "admin@example.com"
