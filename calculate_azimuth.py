import math
def calculate_azimuth(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    azimuth = math.atan2(dy, dx)
    azimuth_degrees = math.degrees(azimuth)
    azimuth_degrees = round((azimuth_degrees + 90) % 360, 1)
    return azimuth_degrees
