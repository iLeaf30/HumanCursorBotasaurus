import random
import pytweening


def generate_random_curve_parameters(driver, from_point, to_point):
    """Generates random parameters for the curve"""
    # Get window size using Botasaurus's run_js
    window_size = driver.run_js("""
        return {
            width: window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth,
            height: window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
        };
    """)
    
    window_width = window_size["width"]
    window_height = window_size["height"]
    
    # Calculate distance between points
    distance = ((from_point[0] - to_point[0]) ** 2 + (from_point[1] - to_point[1]) ** 2) ** 0.5
    
    # Adjust parameters based on distance
    if distance < 100:
        offset_boundary_x = random.randint(10, 20)
        offset_boundary_y = random.randint(10, 20)
        knots_count = random.randint(1, 2)
    elif distance < 300:
        offset_boundary_x = random.randint(20, 40)
        offset_boundary_y = random.randint(20, 40)
        knots_count = random.randint(2, 3)
    else:
        offset_boundary_x = random.randint(40, 80)
        offset_boundary_y = random.randint(40, 80)
        knots_count = random.randint(3, 4)
    
    # Ensure offsets don't go beyond window boundaries
    offset_boundary_x = min(offset_boundary_x, window_width // 4)
    offset_boundary_y = min(offset_boundary_y, window_height // 4)
    
    # Generate random distortion parameters
    distortion_mean = random.uniform(0.8, 1.2)
    distortion_st_dev = random.uniform(0.8, 1.2)
    distortion_frequency = random.uniform(0.3, 0.7)
    
    # Choose a random tweening function
    tween_functions = [
        pytweening.easeInOutQuad,
        pytweening.easeOutQuad,
        pytweening.easeInOutSine,
        pytweening.easeInOutCubic,
        pytweening.easeInOutQuint
    ]
    tween = random.choice(tween_functions)
    
    # Determine target points based on distance
    target_points = max(int(distance / 5), 50)
    target_points = min(target_points, 200)  # Cap at 200 points
    
    return (
        offset_boundary_x,
        offset_boundary_y,
        knots_count,
        distortion_mean,
        distortion_st_dev,
        distortion_frequency,
        tween,
        target_points,
    )


def calculate_absolute_offset(element, relative_position, rect=None):
    """Calculates the absolute offset based on relative position"""
    if rect is None:
        # Get element position using get_bounding_rect
        rect = element.get_bounding_rect()
    
    element_width = rect["width"]
    element_height = rect["height"]
    
    x_exact_off = element_width * relative_position[0]
    y_exact_off = element_height * relative_position[1]
    
    return [x_exact_off, y_exact_off] 