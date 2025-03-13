from time import sleep
import random

from botasaurus_driver import Driver
from botasaurus_driver.driver import Element

from humancursor_botasaurus.utilities.web_adjuster import WebAdjuster


class WebCursor:
    def __init__(self, driver: Driver):
        """
        Initialize WebCursor with a Botasaurus driver
        
        Args:
            driver: Botasaurus Driver instance
        """
        self.__driver = driver
        self.human = WebAdjuster(self.__driver)
        self.origin_coordinates = [0, 0]

    def move_to(
            self,
            element: Element or list,
            relative_position: list = None,
            absolute_offset: bool = False,
            origin_coordinates=None,
            steady=False
    ):
        """Moves to element or coordinates with human curve"""
        if not self.scroll_into_view_of_element(element):
            return False
        if origin_coordinates is None:
            origin_coordinates = self.origin_coordinates
        self.origin_coordinates = self.human.move_to(
            element,
            origin_coordinates=origin_coordinates,
            absolute_offset=absolute_offset,
            relative_position=relative_position,
            steady=steady
        )
        return self.origin_coordinates

    def click_on(
            self,
            element: Element or list,
            number_of_clicks: int = 1,
            click_duration: float = 0,
            relative_position: list = None,
            absolute_offset: bool = False,
            origin_coordinates=None,
            steady=False
    ):
        """Moves to element or coordinates with human curve, and clicks on it a specified number of times, default is 1"""
        self.move_to(
            element,
            origin_coordinates=origin_coordinates,
            absolute_offset=absolute_offset,
            relative_position=relative_position,
            steady=steady
        )
        self.click(number_of_clicks=number_of_clicks, click_duration=click_duration)
        return True

    def click(self, number_of_clicks: int = 1, click_duration: float = 0):
        """Performs the click action"""
        for _ in range(number_of_clicks):
            if click_duration:
                # Using Botasaurus's run_js to perform click and hold
                self.__driver.run_js(f"""
                    (function() {{
                        const event = new MouseEvent('mousedown', {{
                            bubbles: true,
                            cancelable: true,
                            view: window
                        }});
                        var el = document.elementFromPoint({self.origin_coordinates[0]}, {self.origin_coordinates[1]});
                        if (el) {{
                            el.dispatchEvent(event);
                        }}
                        return null;
                    }})();
                """)
                sleep(click_duration)
                self.__driver.run_js(f"""
                    (function() {{
                        const event = new MouseEvent('mouseup', {{
                            bubbles: true,
                            cancelable: true,
                            view: window
                        }});
                        var el = document.elementFromPoint({self.origin_coordinates[0]}, {self.origin_coordinates[1]});
                        if (el) {{
                            el.dispatchEvent(event);
                        }}
                        
                        const clickEvent = new MouseEvent('click', {{
                            bubbles: true,
                            cancelable: true,
                            view: window
                        }});
                        el = document.elementFromPoint({self.origin_coordinates[0]}, {self.origin_coordinates[1]});
                        if (el) {{
                            el.dispatchEvent(clickEvent);
                        }}
                        return null;
                    }})();
                """)
            else:
                # Using Botasaurus's click_at_point method
                self.__driver.click_at_point(self.origin_coordinates[0], self.origin_coordinates[1])
        return True

    def move_by_offset(self, x: int, y: int, steady=False):
        """Moves the cursor with human curve, by specified number of x and y pixels"""
        self.origin_coordinates = self.human.move_to([x, y], absolute_offset=True, steady=steady)
        return True

    def drag_and_drop(
            self,
            drag_from_element: Element or list,
            drag_to_element: Element or list,
            drag_from_relative_position: list = None,
            drag_to_relative_position: list = None,
            steady=False
    ):
        """Moves to element or coordinates, clicks and holds, dragging it to another element, with human curve"""
        if drag_from_relative_position is None:
            self.move_to(drag_from_element)
        else:
            self.move_to(
                drag_from_element, relative_position=drag_from_relative_position
            )

        # Click and hold
        self.__driver.run_js(f"""
            (function() {{
                const event = new MouseEvent('mousedown', {{
                    bubbles: true,
                    cancelable: true,
                    view: window
                }});
                var el = document.elementFromPoint({self.origin_coordinates[0]}, {self.origin_coordinates[1]});
                if (el) {{
                    el.dispatchEvent(event);
                }}
                return null;
            }})();
        """)

        if drag_to_element is None:
            # Just click if no target element
            self.__driver.run_js(f"""
                (function() {{
                    const event = new MouseEvent('mouseup', {{
                        bubbles: true,
                        cancelable: true,
                        view: window
                    }});
                    var el = document.elementFromPoint({self.origin_coordinates[0]}, {self.origin_coordinates[1]});
                    if (el) {{
                        el.dispatchEvent(event);
                    }}
                    
                    const clickEvent = new MouseEvent('click', {{
                        bubbles: true,
                        cancelable: true,
                        view: window
                    }});
                    el = document.elementFromPoint({self.origin_coordinates[0]}, {self.origin_coordinates[1]});
                    if (el) {{
                        el.dispatchEvent(clickEvent);
                    }}
                    return null;
                }})();
            """)
        else:
            # Move to target element
            if drag_to_relative_position is None:
                self.move_to(drag_to_element, steady=steady)
            else:
                self.move_to(
                    drag_to_element, relative_position=drag_to_relative_position, steady=steady
                )
            
            # Release
            self.__driver.run_js(f"""
                (function() {{
                    const event = new MouseEvent('mouseup', {{
                        bubbles: true,
                        cancelable: true,
                        view: window
                    }});
                    var el = document.elementFromPoint({self.origin_coordinates[0]}, {self.origin_coordinates[1]});
                    if (el) {{
                        el.dispatchEvent(event);
                    }}
                    return null;
                }})();
            """)

        return True

    def control_scroll_bar(
            self,
            scroll_bar_element: Element,
            amount_by_percentage: list,
            orientation: str = "horizontal",
            steady=False
    ):
        """Adjusts any scroll bar on the webpage, by the amount you want in float number from 0 to 1
        representing percentage of fullness, orientation of the scroll bar must also be defined by user
        horizontal or vertical"""
        direction = True if orientation == "horizontal" else False

        self.move_to(scroll_bar_element)
        
        # Click and hold
        self.__driver.run_js(f"""
            (function() {{
                const event = new MouseEvent('mousedown', {{
                    bubbles: true,
                    cancelable: true,
                    view: window
                }});
                var el = document.elementFromPoint({self.origin_coordinates[0]}, {self.origin_coordinates[1]});
                if (el) {{
                    el.dispatchEvent(event);
                }}
                return null;
            }})();
        """)
        
        # Move to target position
        if direction:
            self.move_to(
                scroll_bar_element,
                relative_position=[amount_by_percentage, random.randint(0, 100) / 100],
                steady=steady
            )
        else:
            self.move_to(
                scroll_bar_element,
                relative_position=[random.randint(0, 100) / 100, amount_by_percentage],
                steady=steady
            )

        # Release
        self.__driver.run_js(f"""
            (function() {{
                const event = new MouseEvent('mouseup', {{
                    bubbles: true,
                    cancelable: true,
                    view: window
                }});
                var el = document.elementFromPoint({self.origin_coordinates[0]}, {self.origin_coordinates[1]});
                if (el) {{
                    el.dispatchEvent(event);
                }}
                return null;
            }})();
        """)

        return True

    def scroll_into_view_of_element(self, element: Element):
        """Scrolls the element into viewport, if not already in it"""
        if isinstance(element, Element):
            # Get bounding rect from the element
            rect = element.get_bounding_rect()
            if not isinstance(rect, dict):
                try:
                    rect = {"x": rect.x, "y": rect.y, "width": rect.width, "height": rect.height}
                except Exception as e:
                    print("Error converting bounding rect to dict:", e)
                    return False
            try:
                x = float(rect.get("x", 0))
                y = float(rect.get("y", 0))
                width = float(rect.get("width", 0))
                height = float(rect.get("height", 0))
            except Exception as e:
                print("Error converting rect values to float:", e)
                return False

            # Get window size via run_js
            window_size = self.__driver.run_js("return {width: window.innerWidth, height: window.innerHeight};", [])
            try:
                win_width = float(window_size.get("width", 0))
                win_height = float(window_size.get("height", 0))
            except Exception as e:
                print("Error converting window size:", e)
                return False

            # Check if the element's rect is fully within the viewport
            in_viewport = (x >= 0 and y >= 0 and (x + width) <= win_width and (y + height) <= win_height)
            if not in_viewport:
                # Scroll the window so that the element's top-left corner is visible
                self.__driver.run_js(
                    """
                    (function(x, y) {
                        window.scrollTo(x, y);
                        return null;
                    })(arguments[0], arguments[1]);
                    """,
                    [x, y]
                )
                sleep(random.uniform(0.8, 1.4))
            return True
        elif isinstance(element, list):
            # If coordinates are provided directly, assume no scrolling is needed
            return True
        else:
            print("Incorrect Element or Coordinates values!")
            return False

    def show_cursor(self):
        """Shows a red dot cursor on the page to visualize movements"""
        self.__driver.run_js('''
        (function() {
            let dot;
            function displayRedDot() {
              // Get the cursor position
              const x = event.clientX;
              const y = event.clientY;

              if (!dot) {
                // Create a new div element for the red dot if it doesn't exist
                dot = document.createElement("div");
                // Style the dot with CSS
                dot.style.position = "fixed";
                dot.style.width = "5px";
                dot.style.height = "5px";
                dot.style.borderRadius = "50%";
                dot.style.backgroundColor = "red";
                // Add the dot to the page
                document.body.appendChild(dot);
              }

              // Update the dot's position
              dot.style.left = x + "px";
              dot.style.top = y + "px";
            }

            // Add event listener to update the dot's position on mousemove
            document.addEventListener("mousemove", displayRedDot);
        })();
        ''') 