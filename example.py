from botasaurus_driver import Driver
from humancursor_botasaurus import WebCursor
import time

def main():
    # Initialize Botasaurus driver
    driver = Driver(headless=False)
    
    try:
        # Navigate to a website
        driver.get("https://www.google.com")
        
        # Initialize HumanCursor
        cursor = WebCursor(driver)
        
        # Show the cursor (adds a red dot to visualize movements)
        cursor.show_cursor()
        
        # Find the search input
        search_input = driver.select("input[name='q']")
        
        # Move to the search input with human-like movement and click
        cursor.click_on(search_input)
        
        # Type something
        driver.type("input[name='q']", "human cursor botasaurus")
        
        # Find the search button
        search_button = driver.select("input[name='btnK']")
        
        # Move to the search button and click
        cursor.click_on(search_button)
        
        # Wait for results to load
        time.sleep(2)
        
        # Find a result link
        result_link = driver.select("h3", wait=5)
        
        # Move to the result link and click
        cursor.click_on(result_link)
        
        # Wait to see the result
        time.sleep(5)
        
    finally:
        # Close the driver
        driver.close()

if __name__ == "__main__":
    main() 