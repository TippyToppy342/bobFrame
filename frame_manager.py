from display_manager import DisplayManager
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    # Collect arguments from the command line
    sd_path = sys.argv[1]
    refresh_time = int(sys.argv[2])
    print(f"Frame manager received SD path: {sd_path}")
    print(f"Frame manager received refresh time: {refresh_time} seconds")
    
    # Point the display manager DIRECTLY to the SD card
    display_manager = DisplayManager(image_folder=sd_path, refresh_time=refresh_time)
    print("Display manager created")

    # Show startup message
    display_manager.display_message('start.jpg')

    # Start displaying images immediately
    try:
        print("Starting display loop...")
        display_manager.display_images()
    except Exception as e:
        print(f"Error during image display: {e}")
