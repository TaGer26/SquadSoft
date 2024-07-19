import math
def calculate_elevation(real_dist):
    gravity = 9.78
    gravityScale = 1
    vel = 110
    vDelta = 0
    dist = real_dist - 51
    gravity1 = gravity * gravityScale
    if real_dist > 51:
        p1 = vel ** 4 - gravity1 ** 2 * (dist) ** 2
        if p1 > 0:
            elevation = int(math.atan((vel ** 2 + math.sqrt(p1)) / (gravity1 * (dist)+ 2 * vDelta * vel ** 2)) * 1000)
            return elevation
        else:
            elevation = 'Вне радиуса'
            return elevation
    else:
        elevation = 'Вне радиуса'
        return elevation
