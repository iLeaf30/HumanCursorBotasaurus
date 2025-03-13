import time
import random
from botasaurus_driver import Driver
from humancursor_botasaurus import WebCursor
import math


def main():
    # Initialize Botasaurus driver with basic settings
    driver = Driver(
        headless=False,
        block_images=False,
        lang="en-US",
        window_size=(1920, 1080)
    )

    try:
        # Navigate to the website
        driver.get("https://www.browserscan.net/bot-detection")
        time.sleep(3)  # wait for page to load

        # Initialize WebCursor and show the cursor for visualization
        cursor = WebCursor(driver)
        cursor.show_cursor()

        # Get window dimensions
        window_size = driver.run_js("""
            return {
                width: window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth,
                height: window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
            };
        """, [])
        width = window_size.get("width", 1920)
        height = window_size.get("height", 1080)

        # Move mouse in a circular path on the page
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 3  # use a third of the smaller dimension as radius
        steps = 40
        for i in range(steps):
            angle = (2 * math.pi * i) / steps
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            print(f"Moving mouse to: ({x}, {y})")
            cursor.move_by_offset(x, y)
            time.sleep(0.2)

        time.sleep(5)  # Pause to observe movements
    except Exception as ex:
        print(f"An error occurred: {ex}")
    finally:
        driver.close()


if __name__ == "__main__":
    main() 