import random

from botasaurus_driver import Driver
from botasaurus_driver.driver import Element

from humancursor_botasaurus.utilities.human_curve_generator import HumanizeMouseTrajectory
from humancursor_botasaurus.utilities.calculate_and_randomize import generate_random_curve_parameters, calculate_absolute_offset


class WebAdjuster:
    def __init__(self, driver: Driver):
        """
        Initialize WebAdjuster with a Botasaurus driver
        
        Args:
            driver: Botasaurus Driver instance
        """
        self.__driver = driver
        self.origin_coordinate = [0, 0]

    def move_to(
        self,
        element_or_pos,
        origin_coordinates=None,
        absolute_offset=False,
        relative_position=None,
        human_curve=None,
        steady=False
    ):
        """Moves the cursor, trying to mimic human behaviour!"""
        origin = origin_coordinates
        if origin_coordinates is None:
            origin = self.origin_coordinate

        pre_origin = tuple(origin)
        if isinstance(element_or_pos, list):
            if not absolute_offset:
                x, y = element_or_pos[0], element_or_pos[1]
            else:
                x, y = (
                    element_or_pos[0] + pre_origin[0],
                    element_or_pos[1] + pre_origin[1],
                )
        else:
            # Get element position using Botasaurus's get_bounding_rect, with fallback if needed
            try:
                rect = element_or_pos.get_bounding_rect()
            except Exception as e:
                print("Error obtaining bounding rect for element:", e)
                if hasattr(element_or_pos, "_elem"):
                    raw = element_or_pos._elem
                    rect = self.__driver.run_js("(function(el){var r=el.getBoundingClientRect(); return {x: r.x, y: r.y, width: r.width, height: r.height};})(arguments[0]);", [raw])
                else:
                    print("Element does not support _elem attribute, cannot get position.")
                    return origin
            if not isinstance(rect, dict):
                try:
                    rect = {"x": rect.x, "y": rect.y, "width": rect.width, "height": rect.height}
                except Exception as e:
                    print("Error converting bounding rect to dict in move_to:", e)
                    return origin
            if rect.get("width", 0) == 0 or rect.get("height", 0) == 0:
                print("Could not find position for", element_or_pos)
                return origin
            destination = {"x": rect.get("x", 0), "y": rect.get("y", 0)}
            
            if relative_position is None:
                x_random_off = random.choice(range(20, 80)) / 100
                y_random_off = random.choice(range(20, 80)) / 100

                # Get element size from bounding rect
                element_width = rect["width"]
                element_height = rect["height"]
                
                x, y = destination["x"] + (
                    element_width * x_random_off
                ), destination["y"] + (element_height * y_random_off)
            else:
                abs_exact_offset = calculate_absolute_offset(
                    element_or_pos, relative_position, rect
                )
                x_exact_off, y_exact_off = abs_exact_offset[0], abs_exact_offset[1]
                x, y = destination["x"] + x_exact_off, destination["y"] + y_exact_off

        (
            offset_boundary_x,
            offset_boundary_y,
            knots_count,
            distortion_mean,
            distortion_st_dev,
            distortion_frequency,
            tween,
            target_points,
        ) = generate_random_curve_parameters(
            self.__driver, [origin[0], origin[1]], [x, y]
        )
        if steady:
            offset_boundary_x, offset_boundary_y = 10, 10
            distortion_mean, distortion_st_dev, distortion_frequency = 1.2, 1.2, 1
        if not human_curve:
            human_curve = HumanizeMouseTrajectory(
                [origin[0], origin[1]],
                [x, y],
                offset_boundary_x=offset_boundary_x,
                offset_boundary_y=offset_boundary_y,
                knots_count=knots_count,
                distortion_mean=distortion_mean,
                distortion_st_dev=distortion_st_dev,
                distortion_frequency=distortion_frequency,
                tween=tween,
                target_points=target_points,
            )

        # Move the cursor along the human-like curve using Botasaurus's click_at_point
        # We'll use JavaScript to simulate mouse movement
        for point in human_curve.points:
            # Move to each point in the curve
            self.__driver.run_js(f"""
                (function() {{
                    const event = new MouseEvent('mousemove', {{
                        bubbles: true,
                        cancelable: true,
                        view: window,
                        clientX: {point[0]},
                        clientY: {point[1]}
                    }});
                    var el = document.elementFromPoint({point[0]}, {point[1]});
                    if (el) {{
                        el.dispatchEvent(event);
                    }}
                    return null;
                }})();
            """)
            
            # Update the origin coordinates
            origin[0], origin[1] = point[0], point[1]

        self.origin_coordinate = [x, y]
        return [x, y] 