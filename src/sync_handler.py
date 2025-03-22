import os
import subprocess
import logging
import config

def notify(message):
    if config.NOTIFICATIONS_ENABLED:
        logging.info("Notification sent to %s: %s", config.NOTIFICATION_RECIPIENT, message)

class SyncEventHandler:
    def __init__(self, source, destination):
        self.source = os.path.abspath(source) if ":" not in source else source
        self.destination = os.path.abspath(destination) if ":" not in destination else destination

    def run_rsync(self):
        command = ["rsync"] + config.RSYNC_FLAGS[:]
        if config.DRY_RUN:
            command.append("--dry-run")
        if "--itemize-changes" not in command:
            command.append("--itemize-changes")
        for pattern in config.EXCLUDEDIRS:
            command.append("--exclude=" + pattern)
        for pattern in config.EXCLUDED_FILE_PATTERNS:
            command.append("--exclude=" + pattern)
        
        ssh_options = ""
        if ":" in self.source and config.SOURCE_SSH_PORT:
            ssh_options = f"ssh -p {config.SOURCE_SSH_PORT}"
        elif ":" in self.destination and config.DESTINATION_SSH_PORT:
            ssh_options = f"ssh -p {config.DESTINATION_SSH_PORT}"
        if config.SSH_OPTIONS:
            ssh_options += (" " + config.SSH_OPTIONS).strip()
        if ssh_options:
            command.extend(["-e", ssh_options])
        
        source = self.source
        if ":" in source and not source.rstrip().endswith("/"):
            source = source + "/"
        elif ":" not in source and not source.rstrip().endswith(os.sep):
            source = source + os.sep
        
        command.extend([source, self.destination])
        
        logging.debug("Executing command: %s", " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True)
        
        changes = []
        if result.stdout:
            for line in result.stdout.splitlines():
                line = line.strip()
                # Filter out common rsync summary lines that are not indicative of real changes
                if (line.startswith("sent") or line.startswith("total") or
                    line.startswith("receiving incremental file list") or
                    line.startswith("sending incremental file list") or
                    line.startswith("Summary of changed files:")):
                    continue
                if line:
                    changes.append(line)
        
        if result.returncode != 0:
            logging.error("Rsync sync error: %s", result.stderr)
            notify("Rsync sync error: " + result.stderr)
        elif changes:
            logging.info("Summary of changed files:")
            for change in changes:
                logging.info(change)
        else:
            logging.info("No changes detected.")
        
        return changes
