import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import sys
import subprocess

observer = Observer()

class Handler(PatternMatchingEventHandler):

    @staticmethod
    def on_any_event(event):
       subprocess.check_call(['pkill', '--signal', '9', '-f', '/app/main.py'], stdout=subprocess.DEVNULL)
       subprocess.Popen(['python3', '/app/main.py'])


event_handler = Handler(patterns=["*.py"])
observer.schedule(event_handler, '/app', recursive=True)
observer.start()
try:
    subprocess.call(['python3', '/app/main.py'])
except:
    observer.stop()

observer.join()

