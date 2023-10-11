# pyright: reportGeneralTypeIssues=false
# pyright: reportOptionalSubscript=false

import os
import random
import unittest
from collections import defaultdict

import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_Geometry as AllplanGeo
from NemAll_Python_Geometry import Point3D
import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter

from Formwork.Utility import Utility
from Formwork.BaseModules.Enumeration import FormworkSystem
from Formwork.Factories.BIM2WallFactory import BIM2WallFactory

from ..TestBase import TestBase, SINGLE_PATH

MAMMUT_350 = "Mammut 350"
MAMMUT_XT  = "Mammut XT"
TIEROD_DW15  = "Ankerstab DW15"
TIEROD_DW20  = "Ankerstab DW20"
XT_CONE_DW20 = "XT-Konusanker 20"
XT_TIE_DW20  = "XT-Anker DW20"

ETC_PATH = AllplanSettings.AllplanPaths.GetEtcPath()
MODEL_PATH    = os.path.join(ETC_PATH, "Library", "Construction", "Formwork")
M350_PATH = os.path.join(MODEL_PATH, "Meva", "Mammut 350")
MXT_PATH  = os.path.join(MODEL_PATH, "Meva", "Mammut XT")
M350 = FormworkSystem.Mammut350.value
MXT  = FormworkSystem.MammutXT.value
SINGLE_WALL = SINGLE_PATH + "cut_wall_1.sym"


class TestUtility(TestBase):

    @classmethod
    def setUpClass(cls):
        print(f"\n ========== Running {__name__} ========== ")

        cls.wall_dict = defaultdict(list)
        single_walls  = (SINGLE_PATH + "cut_wall_2.sym",
                         SINGLE_PATH + "wall_2_layer.sym",
                         SINGLE_PATH + "wall_2_opening.sym",)

        for wall in single_walls:
            cls.wall_dict["SingleWalls"].append(cls._create_bim2walls(wall))

    @classmethod
    def tearDownClass(cls):
        AllplanUtil.ClearUnitTestDocument()

    def getRandomPoint3D_50_records(self):
        rand_int_lst = [19913,89151,2040,6703,46662,46573,35619,72804,37018,45887,
                        1151,21867,54534,65359,36997,2324,9669,75834,99691,1677,9241]
        random_point_list = []
        for x in rand_int_lst:
            for y in rand_int_lst:
                for z in rand_int_lst:
                    random_point_x = x
                    random_point_y = y
                    random_point_z = z
                    random_point_list.append(AllplanGeo.Point3D(float(random_point_x/100),
                                                                float(random_point_y/100),
                                                                float(random_point_z/100)))
        return random_point_list

    def test_get_attribute(self):
        print("\n ========== Testing Get attribute by element and integer ========== ")

        single_wall = SINGLE_PATH + "cut_wall_1.sym"
        wall = AllplanUtil.LoadSymbolForUnitTest(single_wall, False)
        self.assertIsInstance(wall[4], AllplanElementAdapter.BaseElementAdapter)
        test_result = Utility.get_attribute(wall[4], 209)
        self.assertEqual(test_result, "Concreting work")

    def test_compare_string(self):
        print("\n ========== Testing Get attribute by element and integer ========== ")
        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        str_1 = self.build_ele.System.value
        str_2 = MAMMUT_350
        test_result = Utility.compare_string(str_1, str_2)
        self.assertIsInstance(test_result, bool)
        self.assertEqual(test_result, True)

    def test_get_element_base_points(self):
        print("\n ========== Testing Get element base points ========== ")

        single_wall = SINGLE_WALL
        wall = AllplanUtil.LoadSymbolForUnitTest(single_wall, False)
        self.assertIsInstance(wall[4], AllplanElementAdapter.BaseElementAdapter)
        test_result = Utility.get_element_base_points(wall[4])
        self.assertIsInstance(test_result, list)

    def test_check_polyhedron_min_z_and_base_points(self):
        print("\n ========== Testing Get check polyhedron min z and base points ========== ")

        single_wall = SINGLE_WALL
        wall = AllplanUtil.LoadSymbolForUnitTest(single_wall, False)
        self.assertIsInstance(wall[4], AllplanElementAdapter.BaseElementAdapter)
        ele_base_pnts = []
        ele_polyhedrons = wall[4].GetModelGeometry()
        if not isinstance(ele_polyhedrons, list):
            ele_polyhedrons = [ele_polyhedrons]
        min_z = float('inf')

        for ele_poly in ele_polyhedrons:
            test_result = Utility._check_polyhedron_min_z(ele_poly, min_z)
            self.assertIsInstance(test_result, float)

        for ele_poly in ele_polyhedrons:
            test_result = Utility._check_polyhedron_get_base_points(ele_base_pnts, ele_poly, min_z, 0)
            self.assertIsInstance(test_result, list)

        for ele_poly in ele_polyhedrons:
            test_result = Utility._check_type_points(ele_poly)
            self.assertIsInstance(test_result[0], AllplanGeo.Point3D)

    def test_turn(self):
        print("\n ========== Testing check turn for 3 point========== ")

        data_test = [
            [(Point3D(4800.33, 4585.3, 480.4), Point3D(7213.06, 2433.95, 7621.71), Point3D(3516.91, 8233.34, 7319.22)), 'left'],
            [(Point3D(5630.81, 7452.82, 6993.01), Point3D(5833.39, 4453.99, 8184.13), Point3D(6013.1, 6714.24, 3847.65)), 'left'],
            [(Point3D(2490.8, 4088.51, 9107.51), Point3D(7142.16, 9175.07, 4107.22), Point3D(9549.16, 9161.84, 9357.18)), 'right'],
            [(Point3D(2829.93, 3638.88, 6571.35), Point3D(8087.98, 9089.85, 3258.99), Point3D(9605.53, 7990.36, 3602.79)), 'right'],
            [(Point3D(6619.69, 2416.51, 234.51), Point3D(7360.16, 80.95, 8049.43), Point3D(7874.92, 2165.32, 7538.95)), 'left'],
            [(Point3D(5704.81, 2476.94, 9154.29), Point3D(3627.43, 9038.29, 9036.22), Point3D(7920.02, 4187.59, 2017.25)), 'right'],
            [(Point3D(5805.84, 7187.6, 2806.85), Point3D(6111.14, 7295.46, 5956.08), Point3D(4200.88, 7227.14, 4925.77)), 'left'],
            [(Point3D(7195.98, 9159.03, 1553.72), Point3D(2315.59, 2911.24, 1729.01), Point3D(7017.88, 8998.97, 761.04)), 'right'],
            [(Point3D(2692.05, 3176.45, 5381.6), Point3D(4557.07, 7137.82, 8632.83), Point3D(9883.65, 6489.34, 8866.73)), 'right'],
            [(Point3D(5024.63, 5175.86, 9219.1), Point3D(1283.79, 2359.69, 3554.33), Point3D(9790.06, 4401.42, 8072.81)), 'left'],
            [(Point3D(3628.01, 6007.91, 5195.53), Point3D(3174.44, 1430.7, 9878.54), Point3D(2020.2, 5120.53, 9591.37)), 'right'],
            [(Point3D(3504.32, 1846.14, 4302.98), Point3D(3168.33, 2408.86, 5817.54), Point3D(485.84, 4523.72, 2950.09)), 'left'],
            [(Point3D(5990.04, 1846.72, 6835.13), Point3D(3413, 4064.26, 2036.27), Point3D(7657.07, 7696.58, 6732.36)), 'right'],
            [(Point3D(4526.71, 4456.54, 1951.07), Point3D(1886.14, 5352.09, 7026.06), Point3D(2363.48, 1018.01, 1750.44)), 'left'],
            [(Point3D(8895.35, 2940.04, 2331.25), Point3D(3286.07, 9137.37, 4932.69), Point3D(376.55, 151.54, 1628.49)), 'left'],
            [(Point3D(4510.78, 1653.98, 2590.45), Point3D(7698.31, 9394.14, 4096.69), Point3D(7627.1, 4632.62, 7286.7)), 'right'],
            [(Point3D(8648.3, 6083.77, 4024.39), Point3D(2146.22, 3332.51, 9031.71), Point3D(1663.69, 8735.26, 2408.62)), 'right'],
            [(Point3D(1010.14, 6739.12, 4053.86), Point3D(8135.3, 6941.19, 2695.77), Point3D(1219.18, 8325.6, 7152.39)), 'left'],
            [(Point3D(3398.46, 4967.12, 9219.34), Point3D(2318.04, 7997.6, 1692.98), Point3D(5330.65, 8338.86, 239.59)), 'right'],
            [(Point3D(3667.1, 8896.27, 3825.34), Point3D(1899.71, 613.61, 4244.45), Point3D(9956.65, 3623.47, 6412)), 'left']
        ]

        for test_case in data_test:
            check = Utility.turn(test_case[0][0],test_case[0][1],test_case[0][2])
            self.assertIsInstance(check, str)
            self.assertEqual(check, test_case[1])

    def test_half_hull(self):
        print("\n ========== Testing get half hull of list Point3D ========== ")

        data_test = self.getRandomPoint3D_50_records()
        data_test.append(data_test[25])

        test_result = Utility.half_hull(data_test)
        self.assertIsInstance(test_result, list)
        self.assertLess(len(test_result), len(data_test))

    def test_convex_hull(self):
        print("\n ========== Testing get convex hull of list Point3D ========== ")

        data_test = self.getRandomPoint3D_50_records()
        data_test.append(data_test[25])

        test_result = Utility.convex_hull(data_test)
        self.assertIsInstance(test_result, list)
        self.assertLess(len(test_result), len(data_test))

    def test_get_nearest_point_with_another_point(self):
        print("\n ========== Testing get_nearest_point_with_another_point ========== ")
        data_test = [
            [Point3D(0, 0, 0), [Point3D(23, 36, 0), Point3D(70, 83, 0), Point3D(110, 123, 0), Point3D(107, 120, 0),
                                Point3D(50, 63, 0), Point3D(25, 38, 0), Point3D(101, 114, 0), Point3D(83, 96, 0),
                                Point3D(107, 120, 0), Point3D(38, 51, 0), Point3D(117, 130, 0)], Point3D(23, 36, 0)],
            [Point3D(0, 0, 0), [Point3D(23, 12, 0), Point3D(53, 42, 0), Point3D(45, 34, 0), Point3D(71, 60, 0),
                                Point3D(49, 38, 0), Point3D(46, 35, 0), Point3D(28, 17, 0), Point3D(120, 109, 0),
                                Point3D(78, 67, 0), Point3D(34, 23, 0), Point3D(59, 48, 0)], Point3D(23, 12, 0)],
            [Point3D(0, 0, 0), [Point3D(5, 98, 0), Point3D(31, 124, 0), Point3D(99, 192, 0), Point3D(37, 130, 0),
                                Point3D(27, 120, 0), Point3D(19, 112, 0), Point3D(32, 125, 0), Point3D(51, 144, 0),
                                Point3D(77, 170, 0), Point3D(20, 113, 0), Point3D(61, 154, 0)], Point3D(5, 98, 0)],
            [Point3D(0, 0, 0), [Point3D(35, 1, 0), Point3D(115, 81, 0), Point3D(84, 50, 0), Point3D(91, 57, 0),
                                Point3D(104, 70, 0), Point3D(100, 66, 0), Point3D(84, 50, 0), Point3D(43, 9, 0),
                                Point3D(132, 98, 0), Point3D(86, 52, 0), Point3D(79, 45, 0)], Point3D(35, 1, 0)],
            [Point3D(0, 0, 0), [Point3D(62, 81, 0), Point3D(106, 125, 0), Point3D(123, 142, 0), Point3D(84, 103, 0),
                                Point3D(86, 105, 0), Point3D(101, 120, 0), Point3D(111, 130, 0), Point3D(78, 97, 0),
                                Point3D(158, 177, 0), Point3D(88, 107, 0), Point3D(91, 110, 0)], Point3D(62, 81, 0)],
            [Point3D(0, 0, 0), [Point3D(7, 13, 0), Point3D(20, 26, 0), Point3D(78, 84, 0), Point3D(65, 71, 0),
                                Point3D(21, 27, 0), Point3D(91, 97, 0), Point3D(100, 106, 0), Point3D(91, 97, 0),
                                Point3D(14, 20, 0), Point3D(31, 37, 0), Point3D(100, 106, 0)], Point3D(7, 13, 0)],
            [Point3D(0, 0, 0), [Point3D(85, 92, 0), Point3D(185, 192, 0), Point3D(169, 176, 0), Point3D(91, 98, 0),
                                Point3D(161, 168, 0), Point3D(155, 162, 0), Point3D(123, 130, 0), Point3D(122, 129, 0),
                                Point3D(140, 147, 0), Point3D(109, 116, 0), Point3D(89, 96, 0)], Point3D(85, 92, 0)],
            [Point3D(0, 0, 0), [Point3D(31, 21, 0), Point3D(60, 50, 0), Point3D(78, 68, 0), Point3D(66, 56, 0),
                                Point3D(111, 101, 0), Point3D(53, 43, 0), Point3D(104, 94, 0), Point3D(100, 90, 0),
                                Point3D(94, 84, 0), Point3D(50, 40, 0), Point3D(97, 87, 0)], Point3D(31, 21, 0)],
            [Point3D(0, 0, 0), [Point3D(41, 76, 0), Point3D(112, 147, 0), Point3D(98, 133, 0), Point3D(103, 138, 0),
                                Point3D(74, 109, 0), Point3D(59, 94, 0), Point3D(78, 113, 0), Point3D(51, 86, 0),
                                Point3D(73, 108, 0), Point3D(44, 79, 0), Point3D(42, 77, 0)], Point3D(41, 76, 0)],
            [Point3D(0, 0, 0), [Point3D(58, 46, 0), Point3D(123, 111, 0), Point3D(103, 91, 0), Point3D(80, 68, 0),
                                Point3D(149, 137, 0), Point3D(114, 102, 0), Point3D(77, 65, 0), Point3D(137, 125, 0),
                                Point3D(110, 98, 0), Point3D(114, 102, 0), Point3D(118, 106, 0)], Point3D(58, 46, 0)],
            [Point3D(0, 0, 0), [Point3D(80, 62, 0), Point3D(81, 63, 0), Point3D(138, 120, 0), Point3D(114, 96, 0),
                                Point3D(156, 138, 0), Point3D(137, 119, 0), Point3D(121, 103, 0), Point3D(153, 135, 0),
                                Point3D(161, 143, 0), Point3D(122, 104, 0), Point3D(156, 138, 0)], Point3D(80, 62, 0)]
        ]

        for test_case in data_test:
            test_result = Utility.get_nearest_point_with_another_point(test_case[0], test_case[1])
            self.assertIsInstance(test_result, AllplanGeo.Point3D)
            self.assertEqual(test_result, test_case[2])

    def test_get_two_element_end_points(self):
        print("\n ========== Testing get_two_element_end_points ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} ======== ")
            for bim2wall in self.wall_dict.get(model_key, []):
                if bim2wall:
                    result_end_pnts = []
                    result_end_pnts.append(bim2wall[0].start_point)
                    result_end_pnts.append(bim2wall[0].end_point)
                    extend_endpnts = self.getRandomPoint3D_50_records()
                    for pnt in extend_endpnts:
                        pnt.Z = 0
                    result_end_pnts.extend(extend_endpnts)
                    test_result = Utility.get_two_element_end_points(bim2wall[0], result_end_pnts)
                    self.assertIsInstance(test_result, tuple)
                    self.assertIsInstance(test_result[0], list)
                    self.assertIsInstance(test_result[1], AllplanGeo.Vector3D)
                    self.assertIsInstance(test_result[0][0], AllplanGeo.Point3D)
                    self.assertIsInstance(test_result[0][1], AllplanGeo.Point3D)
                    self.assertIn(test_result[0][0], result_end_pnts[0:2])
                    self.assertIn(test_result[0][1], result_end_pnts[0:2])

        for key in ("SingleWalls",):
            _test_each(key)

    def test_arrange_to_same_orientation(self):
        print("\n ========== Testing arrange to same orientation ========== ")

        data_test = []
        pnt1s = self.getRandomPoint3D_50_records()
        pnt2s = self.getRandomPoint3D_50_records()
        for pnt1, pnt2 in zip(pnt1s, pnt2s):
            data_test.append((pnt1, pnt2, AllplanGeo.Vector3D(pnt1, pnt2), pnt1, pnt2))

        for test_case in data_test:
            test_result = Utility.arrange_to_same_orientation(test_case[0], test_case[1], test_case[2])
            self.assertIsInstance(test_result, tuple)
            self.assertIsInstance(test_result[0], AllplanGeo.Point3D)
            self.assertIsInstance(test_result[1], AllplanGeo.Point3D)
            self.assertEqual(test_result[0], test_case[3])
            self.assertEqual(test_result[1], test_case[4])

    def test_get_best_combination_without_fillers(self):
        print("\n ========== Testing Get best combination without fillers ========== ")

        usable_widths = [1250.0, 450.0, 550.0, 1000.0, 300.0, 750.0, 500.0, 250.0]
        data_tests = [
            [4497.8, 4697.27, False, [1250.0, 1250.0, 1250.0, 750.0]],
            [159.76, 479.14, False, [250.0]],
            [2704.61, 3000.61, False, [1250.0, 750.0, 750.0]],
            [4844.78, 5155.16, False, [1250.0, 1250.0, 1250.0, 1250.0]],
            [7355.54, 7436.7699999999995, False, [1250.0, 1250.0, 1250.0, 1000.0, 1000.0, 550.0, 550.0, 550.0]],
            [9955.58, 10284.26, False, [1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0]],
            [3999.93, 4004.43, False, [1250.0, 1250.0, 750.0, 750.0]],
            [7891.02, 7917.1900000000005, False, [1250.0, 1250.0, 1250.0, 1250.0, 1000.0, 1000.0, 450.0, 450.0]],
            [6957.63, 7351.31, False, [1250.0, 1250.0, 1250.0, 1250.0, 1000.0, 1000.0]],
            [5108.54, 5325.08, False, [1250.0, 1250.0, 1250.0, 1000.0, 450.0]],
            [5985.76, 6152.13, False, [1250.0, 1250.0, 1250.0, 1250.0, 1000.0]],
            [7929.73, 8060.849999999999, False, [1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 450.0]],
            [7417.9, 7580.099999999999, False, [1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0]],
            [3702.34, 3763.27, False, [1250.0, 1250.0, 1250.0]],
            [3514.78, 3580.57, False, [1250.0, 1250.0, 550.0, 500.0]],
            [7606.56, 8000.02, False, [1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1000.0, 450.0]],
            [2207.16, 2528.1099999999997, False, [1250.0, 1000.0]],
            [1812.83, 2168.24, False, [1250.0, 750.0]],
            [1244.61, 1393.1, False, [1250.0]],
            [2672.48, 3098.84, False, [1250.0, 1000.0, 450.0]],
            [7510.42, 7861.35, False, [1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1000.0, 300.0]],
            [5385.62, 5703.21, False, [1250.0, 1250.0, 1250.0, 1250.0, 450.0]],
            [3910.17, 4043.41, False, [1250.0, 1250.0, 1000.0, 450.0]],
            [8416.75, 8733.78, False, [1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1000.0]],
            [9313.13, 9736.06, False, [1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1000.0, 1000.0]],
            [3133.93, 3557.08, False, [1250.0, 1250.0, 750.0]],
            [842.1, 1151.13, False, [1000.0]],
            [4333.15, 4773.219999999999, False, [1250.0, 1250.0, 1250.0, 750.0]],
            [7157.78, 7295.63, False, [1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1000.0]],
            [9719.06, 9916.029999999999, False, [1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1000.0]],
            [7849.36, 8121.799999999999, False, [1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 450.0]],
            [5116.17, 5357.38, False, [1250.0, 1250.0, 1250.0, 1000.0, 450.0]],
            [619.47, 1008.94, False, [750.0]],
            [2777.4, 2910.81, False, [1250.0, 1000.0, 550.0]],
        ]

        for test_case in data_tests:
            test_result = Utility.get_best_combination_without_fillers(usable_widths, test_case[0], test_case[1], test_case[2])
            self.assertIsInstance(test_result, list)
            self.assertEqual(test_result, test_case[3])

    def test_get_best_combination_with_fillers(self):
        print("\n ========== Testing Get best combination with fillers ========== ")

        usable_widths = [1250.0, 450.0, 550.0, 1000.0, 300.0, 750.0, 500.0, 250.0]
        data_tests_2 = [
            [4497.8, ([1250.0, 1000.0, 1000.0, 750.0, 450.0], 47.80000000000018)],
            [159.76, ([], 159.76)],
            [2704.61, ([1250.0, 1000.0, 450.0], 4.610000000000127)],
            [4844.78, ([1250.0, 1250.0, 1250.0, 1000.0], 94.77999999999975)],
            [7355.54, ([1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1000.0], 105.53999999999996)],
            [9955.58, ([1250.0, 1250.0, 1250.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 750.0, 450.0], 5.579999999999927)],
            [3999.93, ([1250.0, 1250.0, 1000.0, 450.0], 49.929999999999836)],
            [7891.02, ([1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1000.0, 550.0], 91.02000000000044)],
            [6957.63, ([1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 550.0], 157.6300000000001)],
            [5108.54, ([1250.0, 1250.0, 1250.0, 1250.0], 108.53999999999996)],
            [5985.76, ([1250.0, 1250.0, 1250.0, 1000.0, 750.0, 450.0], 35.76000000000022)],
            [7929.73, ([1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1000.0, 550.0], 129.72999999999956)],
            [7417.9, ([1250.0, 1250.0, 1250.0, 1000.0, 1000.0, 1000.0, 550.0], 117.89999999999964)],
            [3702.34, ([1250.0, 1250.0, 750.0, 450.0], 2.3400000000001455)],
            [3514.78, ([1250.0, 1250.0, 1000.0], 14.7800000000002)],
            [7606.56, ([1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0], 106.5600000000004)],
            [2207.16, ([1250.0, 500.0, 450.0], 7.1599999999998545)],
            [1812.83, ([1250.0, 550.0], 12.829999999999927)],
            [1244.61, ([750.0, 450.0], 44.6099999999999)],
            [2672.48, ([1250.0, 750.0, 550.0], 122.48000000000002)],
            [7510.42, ([1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0], 10.420000000000073)],
            [5385.62, ([1250.0, 1250.0, 1250.0, 1000.0, 550.0], 85.61999999999989)],
            [3910.17, ([1250.0, 1250.0, 750.0, 550.0], 110.17000000000007)],
            [8416.75, ([1250.0, 1250.0, 1250.0, 1000.0, 1000.0, 1000.0, 1000.0, 550.0], 116.75)],
            [9313.13, ([1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 550.0], 13.1299999999992)],
            [3133.93, ([1250.0, 1250.0, 550.0], 83.92999999999984)],
            [842.1, ([750.0], 92.10000000000002)],
            [4333.15, ([1250.0, 1250.0, 1250.0, 550.0], 33.149999999999636)],
            [7157.78, ([1250.0, 1250.0, 1250.0, 1250.0, 1000.0, 1000.0], 157.77999999999975)],
            [9719.06, ([1250.0, 1250.0, 1250.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 500.0, 450.0], 19.05999999999949)],
            [7849.36, ([1250.0, 1250.0, 1250.0, 1250.0, 1250.0, 1000.0, 550.0], 49.35999999999967)],
            [5116.17, ([1250.0, 1250.0, 1250.0, 1250.0], 116.17000000000007)],
            [619.47, ([550.0], 69.47000000000003)],
            [2777.4, ([1250.0, 1000.0, 500.0], 27.40000000000009)]
        ]

        for test_case in data_tests_2:
            max_filler_width = 160.0
            test_result = Utility.get_best_combination_with_fillers(usable_widths, test_case[0], max_filler_width)
            self.assertIsInstance(test_result, tuple)
            self.assertEqual(test_result[0], test_case[1][0])

    def test_find_and_replace_string(self):
        print("\n ========== Testing find and replace string ========== ")
        original_string =  "Testing find and replace string"
        pattern = "Testing"
        replacement = "Checked"
        target_string =  "Checked find and replace string"
        test_result = Utility.find_and_replace_string(original_string, pattern, replacement)
        self.assertIsInstance(test_result, str)
        self.assertEqual(test_result, target_string)

    def test_replace_dict_string(self):
        print("\n ========== Testing replace dict string ========== ")
        pattern = "Testing"
        replace_dict = {
            "Testing" : "Passed",
        }
        test_result = Utility.replace_dict_string(pattern, replace_dict, swap= False)
        self.assertIsInstance(test_result, str)
        self.assertEqual(test_result, "Passed")

    def test_format_show_units(self):
        print("\n ========== Testing format show units ========== ")
        test_result = Utility.format_show_units((1250, 2500, 3000, 3500))
        target_result = "1.25 m, 2.50 m, 3.00 m, 3.50 m"
        self.assertIsInstance(test_result, str)
        self.assertEqual(test_result, target_result)

    def test_check_tierod_and_flange_nuts_mammut350(self):
        print("\n ========== Run test_check_tierod_and_flange_nuts_mammut350 ========== ")

        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        test_result = Utility._check_tierod_and_flange_nuts_mammut350(self.str_table, self.build_ele)

        self.assertIsInstance(test_result, tuple)
        self.assertEqual(test_result, ('Tie Rod DW15', 'Ankerstab DW15', 'Tie Rod DW15', 'Tie Rod DW20'))

    def test_check_single_sided_tierod_mammutxt(self):
        print("\n ========== Run test_check_single_sided_tierod_mammutxt ========== ")

        self.interactor.modify_element_property(0, "System", MAMMUT_XT)
        test_result = Utility._check_single_sided_tierod_mammutxt(self.str_table, self.build_ele)

        self.assertIsInstance(test_result, tuple)
        self.assertEqual(test_result, ('XT-Cone DW20', 'XT-Konusanker 20', 'Tie Rod DW20', 'XT-Cone DW20', 'XT-Tie DW20'))

    def test_change_distance_tierod_constellation(self):
        print("\n ========== Testing change distance tierod constellation ========== ")
        tuples_value = ((125.0, 550.0), (125.0, 1950.0), ())
        new_value = 155.0
        test_result = Utility.change_distance_tierod_constellation(tuples_value, new_value)
        target_result = ((155.0, 550.0), (155.0, 1950.0))
        self.assertIsInstance(test_result, tuple)
        self.assertEqual(test_result, target_result)

    def test_check_compare_to_get_extension_by_system(self):
        print("\n ========== Testing check compare to get extension by system ========== ")

        data_tests = [
            (MAMMUT_350, ['MEVA-OID-010-060', 'MEVA-EID-060', 'Mammut350'], False, 'MEVA-EID-060'),
            (MAMMUT_XT,  ['MEVA-OID-010-080', 'MEVA-EID-080', 'MammutXT'],  False, 'MEVA-EID-080'),
            (MAMMUT_XT,  ['MEVA-OID-010-080', 'MEVA-EID-080', 'MammutXT'],  True,  'MEVA-EID-081')
        ]
        for data_row in data_tests:
            self.interactor.modify_element_property(0, "System", data_row[0])
            test_result = Utility.check_compare_to_get_extension_by_system(
                data_row[0], data_row[1], data_row[2])
            self.assertIsInstance(test_result, str)
            self.assertEqual(test_result, data_row[3])

    def test_is_single_sided_tierod(self):
        print("\n ========== Testing is single sided tierod ========== ")
        data_tests = [
            (MAMMUT_350, TIEROD_DW15,  False),
            (MAMMUT_350, TIEROD_DW20,  False),
            (MAMMUT_XT,  XT_TIE_DW20,  True),
            (MAMMUT_XT,  XT_CONE_DW20, True),
        ]
        for data_row in data_tests:
            self.interactor.modify_element_property(0, "System", data_row[0])
            test_result = Utility.is_single_sided_tierod(self.str_table, self.build_ele)
            self.assertIsInstance(test_result, bool)
            self.assertEqual(test_result, data_row[2])

    def test_check_system_path(self):
        print("\n ========== Testing check system path ========== ")
        data_tests = [
            (MAMMUT_350, M350_PATH, M350, True),
            (MAMMUT_350, M350_PATH, MXT,  False),
            (MAMMUT_XT,  MXT_PATH,  M350, False),
            (MAMMUT_XT,  MXT_PATH,  MXT,  True)
        ]
        for data_row in data_tests:
            self.interactor.modify_element_property(0, "System", data_row[0])
            current_system = self.build_ele.System.value
            test_result = Utility.check_system_path(current_system)
            self.assertIsInstance(test_result, str)
            endswith_result = test_result.replace(" ", "").endswith(data_row[2])
            self.assertEqual(endswith_result, data_row[3])

    def test_get_unique_value_from_nested_list(self):
        print("\n ========== Testing get unique value from nested list ========== ")
        nested_list = [["value1", "value1"], ["value1", "value1"], ["value1", "value1"]]
        target = ["value1"]
        test_result = Utility.get_unique_value_from_nested_list(nested_list)
        self.assertIsInstance(test_result, list)
        self.assertEqual(test_result, target)

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

    test_suite.addTest(unittest.makeSuite(TestUtility))

    return test_suite
