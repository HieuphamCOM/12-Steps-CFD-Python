# pyright: reportGeneralTypeIssues=false
# pyright: reportOptionalSubscript=false

import unittest

from Formwork.Factories.BIM2FaceFactory import BIM2Face
from Formwork.Factories.BIM2WallFactory import BIM2WallFactory
from Formwork.Utility.Utility import get_attribute
from Formwork.Utility.TestUtils import compare_points, compare_lines

import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Utility as AllplanUtil

from ..TestBase import TestBase, SINGLE_PATH

WALL_MODEL = (SINGLE_PATH + "wall_2_layer.sym", SINGLE_PATH + "wall_2_opening.sym",
              SINGLE_PATH + "wall_3_layer.sym", SINGLE_PATH + "wall_full_opening.sym",
              SINGLE_PATH + "wall_half_opening.sym", SINGLE_PATH + "wall_niche.sym",
              SINGLE_PATH + "wall_normal.sym", SINGLE_PATH + "wall_outside_opening.sym",
              SINGLE_PATH + "cut_wall_1.sym", SINGLE_PATH + "cut_wall_2.sym")


class TestBIM2WallFactory(TestBase):

    @classmethod
    def setUpClass(cls):
        print(f"\n ========== Running {__name__} ========== ")

        walls = {AllplanUtil.LoadSymbolForUnitTest(wall, False): f"Symbol: {wall}"
                 for wall in WALL_MODEL}

        used_walls = {ele: message + f" - Trade: {get_attribute(ele, 209)}"
                      for wall, message in walls.items()
                      for ele in wall if ele == AllplanElementAdapter.WallTier_TypeUUID}

        bim2wall_factory = BIM2WallFactory()

        cls.bim2faces = {}
        for wall, message in used_walls.items():
            bim2wall = bim2wall_factory.create_from(wall)
            for key, value in bim2wall.__dict__.items():
                if isinstance(value, BIM2Face):
                    cls.bim2faces[value] = message + f" - Face: {key}"


    @classmethod
    def tearDownClass(cls):
        AllplanUtil.ClearUnitTestDocument()

    def test_object_type(self):
        print("\n ========== Testing Object Type ========== ")

        for bim2face, message in self.bim2faces.items():
            print(f" ======== Test {message} ======== ")
            self.assertIsInstance(bim2face, BIM2Face)
            # Test attributes
            self.assertTrue(hasattr(bim2face, "list_points"))
            self.assertTrue(hasattr(bim2face, "normal_vector"))
            self.assertTrue(hasattr(bim2face, "list_edges"))
            self.assertTrue(hasattr(bim2face, "min_point"))
            self.assertTrue(hasattr(bim2face, "max_point"))
            self.assertTrue(hasattr(bim2face, "center_point"))
            self.assertTrue(hasattr(bim2face, "diagonal"))
            self.assertTrue(hasattr(bim2face, "bottom_line"))

            # Test points
            self.assertIsInstance(bim2face.list_points, list)
            self.assertEqual(len(bim2face.list_points), 4)
            for face in bim2face.list_points:
                self.assertIsInstance(face, AllplanGeo.Point3D)
            self.assertIsInstance(bim2face.min_point, AllplanGeo.Point3D)
            self.assertIsInstance(bim2face.max_point, AllplanGeo.Point3D)
            self.assertIsInstance(bim2face.center_point, AllplanGeo.Point3D)

            # Test lines
            self.assertIsInstance(bim2face.normal_vector, AllplanGeo.Vector3D)
            self.assertIsInstance(bim2face.list_edges, list)
            self.assertEqual(len(bim2face.list_edges), 4)
            for face in bim2face.list_edges:
                self.assertIsInstance(face, AllplanGeo.Line3D)
            self.assertIsInstance(bim2face.diagonal, AllplanGeo.Line3D)
            self.assertIsInstance(bim2face.bottom_line, AllplanGeo.Line3D)

    def test_object_value(self):
        print("\n ========== Testing Object Value ========== ")

        for bim2face, message in self.bim2faces.items():
            print(f" ======== Test {message} ======== ")
            self.assertIsInstance(bim2face, BIM2Face)

            # Test points, lines
            self.assertIn(bim2face.min_point, bim2face.list_points)
            self.assertIn(bim2face.max_point, bim2face.list_points)
            self.assertIn(bim2face.bottom_line, bim2face.list_edges)
            self.assertNotIn(bim2face.center_point, bim2face.list_points)
            self.assertTrue(compare_points(bim2face.center_point,
                                           bim2face.diagonal.GetCenterPoint()))
            self.assertTrue(compare_lines(bim2face.bottom_line, bim2face.list_edges[0]))

    def _compare_points(self, point1: AllplanGeo.Point3D, point2: AllplanGeo.Point3D):
        distance = point1.GetDistance(point2)
        if abs(distance) < 0.01:
            return True
        else:
            return False

    def _compare_lines(self, line1: AllplanGeo.Line3D, line2: AllplanGeo.Line3D):
        start_point_1 = line1.GetStartPoint()
        end_point_1 = line1.GetEndPoint()
        start_point_2 = line2.GetStartPoint()
        end_point_2 = line2.GetEndPoint()
        if compare_points(start_point_1, start_point_2) \
            and compare_points(end_point_1, end_point_2):
            return True
        else:
            return False


def suite() -> unittest.TestSuite:
    """
    This defines all the tests of TestStringEvaluate

    Returns:
        test suite
    """

    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestBIM2WallFactory))

    return test_suite
