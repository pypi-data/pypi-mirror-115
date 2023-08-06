import math
import random


class Vec4:

    def __init__(self, x=0.0, y=0.0, w=0.0, h=0.0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.x

    def setY(self, y):
        self.y = y

    def getW(self):
        return self.w

    def setW(self, w):
        self.w = w

    def getH(self):
        return self.h

    def setH(self, h):
        self.h = h

    def getPos(self):
        return self.x, self.y, self.w, self.h

    def setPos(self, newPos):
        self.x = newPos.x
        self.y = newPos.y
        self.w = newPos.w
        self.h = newPos.h

    def div(self, xDiv=1.0, yDiv=1.0, wDiv=1.0, hDiv=1.0, globalDiv=1.0):
        self.x = self.x / xDiv / globalDiv
        self.y = self.y / yDiv / globalDiv
        self.w = self.w / wDiv / globalDiv
        self.h = self.h / hDiv / globalDiv

    def mult(self, xMult=1.0, yMult=1.0, wMult=1.0, hMult=1.0, globalMult=1.0):
        self.x *= xMult * globalMult
        self.y *= yMult * globalMult
        self.w *= wMult * globalMult
        self.h *= hMult * globalMult

    def inverse(self, inverseX, inverseY, inverseW, inverseH):
        if inverseX:
            self.x *= -1
        if inverseY:
            self.y *= -1
        if inverseW:
            self.w *= -1
        if inverseH:
            self.h *= -1

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.w ** 2 + self.h ** 2)

    def normalize(self):
        self.div(globalDiv=self.length())

    def normal(self):
        return self / self.length()

    def clone(self):
        return Vec4(self.x, self.y, self.w, self.h)

    @classmethod
    def randomIntVec(cls, minX=-50, maxX=50, minY=-50, maxY=50, minW=-50, maxW=50, minH=-50, maxH=50):
        x = random.randint(minX, maxX)
        y = random.randint(minY, maxY)
        w = random.randint(minW, maxW)
        h = random.randint(minH, maxH)
        return Vec4(x, y, w, h)

    @classmethod
    def randomVec(cls, minX=-50, maxX=50, minY=-50, maxY=50, minW=-50, maxW=50, minH=-50, maxH=50):
        x = random.randrange(minX, maxX)
        y = random.randrange(minY, maxY)
        w = random.randint(minW, maxW)
        h = random.randint(minH, maxH)
        return Vec4(x, y, w, h)

    @classmethod
    def dist(cls, vectorA, vectorB):
        return math.sqrt((vectorA.x - vectorB.x) ** 2 + (vectorA.y - vectorB.y) ** 2 +
                         (vectorA.w - vectorB.w) ** 2 + (vectorA.h - vectorB.h) ** 2)

    @classmethod
    def lerp(cls, vecA, vecB, step):
        x = (1 - step) * vecA.x + step * vecB.x
        y = (1 - step) * vecA.y + step * vecB.y
        w = (1 - step) * vecA.w + step * vecB.w
        h = (1 - step) * vecA.h + step * vecB.h
        return Vec4(x, y, w, h)

    @classmethod
    def collinear(cls, vecA, vecB, vecC):
        vecAB = vecB - vecA
        vecAC = vecC - vecA
        coefX = vecAB.x / vecAC.x
        coefY = vecAB.y / vecAC.y
        coefW = vecAB.w / vecAC.w
        coefH = vecAB.h / vecAC.h

        return coefX == coefY and coefY == coefW and coefW == coefH

    @classmethod
    def between(cls, vecA, vecB, target):
        result = False
        if Vec4.collinear(vecA, vecB, target):
            if vecA.x <= target.x <= vecB.x and vecA.y <= target.y <= vecB.y and vecA.w <= target.w <= vecB.w \
                    and vecA.h <= target.h <= vecB.h:
                result = True
        return result

    def __add__(self, other):
        return Vec4(self.x + other.x, self.y + other.y, self.w + other.w, self.h + other.h)

    def __sub__(self, other):
        return Vec4(self.x - other.x, self.y - other.y, self.w - other.w, self.h - other.h)

    def __mul__(self, other):
        return Vec4(self.x * other, self.y * other, self.w * other, self.h * other.h)

    def __truediv__(self, other):
        return Vec4(self.x / other, self.y / other, self.w / other, self.h / other)

    def __lt__(self, other) -> bool:
        return self.length() < other.length()

    def __le__(self, other) -> bool:
        return self.length() <= other.length()

    def __gt__(self, other) -> bool:
        return self.length() > other.length()

    def __ge__(self, other) -> bool:
        return self.length() >= other.length()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.w == other.w and self.h == other.h

    def __ne__(self, other) -> bool:
        return self.x != other.x or self.y != other.y or self.w != other.w or self.h != other.h

    def __hash__(self) -> hash:
        return hash(self.getPos())

    def __str__(self):
        return f"x = {self.x}, y = {self.y}, w = {self.w}, h = {self.h}"

    def __repr__(self) -> str:
        return f"(x = {self.x}, y = {self.y}, w = {self.w}, h = {self.w})"

