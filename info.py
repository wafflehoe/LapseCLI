import time
import psutil

original = {p.pid: p for p in psutil.process_iter()}

while True:
    for proc in psutil.process_iter(['name']):
        try:
            if (not (original.get(proc.pid))):
                print(proc.info['name'])
                original[proc.pid] = proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    time.sleep(1)