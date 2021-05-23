import time
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .steps import upload_file_to_server, web_hook, move_files_to_archive

class Watcher:
    DIRECTORY_TO_WATCH = os.getenv("DIRECTORY_TO_WATCH" ,"/var/tmp/files")

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


class Handler(FileSystemEventHandler):

    def on_created(self, event):
        """Called when a file or directory is created."""
        if event.is_directory:
            return None

        filename = os.path.basename(event.src_path)
        ts = upload_file_to_server(event.src_path)
        web_hook(filename, ts)
        move_files_to_archive(event.src_path, filename)
