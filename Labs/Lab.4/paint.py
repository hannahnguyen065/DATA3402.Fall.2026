import math

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]

    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]

    def v_line(self, x, y, h, **kargs):
        for i in range(x, x+h):
            self.set_pixel(i, y, **kargs)

    def h_line(self, x, y, w, **kargs):
        for i in range(y, y+w):
            self.set_pixel(x, i, **kargs)

    def line(self, x1, y1, x2, y2, **kargs):
        slope = (x2-x1) / (y2-y1)
        for y in range(y1, y2):
            x = x1 + int(slope * (y-y1))
            self.set_pixel(x, y, **kargs)

    def display(self):
        print("\n".join("".join(row) for row in self.data))

##shape
class Shape:
    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def perimeter_points(self):
        raise NotImplementedError

    def contains(self, x, y):
        raise NotImplementedError

    def overlaps(self, other):
        for x, y in self.perimeter_points():
            if other.contains(x, y):
                return True

        for x, y in other.perimeter_points():
            if self.contains(x, y):
                return True

        return False

    def paint(self, canvas):
        for x, y in self.perimeter_points():
            x = round(x)
            y = round(y)

            if 0 <= x < canvas.height and 0 <= y < canvas.width:
                canvas.set_pixel(x, y)


##rectangle
class Rectangle(Shape):
    def __init__(self, length, width, x, y):
        self.__length = length
        self.__width = width
        self.__x = x
        self.__y = y

    def area(self):
        return self.__length * self.__width

    def perimeter(self):
        return 2 * (self.__length + self.__width)

    def get_length(self):
        return self.__length

    def get_width(self):
        return self.__width

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def perimeter_points(self):
        x = self.__x
        y = self.__y
        w = self.__width
        l = self.__length

        return [
            (x, y),
            (x + w/3, y),
            (x + 2*w/3, y),
            (x + w, y),
            (x + w, y + l/3),
            (x + w, y + 2*l/3),
            (x + w, y + l),
            (x + 2*w/3, y + l),
            (x + w/3, y + l),
            (x, y + l),
            (x, y + 2*l/3),
            (x, y + l/3)
        ]

    def contains(self, x, y):
        return (self.__x <= x <= self.__x + self.__width and
                self.__y <= y <= self.__y + self.__length)


##circle
class Circle(Shape):
    def __init__(self, radius, x, y):
        self.__radius = radius
        self.__x = x
        self.__y = y

    def area(self):
        return math.pi * self.__radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.__radius

    def get_radius(self):
        return self.__radius

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def perimeter_points(self):
        points = []

        for i in range(16):
            angle = 2 * math.pi * i / 16

            px = self.__x + self.__radius * math.cos(angle)
            py = self.__y + self.__radius * math.sin(angle)

            points.append((px, py))

        return points

    def contains(self, x, y):
        distance = math.sqrt(
            (x - self.__x)**2 +
            (y - self.__y)**2
        )

        return distance <= self.__radius

##triangle
class Triangle(Shape):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__x3 = x3
        self.__y3 = y3

    def area(self):
        return abs(
            self.__x1 * (self.__y2 - self.__y3) +
            self.__x2 * (self.__y3 - self.__y1) +
            self.__x3 * (self.__y1 - self.__y2)
        ) / 2

    def perimeter(self):
        side1 = math.sqrt(
            (self.__x2 - self.__x1)**2 +
            (self.__y2 - self.__y1)**2
        )

        side2 = math.sqrt(
            (self.__x3 - self.__x2)**2 +
            (self.__y3 - self.__y2)**2
        )

        side3 = math.sqrt(
            (self.__x1 - self.__x3)**2 +
            (self.__y1 - self.__y3)**2
        )

        return side1 + side2 + side3

    def perimeter_points(self):
        return [
            (self.__x1, self.__y1),
            (self.__x2, self.__y2),
            (self.__x3, self.__y3)
        ]

    def contains(self, x, y):
        def get_area(x1, y1, x2, y2, x3, y3):
            return abs(
                x1*(y2-y3) +
                x2*(y3-y1) +
                x3*(y1-y2)
            ) / 2

        total = self.area()

        a1 = get_area(
            x, y,
            self.__x2, self.__y2,
            self.__x3, self.__y3
        )

        a2 = get_area(
            self.__x1, self.__y1,
            x, y,
            self.__x3, self.__y3
        )

        a3 = get_area(
            self.__x1, self.__y1,
            self.__x2, self.__y2,
            x, y
        )

        return abs(total - (a1 + a2 + a3)) < 0.000001

##compound shape
class CompoundShape:
    def __init__(self):
        self.shapes = []

    def add(self, shape):
        self.shapes.append(shape)

    def paint(self, canvas):
        for shape in self.shapes:
            shape.paint(canvas)