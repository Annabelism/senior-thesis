from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from data_cleaning import MBFC_DATA

def set_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
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


def find_href(driver):
    elements = driver.find_elements(By.TAG_NAME, "a")
    
    href = []
    for element in elements:
        t = element.get_attribute('href')
        print(t)
    return href


def main():
    # Set up web driver
    chrome_options = set_chrome_options()
    driver = setup_webdriver(chrome_options, 1500, 850)
    
    driver.get("https://www.cnn.com")
    find_href(driver)
    time.sleep(random.uniform(10, 20))  # Wait 10-20 seconds


    # Close browser
    driver.quit()


if __name__ == "__main__":
    main()