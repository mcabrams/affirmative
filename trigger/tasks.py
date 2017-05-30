from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


from confirm.actions import request_confirm


def watch_for_new_file(path):
    watch_directory(NewFileHandler(), path)


def watch_directory(handler, path):
    observer = Observer()
    observer.schedule(handler, path)
    observer.start()


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        request_confirm(event.src_path)
