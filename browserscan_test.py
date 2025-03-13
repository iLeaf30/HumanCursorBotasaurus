import time
import random
from botasaurus_driver import Driver
from humancursor_botasaurus import WebCursor

def random_sleep(min_time=0.5, max_time=2.0):
    """Sleep for a random amount of time to mimic human behavior"""
    time.sleep(random.uniform(min_time, max_time))

def main():
    # Initialize Botasaurus driver with anti-detection settings
    driver = Driver(
        headless=False,
        block_images=False,
        lang="en-US",
        window_size=(1920, 1080)
    )
    
    try:
        # Navigate to the BrowserScan bot detection website
        driver.get("https://www.browserscan.net/bot-detection")
        random_sleep(2.0, 3.0)  # Wait for page to fully load
        
        # Initialize HumanCursor
        cursor = WebCursor(driver)
        
        # Show the cursor for visualization
        cursor.show_cursor()
        
        # First, let's move to a random point on the page to initialize
        window_size = driver.run_js("""
            return {
                width: window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth,
                height: window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
            };
        """)
        
        # Move to a random initial position
        initial_x = random.randint(100, window_size["width"] - 200)
        initial_y = random.randint(100, 300)  # Upper part of the page
        cursor.move_by_offset(initial_x, initial_y)
        random_sleep()
        
        # Find and interact with the main sections on the page
        sections = driver.select_all("h3, h2, h1")
        
        # Move to and hover over different sections
        for section in sections[:min(5, len(sections))]:
            cursor.move_to(section)
            random_sleep()
        
        # Find some links to interact with
        links = driver.select_all("a")
        random_links = random.sample(links, min(3, len(links)))
        
        for link in random_links:
            # Move to the link with human-like movement
            cursor.move_to(link)
            random_sleep()
            
            # Don't click, just hover to avoid navigating away
        
        # Find the test results section
        test_results = driver.select_all("div", contains_text="Test Results")
        if test_results:
            cursor.move_to(test_results[0])
            random_sleep(1.0, 2.0)
        
        # Scroll down slowly to view more content
        for i in range(3):
            scroll_amount = random.randint(300, 500)
            driver.run_js(f"window.scrollBy(0, {scroll_amount});")
            random_sleep()
            
            # Move the cursor to follow the scroll
            cursor.move_by_offset(
                random.randint(-100, 100),
                scroll_amount - random.randint(0, 100)
            )
            random_sleep()
        
        # Find some buttons or interactive elements
        buttons = driver.select_all("button")
        if buttons:
            # Choose a random button to hover over
            random_button = random.choice(buttons)
            cursor.move_to(random_button)
            random_sleep(1.0, 2.0)
        
        # Move to a random position again
        cursor.move_by_offset(
            random.randint(-200, 200),
            random.randint(-100, 100)
        )
        random_sleep()
        
        # Scroll back up slowly
        for i in range(2):
            scroll_amount = random.randint(-400, -200)
            driver.run_js(f"window.scrollBy(0, {scroll_amount});")
            random_sleep()
            
            # Move the cursor to follow the scroll
            cursor.move_by_offset(
                random.randint(-100, 100),
                scroll_amount + random.randint(0, 100)
            )
            random_sleep()
        
        # Find the bot detection section specifically
        bot_detection_sections = driver.select_all("h2, h3", contains_text="Bot Detection")
        if bot_detection_sections:
            cursor.move_to(bot_detection_sections[0])
            random_sleep(1.0, 2.0)
            
            # Find nearby paragraphs to read
            paragraphs = driver.select_all("p")
            for p in paragraphs[:min(3, len(paragraphs))]:
                cursor.move_to(p)
                random_sleep(1.5, 3.0)  # Longer pause as if reading
        
        # Wait on the page to see the results
        print("Waiting on page to observe bot detection results...")
        time.sleep(10)
        
        # Take a screenshot of the results
        driver.save_screenshot("bot_detection_results.png")
        print("Screenshot saved as 'bot_detection_results.png'")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the driver
        driver.close()

if __name__ == "__main__":
    main() 