import sys
import os
import threading
from datetime import datetime

try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
except ImportError:
    print("This tool requires sounddevice, soundfile, and numpy. Install them with:")
    print("    pip install sounddevice soundfile numpy --break-system-packages")
    sys.exit(1)

RECORDINGS_DIR = "recordings"
SAMPLE_RATE = 44100
CHANNELS = 1

def ensure_recordings_dir():
    if not os.path.exists(RECORDINGS_DIR):
        os.makedirs(RECORDINGS_DIR)

def record_audio():
    """Record audio until the user presses Enter, then return the recorded frames."""
    print("\nRecording... press Enter to stop.")

    frames = []
    stop_flag = threading.Event()

    def callback(indata, frame_count, time_info, status):
        if status:
            print(f"Recording status: {status}")
        frames.append(indata.copy())

    def wait_for_enter():
        input()
        stop_flag.set()

    listener = threading.Thread(target=wait_for_enter, daemon=True)
    listener.start()

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback):
        while not stop_flag.is_set():
            sd.sleep(100)

    if not frames:
        return None

    return np.concatenate(frames, axis=0)

def save_recording(audio_data):
    ensure_recordings_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(RECORDINGS_DIR, f"recording_{timestamp}.wav")
    sf.write(filename, audio_data, SAMPLE_RATE)
    return filename

def list_recordings():
    ensure_recordings_dir()
    files = sorted(f for f in os.listdir(RECORDINGS_DIR) if f.endswith(".wav"))

    if not files:
        print("No recordings found yet.")
        return []

    print("\nSaved recordings:")
    for i, filename in enumerate(files, start=1):
        print(f"{i}. {filename}")

    return files

def play_recording():
    files = list_recordings()
    if not files:
        return

    choice = input("\nEnter the number of the recording to play: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(files)):
        print("Invalid selection.")
        return

    filepath = os.path.join(RECORDINGS_DIR, files[int(choice) - 1])
    data, samplerate = sf.read(filepath)

    print(f"Playing {files[int(choice) - 1]}... (Ctrl+C to stop early)")
    try:
        sd.play(data, samplerate)
        sd.wait()
    except KeyboardInterrupt:
        sd.stop()
        print("\nStopped.")

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
    print("       VOICE RECORDER")
    print("=" * 30)
    print("1. Record a new voice memo")
    print("2. List recordings")
    print("3. Play a recording")
    print("4. Delete a recording")
    print("5. Exit")

def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            input("Press Enter when you're ready to start recording...")
            audio_data = record_audio()
            if audio_data is None:
                print("No audio was captured.")
            else:
                filename = save_recording(audio_data)
                print(f"Saved recording to {filename}")
        elif choice == "2":
            list_recordings()
        elif choice == "3":
            play_recording()
        elif choice == "4":
            delete_recording()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()