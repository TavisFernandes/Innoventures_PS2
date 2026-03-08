import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .retriever import FinanceRetriever

class DocumentWatcherHandler(FileSystemEventHandler):
    def __init__(self, retriever: FinanceRetriever):
        self.retriever = retriever

    def on_created(self, event):
        if not event.is_directory:
            # Short delay to assure file is fully written
            time.sleep(1)
            print(f"\n[Watcher] New file detected: {event.src_path}")
            self.retriever.add_document(event.src_path)
            print("[Watcher] RAG Knowledge Base Updated successfully.\n")

class DocumentWatcher:
    def __init__(self, watch_dir: str, retriever: FinanceRetriever):
        self.watch_dir = watch_dir
        self.retriever = retriever
        self.observer = Observer()
        
        if not os.path.exists(self.watch_dir):
            os.makedirs(self.watch_dir)

    def start(self):
        event_handler = DocumentWatcherHandler(self.retriever)
        self.observer.schedule(event_handler, self.watch_dir, recursive=False)
        self.observer.start()
        print(f"Started watching {self.watch_dir} for new documents...")

    def stop(self):
        self.observer.stop()
        self.observer.join()
