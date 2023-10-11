# pyright: reportGeneralTypeIssues=false
# pyright: reportOptionalSubscript=false

import unittest
from collections import defaultdict
from itertools import product

import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Utility as AllplanUtil

from Formwork.Factories.BIM2WallFactory import BIM2WallFactory, BIM2Wall
from Formwork.Factories.BIM2FaceFactory import BIM2Face
from Formwork.Shape.Recognizer import ShapeRecognizer
from Formwork.Shape.Classes import (Shape, XShape, 
                                    LShape, TShape, 
                                    YShape, CShape, 
                                    VShape, ShapeMember, 
                                    LVShape, CXShape, 
                                    TYShape, ShapeMember)
from Formwork.Utility.TestUtils import random_point, randint

from ..TestBase import TestBase, CONNECT_PATH


class TestShapeRecognizer(TestBase):

    @classmethod
    def setUpClass(cls):
        print(f"\n ========== Running {__name__} ========== ")

        cls.models_dict = defaultdict(list)
        t_shape  = (CONNECT_PATH + "TShape.sym",)
        y_shape  = (CONNECT_PATH + "YShape.sym",)
        v_shape  = (CONNECT_PATH + "VShape_greater90.sym", CONNECT_PATH + "VShape_smaller90.sym")
        l_shape  = (CONNECT_PATH + "LShape.sym",)
        c_shape  = (CONNECT_PATH + "CShape.sym",)
        x_shape  = (CONNECT_PATH + "XShape.sym",)
        no_shape = (CONNECT_PATH + "NoShape.sym", CONNECT_PATH + "NoShape_temp.sym")

        for shape in t_shape:
            cls.models_dict["TShape"].append(cls._create_bim2walls(shape))
        for shape in y_shape:
            cls.models_dict["YShape"].append(cls._create_bim2walls(shape))
        for shape in v_shape:
            cls.models_dict["VShape"].append(cls._create_bim2walls(shape))
        for shape in l_shape:
            cls.models_dict["LShape"].append(cls._create_bim2walls(shape))
        for shape in c_shape:
            cls.models_dict["CShape"].append(cls._create_bim2walls(shape))
        for shape in x_shape:
            cls.models_dict["XShape"].append(cls._create_bim2walls(shape))
        for shape in no_shape:
            cls.models_dict["NoShape"].append(cls._create_bim2walls(shape))

        cls.recognizer = ShapeRecognizer()

    @classmethod
    def tearDownClass(cls):
        AllplanUtil.ClearUnitTestDocument()

    def test_calculate_midpoint(self):
        print("\n ========== Testing Calculate Midpoint ========== ")

        def _test_each(model_key):
            print(f" ======== Test all {model_key} models ======== ")
            for walls in self.models_dict.get(model_key, []):
                bim2wall_1, bim2wall_2 = walls
                allfaces_1 = bim2wall_1.side_faces + bim2wall_1.profile_faces + (bim2wall_1.top_face, bim2wall_1.bottom_face)
                allfaces_2 = bim2wall_2.side_faces + bim2wall_2.profile_faces + (bim2wall_2.top_face, bim2wall_2.bottom_face)
                for face_1, face_2 in product(allfaces_1, allfaces_2):
                    mid_point = self.recognizer._calculate_midpoint(face_1, face_2)
                    center_1, center_2 = face_1.center_point, face_2.center_point
                    self.assertIsInstance(mid_point, AllplanGeo.Point3D)
                    self.assertEqual(mid_point.GetDistance(center_1), mid_point.GetDistance(center_2))

        for key in ("TShape", "YShape", "LShape", "VShape", "CShape", "XShape", "NoShape"):
            _test_each(key)

    def test_check_touch(self):
        print("\n ========== Testing Check Touch ========== ")

        def _test_each(model_key):
            print(f" ======== Test all {model_key} models ======== ")
            for walls in self.models_dict.get(model_key, []):
                bim2wall_1, bim2wall_2 = walls
                allfaces_1 = bim2wall_1.side_faces + bim2wall_1.profile_faces + (bim2wall_1.top_face, bim2wall_1.bottom_face)
                allfaces_2 = bim2wall_2.side_faces + bim2wall_2.profile_faces + (bim2wall_2.top_face, bim2wall_2.bottom_face)

                negative_points = [random_point(z=randint(-10_000, -1)) for _ in range(20)]

                all_res_touch = [self.recognizer._check_touch(face_1, face_2.center_point) or self.recognizer._check_touch(face_2, face_1.center_point)
                                 for face_1, face_2 in product(allfaces_1, allfaces_2)]
                face_1_untouch = [self.recognizer._check_touch(face_1, point)
                                  for face_1, point in product(allfaces_1, negative_points)]
                face_2_untouch = [self.recognizer._check_touch(face_2, point)
                                  for face_2, point in product(allfaces_2, negative_points)]
                if model_key != "NoShape":
                    self.assertGreaterEqual(all_res_touch.count(True), 1)
                else:
                    self.assertGreaterEqual(all_res_touch.count(True), 0)
                self.assertEqual(face_1_untouch.count(True), 0)
                self.assertEqual(face_2_untouch.count(True), 0)


        for key in ("TShape", "YShape", "LShape", "VShape", "NoShape"):
            _test_each(key)

    def test_calculate_angle(self):
        print("\n ========== Testing Calculate Angle ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} models ======== ")
            for walls in self.models_dict.get(model_key, []):
                bim2wall_1, bim2wall_2 = walls
                small_angle, big_angle = self.recognizer._calculate_angle(bim2wall_1, bim2wall_2)
                if model_key in ("TShape", "LShape"):
                    self.assertAlmostEqual(small_angle, 90, delta=0.01)
                    self.assertAlmostEqual(big_angle, 90, delta=0.01)
                elif model_key in ("YShape", "VShape"):
                    self.assertGreater(big_angle, 90)
                    self.assertLess(small_angle, 90)


        for key in ("TShape", "YShape", "LShape", "VShape", "CShape", "XShape", "NoShape"):
            _test_each(key)

    def test_recognize(self):
        print("\n ========== Testing Recognize Shapes ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} models ======== ")
            for walls in self.models_dict.get(model_key, []):
                bim2wall_1, bim2wall_2 = walls
                shape_type = self.recognizer.recognize(bim2wall_1, bim2wall_2)
                if model_key == "NoShape":
                    self.assertIsNone(shape_type)
                else:
                    class_ = shape_type.value
                    self.assertIsInstance(class_, type)
                    self.assertEqual(class_.__name__, f"{model_key}Builder")

        for key in ("TShape", "YShape", "LShape", "VShape", "CShape", "XShape", "NoShape"):
            _test_each(key)

    def test_create_shape_member(self):
        print("\n ========== Testing Create ShapeMembers ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} models ======== ")
            for walls in self.models_dict.get(model_key, []):
                bim2wall_1, bim2wall_2 = walls

                self.recognizer.recognize(bim2wall_1, bim2wall_2)
                host, guest = self.recognizer._build_shape_members()

                # Test host member
                self.assertIsInstance(host, ShapeMember)
                self.assertIsInstance(host, BIM2Wall)
                self.assertTrue(hasattr(host, "direction_close_far_side"))
                self.assertTrue(hasattr(host, "closeside_face"))
                self.assertTrue(hasattr(host, "farside_face"))
                self.assertTrue(hasattr(host, "interior_face"))
                self.assertTrue(hasattr(host, "exterior_face"))
                self.assertIsInstance(host.direction_close_far_side, AllplanGeo.Vector3D)
                self.assertIsInstance(host.closeside_face, BIM2Face)
                self.assertIsInstance(host.farside_face, BIM2Face)
                self.assertIsInstance(host.interior_face, BIM2Face)
                self.assertIsInstance(host.exterior_face, BIM2Face)
                self.assertIn(host.closeside_face, host.side_faces)
                self.assertIn(host.farside_face, host.side_faces)
                self.assertIn(host.interior_face, host.profile_faces)
                self.assertIn(host.exterior_face, host.profile_faces)

                # Test guest member
                self.assertIsInstance(guest, ShapeMember)
                self.assertIsInstance(guest, BIM2Wall)
                self.assertTrue(hasattr(guest, "direction_close_far_side"))
                self.assertTrue(hasattr(guest, "closeside_face"))
                self.assertTrue(hasattr(guest, "farside_face"))
                self.assertTrue(hasattr(guest, "interior_face"))
                self.assertTrue(hasattr(guest, "exterior_face"))
                self.assertIsInstance(guest.direction_close_far_side, AllplanGeo.Vector3D)
                self.assertIsInstance(guest.closeside_face, BIM2Face)
                self.assertIsInstance(guest.farside_face, BIM2Face)
                self.assertIsInstance(guest.interior_face, BIM2Face)
                self.assertIsInstance(guest.exterior_face, BIM2Face)
                self.assertIn(guest.closeside_face, guest.side_faces)
                self.assertIn(guest.farside_face, guest.side_faces)
                self.assertIn(guest.interior_face, guest.profile_faces)
                self.assertIn(guest.exterior_face, guest.profile_faces)

        for key in ("TShape", "YShape", "LShape", "VShape", "CShape", "XShape",):
            _test_each(key)

    def _test_lv_shape(self, shape):
        # Test instance, attributes
        self.assertIsInstance(shape, LVShape)
        self.assertTrue(hasattr(shape, "angle"))
        self.assertTrue(hasattr(shape, "exterior_point"))
        self.assertTrue(hasattr(shape, "interior_point"))
        self.assertIsInstance(shape.angle, float)
        self.assertIsInstance(shape.exterior_point, AllplanGeo.Point3D)
        self.assertIsInstance(shape.interior_point, AllplanGeo.Point3D)

    def _test_v_shape(self, shape):
        self._test_lv_shape(shape)
        # Test instance, attributes
        self.assertIsInstance(shape, VShape)

        # Test value
        self.assertLess(shape.host_wall.interior_face.distance_to_point(shape.interior_point), 0.01)
        self.assertLess(shape.host_wall.exterior_face.distance_to_point(shape.exterior_point), 0.01)

    def _test_l_shape(self, shape):
        self._test_lv_shape(shape)
        # Test instance, attributes
        self.assertIsInstance(shape, LShape)

        # Test value
        self.assertLess(shape.host_wall.interior_face.distance_to_point(shape.interior_point), 0.01)
        self.assertLess(shape.host_wall.exterior_face.distance_to_point(shape.exterior_point), 0.01)
        self.assertEqual(shape.angle, 90.0)

    def _test_ty_shape(self, shape):
        # Test instance, attributes
        self.assertIsInstance(shape, TYShape)
        self.assertTrue(hasattr(shape, "direction_hostface_one_hostface_two"))
        self.assertTrue(hasattr(shape, "direction_closeface_farface"))
        self.assertTrue(hasattr(shape, "interior_point_1"))
        self.assertTrue(hasattr(shape, "interior_point_2"))
        self.assertTrue(hasattr(shape, "angle_1"))
        self.assertTrue(hasattr(shape, "angle_2"))
        self.assertIsInstance(shape.direction_hostface_one_hostface_two, AllplanGeo.Vector3D)
        self.assertIsInstance(shape.direction_closeface_farface, AllplanGeo.Vector3D)
        self.assertIsInstance(shape.interior_point_1, AllplanGeo.Point3D)
        self.assertIsInstance(shape.interior_point_2, AllplanGeo.Point3D)
        self.assertIsInstance(shape.angle_1, float)
        self.assertIsInstance(shape.angle_2, float)

    def _test_t_shape(self, shape):
        self._test_ty_shape(shape)
        # Test instance, attributes
        self.assertIsInstance(shape, TShape)

        # Test value
        self.assertLess(shape.host_wall.interior_face.distance_to_point(shape.interior_point_1), 0.01)
        self.assertLess(shape.host_wall.interior_face.distance_to_point(shape.interior_point_2), 0.01)
        self.assertEqual(shape.angle_1, 90.0)
        self.assertEqual(shape.angle_2, 90.0)

    def _test_y_shape(self, shape):
        self._test_ty_shape(shape)
        # Test instance, attributes
        self.assertIsInstance(shape, YShape)

        # Test value
        self.assertLess(shape.host_wall.interior_face.distance_to_point(shape.interior_point_1), 0.01)
        self.assertLess(shape.host_wall.interior_face.distance_to_point(shape.interior_point_2), 0.01)
        self.assertLessEqual(shape.angle_1, shape.angle_2)

    def _test_cx_shape(self, shape):
        # Test instance, attributes
        self.assertIsInstance(shape, CXShape)
        self.assertTrue(hasattr(shape, "direction_1"))
        self.assertTrue(hasattr(shape, "direction_2"))
        self.assertTrue(hasattr(shape, "face_1"))
        self.assertTrue(hasattr(shape, "face_2"))
        self.assertTrue(hasattr(shape, "face_3"))
        self.assertTrue(hasattr(shape, "face_4"))
        self.assertTrue(hasattr(shape, "face_5"))
        self.assertTrue(hasattr(shape, "face_6"))
        self.assertTrue(hasattr(shape, "face_7"))
        self.assertTrue(hasattr(shape, "face_8"))
        self.assertTrue(hasattr(shape, "intersection_point"))
        self.assertTrue(hasattr(shape, "point_1"))
        self.assertTrue(hasattr(shape, "point_2"))
        self.assertTrue(hasattr(shape, "point_3"))
        self.assertTrue(hasattr(shape, "point_4"))
        self.assertTrue(hasattr(shape, "angle_1"))
        self.assertTrue(hasattr(shape, "angle_2"))
        self.assertIsInstance(shape.direction_1, AllplanGeo.Vector3D)
        self.assertIsInstance(shape.direction_2, AllplanGeo.Vector3D)
        self.assertIsInstance(shape.face_1, BIM2Face)
        self.assertIsInstance(shape.face_2, BIM2Face)
        self.assertIsInstance(shape.face_3, BIM2Face)
        self.assertIsInstance(shape.face_4, BIM2Face)
        self.assertIsInstance(shape.face_5, BIM2Face)
        self.assertIsInstance(shape.face_6, BIM2Face)
        self.assertIsInstance(shape.face_7, BIM2Face)
        self.assertIsInstance(shape.face_8, BIM2Face)
        self.assertIsInstance(shape.intersection_point, AllplanGeo.Point3D)
        self.assertIsInstance(shape.point_1, AllplanGeo.Point3D)
        self.assertIsInstance(shape.point_2, AllplanGeo.Point3D)
        self.assertIsInstance(shape.point_3, AllplanGeo.Point3D)
        self.assertIsInstance(shape.point_4, AllplanGeo.Point3D)
        self.assertIsInstance(shape.angle_1, float)
        self.assertIsInstance(shape.angle_2, float)

    def _test_c_shape(self, shape):
        self._test_cx_shape(shape)
        # Test instance, attributes
        self.assertIsInstance(shape, CShape)

        # Test value
        self.assertEqual(shape.angle_1, 90.0)
        self.assertEqual(shape.angle_2, 90.0)

    def _test_x_shape(self, shape):
        self._test_cx_shape(shape)
        # Test instance, attributes
        self.assertIsInstance(shape, XShape)

        # Test value
        self.assertLessEqual(shape.angle_1, shape.angle_2)
        
    def _test_geometry_shape(self, shape, model_key):
            if model_key == "VShape":
                self._test_v_shape(shape)
            elif model_key == "LShape":
                self._test_l_shape(shape)
            elif model_key == "YShape":
                self._test_y_shape(shape)
            elif model_key == "TShape":
                self._test_t_shape(shape)
            elif model_key == "CShape":
                self._test_c_shape(shape)
            elif model_key == "XShape":
                self._test_x_shape(shape)

    def test_create_shape(self):
        print("\n ========== Testing Create Shape Objects ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} models ======== ")
            for walls in self.models_dict.get(model_key, []):
                bim2wall_1, bim2wall_2 = walls

                self.recognizer.recognize(bim2wall_1, bim2wall_2)
                shape = self.recognizer.create_shape()

                if model_key == "NoShape":
                    self.assertIsNone(shape)
                else:
                    self.assertIsInstance(shape, Shape)
                    self._test_geometry_shape(shape, model_key)

        for key in ("TShape", "YShape", "LShape", "VShape", "CShape", "XShape", "NoShape"):
            _test_each(key)

    @staticmethod
    def _create_bim2walls(model_name) -> list:
        bim2wall_factory = BIM2WallFactory()
        walls = AllplanUtil.LoadSymbolForUnitTest(model_name, False)
        used_walls = [ele for ele in walls if ele == AllplanElementAdapter.WallTier_TypeUUID]
        bim2walls = [bim2wall_factory.create_from(wall) for wall in used_walls]

        return bim2walls


def suite() -> unittest.TestSuite:
    """
    This defines all the tests of TestStringEvaluate

    Returns:
        test suite
    """

    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestShapeRecognizer))

    return test_suite
