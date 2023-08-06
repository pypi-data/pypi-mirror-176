import math

from Geometry import Point, Line

class Lines:
    def __init__(self):
        self.point1 = Point(0, 0)
        self.point2 = Point(0, 1)
        Line(self.point1, self.point2)

    def length(self):
        print(math.hypot(self.point2[0] - self.point1[0], self.point2[1] - self.point1[0]))



my_line = Lines()
my_line.length()


