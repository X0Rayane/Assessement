import os
import colorsys
from PIL import Image

class Badge:
    def __init__(self, img_path, username=None):
        self.img = Image.open(img_path) #Open the image
        self.img_path = img_path
        self.username = username

    def verify_badge(self)  -> bool:
        """Verifies if a given image is a valid badge.
        Returns:
            True if the image is a valid badge, False otherwise.
            With the message expliciting why it's False.
        Raises:
            OSError: If there's an error opening or reading the file.
        """
        #Check the badge size
        if (self.img.width != 512 or self.img.height != 512):
            return False, 'Badge have invalid size (Should be 512x512)'
        
        if not self.is_happy_badge():
            return False, "Badge contains unhappy colors"

        #Check non transparent pixels within a circle
        for x in range(self.img.width):
            for y in range(self.img.height):
                if (x - 256) ** 2 + (y - 256) ** 2 >= 256 ** 2: #Check pixels Outside of the circle
                    if self.img.getpixel((x,y))[3] != 0: #Pixel should be transparent
                        return False, "Found Non-Transparent pixel outside of the circle"
        
        return True, 'Badge is Valid'

    def is_happy_badge(self) -> bool:
        """
        Checks if the badge contains a sufficient percentage of "happy" colors.
        Returns:
            bool: True if the percentage of "happy" colors is above 75%, False otherwise.
        """
        total_pixels = 0
        happy_pixels = 0
        for x in range(self.img.width):
            for y in range(self.img.height):
                pixel = self.img.getpixel((x, y))

                if pixel[3]==0: #If pixel is transparent we skip him
                    continue

                total_pixels += 1

                hue_ranges = [
                    (0.0, 0.3),   #yellow and green (is modular)
                    (0.35, 1.0),  #red, orange and purple (is modular)
                    (0.25, 0.5),  #blue (is modular)
                    ]
                
                #Convert to HSL and extract relevant values
                h, s, l = colorsys.rgb_to_hls(pixel[0] / 255, pixel[1] / 255, pixel[2] / 255)

                #A tiny filter to see if it fits the happy colors and brightness 
                is_happy = False
                for hue_range in hue_ranges:
                    if l > 0.7 and s > 0.2 and hue_range[0] <= h <= hue_range[1]: #brightness, saturation and Hue (is modular)
                        is_happy = True
                        break

                if is_happy:
                    happy_pixels += 1

        happy_percent = (happy_pixels / total_pixels) * 100
        return happy_percent >= 75  #You can modify the percentage of happy pixels

    def convert_img(self):
        """
        Converts an image to an image who respect the validation of badge except the happy color validation,
        Then it saves this new Image and give its path.
        Returns:
            None, it changes the PIL Image object directly. 
        Raises:
            Exception: If the image is already valid
        """
        if not self.verify_badge()[0]: #If it doesn't pass verification
            badge = Image.new("RGBA", (512, 512), (255, 255, 255, 0)) #Create new image with transparant background
            
            if (self.img.width, self.img.height) != (512,512): #Check if the image have the correct size
                self.img.thumbnail((512, 512)) #Resizing the original image to 512x512
            else:
                self.resize_to_fit_circle() 

            #Calculating coordinates to center the image in the badge
            x_offset = (512 - self.img.width) // 2
            y_offset = (512 - self.img.height) // 2
            badge.paste(self.img, (x_offset, y_offset)) #Copying resized image into the circular part of the badge
            new_path=self.new_img_path("resized_")
            badge.save(new_path) #Save the badge as new .png file
            print(f"Badge saved as {new_path}")
            self.img = badge

        else:
            raise Exception("Image already valid")

    #Function that returns a new path to save the converted image
    def new_img_path(self, identifyer)  -> str:
        """
        Changes the path name of an image after being resized.
        Args:
            identifyer (str): A string to add at the beginning of the filename.
        Returns:
            A string with the new path.
        """
        directory, filename = os.path.split(self.img_path) #Extract the directory and file name from the image path
        resized_filename = identifyer + filename #Create the new file name for the resized image
        new_img_path = os.path.join(directory, resized_filename) #Join the directory path and the new file name
        
        return new_img_path

    def resize_to_fit_circle(self):
        """
        Resize an image by calling the appropriate function to do so.
        This is done by comparing the aspect ratio of the original image to the desired aspect ratio.
        Returns:
            None, it changes the PIL Image object directly.
        """
        center_x, center_y = self.img.width // 2, self.img.height // 2 #Find the center coordinates of the image
        max_radius = min(center_x, center_y) #Find the maximum radius that fits within the circle

        # Iterate over the image pixels
        for x in range(self.img.width):
            for y in range(self.img.height):
                #Check if the pixel is outside the circle and non-transparent
                if (x - center_x) ** 2 + (y - center_y) ** 2 > max_radius ** 2 or self.img.getpixel((x, y))[3] != 0:

                    scaling_factor = max_radius / ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5 #Calculate the scaling factor to fit the pixel inside the circle

                    max_radius = int(((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5) #Update the maximum radius based on the current pixel

                    self.img = self.img.resize((int(self.img.width * scaling_factor), int(self.img.height * scaling_factor))) #Resize the image with the new scaling factor
                    
                    center_x, center_y = self.img.width // 2, self.img.height // 2 #Update the center coordinates based on the resized image
                    break
            else:
                continue
            break

    def get_badge(self):
        """
        Show the badge to the user.
        Returns:
            None
        """
        self.img.show()