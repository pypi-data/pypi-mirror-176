import keyboard as key_b
import os

def failsafe_kill():
    try:
        os._exit(1)
    except Exception:
        try:
            os.system(f'taskkill /pid {os.getpid()}')
        except Exception:
            pass
        try:
            os.system(f'taskkill /pid {os.getppid()}')
        except Exception:
            pass


def start_failsafe(hotkey='ctrl+e'):
    key_b.add_hotkey(hotkey, failsafe_kill)
