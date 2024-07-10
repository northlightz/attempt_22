import subprocess
import time
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Paths
BOT_SCRIPT = os.path.join("TEST_TG_BOT", "bot.py")
REMOTE_SCRIPT = "remote.py"
JSON_FILE = "blog_posts.json"


class BlogPostHandler(FileSystemEventHandler):

    def __init__(self):
        self.last_position = 0

    def on_modified(self, event):
        if event.src_path == JSON_FILE:
            self.process_new_entries()

    def process_new_entries(self):
        with open(JSON_FILE, 'r') as f:
            f.seek(self.last_position)
            new_data = f.read()
            if new_data:
                print("New data detected. Running remote.py...")
                subprocess.run(["python", REMOTE_SCRIPT])
                self.last_position = f.tell()


def run_bot():
    print("Starting Telegram bot...")
    bot_process = subprocess.Popen(["python", BOT_SCRIPT])
    return bot_process


def monitor_json_file():
    print(f"Monitoring {JSON_FILE} for changes...")
    event_handler = BlogPostHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    return observer


def main():
    # Ensure the JSON file exists
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w') as f:
            pass  # Create an empty file

    # Start the Telegram bot
    bot_process = run_bot()

    # Start monitoring the JSON file
    observer = monitor_json_file()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        observer.stop()
        bot_process.terminate()

    observer.join()
    bot_process.wait()


if __name__ == "__main__":
    main()
