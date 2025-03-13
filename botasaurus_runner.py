import time
import random
from botasaurus_driver import Driver, cdp
from humancursor_botasaurus import WebCursor


def random_sleep(min_time=0.5, max_time=2.0):
    """Sleep for a random amount of time to mimic human behavior"""
    time.sleep(random.uniform(min_time, max_time))


def cdp_mouse_click(driver, x, y):
    """Simulate a mouse click using CDP commands"""
    # Move mouse to the position
    driver.run_cdp_command(cdp.input_.dispatch_mouse_event("mouseMoved", x=x, y=y))
    random_sleep(0.1, 0.2)
    # Press the mouse button
    driver.run_cdp_command(cdp.input_.dispatch_mouse_event(
        "mousePressed",
        x=x,
        y=y,
        button=cdp.input_.MouseButton.LEFT,
        click_count=1
    ))
    random_sleep(0.1, 0.2)
    # Release the mouse button
    driver.run_cdp_command(cdp.input_.dispatch_mouse_event(
        "mouseReleased",
        x=x,
        y=y,
        button=cdp.input_.MouseButton.LEFT,
        click_count=1
    ))


def cdp_mouse_move(driver, x, y):
    """Simulate a mouse movement using CDP commands"""
    driver.run_cdp_command(cdp.input_.dispatch_mouse_event("mouseMoved", x=x, y=y))


def simulate_cursor_movements(driver, moves=5, steps=15):
    """Simulate human-like cursor movements by interpolating between positions"""
    # Assume an initial position on the page
    current_x, current_y = 300, 300
    for i in range(moves):
        # Determine a random target position within given bounds
        target_x = random.randint(100, 600)
        target_y = random.randint(100, 600)
        print(f"Moving cursor from: ({current_x}, {current_y}) to: ({target_x}, {target_y})")
        # Smoothly interpolate between the current and target positions
        for step in range(1, steps + 1):
            interp_x = current_x + (target_x - current_x) * (step / steps)
            interp_y = current_y + (target_y - current_y) * (step / steps)
            cdp_mouse_move(driver, int(interp_x), int(interp_y))
            time.sleep(0.1)  # increased delay for slower, more human-like movement
        current_x, current_y = target_x, target_y
        random_sleep(0.2, 0.5)


def click_checkbox(driver):
    """Simulate clicking on a checkbox element using CDP commands, targeting #uATa8 > div > label > input[type=checkbox]"""
    # Retrieve the bounding box of the checkbox element safely using the new selector
    rect = driver.run_js("var el = document.querySelector('#uATa8 > div > label > input[type=checkbox]'); if(el){ return el.getBoundingClientRect(); } else { return null; }")
    if rect is None:
        print("Checkbox element (#uATa8 > div > label > input[type=checkbox]) not found on the page.")
        return
    cx = int(rect['left'] + rect['width'] / 2)
    cy = int(rect['top'] + rect['height'] / 2)
    print(f"Clicking checkbox at: ({cx}, {cy})")
    cdp_mouse_click(driver, cx, cy)


def list_all_elements(driver):
    """List all elements found on the page (including shadow DOM)"""
    js_code = '''
    function findAllElements() {
        var elements = [];
        
        // Function to traverse a document or shadow root
        function traverse(root) {
            try {
                // Get all elements in this root
                var allElements = root.querySelectorAll('*');
                
                // Add each element to our list
                for (var i = 0; i < allElements.length; i++) {
                    var node = allElements[i];
                    var info = node.tagName;
                    if (node.id) { info += '#' + node.id; }
                    if (node.className) { info += '.' + node.className.split(' ').join('.'); }
                    elements.push(info);
                    
                    // Check for shadow root
                    if (node.shadowRoot) {
                        elements.push("--- SHADOW ROOT START ---");
                        traverse(node.shadowRoot);
                        elements.push("--- SHADOW ROOT END ---");
                    }
                }
                
                // Check for frames and iframes
                var frames = root.querySelectorAll('iframe, frame');
                for (var j = 0; j < frames.length; j++) {
                    try {
                        var frameDoc = frames[j].contentDocument;
                        if (frameDoc) {
                            elements.push("--- IFRAME START ---");
                            traverse(frameDoc);
                            elements.push("--- IFRAME END ---");
                        }
                    } catch (frameErr) {
                        elements.push("Cannot access iframe: " + frameErr.message);
                    }
                }
            } catch (err) {
                elements.push("Error traversing DOM: " + err.message);
            }
        }
        
        // Start traversal from document
        traverse(document);
        return elements;
    }
    return findAllElements();
    '''
    result = driver.run_js(js_code)
    print("Found elements in document (including shadow DOM and iframes):")
    for elem in result:
        print(elem)


def find_cloudflare_checkbox(driver):
    """Find the Cloudflare checkbox by looking for specific visual elements"""
    js_code = '''
    function findCloudflareCheckbox() {
        // Look for common Cloudflare checkbox container patterns
        var possibleCheckboxes = [];
        
        // Look for elements that might be the checkbox or its container
        var elements = document.querySelectorAll('div[class*="checkbox"], div[class*="check"], div[class*="captcha"], iframe');
        
        for (var i = 0; i < elements.length; i++) {
            var el = elements[i];
            possibleCheckboxes.push({
                tag: el.tagName,
                id: el.id,
                className: el.className,
                rect: el.getBoundingClientRect(),
                text: el.innerText || ''
            });
        }
        
        return possibleCheckboxes;
    }
    return findCloudflareCheckbox();
    '''
    result = driver.run_js(js_code)
    print("Possible Cloudflare checkbox elements:")
    for elem in result:
        print(elem)
    
    return result


def click_cloudflare_checkbox(driver):
    """Click the Cloudflare checkbox based on the exact structure from the screenshot"""
    js_code = '''
    function clickCloudflareCheckbox() {
        try {
            // First, find the iframe with the Cloudflare challenge
            const iframe = document.querySelector('iframe[src*="challenges.cloudflare.com"]');
            if (!iframe) {
                return { success: false, message: "Cloudflare iframe not found" };
            }
            
            // Try to access the iframe content
            const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
            if (!iframeDoc) {
                return { success: false, message: "Cannot access iframe content" };
            }
            
            // Find the checkbox inside the iframe
            // Based on the screenshot, we need to find the input[type="checkbox"] inside the shadow root
            let checkbox = null;
            
            // First try direct selector
            checkbox = iframeDoc.querySelector('input[type="checkbox"]');
            
            // If not found, try to find it in the shadow root
            if (!checkbox) {
                // Look for the div with id="uATa8"
                const container = iframeDoc.querySelector('#uATa8');
                if (container) {
                    // Try to find the checkbox inside this container
                    checkbox = container.querySelector('input[type="checkbox"]');
                }
            }
            
            // If still not found, try to find by class names
            if (!checkbox) {
                checkbox = iframeDoc.querySelector('.cb-l input[type="checkbox"]');
            }
            
            if (checkbox) {
                // Return the bounding box for clicking
                const rect = checkbox.getBoundingClientRect();
                // Adjust coordinates to account for iframe position
                const iframeRect = iframe.getBoundingClientRect();
                return {
                    success: true,
                    x: iframeRect.left + rect.left + (rect.width / 2),
                    y: iframeRect.top + rect.top + (rect.height / 2)
                };
            } else {
                return { success: false, message: "Checkbox not found in iframe" };
            }
        } catch (error) {
            return { success: false, message: "Error: " + error.message };
        }
    }
    return clickCloudflareCheckbox();
    '''
    
    result = driver.run_js(js_code)
    print("Cloudflare checkbox search result:", result)
    
    if result and result.get('success'):
        cx = int(result['x'])
        cy = int(result['y'])
        print(f"Clicking Cloudflare checkbox at: ({cx}, {cy})")
        cdp_mouse_click(driver, cx, cy)
        return True
    else:
        print(f"Failed to find Cloudflare checkbox: {result.get('message', 'Unknown error')}")
        return False


def click_cloudflare_checkbox_direct(driver):
    """Click the Cloudflare checkbox by targeting the div#uATa8 directly with human-like movement"""
    js_code = '''
    function clickCloudflareCheckboxDirect() {
        try {
            // Look for the div with id="uATa8" which was found in the element list
            const container = document.querySelector('#uATa8');
            if (!container) {
                return { success: false, message: "Container div#uATa8 not found" };
            }
            
            // Get the bounding box of this container
            const rect = container.getBoundingClientRect();
            
            // Return coordinates to click in the center of this container
            return {
                success: true,
                x: rect.left + (rect.width / 2),
                y: rect.top + (rect.height / 2)
            };
        } catch (error) {
            return { success: false, message: "Error: " + error.message };
        }
    }
    return clickCloudflareCheckboxDirect();
    '''
    
    result = driver.run_js(js_code)
    print("Direct Cloudflare checkbox search result:", result)
    
    if result and result.get('success'):
        cx = int(result['x'])
        cy = int(result['y'])
        
        # First, move the cursor to a position slightly above the checkbox
        hover_y = cy - 30  # 30 pixels above the checkbox
        print(f"Moving cursor above the checkbox to: ({cx}, {hover_y})")
        cdp_mouse_move(driver, cx, hover_y)
        
        # Wait a moment (human-like pause)
        print("Hovering above checkbox...")
        random_sleep(0.8, 1.2)
        
        # Now move to the checkbox itself
        print(f"Moving cursor to the checkbox at: ({cx}, {cy})")
        cdp_mouse_move(driver, cx, cy)
        
        # Pause briefly before clicking
        random_sleep(0.3, 0.7)
        
        # Finally click
        print(f"Clicking directly on Cloudflare checkbox container at: ({cx}, {cy})")
        cdp_mouse_click(driver, cx, cy)
        return True
    else:
        print(f"Failed to find Cloudflare checkbox container: {result.get('message', 'Unknown error')}")
        return False


def main():
    # Initialize Botasaurus driver with anti-detection settings
    driver = Driver(
        headless=False,
        # block_images=False,
        # lang="en-US",
        # window_size=(1920, 1080)
    )

    # Navigate to the BrowserScan bot detection website
    driver.get("https://nopecha.com/demo/cloudflare")
    
    # Wait longer for the page to fully load
    print("Waiting for page to fully load...")
    random_sleep(5.0, 7.0)  # Increased wait time
    
    # Initialize HumanCursor for visualization
    cursor = WebCursor(driver)
    cursor.show_cursor()

    # Simulate human-like cursor movements on the page
    simulate_cursor_movements(driver, moves=3, steps=10)
    
    # Wait again after movements
    print("Waiting after cursor movements...")
    random_sleep(2.0, 3.0)
    
    # Try the direct method to click on the div#uATa8 container
    if not click_cloudflare_checkbox_direct(driver):
        # If that fails, try the iframe method
        print("Direct container method failed, trying iframe method...")
        if not click_cloudflare_checkbox(driver):
            # If both methods fail, try the other methods
            print("Iframe method failed, trying alternative methods...")
            
            # List all elements found on the page
            list_all_elements(driver)
            
            # Try to find the Cloudflare checkbox using the generic method
            print("\nSearching for Cloudflare checkbox using generic method...")
            possible_checkboxes = find_cloudflare_checkbox(driver)
            
            # If we found possible checkboxes, try to click the first one
            if possible_checkboxes and len(possible_checkboxes) > 0:
                first_checkbox = possible_checkboxes[0]
                if 'rect' in first_checkbox:
                    rect = first_checkbox['rect']
                    cx = int(rect['left'] + rect['width'] / 2)
                    cy = int(rect['top'] + rect['height'] / 2)
                    print(f"Attempting to click possible checkbox at: ({cx}, {cy})")
                    cdp_mouse_click(driver, cx, cy)

    # Prompt for further interactions
    driver.prompt()


if __name__ == "__main__":
    main() 