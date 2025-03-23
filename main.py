#!/usr/bin/env python3
# main.py
import sys
import os
import time
import argparse
import importlib
import logging
import config
from src.sync_handler import SyncEventHandler

def main():
    parser = argparse.ArgumentParser(description="Sync directories using rsync with extended features")
    parser.add_argument("--source", help="Source directory", default=config.SOURCE)
    parser.add_argument("--destination", help="Destination directory", default=config.DESTINATION)
    parser.add_argument("--dry-run", action="store_true", help="Enable dry-run mode (no changes will be made)")
    parser.add_argument("--check-interval", type=int, help="Interval in seconds for periodic checks", default=config.CHECK_INTERVAL)
    args = parser.parse_args()
    
    VALID_DIRECTIONS = ["source_to_destination", "destination_to_source"]
    if config.SYNC_DIRECTION not in VALID_DIRECTIONS:
        logging.error("Ungültiger SYNC_DIRECTION-Wert: %s. Muss einer von %s sein", config.SYNC_DIRECTION, VALID_DIRECTIONS)
        sys.exit(1)
    if config.SYNC_DIRECTION == "destination_to_source":
        args.source, args.destination = args.destination, args.source
    
    config.DRY_RUN = args.dry_run
    config.CHECK_INTERVAL = args.check_interval
    
    setup_logging()
    logging.info("Starting sync process.")
    
    if ":" not in args.source and not os.path.isdir(args.source):
        logging.error("Source directory does not exist.")
        return
    if ":" not in args.destination and not os.path.isdir(args.destination):
        logging.info("Destination directory does not exist, creating it.")
        os.makedirs(args.destination, exist_ok=True)
    
    handler = SyncEventHandler(args.source, args.destination)
    
    config_file = "config.py"
    if not os.path.exists(config_file):
        config_file = "./config.py"
    last_config_mtime = os.path.getmtime(config_file) if os.path.exists(config_file) else None
    
    if ":" in args.source or ":" in args.destination:
        logging.info("Remote source/destination detected; starting periodic rsync every %s seconds.", config.CHECK_INTERVAL)
        try:
            while True:
                if last_config_mtime:
                    current_mtime = os.path.getmtime(config_file)
                    if current_mtime != last_config_mtime:
                        importlib.reload(config)
                        last_config_mtime = current_mtime
                        logging.info("Configuration reloaded.")
                handler.run_rsync()
                time.sleep(config.CHECK_INTERVAL)
        except KeyboardInterrupt:
            logging.info("Exiting periodic sync.")
    else:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        
        class LocalEventHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                handler.run_rsync()
        
        observer = Observer()
        observer.schedule(LocalEventHandler(), args.source, recursive=True)
        observer.start()
        logging.info("Monitoring %s and syncing with %s", args.source, args.destination)
        try:
            while True:
                if last_config_mtime:
                    current_mtime = os.path.getmtime(config_file)
                    if current_mtime != last_config_mtime:
                        importlib.reload(config)
                        last_config_mtime = current_mtime
                        logging.info("Configuration reloaded.")
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
