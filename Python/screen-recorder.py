import sys
import os
import time
import threading
from datetime import datetime

try:
    import mss
    import numpy as np
    import cv2
except ImportError:
    print("This tool requires mss, opencv-python, and numpy. Install them with:")
    print("    pip install mss opencv-python numpy --break-system-packages")
    sys.exit(1)

RECORDINGS_DIR = "screen_recordings"
FPS = 15

def ensure_recordings_dir():
    if not os.path.exists(RECORDINGS_DIR):
        os.makedirs(RECORDINGS_DIR)

def choose_monitor():
    with mss.mss() as sct:
        monitors = sct.monitors[1:]

        if len(monitors) == 1:
            return 1

        print("\nMultiple monitors detected:")
        for i, m in enumerate(monitors, start=1):
            print(f"{i}. {m['width']}x{m['height']} at ({m['left']}, {m['top']})")

        while True:
            choice = input(f"Choose a monitor (1-{len(monitors)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(monitors):
                return int(choice)
            print("Invalid choice.")

def record_screen(monitor_index):
    ensure_recordings_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(RECORDINGS_DIR, f"screen_{timestamp}.mp4")

    stop_flag = threading.Event()

    def wait_for_enter():
        input()
        stop_flag.set()

    listener = threading.Thread(target=wait_for_enter, daemon=True)
    listener.start()

    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]
        width, height = monitor["width"], monitor["height"]

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(filename, fourcc, FPS, (width, height))

        print(f"\nRecording at {width}x{height}, {FPS} fps... press Enter to stop.")

        frame_interval = 1 / FPS
        frame_count = 0
        start_time = time.time()

        try:
            while not stop_flag.is_set():
                loop_start = time.time()

                frame = np.array(sct.grab(monitor))
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                writer.write(frame_bgr)
                frame_count += 1

                elapsed = time.time() - loop_start
                sleep_time = frame_interval - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
        finally:
            writer.release()

    duration = time.time() - start_time
    print(f"Recorded {frame_count} frames over {duration:.1f} seconds.")
    return filename

def list_recordings():
    ensure_recordings_dir()
    files = sorted(f for f in os.listdir(RECORDINGS_DIR) if f.endswith(".mp4"))

    if not files:
        print("No recordings found yet.")
        return []

    print("\nSaved recordings:")
    for i, filename in enumerate(files, start=1):
        path = os.path.join(RECORDINGS_DIR, filename)
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"{i}. {filename} ({size_mb:.1f} MB)")

    return files

def delete_recording():
    files = list_recordings()
    if not files:
        return

    choice = input("\nEnter the number of the recording to delete: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(files)):
        print("Invalid selection.")
        return

    filename = files[int(choice) - 1]
    confirm = input(f"Delete '{filename}'? This can't be undone. (y/n): ").strip().lower()
    if confirm == "y":
        os.remove(os.path.join(RECORDINGS_DIR, filename))
        print(f"Deleted {filename}.")
    else:
        print("Cancelled.")

def show_menu():
    print("\n" + "=" * 30)
    print("       SCREEN RECORDER")
    print("=" * 30)
    print("1. Start a new recording")
    print("2. List recordings")
    print("3. Delete a recording")
    print("4. Exit")

def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            monitor_index = choose_monitor()
            input("Press Enter when you're ready to start recording...")
            filename = record_screen(monitor_index)
            print(f"Saved recording to {filename}")
        elif choice == "2":
            list_recordings()
        elif choice == "3":
            delete_recording()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please enter a number from 1 to 4.")

if __name__ == "__main__":
    main()