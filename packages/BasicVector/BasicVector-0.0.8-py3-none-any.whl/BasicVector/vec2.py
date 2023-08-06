import math
import random


class Vec2:

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.x

    def setY(self, y):
        self.y = y

    def getPos(self):
        return self.x, self.y

    def setPos(self, newPos):
        self.x = newPos.x
        self.y = newPos.y

    def div(self, xDiv=1.0, yDiv=1.0, globalDiv=1.0):
        self.x = self.x / xDiv / globalDiv
        self.y = self.y / yDiv / globalDiv

    def mult(self, xMult=1.0, yMult=1.0, globalMult=1.0):
        self.x *= xMult * globalMult
        self.y *= yMult * globalMult

    def inverse(self, inverseX, inverseY):
        if inverseX:
            self.x *= -1
        if inverseY:
            self.y *= -1

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        self.div(globalDiv=self.length())

    def normal(self):
        return self / self.length()

    def clone(self):
        return Vec2(self.x, self.y)

    @classmethod
    def randomIntVec(cls, minX=-50, maxX=50, minY=-50, maxY=50):
        x = random.randint(minX, maxX)
        y = random.randint(minY, maxY)
        return Vec2(x, y)

    @classmethod
    def randomVec(cls, minX=-50, maxX=50, minY=-50, maxY=50):
        x = random.randrange(minX, maxX)
        y = random.randrange(minY, maxY)
        return Vec2(x, y)

    @classmethod
    def dist(cls, vecA, vecB):
        return math.sqrt((vecA.x - vecB.x) ** 2 + (vecA.y - vecB.y) ** 2)

    @classmethod
    def degreesToVec2(cls, degrees):
        radians = degrees * (math.pi / 180)
        return Vec2(math.cos(radians), math.sin(radians))

    @classmethod
    def radiansToVec2(cls, radians):
        return Vec2(math.cos(radians), math.sin(radians))

    @classmethod
    def vec2ToRadians(cls, vector):
        return math.acos(vector.normal().x)

    @classmethod
    def vec2ToDegrees(cls, vector):
        return Vec2.vec2ToRadians(vector) / (math.pi / 180)

    @classmethod
    def lerp(cls, vecA, vecB, step):
        x = (1 - step) * vecA.x + step * vecB.x
        y = (1 - step) * vecA.y + step * vecB.y
        return Vec2(x, y)

    @classmethod
    def collinear(cls, vecA, vecB, vecC):
        vecAB = vecB - vecA
        vecAC = vecC - vecA
        coefX = vecAB.x / vecAC.x
        coefY = vecAB.y / vecAC.y
        return coefX == coefY

    @classmethod
    def between(cls, vecA, vecB, target):
        result = False
        if Vec2.collinear(vecA, vecB, target):
            if vecA.x <= target.x <= vecB.x and vecA.y <= target.y <= vecB.y:
                result = True
        return result

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __lt__(self, other) -> bool:
        return self.length() < other.length()

    def __le__(self, other) -> bool:
        return self.length() <= other.length()

    def __gt__(self, other) -> bool:
        return self.length() > other.length()

    def __ge__(self, other) -> bool:
        return self.length() >= other.length()

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return self.x != other.x or self.y != other.y

    def __hash__(self) -> hash:
        return hash(self.getPos())

    def __str__(self) -> str:
        return f"x = {self.x}, y = {self.y}"

    def __repr__(self) -> str:
        return f"(x = {self.x}, y = {self.y})"


if __name__ == '__main__':
    a = Vec2(5, 5)
    print(a)
    a.x = 10
    print(a.getPos())
