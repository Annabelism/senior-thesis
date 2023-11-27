import sys
import time
import random
import signal

from generator_components import (set_chrome_options, setup_webdriver, fake_human_scrolling, capture_screenshots, test_disabling_popup, timeout_handler)

def main():
    try:
        # Set up the timeout using signal
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(300)  # Set the alarm for 300 seconds (5 minutes)

        chrome_options = set_chrome_options()
        driver = setup_webdriver(chrome_options, 1500, 850)
        url, site_name = sys.argv[1], sys.argv[2]

        driver.get(url)
        time.sleep(random.uniform(10, 15))
        test_disabling_popup(driver, url)
        fake_human_scrolling(driver, 5)
        capture_screenshots(driver, site_name) 

        driver.quit()

    except Exception as e:
        print(f"An error occurred: {e}")
        # Perform any necessary cleanup here
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()
