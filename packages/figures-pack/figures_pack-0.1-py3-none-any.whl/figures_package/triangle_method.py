import math

from Geometry import Point, Triangle

class Triang:
    def __init__(self):
        self.point1 = Point(0, 0)
        self.point2 = Point(0, 1)
        self.point3 = Point(1, 0)
        Triangle(self.point1, self.point2, self.point3)

    def perimetr(self):
        st1 = math.hypot(self.point2[0] - self.point1[0], self.point2[1] - self.point1[0])
        st2 = math.hypot(self.point2[0] - self.point3[0], self.point2[1] - self.point3[0])
        st3 = math.hypot(self.point1[0] - self.point3[0], self.point1[1] - self.point3[0])
        print(round(st1+st2+st3, 4))

    def square(self):
        print(round(0.5*abs((self.point2[0] - self.point1[0])*(self.point3[1] - self.point1[1])
                            -(self.point3[0] - self.point1[0])*(self.point2[1] - self.point1[1])), 4))



my_triangle = Triang()
my_triangle.perimetr()
my_triangle.square()