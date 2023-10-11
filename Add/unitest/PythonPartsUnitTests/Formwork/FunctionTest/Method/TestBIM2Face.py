# pyright: reportGeneralTypeIssues=false
# pyright: reportOptionalSubscript=false

import unittest
from random import randint

from Formwork.Factories.BIM2FaceFactory import BIM2FaceBuilder
from Formwork.Utility.TestUtils import random_point, random_vector

import NemAll_Python_Utility as AllplanUtil

from ..TestBase import TestBase


class TestBIM2Wall(TestBase):

    @classmethod
    def setUpClass(cls):
        print(f"\n ========== Running {__name__} ========== ")

        # X plane data
        cls.x_points = [[random_point(x = 0), random_point(x = 0), random_point(x = 0), random_point(x = 0)]
                        for _ in range (0,5)]
        cls.x_vectors = [random_vector(same_y = True, same_z = True)
                         for _ in range (0,5)]

        # Y plane data
        cls.y_points = [[random_point(y = 0), random_point(y = 0), random_point(y = 0), random_point(y = 0)]
                        for _ in range (0,5)]
        cls.y_vectors = [random_vector(same_x = True, same_z = True)
                         for _ in range (0,5)]

        # Z plane data
        cls.z_points = [[random_point(z = 0), random_point(z = 0), random_point(z = 0), random_point(z = 0)]
                        for _ in range (0,5)]
        cls.z_vectors = [random_vector(same_y = True, same_x = True)
                         for _ in range (0,5)]

    @classmethod
    def tearDownClass(cls):
        AllplanUtil.ClearUnitTestDocument()

    def test_distance_to_point(self):
        print("\n ========== Testing Distance to Point ========== ")

        random_numbers = randint(0,4)
        x_face_builder = BIM2FaceBuilder(self.x_points[random_numbers], self.x_vectors[random_numbers])
        x_face = x_face_builder.set_vertices().set_normal_vector().set_edges().set_special_points().set_special_lines().build()

        y_face_builder = BIM2FaceBuilder(self.y_points[random_numbers], self.y_vectors[random_numbers])
        y_face = y_face_builder.set_vertices().set_normal_vector().set_edges().set_special_points().set_special_lines().build()

        z_face_builder = BIM2FaceBuilder(self.z_points[random_numbers], self.z_vectors[random_numbers])
        z_face = z_face_builder.set_vertices().set_normal_vector().set_edges().set_special_points().set_special_lines().build()

        print(f" ======== Faces using = X: {x_face}\n\t\t\tY: {y_face}\n\t\t\tZ: {z_face} ======== ")
        for _ in range(0,20):
            random_numbers_2 = randint(-10_000, 10_000)
            fixed_x = random_numbers_2
            fixed_y = random_numbers_2
            fixed_z = random_numbers_2
            input_point_x = random_point(x = fixed_x)
            input_point_y = random_point(y = fixed_y)
            input_point_z = random_point(z = fixed_z)

            x_dis = x_face.distance_to_point(input_point_x)
            y_dis = y_face.distance_to_point(input_point_y)
            z_dis = z_face.distance_to_point(input_point_z)

            self.assertAlmostEqual(x_dis, abs(fixed_x),
                                   msg = f"Fail when X distance = {fixed_x} and with BIM2Face: {x_face}", delta=3)
            self.assertAlmostEqual(y_dis, abs(fixed_y),
                                   msg = f"Fail when Y distance = {fixed_y} and with BIM2Face: {y_face}", delta=3)
            self.assertAlmostEqual(z_dis, abs(fixed_z),
                                   msg = f"Fail when Z distance = {fixed_z} and with BIM2Face: {z_face}", delta=3)


def suite() -> unittest.TestSuite:
    """
    This defines all the tests of TestStringEvaluate

    Returns:
        test suite
    """

    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestBIM2Wall))

    return test_suite
