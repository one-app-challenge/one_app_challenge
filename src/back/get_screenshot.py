def get_screenshot(screenshot: float):
    screenshot_path = Users/a/"Desktop"/screenshot
    file_size = screenshot_path.stat().st_size
    
    return (file_size,screenshot_path)


