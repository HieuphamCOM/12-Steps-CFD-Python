# pyright: reportGeneralTypeIssues=false
# pyright: reportOptionalSubscript=false

import unittest

from Formwork.Factories.BIM2FaceFactory import BIM2Face
from Formwork.Factories.BIM2WallFactory import BIM2WallFactory, BIM2Wall
from Formwork.Utility.Utility import get_attribute

import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Geometry as AllplanGeo

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

        cls.walls = {ele: message + f" - Trade: {get_attribute(ele, 209)}"
                     for wall, message in walls.items()
                     for ele in wall if ele == AllplanElementAdapter.WallTier_TypeUUID}

        cls.bim2wall_factory = BIM2WallFactory()

    @classmethod
    def tearDownClass(cls):
        AllplanUtil.ClearUnitTestDocument()

    def test_object_type(self):
        print(" ========== Testing Object Type ========== ")

        bim2walls = {self.bim2wall_factory.create_from(wall): message
                     for wall, message in self.walls.items()}

        for wall, message in bim2walls.items():
            print(f" ======== Test {message} ======== ")
            # Test attributes
            self.assertIsInstance(wall, BIM2Wall)
            self.assertTrue(hasattr(wall, "origin_wall"))
            self.assertTrue(hasattr(wall, "bottom_face"))
            self.assertTrue(hasattr(wall, "top_face"))
            self.assertTrue(hasattr(wall, "first_face"))
            self.assertTrue(hasattr(wall, "second_face"))
            self.assertTrue(hasattr(wall, "third_face"))
            self.assertTrue(hasattr(wall, "fourth_face"))
            self.assertTrue(hasattr(wall, "profile_faces"))
            self.assertTrue(hasattr(wall, "side_faces"))

            self.assertTrue(hasattr(wall, "start_point"))
            self.assertTrue(hasattr(wall, "end_point"))
            self.assertTrue(hasattr(wall, "location_line"))
            self.assertTrue(hasattr(wall, "orientation"))
            self.assertTrue(hasattr(wall, "length"))
            self.assertTrue(hasattr(wall, "width"))
            self.assertTrue(hasattr(wall, "height"))

            # Test origin wall
            self.assertIsInstance(wall.origin_wall, AllplanElementAdapter.BaseElementAdapter)

            # Test BIM2 objects
            self.assertIsInstance(wall.bottom_face, BIM2Face)
            self.assertIsInstance(wall.top_face, BIM2Face)
            self.assertIsInstance(wall.first_face, BIM2Face)
            self.assertIsInstance(wall.second_face, BIM2Face)
            self.assertIsInstance(wall.third_face, BIM2Face)
            self.assertIsInstance(wall.fourth_face, BIM2Face)

            self.assertIsInstance(wall.profile_faces, tuple)
            self.assertEqual(len(wall.profile_faces), 2)
            for face in wall.profile_faces:
                self.assertIsInstance(face, BIM2Face)

            self.assertIsInstance(wall.side_faces, tuple)
            self.assertEqual(len(wall.side_faces), 2)
            for face in wall.side_faces:
                self.assertIsInstance(face, BIM2Face)

            # Test Allplan object
            self.assertIsInstance(wall.start_point, AllplanGeo.Point3D)
            self.assertIsInstance(wall.end_point, AllplanGeo.Point3D)
            self.assertIsInstance(wall.location_line, AllplanGeo.Line3D)
            self.assertIsInstance(wall.orientation, AllplanGeo.Vector3D)

    def test_object_value(self):
        print("\n ========== Testing Object Value ========== ")

        bim2walls = {self.bim2wall_factory.create_from(wall): message
                     for wall, message in self.walls.items()}

        for wall, message in bim2walls.items():
            print(f" ======== Test {message} ======== ")
            # Test Faces
            self.assertTrue(wall.profile_faces[0] is wall.third_face)
            self.assertTrue(wall.profile_faces[1] is wall.fourth_face)
            self.assertTrue(wall.side_faces[0] is wall.first_face)
            self.assertTrue(wall.side_faces[1] is wall.second_face)

def suite() -> unittest.TestSuite:
    """
    This defines all the tests of TestStringEvaluate

    Returns:
        test suite
    """

    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestBIM2WallFactory))

    return test_suite
