import math
import time

class GestureTimer:
    def __init__(self, hold_seconds=2.0):
        self.hold_seconds = hold_seconds
        self.active_gesture = None
        self.start_time = None
        self.triggered = False

    def update(self, gesture):
        now = time.monotonic()

        # Gesture changed or disappeared
        if gesture != self.active_gesture:
            self.active_gesture = gesture
            self.start_time = now if gesture is not None else None
            self.triggered = False

            if gesture is not None:
                print(f"Gesture detected: {gesture}")

            return

        # No gesture is currently active
        if gesture is None:
            return

        # Check whether the gesture has been held long enough
        elapsed = now - self.start_time

        if elapsed >= self.hold_seconds and not self.triggered:
            print(f"Gesture activated: {gesture}")
            self.triggered = True

def calculate_distance(point_a, point_b, width, height):
    return math.hypot(
        (point_a.x - point_b.x) * width,
        (point_a.y - point_b.y) * height
    )

def get_finger_direction(mcp, tip, width, height):
    dx = (tip.x - mcp.x) * width
    dy = (tip.y - mcp.y) * height

    threshold = 30

    if abs(dx) < threshold and abs(dy) < threshold:
        return "neutral"

    if abs(dx) > abs(dy):
        if dx > 0:
            return "left"
        else:
            return "right"
    else:
        if dy > 0:
            return "down"
        else:
            return "up"