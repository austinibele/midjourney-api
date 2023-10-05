import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import requests
import traceback
from bs4 import BeautifulSoup
import re
import random
import dotenv
import os
import uuid
dotenv.load_dotenv()

# Set chrome options for headless browsing
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/google-chrome-stable"
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--headless")


class Scraper:
    def init_driver(self):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"browser": "ALL"}
        webdriver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options) #, desired_capabilities=capabilities)
        return driver
   
    def scrape(self, driver, channel_url, prompt):
        try:
            email_input_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/input"))
            )
        except:
            email_input_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/form/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/input"))
            )
        print('Found email input element')    
        
        try:
            password_input_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[2]/div/input"))
            ) 
        except:
            password_input_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/form/div[2]/div/div[1]/div[2]/div[2]/div/input"))
            ) 
        print('Found password input element')
        
        time.sleep((0.5+random.random()*2)*2)
        # Enter 'email' into the email field
        email_input_element.send_keys(os.environ['discord_email'])
        time.sleep((0.5+random.random()*2)*3)
        # Enter 'password' into the password field
        password_input_element.send_keys(os.environ['discord_password'])
        time.sleep(1+random.random()*2)
        
        try:
            submit_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]'))
            )
        except:
            submit_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]'))
            )
        time.sleep((0.5+random.random()*2)*2)
        submit_button.click()
        time.sleep((0.5+random.random()*2)*4)
        # Wait for next page to load
        WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]'))
            ) 
        print('Logged in')
        
        driver.get(channel_url)

        prompt_input_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[1]/div/div[3]/div/div[2]"))
            )
    
        time.sleep((0.5+random.random()*2)*2)
        # Enter 'email' into the email field
        prompt_input_element.send_keys('/imagine')
        time.sleep((0.5+random.random()*2)*2)
        prompt_input_element.send_keys(Keys.RETURN)
        time.sleep((0.5+random.random()*2)*6)
        prompt_input_element.send_keys(prompt)
        time.sleep((0.5+random.random()*2)*3)
       
        # Send the "Enter" key
        prompt_input_element.send_keys(Keys.RETURN)
        print('Prompt sent')
        time.sleep(80)  # Wait for image to generate
        driver.get(channel_url) 
        time.sleep(10)  # Wait to load
        
        # Use regex to find all URLs starting with 'https://cdn.discordapp.com/attachments/'
        pattern = r'https://cdn\.discordapp\.com/attachments/[\S]+'
        image_urls = re.findall(pattern, str(BeautifulSoup(driver.page_source, 'html.parser')))
        new_image_url = image_urls[-1].split('.png')[0] + '.png'
        
        print('Downloading Image')
        # Download the new image and save it to the 'images' folder.
        img_data = requests.get(new_image_url).content
        save_path = f'images/{uuid.uuid1()}'
        with open(save_path, 'wb') as handler:
            handler.write(img_data)
        
        return save_path
    
    def run(self, prompt, channel_url='https://discord.com/channels/1109938733857390624/1109938734532657234'):
        print('Attempting to initialize driver')
        driver = self.init_driver()
        print('Driver initialized')
        driver.get(channel_url)
        print('Driver navigated to channel url')
        print('Scraping image')
        try:
            save_path = self.scrape(driver, channel_url, prompt)
        except Exception as e:
            print('Exception Encountered: ', e)
            traceback.print_exc()
            print('**********')
            print('**********')
            print('**********')
            print('DRIVER LOGS: ')
            for entry in driver.get_log("browser"):
                print(entry)
            driver.quit()
            raise Exception('Failed to scrape image')
        print('Image scraped')
        return save_path
    
if __name__ == "__main__":
    scraper = Scraper()
    wait_times = scraper.run()
