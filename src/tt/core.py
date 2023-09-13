from math import sin, cos, radians

class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Shape():
    def __init__(self, angle=None):
        self.angle = angle

    def indexToPoint(self, index):
        raise NotImplementedError

class RegularPolygon(Shape):
    def __init__(self, n, center, radius, edgeSubdivision=0):
        self.firstEdgePts = None
        self.edgeSubdivision = edgeSubdivision
        self.n = n

        self._build(n, center, radius, edgeSubdivision) 

    def _build(self, n, center, radius, edgeSubdivision=0):
        assert(n > 2)

        self.angle = 360/n # compute exterior angle of regular convex n-gon
        firstPt = Point(center.x, center.y + radius)
        self.firstEdgePts = [firstPt]

        if edgeSubdivision:
            pt = rotatePoint(firstPt, self.angle)
            self.firstEdgePts.extend(getPointsOnEdge(firstPt, pt, edgeSubdivision))

    def indexToPoint(self, index):
        edgeNum = index // (self.edgeSubdivision+1)
        angle = self.angle * edgeNum

        normalizedIndex = index - (edgeNum * (self.edgeSubdivision + 1))
        p = self.firstEdgePts[normalizedIndex]

        return rotatePoint(p, angle)

    def getCornerVertices(self):
        pts = [self.firstEdgePts[0]]

        for i in range(1, self.n):
            pt = rotatePoint(pts[0], self.angle*i)
            pts.append(pt)

        return pts

class Circle(Shape):
    def __init__(self, subdivision, radius=100):
        self.subdivision = subdivision
        self.angle = 360 / subdivision
        self.radius = radius

    def indexToPoint(self, index):
        p = Point(0, self.radius)
        return rotatePoint(p, self.angle * index)

def rotatePoint(point, angle, center=Point(0,0)):
    angleToRad = radians(angle)
    s = sin(angleToRad)
    c = cos(angleToRad)

    # translate point back to origin
    p = Point(point.x - center.x, point.y - center.y)

    xnew = p.x * c - p.y * s
    ynew = p.x * s + p.y * c

    return Point(xnew + center.x, ynew + center.y)

def getPointsOnEdge(start, end, nbPts):
    u = Point((end.x - start.x) / (nbPts+1), (end.y - start.y) / (nbPts+1)) # compute directional vector
    pts = []

    for i in range(1, nbPts + 1):
        p = Point(start.x + u.x * i, start.y + u.y * i)
        pts.append(p)

    return pts

def computePaire(ptIndex, factor, shape):
    srcPt = shape.indexToPoint(ptIndex)
    dstPt = shape.indexToPoint(ptIndex * factor)

    return srcPt, dstPt

