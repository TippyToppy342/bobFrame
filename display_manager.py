import os
import sys
import time
import random
from PIL import Image
from datetime import datetime
from lib.waveshare_epd import epd7in3f

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(SCRIPT_DIR, 'lib')
sys.path.append(LIB_PATH)

class DisplayManager:
    """
    Class to manage the display of images on the e-Paper screen.
    """

    # Initializes the display using the epd7in3f library.
    # Sets the rotation and refresh time for the display.
    # Initializes the last display time and selected image to None.
    def __init__(self, image_folder, refresh_time):
        self.last_display_time = time.time()
        self.last_selected_image = None
        self.image_folder = image_folder
        self.rotation = 0
        self.refresh_time = refresh_time
        self.epd = epd7in3f.EPD()
        self.epd.init()
        self.stop_display = False

    # Fetches the image files from the specified folder.
    # def fetch_image_files(self):
    #     return [f for f in os.listdir(self.image_folder)]
    def fetch_image_files(self):
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
        return [f for f in os.listdir(self.image_folder) if f.lower().endswith(valid_extensions)]

    def find_today_image(self, images):
        now = datetime.now()
        formats = [
            now.strftime("%Y-%m-%d"),
            now.strftime("%m-%d"),
            now.strftime("%m%d")
        ]
        for img in images:
            for fmt in formats:
                if fmt in img:
                    return img
        return None

    # Selects a random image from the list of images.
    def select_random_image(self, images):
        # If one image or less
        if len(images) <= 1:
            return images[0]
        
        # Select a random image unless it was previously selected
        random_image = random.choice([img for img in images if img != self.last_selected_image])
        
        return random_image


    # Continuously loop to display a random image from the specified folder at the specified refresh time.
    # def display_images(self):
    #     self.stop_display = False

    #     images = self.fetch_image_files()

    #     if not images:
    #         print("No images found, displaying default image.")
    #         self.display_message('no_valid_images.jpg')
    #         return

    #     # random_image = self.select_random_image(images)
    #     today_image = self.find_today_image(images)
        
    #     if today_image:
    #         selected_image = today_image
    #         print(f"Displaying today's image: {selected_image}")
    #     else:
    #         selected_image = self.select_random_image(images)
    #         print(f"No image for today, using random: {selected_image}")
        
    #     self.last_selected_image = selected_image
    #     # self.last_selected_image = random_image
            
    #     # Open and display the image
    #     # with Image.open(os.path.join(self.image_folder, random_image)) as pic:
    #     #     pic = pic.rotate(self.rotation)
    #     #     self.epd.display(self.epd.getbuffer(pic))
    #     #     self.last_display_time = time.time()
    #     with Image.open(os.path.join(self.image_folder, selected_image)) as pic:
    #         pic = pic.rotate(self.rotation)
    #         self.epd.display(self.epd.getbuffer(pic))
    #         self.last_display_time = time.time()

    #     while not self.stop_display:
    #         current_time = time.time()
    #         elapsed_time = current_time - self.last_display_time
            
    #         if elapsed_time >= self.refresh_time:
    #             images = self.fetch_image_files()
    #             # random_image = self.select_random_image(images)
    #             today_image = self.find_today_image(images)
                
    #             if today_image:
    #                 selected_image = today_image
    #             else:
    #                 selected_image = self.select_random_image(images)
    #             self.last_selected_image = selected_image
    #             # self.last_selected_image = random_image

    #             # Open and display the image
    #             with Image.open(os.path.join(self.image_folder, selected_image)) as pic:
    #                 print(f"Displaying new image: {selected_image}")
    #                 pic = pic.rotate(self.rotation)
    #                 self.epd.display(self.epd.getbuffer(pic))
    #                 self.last_display_time = time.time()
    def display_images(self):
        self.stop_display = False
        # Track the last date we performed a midnight refresh to avoid 
        # refreshing multiple times during the 00:00 minute.
        last_midnight_date = None

        # Perform the initial display immediately on start
        self.refresh_logic()

        while not self.stop_display:
            now = datetime.now()
            
            # 1. Midnight Trigger
            # Check if it is currently the 00:00 hour/minute and 
            # if we haven't already done the midnight refresh for today.
            # if now.hour == 0 and now.minute == 0 and last_midnight_date != now.date():
            # TEST TIME
            if now.hour == 17 and now.minute == 15 and last_midnight_date != now.date():
                print(f"Midnight reached ({now.strftime('%Y-%m-%d %H:%M:%S')}). Refreshing...")
                self.refresh_logic()
                last_midnight_date = now.date()

            # 2. Regular Interval Trigger
            current_time = time.time()
            elapsed_time = current_time - self.last_display_time
            
            if elapsed_time >= self.refresh_time:
                print(f"Refresh interval reached. Updating display...")
                self.refresh_logic()

            # Sleep for a short period (e.g., 30 seconds) so the loop 
            # doesn't max out your Raspberry Pi Zero's CPU.
            time.sleep(30)

    def refresh_logic(self):
        """Helper method to handle the actual image selection and drawing."""
        images = self.fetch_image_files()

        if not images:
            print("No images found, displaying default image.")
            self.display_message('no_valid_images.jpg')
            return

        today_image = self.find_today_image(images)
        
        if today_image:
            selected_image = today_image
            print(f"Displaying today's image: {selected_image}")
        else:
            selected_image = self.select_random_image(images)
            print(f"No image for today, using random: {selected_image}")
        
        self.last_selected_image = selected_image
            
        with Image.open(os.path.join(self.image_folder, selected_image)) as pic:
            pic = pic.rotate(self.rotation)
            self.epd.display(self.epd.getbuffer(pic))
            self.last_display_time = time.time()
    

    def display_message(self, message_file):
        with Image.open(os.path.join(SCRIPT_DIR, f"messages/{message_file}")) as img_start:
                img_start = img_start.rotate(self.rotation)
                self.epd.display(self.epd.getbuffer(img_start))

