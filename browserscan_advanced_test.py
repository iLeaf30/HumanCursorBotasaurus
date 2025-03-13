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
        window_size="1920,1080",
        # Additional options to avoid detection
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    )
    
    try:
        # Navigate to the BrowserScan bot detection website
        driver.get("https://www.browserscan.net/bot-detection")
        random_sleep(3.0, 5.0)  # Wait for page to fully load
        
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
        
        # ===== MOUSE MOVEMENT TEST =====
        # Find the mouse movement test section
        mouse_test_sections = driver.select_all("h2, h3", contains_text="Mouse Movement")
        if mouse_test_sections:
            # Move to the mouse movement section
            cursor.move_to(mouse_test_sections[0])
            random_sleep(1.0, 2.0)
            
            # Perform random mouse movements across the page
            for _ in range(5):
                # Generate random target coordinates
                target_x = random.randint(100, window_size["width"] - 200)
                target_y = random.randint(100, window_size["height"] - 200)
                
                # Move to the random position with human-like curve
                cursor.move_by_offset(target_x - cursor.origin_coordinates[0], 
                                     target_y - cursor.origin_coordinates[1])
                random_sleep(0.8, 1.5)
        
        # ===== SCROLL BEHAVIOR TEST =====
        # Scroll down slowly with natural pauses
        for i in range(4):
            # Random scroll amount
            scroll_amount = random.randint(200, 400)
            
            # Scroll with smooth behavior
            driver.run_js(f"""
                window.scrollBy({{
                    top: {scroll_amount},
                    left: 0,
                    behavior: 'smooth'
                }});
            """)
            
            # Move cursor slightly while scrolling to mimic human behavior
            cursor.move_by_offset(
                random.randint(-50, 50),
                random.randint(50, 150)
            )
            
            random_sleep(1.0, 2.5)
        
        # ===== INTERACTION WITH PAGE ELEMENTS =====
        # Find interactive elements like buttons or links
        interactive_elements = driver.select_all("button, a.btn, .interactive")
        
        if interactive_elements:
            # Select a few random elements to interact with
            elements_to_interact = random.sample(
                interactive_elements, 
                min(3, len(interactive_elements))
            )
            
            for element in elements_to_interact:
                # Move to the element with human-like movement
                cursor.move_to(element)
                random_sleep(0.7, 1.5)
                
                # Hover for a bit
                random_sleep(0.5, 1.2)
                
                # Click on some elements (but avoid links that navigate away)
                if element.tag_name.lower() == "button":
                    cursor.click_on(element)
                    random_sleep(1.0, 2.0)
        
        # ===== TEXT SELECTION TEST =====
        # Find paragraphs to potentially select text from
        paragraphs = driver.select_all("p")
        
        if paragraphs and len(paragraphs) > 2:
            # Choose a random paragraph
            paragraph = random.choice(paragraphs)
            
            # Move to the paragraph
            cursor.move_to(paragraph)
            random_sleep(0.8, 1.5)
            
            # Get paragraph position and dimensions
            rect = paragraph.get_bounding_rect()
            
            # Simulate text selection by dragging
            start_x = rect["x"] + rect["width"] * 0.2
            start_y = rect["y"] + rect["height"] * 0.5
            end_x = rect["x"] + rect["width"] * 0.8
            end_y = rect["y"] + rect["height"] * 0.5
            
            # Move to start position
            cursor.move_to([start_x, start_y], absolute_offset=True)
            random_sleep(0.5, 1.0)
            
            # Perform drag operation to select text
            cursor.drag_and_drop(
                [start_x, start_y],
                [end_x, end_y],
                steady=True
            )
            
            random_sleep(1.5, 3.0)
            
            # Click somewhere else to deselect
            cursor.move_by_offset(
                random.randint(100, 200),
                random.randint(50, 100)
            )
            cursor.click()
            random_sleep(1.0, 2.0)
        
        # ===== FORM INTERACTION TEST =====
        # Find form elements like inputs
        input_elements = driver.select_all("input[type='text'], input:not([type])")
        
        if input_elements:
            # Choose a random input
            input_element = random.choice(input_elements)
            
            # Move to the input
            cursor.move_to(input_element)
            random_sleep(0.8, 1.5)
            
            # Click on the input
            cursor.click_on(input_element)
            random_sleep(0.5, 1.0)
            
            # Type some text with human-like timing
            human_text = "This is a human typing test"
            for char in human_text:
                # Type character by character with variable timing
                driver.run_js(f"""
                    document.activeElement.value += '{char}';
                    document.activeElement.dispatchEvent(new Event('input', {{ bubbles: true }}));
                """)
                # Random delay between keystrokes
                random_sleep(0.05, 0.25)
            
            random_sleep(1.0, 2.0)
        
        # ===== FINAL CHECKS =====
        # Scroll back to top
        driver.run_js("window.scrollTo({ top: 0, behavior: 'smooth' });")
        random_sleep(1.5, 2.5)
        
        # Look for test result sections
        result_sections = driver.select_all("div.result, .test-result, div[id*='result']")
        
        if result_sections:
            for result in result_sections[:min(3, len(result_sections))]:
                # Move to each result section
                cursor.move_to(result)
                random_sleep(1.0, 2.5)  # Pause as if reading the results
        
        # Wait on the page to see the final results
        print("Waiting on page to observe bot detection results...")
        time.sleep(10)
        
        # Take a screenshot of the results
        driver.save_screenshot("bot_detection_advanced_results.png")
        print("Screenshot saved as 'bot_detection_advanced_results.png'")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the driver
        driver.close()

if __name__ == "__main__":
    main() 