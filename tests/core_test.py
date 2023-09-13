import unittest
from src.tt.core import *
from src.tt.core import RegularPolygon

class CoreFunctionsTest(unittest.TestCase):
    def test_rotatePoint(self):
        p = Point(100, 0)
        rotP = rotatePoint(p, 90)

        self.assertAlmostEqual(rotP.x, 0)
        self.assertAlmostEqual(rotP.y, 100)

    def test_getPointsOnEdge(self):
        a = Point(0, 100)
        b = Point(-86.6, 50)
        expectedPts = [Point(-21.65, 87.5), Point(-43.3, 75), Point(-64.95, 62.5)]
        pts = getPointsOnEdge(a, b, 3)

        for i in range(0, len(pts)):
            self.assertAlmostEqual(pts[i].x, expectedPts[i].x)
            self.assertAlmostEqual(pts[i].y, expectedPts[i].y)

    def test_computePaire(self):
        pass

class RegularPolygonTest(unittest.TestCase):
    def test_build(self):
        poly = RegularPolygon(3, Point(0,0), 100, 3)
        expectedPts = [Point(0, 100), Point(-21.65, 62.5), Point(-43.3, 25), Point(-64.95, -12.5)]
        pts = poly.firstEdgePts

        for i in range(0, len(pts)):
            self.assertAlmostEqual(pts[i].x, expectedPts[i].x, places=2)
            self.assertAlmostEqual(pts[i].y, expectedPts[i].y, places=2)


        self.assertEqual(poly.angle, 120)

    def test_getCornerVertices(self):
        poly = RegularPolygon(3, Point(0,0), 100, 3)
        vertices = poly.getCornerVertices()
        expectedPts = [Point(0, 100), Point(-86.6, -50), Point(86.6, -50)]

        self.assertEqual(len(vertices), 3)

        for i in range(0, len(vertices)):
            self.assertAlmostEqual(expectedPts[i].x, vertices[i].x, places=2)
            self.assertAlmostEqual(expectedPts[i].y, vertices[i].y, places=2)

    def test_indexToPoint(self):
        poly = RegularPolygon(3, Point(0,0), 100, 3)
        pts = poly.firstEdgePts

        for i in range(0, 3 + 9 + 1):
            edgeNum = i // (poly.edgeSubdivision+1)
            p = poly.indexToPoint(i)
            pFirstEdge = rotatePoint(pts[i%(len(pts))], poly.angle*edgeNum)

            self.assertAlmostEqual(pFirstEdge.x, p.x, places=2)
            self.assertAlmostEqual(pFirstEdge.y, p.y, places=2)

class CircleTest(unittest.TestCase):
    def test_indexToPoint(self):
        circle = Circle(10)

        self.assertEqual(circle.angle, 36)

        for i in range(0, circle.subdivision):
            p = circle.indexToPoint(i)
            expectedP = rotatePoint(Point(0, 100), circle.angle*i)

            self.assertAlmostEqual(expectedP.x, p.x)
            self.assertAlmostEqual(expectedP.y, p.y)

if __name__ == '__main__':
    unittest.main()
