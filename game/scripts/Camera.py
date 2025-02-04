class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset_x = 0  # Horizontal offset

    def update(self, target):
        """Update the X offset to center the player horizontally."""
        target_center_x = target.boundary.x + (target.boundary.width // 2)
        self.offset_x = target_center_x - (self.screen_width // 2)