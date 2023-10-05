import imageio
import base64
import os
import json
from .scraper import Scraper

class ImageProcessor:
    @staticmethod
    def split_image(image_path):
        # Load the image with numpy and imageio
        img = imageio.imread(image_path)
        h, w, _ = img.shape
        
        # Split the image into 4 equal sections
        top_left = img[:h//2, :w//2]
        top_right = img[:h//2, w//2:]
        bottom_left = img[h//2:, :w//2]
        bottom_right = img[h//2:, w//2:]
        
        return [top_left, top_right, bottom_left, bottom_right]
    
    @staticmethod
    def save_and_encode(images):
        paths = []
        encoded_list = []
        
        # Convert each numpy image to .jpg and encode to base64
        for i, img in enumerate(images):
            temp_path = f'images/temp_img_{i}.jpg'
            paths.append(temp_path)
            imageio.imwrite(temp_path, img)
            
            with open(temp_path, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
                encoded_list.append(encoded)
                
        return encoded_list, paths
    
    @staticmethod
    def clean_up(paths, original_image):
        for path in paths:
            os.remove(path)
        os.remove(original_image)
    
    def process_image(self, prompt, channel_url, scraper):
        save_path = scraper.run(prompt, channel_url)
        sections = self.split_image(save_path)
        encoded_list, temp_paths = self.save_and_encode(sections)
        
        # Create JSON object
        json_obj = json.dumps({
            'top_left': encoded_list[0],
            'top_right': encoded_list[1],
            'bottom_left': encoded_list[2],
            'bottom_right': encoded_list[3]
        })
        
        self.clean_up(temp_paths, save_path)
        
        return json_obj

if __name__ == "__main__":
    channel_url = 'https://discord.com/channels/1109938733857390624/1109938734532657234'
    prompt = 'An image of a beutiful turkish cat.'
    
    processor = ImageProcessor()
    scraper = Scraper()
    json_obj = processor.process_image(prompt=prompt, channel_url=channel_url, scraper=scraper)
    print(json_obj)

