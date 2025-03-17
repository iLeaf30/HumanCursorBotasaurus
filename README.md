# HumanCursor-Botasaurus

A fork of [HumanCursor](https://github.com/zajcikk/HumanCursor) that uses [Botasaurus](https://github.com/omkarcloud/botasaurus) driver for human-like mouse movements.

## Description

HumanCursor-Botasaurus is a Python library that enables human-like mouse movements in web automation using the Botasaurus driver. It's designed to help you create more natural and less detectable web automation by simulating human-like cursor movements, clicks, and interactions.

This library is a fork of the original HumanCursor project, adapted to work with Botasaurus driver instead of Selenium.

## Features

- Human-like mouse movements using Bezier curves
- Randomized movement patterns to avoid detection
- Support for clicking, dragging, and scrolling with human-like behavior
- Easy integration with Botasaurus driver
- Customizable movement parameters

## Installation

```bash
pip install humancursor-botasaurus
```

## Usage

### Basic Example

```python
from botasaurus_driver import Driver
from humancursor_botasaurus import WebCursor

# Initialize Botasaurus driver
driver = Driver(headless=False)

# Navigate to a website
driver.get("https://www.example.com")

# Initialize HumanCursor
cursor = WebCursor(driver)

# Find an element
button = driver.select("button.login")

# Move to the element and click it with human-like movement
cursor.click_on(button)

# Close the driver
driver.close()
```

### Advanced Usage

```python
from botasaurus_driver import Driver
from humancursor_botasaurus import WebCursor

# Initialize Botasaurus driver
driver = Driver(headless=False)

# Navigate to a website
driver.get("https://www.example.com")

# Initialize HumanCursor
cursor = WebCursor(driver)

# Show the cursor (adds a red dot to visualize movements)
cursor.show_cursor()

# Find elements
input_field = driver.select("input[name='username']")
login_button = driver.select("button.login")

# Move to the input field with human-like movement and click
cursor.click_on(input_field)

# Type something (using Botasaurus's type method)
driver.type("input[name='username']", "example_user")

# Find password field and click on it
password_field = driver.select("input[name='password']")
cursor.click_on(password_field)

# Type password
driver.type("input[name='password']", "example_password")

# Move to login button and click
cursor.click_on(login_button)

# Close the driver
driver.close()
```

### Drag and Drop Example

```python
from botasaurus_driver import Driver
from humancursor_botasaurus import WebCursor

# Initialize Botasaurus driver
driver = Driver(headless=False)

# Navigate to a website
driver.get("https://www.example.com/drag-and-drop")

# Initialize HumanCursor
cursor = WebCursor(driver)

# Find elements
drag_element = driver.select("#draggable")
drop_target = driver.select("#droppable")

# Perform drag and drop with human-like movement
cursor.drag_and_drop(drag_element, drop_target)

# Close the driver
driver.close()
```

## Credits

- Original [HumanCursor](https://github.com/zajcikk/HumanCursor) project by [zajcikk](https://github.com/zajcikk)
- [Botasaurus](https://github.com/omkarcloud/botasaurus) by [omkarcloud](https://github.com/omkarcloud)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Donate

If you would like to support this project, please consider buying me a coffee:

[Buy Me A Coffee](https://buymeacoffee.com/ileaf)

<a href="https://buymeacoffee.com/ileaf"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&amp;emoji=&amp;slug=ileaf&amp;button_colour=FFDD00&amp;font_colour=000000&amp;font_family=Poppins&amp;outline_colour=000000&amp;coffee_colour=ffffff" alt="Buy Me A Coffee" style="height: 45px;"></a> 