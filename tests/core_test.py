import tt
from tt.core import Point
from pytest import approx

class CircleTest(tt.CircleBase):
    def __init__(self, radius=200, position=Point(), subdivision=60, batch=None):
        super().__init__(radius, position, subdivision, batch)
        self.linkLines = []

    def linkPoints(self, window, factor, batch=None):
        self.linkLines.clear()
        return super().linkPoints(window, factor, batch)

    def _linkPointsDelegate(self, window, ptA, ptB, batch):
        self.linkLines.append((ptA, ptB))

class RegularPolygonTest(tt.RegularPolygonBase):
    def __init__(self, n_gon=3, radius=200, position=Point(), subdivision=30, batch=None):
        super().__init__(n_gon, radius, position, subdivision, batch)

        self.shapeLines = []
        self.linkLines = []

    def _drawShapeDelegate(self, window, ptA, ptB, batch):
        self.shapeLines.extend([ptA, ptB])
    
    def _linkPointsDelegate(self, window, ptA, ptB, batch):
        self.linkLines.append([ptA, ptB])

def test_Circle():
    circle = CircleTest(radius=1, subdivision=10)
    circle.linkPoints(None, 2)

    A = Point(0, 1)
    B = Point(-0.587, 0.809)
    C = Point(-0.951, 0.309)
    D = Point(C.x, -C.y)
    E = Point(B.x, -B.y)
    F = Point(A.x, -A.y)
    G = Point(-E.x, E.y)
    H = Point(-D.x, D.y)
    I = Point(H.x, -H.y)
    J = Point(G.x, -G.y)

    expectedLinks = [
        [B, C],
        [C, E],
        [D, G],
        [E, I],
        [F, A],
        [G, C],
        [H, E],
        [I, G],
        [J, I]
    ]

    links = circle.linkLines

    # not testing drawShape because process delegated to pyglet

    assert len(links) == (circle.subdivision - 1) # subdivision - 1 because first point is always 0

    #links coord
    for i in range(0, len(links)):
        for j in range(0, 2):
            ptA = expectedLinks[i][j]
            ptB = links[i][j]

            print(i, ptA.x, ptA.y, ptB.x, ptB.y)

            assert ptA.x == approx(ptB.x, rel=1e-2)
            assert ptA.y == approx(ptB.y, rel=1e-2)

def test_RegularPolygon():
    poly = RegularPolygonTest(radius=1, subdivision=2)
    poly.drawShape(None)
    poly.linkPoints(None, 2)

    A = Point(0, 1)
    B = Point(-0.866, -0.5)
    C = Point(-B.x, -0.5)
    AB1 = Point(-0.288, 0.5)
    AB2 = Point(-0.577, 0)
    BC1 = Point(AB1.x, -AB1.y)
    BC2 = Point(-AB1.x, -AB1.y)
    AC1 = Point(-AB2.x, AB2.y)
    AC2 = Point(-AB1.x, AB1.y)


    def _cmpListVertices(a, b):
        a.sort(key=lambda e: e.x)
        b.sort(key=lambda e: e.x)

        assert len(a) == len(b)

        for i in range(0, len(b)):
            pta = a[i]
            ptb = b[i]

            assert pta.x == approx(ptb.x, rel=1e-2)
            assert pta.y == approx(ptb.y, rel=1e-2)

    def edgeTest():
        expectedTriangleVertices = [A, AB1, AB2]
        vertices = list(set(poly.edge))

        _cmpListVertices(expectedTriangleVertices, vertices)

    def buildTest():
        # check triangle points
        expectedTriangleVertices = [A,B,C]
        vertices = list(set(poly.shapeLines))

        _cmpListVertices(expectedTriangleVertices, vertices)

    def linkPointsTest():
        # Points ordered in anti clock order (0 to 2pi)
        expectedVertices = [[A, A],
                            [AB1, AB2],
                            [AB2, BC1],
                            [B, C],
                            [BC1, AC2],
                            [BC2, AB1],
                            [C, B],
                            [AC1, BC2],
                            [AC2, AC1]]
        
        vertices = poly.linkLines

        assert len(expectedVertices) == len(vertices)

        for i in range(0, len(vertices)):
            for j in range(0, 2):
                pta = expectedVertices[i][j]
                ptb = vertices[i][j]

                print(pta.x, pta.y, ptb.x, ptb.y)

                assert pta.x == approx(ptb.x, rel=1e-2)
                assert pta.y == approx(ptb.y, rel=1e-2)

    edgeTest()
    buildTest()
    linkPointsTest()