import math
import random


class Vec3:

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.x

    def setY(self, y):
        self.y = y

    def getZ(self):
        return self.z

    def setZ(self, z):
        self.z = z

    def getPos(self):
        return self.x, self.y, self.z

    def setPos(self, newPos):
        self.x = newPos.x
        self.y = newPos.y
        self.z = newPos.z

    def div(self, xDiv=1.0, yDiv=1.0, zDiv=1.0, globalDiv=1.0):
        self.x = self.x / xDiv / globalDiv
        self.y = self.y / yDiv / globalDiv
        self.z = self.z / zDiv / globalDiv

    def mult(self, xMult=1.0, yMult=1.0, zMult=1.0, globalMult=1.0):
        self.x *= xMult * globalMult
        self.y *= yMult * globalMult
        self.z *= zMult * globalMult

    def inverse(self, inverseX, inverseY, inverseZ):
        if inverseX:
            self.x *= -1
        if inverseY:
            self.y *= -1
        if inverseZ:
            self.z *= -1

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        self.div(globalDiv=self.length())

    def normal(self):
        return self / self.length()

    def clone(self):
        return Vec3(self.x, self.y, self.z)

    @classmethod
    def randomIntVec(cls, minX=-50, maxX=50, minY=-50, maxY=50, minZ=-50, maxZ=50):
        x = random.randint(minX, maxX)
        y = random.randint(minY, maxY)
        z = random.randint(minZ, maxZ)
        return Vec3(x, y, z)

    @classmethod
    def randomVec(cls, minX=-50, maxX=50, minY=-50, maxY=50, minZ=-50, maxZ=50):
        x = random.randrange(minX, maxX)
        y = random.randrange(minY, maxY)
        z = random.randint(minZ, maxZ)
        return Vec3(x, y, z)

    @classmethod
    def dist(cls, vectorA, vectorB):
        return math.sqrt((vectorA.x - vectorB.x) ** 2 + (vectorA.y - vectorB.y) ** 2 + (vectorA.z - vectorB.z) ** 2)

    @classmethod
    def lerp(cls, vecA, vecB, step):
        x = (1 - step) * vecA.x + step * vecB.x
        y = (1 - step) * vecA.y + step * vecB.y
        z = (1 - step) * vecA.z + step * vecB.z
        return Vec3(x, y, z)

    @classmethod
    def collinear(cls, vecA, vecB, vecC):
        vecAB = vecB - vecA
        vecAC = vecC - vecA
        coefX = vecAB.x / vecAC.x
        coefY = vecAB.y / vecAC.y
        coefZ = vecAB.z / vecAC.z
        return coefX == coefY and coefY == coefZ

    @classmethod
    def between(cls, vecA, vecB, target):
        result = False
        if Vec3.collinear(vecA, vecB, target):
            if vecA.x <= target.x <= vecB.x and vecA.y <= target.y <= vecB.y and vecA.z <= target.z <= vecB.z:
                result = True
        return result

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vec3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)

    def __lt__(self, other) -> bool:
        return self.length() < other.length()

    def __le__(self, other) -> bool:
        return self.length() <= other.length()

    def __gt__(self, other) -> bool:
        return self.length() > other.length()

    def __ge__(self, other) -> bool:
        return self.length() >= other.length()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other) -> bool:
        return self.x != other.x or self.y != other.y or self.z != other.z

    def __hash__(self) -> hash:
        return hash(self.getPos())

    def __str__(self) -> str:
        return f"x = {self.x}, y = {self.y}, z = {self.z}"

    def __repr__(self) -> str:
        return f"(x = {self.x}, y = {self.y}, z = {self.z})"
