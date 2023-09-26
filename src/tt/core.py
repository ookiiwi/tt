from math import sin, cos, radians
import pyglet

class Point(tuple):
    def __new__(cls, x=0, y=0):
        return tuple.__new__(cls, (x, y))

    @property
    def x(self):
        return tuple.__getitem__(self, 0)
    
    @property
    def y(self):
        return tuple.__getitem__(self, 1)

class ShapeBase():
    def __init__(self, angle=0, subdivision=0):
        self._angle = angle
        self._subdivision = subdivision
        self.linkStash = []
        self.shapeStash = []

    def drawShape(self, window, batch=None):
        raise NotImplementedError
    
    def _drawShapeDelegate(self, window, ptA, ptB, batch):
        raise NotImplementedError

    def linkPoints(self, window, factor, batch=None):
        raise NotImplementedError
    
    def _linkPointsDelegate(self, window, ptA, ptB, batch):
        raise NotImplementedError
    
    def toScreenCoord(self, window, p):
        return [round(p.x) + window.width//2, round(p.y) + window.height//2]
    
    @property
    def subdivision(self):
        return self._subdivision
    
    @subdivision.setter
    def subdivision(self, value):
        # variables must be ajusted
        raise NotImplementedError

    def delete(self):
        self.shapeStash.clear()
        self.linkStash.clear()

### In order to easily test drawing functions we need to split drawing process from computation function    
class CircleBase(ShapeBase):
    def __init__(self, radius=200, position=Point(), subdivision=60, batch=None):
        assert(subdivision >= 10)

        super().__init__(360/subdivision, subdivision)
        self.radius = radius
        self.position = position

    def drawShape(self, window, batch=None):
        circle = pyglet.shapes.Arc(*self.toScreenCoord(window, self.position), radius=self.radius, closed=True, batch=batch)
        self.shapeStash = [circle]

    def linkPoints(self, window, factor, batch=None):
        self.linkStash.clear()  # clear pyglet lines in memory

        pt0 = Point(0, self.radius)   # starts from right

        for i in range(1, self.subdivision):
            ptA = rotatePoint(pt0, i * self._angle)
            ptB = rotatePoint(pt0, i * factor * self._angle)

            self._linkPointsDelegate(window, ptA, ptB, batch)

    @ShapeBase.subdivision.setter
    def subdivision(self, value):
        self._angle = 360/value
        self._subdivision = value

class Circle(CircleBase):
    def __init__(self, radius=200, position=Point(), subdivision=60, batch=None):
        super().__init__(radius, position, subdivision, batch)

    def _linkPointsDelegate(self, window, ptA, ptB, batch):
        link = pyglet.shapes.Line(*self.toScreenCoord(window, ptA), *self.toScreenCoord(window, ptB), batch=batch)
        self.linkStash.append(link) # keep lines in memory

class RegularPolygonBase(ShapeBase):
    def __init__(self, n_gon=3, radius=200, position=Point(), subdivision=30, batch=None):
        assert(n_gon > 2) # must be at least a triangle

        super().__init__(360/n_gon, subdivision)
        self._n_gon = n_gon
        self._radius = radius
        self._position = position

        self._computeFirstEdge()

    def _computeFirstEdge(self):
        firstEdgeStartPt = Point(0, self._radius)
        firstEdgeEndPt = rotatePoint(firstEdgeStartPt, self._angle, center=self._position)

        self.edge = [firstEdgeStartPt]
        self.edge.extend(getPointsOnEdge(firstEdgeStartPt, firstEdgeEndPt, self.subdivision))

    def drawShape(self, window, batch=None):
        pt0 = self.edge[0]

        for i in range(0, self._n_gon):
            ptA = rotatePoint(pt0, i * self._angle)
            ptB = rotatePoint(pt0, ((i+1)%self._n_gon) * self._angle)

            self._drawShapeDelegate(window, ptA, ptB, batch)

    def linkPoints(self, window, factor, batch=None):
        def indexToPoint(index):
            edgeNum = index // (self.subdivision+1)
            angle = self._angle * edgeNum

            normalizedIndex = index - (edgeNum * (self.subdivision + 1))
            p = self.edge[normalizedIndex]

            return rotatePoint(p, angle)

        self.linkStash.clear()
        nbPointsOnEdge = len(self.edge)

        for i in range(0, self._n_gon*nbPointsOnEdge):
            ptA = indexToPoint(i)
            ptB = indexToPoint(i*factor)

            self._linkPointsDelegate(window, ptA, ptB, batch)

    def _linkPointsDelegate(self, window, ptA, ptB, batch):
        return super()._linkPointsDelegate(window, ptA, ptB, batch)

    @ShapeBase.subdivision.setter
    def subdivision(self, value):
        self._subdivision = value
        self._computeFirstEdge()

    @property
    def n_gon(self):
        return self._n_gon

    @n_gon.setter
    def n_gon(self, value):
        self._angle = 360/value
        self._n_gon = value
        self._computeFirstEdge()

class RegularPolygon(RegularPolygonBase):
    def __init__(self, n_gon=3, radius=200, position=Point(), subdivision=30, batch=None):
        super().__init__(n_gon, radius, position, subdivision, batch)

    def _drawShapeDelegate(self, window, ptA, ptB, batch):
        line = pyglet.shapes.Line(*self.toScreenCoord(window, ptA), *self.toScreenCoord(window, ptB), batch=batch)
        self.shapeStash.append(line)

    def _linkPointsDelegate(self, window, ptA, ptB, batch):
        link = pyglet.shapes.Line(*self.toScreenCoord(window, ptA), *self.toScreenCoord(window, ptB), batch=batch)
        self.linkStash.append(link) # keep lines in memory

def rotatePoint(point, angle, center=Point()):
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
