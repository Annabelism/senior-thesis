from selenium import webdriver
import time
import random
from PIL import ImageChops, Image
import os

EXTENSION_PATH = "ublock.crx"

def find_sticky_height(image1, image2, position='top'):
    width, height = image1.size
    sticky_height = 0
    image1 = image1.convert('RGB')
    image2 = image2.convert('RGB') 

    diff = ImageChops.difference(image1, image2).load()

    if position == "bottom":
        for y in range(height - 1, -1, -1):  # Start from the bottom row and go upwards
            is_black_row = True
            for x in range(width):
                if diff[x, y] != (0, 0, 0):  # Check if the pixel is not black
                    is_black_row = False
                    break  # Break out of the inner loop as soon as a non-black pixel is found
            if not is_black_row:
                break  # Break out of the outer loop if this row is not entirely black
            sticky_height += 1  # Increment the count if the entire row is black
        return sticky_height
    elif position == "top":
        for y in range(height):
            is_black_row = True
            for x in range(width):
                if diff[x, y] != (0, 0, 0): 
                    is_black_row = False
                    break  
            if not is_black_row:
                break  
            sticky_height += 1 
        return sticky_height

def get_sticky_height(driver, blockerOn):
    device_pixel_ratio = driver.execute_script("return window.devicePixelRatio") # Adjust pixel ratio by device
    driver.execute_script("window.scrollBy(0, 300);")  # Scroll by an arbitrary amount
    if blockerOn:
        driver.save_screenshot('no_ad_temp1.png')
        image1 = Image.open('no_ad_temp1.png')
    else:
        driver.save_screenshot('temp1.png')
        image1 = Image.open('temp1.png')

    # Scroll a little to take another screenshot
    driver.execute_script("window.scrollBy(0, 500);")  # Scroll by an arbitrary amount
    time.sleep(1)  # Wait for the scroll to complete
    if blockerOn:
        driver.save_screenshot('no_ad_temp2.png')
        image2 = Image.open('no_ad_temp2.png')
    else:
        driver.save_screenshot('temp2.png')
        image2 = Image.open('temp2.png')

    # Find sticky header height
    sticky_header_height = find_sticky_height(image1, image2, position='top')

    # Find sticky footer height
    sticky_footer_height = find_sticky_height(image1, image2, position='bottom')

    return (sticky_header_height + sticky_footer_height)/device_pixel_ratio



def set_chrome_options(blockerOn=False):        
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    if blockerOn:
        chrome_options.add_extension(EXTENSION_PATH)
    return chrome_options


def set_viewport_size(driver, width, height):
    driver.set_window_size(width, height)
    actual_viewport_width = driver.execute_script("return window.innerWidth")
    actual_viewport_height = driver.execute_script("return window.innerHeight")
    width_diff = width - actual_viewport_width
    height_diff = height - actual_viewport_height
    driver.set_window_size(width + width_diff, height + height_diff)


def setup_webdriver(options, width, height):
    driver = webdriver.Chrome(options=options)
    set_viewport_size(driver, width, height)
    return driver


def fake_human_scrolling(driver, scroll_time):
    end_time = time.time() + scroll_time
    while time.time() < end_time:
        scroll_direction = random.choice(["up", "down"])  # Random scroll direction
        if scroll_direction == "up":
            driver.execute_script(f"window.scrollBy(0, 500);")
        else:
            driver.execute_script(f"window.scrollBy(0, 500);")
        time.sleep(random.uniform(0.5, 1.5))  # Random sleep time between 0.5 and 1.5 seconds
    driver.execute_script("window.scrollTo(0, 0);")  # Return to the top of the page


def capture_screenshots(driver, site_name, blockerOn=False):
    screenshot_index = 1
    viewport_height = driver.execute_script("return window.innerHeight")
    total_height = driver.execute_script("return document.body.scrollHeight")
    scroll_position = 0
    sticky_height = get_sticky_height(driver, blockerOn)
    
    while scroll_position < total_height:
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(2)  # Ensuring content loads
        if blockerOn:
            driver.save_screenshot(f"screenshots/no_ad_{site_name}_{screenshot_index}.png")
        else:
            driver.save_screenshot(f"screenshots/{site_name}_{screenshot_index}.png")
        screenshot_index += 1
        scroll_position += viewport_height - sticky_height

def test_disabling_popup(driver, url):
    initial_scroll_position = driver.execute_script("return window.pageYOffset;")
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(1)  
    new_scroll_position = driver.execute_script("return window.pageYOffset;")
    if new_scroll_position <= initial_scroll_position:
        with open("mal_data.py", 'a') as file:
            file.write(f"{url}\n")
        driver.quit()

def timeout_handler(signum, frame):
    raise Exception("Timeout occurred")