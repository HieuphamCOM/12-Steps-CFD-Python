# pyright: reportGeneralTypeIssues=false
# pyright: reportOptionalSubscript=false

import random
import unittest
from numbers import Real
from collections import defaultdict

import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
from Utils.TabularDataUtil import DataFrame

from Formwork.Data.DataHandler import DataHandler
from Formwork.BaseModules.Enumeration import FormworkElement
from Formwork.Factories.BIM2WallFactory import BIM2WallFactory

from Formwork.Utility.Utility import get_best_combination_without_fillers
from Formwork.Utility.TestUtils import randint

from ..TestBase import TestBase, SINGLE_PATH

MAMMUT_350   = "Mammut 350"
MAMMUT_XT    = "Mammut XT"
TIEROD_DW15  = "Ankerstab DW15"
TIEROD_DW20  = "Ankerstab DW20"
XT_CONE_DW20 = "XT-Konusanker 20"
XT_TIE_DW20  = "XT-Anker DW20"


class TestDataHandler(TestBase):

    @classmethod
    def setUpClass(cls):
        print(f"\n ========== Running {__name__} ========== ")
        cls.data_handler = DataHandler()
        cls.wall_dict = defaultdict(list)
        single_walls  = (SINGLE_PATH + "cut_wall_1.sym",
                         SINGLE_PATH + "cut_wall_2.sym",
                         SINGLE_PATH + "wall_2_layer.sym",
                         SINGLE_PATH + "wall_2_opening.sym",)

        for wall in single_walls:
            cls.wall_dict["SingleWalls"].append(cls._create_bim2walls(wall))

    @classmethod
    def tearDownClass(cls):
        AllplanUtil.ClearUnitTestDocument()

    def test_create_handler(self):
        print("\n ========== Testing Create Data Handler ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        # Test attributes
        self.assertTrue(hasattr(data_handler, "db_file"))
        self.assertTrue(hasattr(data_handler, "db_path"))
        self.assertTrue(hasattr(data_handler, "data"))

        # Test instance
        self.assertIsInstance(data_handler, DataHandler)
        self.assertIsInstance(data_handler.db_file, str)
        self.assertIsInstance(data_handler.db_path, str)
        self.assertIsInstance(data_handler.data, dict)

    def test_get_formwork_element_type_mammut_350(self):
        print("\n ========== Testing get formwork element type for Mammut 350 ========== ")

        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        data_handler = DataHandler(build_ele=self.build_ele)
        data_test = [
            ("M350_InI_350x250", "Grossflaechenelement"),
            ("M350_InI_350x125", "Element"),
            ("M350_InI_350x100", "Element"),
            ("M350_InI_350x75", "Element"),
            ("M350_InI_350x55", "Element"),
            ("M350_InI_350x50", "Element"),
            ("M350_InI_350x45", "Element"),
            ("M350_InI_350x30", "Element"),
            ("M350_InI_350x25", "Element"),
            ("M350_InI_300x250", "Grossflaechenelement"),
            ("M350_InI_300x125", "Element"),
            ("M350_InI_300x100", "Element"),
            ("M350_InI_300x75", "Element"),
            ("M350_InI_300x55", "Element"),
            ("M350_InI_300x50", "Element"),
            ("M350_InI_300x45", "Element"),
            ("M350_InI_300x30", "Element"),
            ("M350_InI_300x25", "Element"),
            ("M350_InI_250x125", "Element"),
            ("M350_InI_250x100", "Element"),
            ("M350_InI_250x75", "Element"),
            ("M350_InI_250x55", "Element"),
            ("M350_InI_250x50", "Element"),
            ("M350_InI_250x45", "Element"),
            ("M350_InI_250x30", "Element"),
            ("M350_InI_250x25", "Element"),
            ("M350_InI_125x125", "Element"),
            ("M350_InI_125x100", "Element"),
            ("M350_InI_125x75", "Element"),
            ("M350_InI_125x55", "Element"),
            ("M350_InI_125x50", "Element"),
            ("M350_InI_125x45", "Element"),
            ("M350_InI_125x30", "Element"),
            ("M350_InI_125x25", "Element"),
            ("M350_InI_IC350", "Innenecke"),
            ("M350_InI_IC300", "Innenecke"),
            ("M350_InI_IC250", "Innenecke"),
            ("M350_InI_IC125", "Innenecke"),
            ("M350_InI_OC350", "Aussenecke"),
            ("M350_InI_OC300", "Aussenecke"),
            ("M350_InI_OC250", "Aussenecke"),
            ("M350_InI_OC125", "Aussenecke"),
            ("M350_InI_AIC350", "Gelenkinnenecke"),
            ("M_InI_AIC300", "Gelenkinnenecke"),
            ("M_InI_AIC250", "Gelenkinnenecke"),
            ("M_InI_AIC125", "Gelenkinnenecke"),
            ("M350_InI_AOC350", "Gelenkaussenecke"),
            ("M_InI_AOC300", "Gelenkaussenecke"),
            ("M_InI_AOC250", "Gelenkaussenecke"),
            ("M_InI_AOC125", "Gelenkaussenecke"),
        ]
        
        for test_case in data_test:
            check = data_handler.get_formwork_element_type(test_case[0])
            self.assertIsInstance(check, str)
            self.assertEqual(check, test_case[1])

    def test_get_product_by_system_mammut_350(self):
        print("\n ========== Testing Get Product by System for Mammut_350 ========== ")
        
        data_handler = DataHandler(build_ele=self.build_ele)
        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        current_system = self.build_ele.System.value
        results = data_handler._get_product_by_system(current_system)
        self.assertIsInstance(results, list)
        self.assertEqual(results[0], 'MEVA-OID-010-060')
        self.assertEqual(results[1], 'MEVA-EID-060')
        self.assertEqual(results[2], 'Mammut350')
        
    def test_get_product_by_system_mammut_xt(self):
        print("\n ========== Testing Get Product by System for Mammut_XT ========== ")
        
        data_handler = DataHandler(build_ele=self.build_ele)
        self.interactor.modify_element_property(0, "System", MAMMUT_XT)
        current_system = self.build_ele.System.value
        results = data_handler._get_product_by_system(current_system)
        self.assertIsInstance(results, list)
        self.assertEqual(results[0], 'MEVA-OID-010-080')
        self.assertEqual(results[1], 'MEVA-EID-080')
        self.assertEqual(results[2], 'MammutXT')
        
    def test_filter_dataframe_by_system(self):
        print("\n ========== Testing Filter DataFrame by System ========== ")
        
        data_handler = DataHandler(build_ele=self.build_ele)
        self.interactor.modify_element_property(0, "System", MAMMUT_XT)
        current_system = self.build_ele.System.value
        
        objectid = data_handler.data.get('ObjectID', None)
        prefix_mammut = data_handler._get_product_by_system(current_system)
        data_filtered = data_handler.filter_dataframe_by_system(objectid, 'ObjectID', prefix_mammut[0])
        self.assertIsInstance(data_filtered, dict)

    def test_get_height_constellation(self):
        print("\n ========== Testing Create Height Constellation ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        for _ in range(50):
            wall_height = randint(0, 10750)
            if wall_height in range(1251, 2501):
                continue
            result = data_handler.get_height_constellation(wall_height)
            self.assertIsInstance(result, list)

    def test_get_inside_square_corner(self):
        print("\n ========== Testing Get Inside Square Corner ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        self.assertTrue(hasattr(data_handler, "get_inside_square_corner"))

        constellation = data_handler.get_height_constellation(randint(1900, 5000))
        inside_corners = data_handler.get_inside_square_corner(constellation)

        self.assertIsInstance(inside_corners, tuple)
        for name in inside_corners:
            self.assertIsInstance(name, str)

    def test_get_inside_square_corner_mxt(self):
        print("\n ========== Testing Get Inside Square Corner  Mammut XT ========== ")
        
        for _ in range(50):
            wall_thickness = randint(150, 500)
            if wall_thickness in range(0, 150):
                continue
        data_handler = DataHandler(build_ele=self.build_ele)
        self.assertTrue(hasattr(data_handler, "get_inside_square_corner_mxt"))
        constellation = data_handler.get_height_constellation(randint(1900, 5000))
        inside_corners = data_handler.get_inside_square_corner_mxt(constellation, wall_thickness)

        self.assertIsInstance(inside_corners, tuple)
        for name in inside_corners:
            self.assertIsInstance(name, str)

    def test_get_outside_square_corner_mxt(self):
        print("\n ========== Testing Get Outside Square Corner Mammut XT ========== ")
        for _ in range(50):
            wall_thickness = randint(150, 500)
            if wall_thickness in range(0, 150):
                continue
        data_handler = DataHandler(build_ele=self.build_ele)
        self.assertTrue(hasattr(data_handler, "get_outside_square_corner_mxt"))
        constellation = data_handler.get_height_constellation(randint(1900, 5000))
        outside_corners = data_handler.get_outside_square_corner_mxt(constellation, wall_thickness)

        self.assertIsInstance(outside_corners, tuple)
        for name in outside_corners:
            self.assertIsInstance(name, str)

    def test_get_suitable_panel(self):
        print("\n ========== Testing Get Suitable Panels ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        constellations = [(125,),
                         (250, ),
                         (300, ),
                         (250, 125 ),
                         (125, 125, 125),
                         (250, 125, 125),
                         (300, 125, 125),
                         (350, 125, 125),
                         (250, 250, 300, 125),
                         (300, 300, 250, 125),
                         (350, 300, 300, 125)]

        for constellation in constellations:
            wall_width = randint(200, 700)
            inter_thickness = 250
            target_width = wall_width + inter_thickness

            result_panels, fillers, _ = data_handler.get_suitable_panel(constellation, target_width)
            self.assertIsInstance(result_panels, tuple)
            if len(result_panels) > 1:
                for panel in result_panels:
                    self.assertIsInstance(panel, str)
                self.assertIsInstance(fillers, tuple)
                for filler in fillers:
                    self.assertIsInstance(filler, Real)
                panel_width = 10*int(result_panels[0].split("/")[-1])
                self.assertEqual(panel_width + fillers[0], target_width)
    
    def test_get_suitable_panel_mammut_xt(self):
        print("\n ========== Testing Get Suitable Panels Mammut XT ========== ")
        
        data_handler = DataHandler(build_ele=self.build_ele)
        self.interactor.modify_element_property(0, "SelectionMode", 0)
        self.interactor.modify_element_property(0, "System", MAMMUT_XT)
        self.interactor.modify_element_property(0, "TieRod", XT_TIE_DW20)
        
        constellations = [(125,),
                        (250, ),
                        (300, ),
                        (250, 125 ),
                        (125, 125, 125),
                        (250, 125, 125),
                        (300, 125, 125),
                        (350, 125, 125),
                        (250, 250, 300, 125),
                        (300, 300, 250, 125),
                        (350, 300, 300, 125)]

        if self.build_ele.TieRod.value == XT_TIE_DW20: # single sided tierod
            wall_width = 200
            inter_thickness = 400
            target_width = wall_width + inter_thickness

            result_panels, fillers, _ = data_handler.get_suitable_panel_mammut_xt(constellations[0], target_width, wall_width)
            self.assertIsInstance(result_panels, tuple)
            if len(result_panels) > 1:
                for panel in result_panels:
                    self.assertIsInstance(panel, str)
                self.assertIsInstance(fillers, tuple)
                for filler in fillers:
                    self.assertIsInstance(filler, Real)
                panel_width = 10*int(result_panels[0].split("/")[-1])
                self.assertEqual(panel_width + fillers[0], target_width)

    def test_get_height_outside_01(self):
        print("\n ========== Testing Get Height Outside 01 ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)

        constellation = data_handler.get_height_constellation(randint(1900,5000))
        height_outside_01_true = data_handler.get_height_outside_01(constellation, True)
        height_outside_01_false = data_handler.get_height_outside_01(constellation, False)

        self.assertIsInstance(height_outside_01_true, tuple)
        self.assertIsInstance(height_outside_01_false, tuple)
        for height in height_outside_01_true:
            self.assertIsInstance(height, tuple)
        for height in height_outside_01_false:
            self.assertIsInstance(height, tuple)

    def test_get_height_outside_02(self):
        print("\n ========== Testing Get Height Outside 02 ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)

        constellation = data_handler.get_height_constellation(randint(1900,5000))
        height_outside_02_true = data_handler.get_height_outside_02(constellation, True)
        height_outside_02_false = data_handler.get_height_outside_02(constellation, False)

        self.assertIsInstance(height_outside_02_true, tuple)
        self.assertIsInstance(height_outside_02_false, tuple)
        for height in height_outside_02_true:
            self.assertIsInstance(height, tuple)
        for height in height_outside_02_false:
            self.assertIsInstance(height, tuple)

    def test_get_bracket_constellation(self):
        print("\n ========== Testing Get Bracket Constellation ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        for _ in range(50):
            wall_thickness = randint(150, 650)
        bracket_type = data_handler.get_bracket_type(wall_thickness)
        constellation = data_handler.get_height_constellation(randint(1900, 5000))
        height_bracket = data_handler.get_bracket_constellation(constellation)

        self.assertIsInstance(bracket_type, int)
        if bracket_type:
            self.assertIsInstance(height_bracket, tuple)
            for height in height_bracket:
                self.assertIsInstance(height, tuple)

    def test_get_bracket_type(self):
        print("\n ========== Testing Get Bracket Type ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        # Test attributes
        self.assertTrue(hasattr(data_handler, "get_bracket_type"))
        for _ in range(50):
            wall_thickness = randint(150, 650)
        bracket_type = data_handler.get_bracket_type(wall_thickness)
        self.assertIsInstance(bracket_type, int)

    def test_get_height_panel(self):
        print("\n ========== Testing get height panel for placing horizontal assembly lock ========== ")

        data_test = dict({(1250.0,): (120.0, 1100.0),
                    (2500.0,): (120.0, 1740.0),
                    (3000.0,): (120.0, 2140.0),
                    (3500.0,): (120.0, 1550.0, 2740.0),
                    (2500.0, 1250.0): (120.0, 1740.0, 2620.0, 3600.0),
                    (1250.0, 1250.0, 1250.0): (120.0, 1100.0, 1370.0, 2350.0, 2620.0, 3600.0),
                    (3000.0, 1250.0): (120.0, 2140.0, 3120.0, 4100.0),
                    (3500.0, 1250.0): (120.0, 1550.0, 2740.0, 3620.0, 4600.0),
                    (2500.0, 2500.0): (120.0, 1740.0, 2620.0, 4240.0),
                    (2500.0, 1250.0, 1250.0): (120.0, 1740.0, 2620.0, 3600.0, 3870.0, 4850.0),
                    (2500.0, 3000.0): (120.0, 1740.0, 2620.0, 4640.0),
                    (3000.0, 1250.0, 1250.0): (120.0, 2140.0, 3120.0, 4100.0, 4370.0, 5350.0),
                    (3000.0, 3000.0): (120.0, 2140.0, 3120.0, 5140.0),
                    (3500.0, 2500.0): (120.0, 1550.0, 2740.0, 3620.0, 5240.0),
                    (3500.0, 1250.0, 1250.0): (120.0, 1550.0, 2740.0, 3620.0, 4600.0, 4870.0, 5850.0),
                    (2500.0, 2500.0, 1250.0): (120.0, 1740.0, 2620.0, 4240.0, 5120.0, 6100.0),
                    (3500.0, 3000.0): (120.0, 1550.0, 2740.0, 3620.0, 5640.0),
                    (3000.0, 2500.0, 1250.0): (120.0, 1740.0, 2620.0, 4640.0, 5620.0, 6600.0),
                    (3500.0, 3500.0): (120.0, 1550.0, 2740.0, 3620.0, 5050.0, 6240.0),
                    (3500.0, 2500.0, 1250.0): (120.0, 1550.0, 2740.0, 3620.0, 5240.0, 6120.0, 7100.0),
                    (3000.0, 3000.0, 1250.0): (120.0, 2140.0, 3120.0, 5140.0, 6120.0, 7100.0),
                    (2500.0, 2500.0, 2500.0): (120.0, 1740.0, 2620.0, 4240.0, 5120.0, 6740.0),
                    (3500.0, 3000.0, 1250.0): (120.0, 1550.0, 2740.0, 3620.0, 5640.0, 6620.0, 7600.0),
                    (2500.0, 2500.0, 3000.0): (120.0, 1740.0, 2620.0, 4240.0, 5120.0, 7140.0),
                    (3500.0, 3500.0, 1250.0): (120.0, 1550.0, 2740.0, 3620.0, 5050.0, 6240.0, 7120.0, 8100.0),
                    (3500.0, 2500.0, 2500.0): (120.0, 1550.0, 2740.0, 3620.0, 5240.0, 6120.0, 7740.0),
                    (2500.0, 2500.0, 2500.0, 1250.0): (120.0, 1740.0, 2620.0, 4240.0, 5120.0, 6740.0, 7620.0, 8600.0),
                    (3500.0, 2500.0, 3000.0): (120.0, 1550.0, 2740.0, 3620.0, 5240.0, 6120.0, 8140.0),
                    (2500.0, 2500.0, 3000.0, 1250.0): (120.0, 1740.0, 2620.0, 4240.0, 5120.0, 7140.0, 8120.0, 9100.0),
                    (3500.0, 3500.0, 2500.0): (120.0, 1550.0, 2740.0, 3620.0, 5050.0, 6240.0, 7120.0, 8740.0),
                    (3000.0, 3000.0, 2500.0, 1250.0): (120.0, 2140.0, 3120.0, 5140.0, 6120.0, 7740.0, 8620.0, 9600.0),
                    (3500.0, 2500.0, 2500.0, 1250.0): (120.0, 1550.0, 2740.0, 3620.0, 5240.0, 6120.0, 7740.0, 8620.0, 9600.0),
                    (2500.0, 2500.0, 2500.0, 2500.0): (120.0, 1740.0, 2620.0, 4240.0, 5120.0, 6740.0, 7620.0, 9240.0),
                    (3500.0, 3500.0, 3000.0): (120.0, 1550.0, 2740.0, 3620.0, 5050.0, 6240.0, 7120.0, 9140.0),
                    (3000.0, 3000.0, 3000.0, 1250.0): (120.0, 2140.0, 3120.0, 5140.0, 6120.0, 8140.0, 9120.0, 10100.0),
                    (3500.0, 3000.0, 2500.0, 1250.0): (120.0, 1550.0, 2740.0, 3620.0, 5640.0, 6620.0, 8240.0, 9120.0, 10100.0),
                    (3500.0, 3500.0, 3500.0): (120.0, 1550.0, 2740.0, 3620.0, 5050.0, 6240.0, 7120.0, 8550.0, 9740.0),
                    (3500.0, 3000.0, 3000.0, 1250.0): (120.0, 1550.0, 2740.0, 3620.0, 5640.0, 6650.0, 8640.0, 9620.0, 10600.0)})

        data_handler = DataHandler(build_ele=self.build_ele)
        for _ in range(50):
            wall_height = randint(0, 10750)
            if wall_height in range(1251, 1951):
                continue
            constellations = data_handler.get_height_constellation(wall_height)
            for constellation in constellations:
                height_panel_true = data_handler.get_height_panel(constellation, True)
                height_panel_false = data_handler.get_height_panel(constellation, False)
                self.assertIsInstance(height_panel_true, tuple)
                self.assertIsInstance(height_panel_false, tuple)
                self.assertEqual(height_panel_true,data_test[constellation])
                self.assertEqual(height_panel_false,data_test[constellation])
                for height in height_panel_true:
                    self.assertIsInstance(height, float)
                for height in height_panel_false:
                    self.assertIsInstance(height, float)

    def test_get_panel_thickness(self):
        print("\n ========== Testing Get Panel Thickness ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        panel_name_data = [ ("M350-125/25", 120),
                            ("M350-125/30", 120),
                            ("M350-125/45", 120),
                            ("M350-125/50", 120),
                            ("M350-125/55", 120),
                            ("M350-125/75", 120),
                            ("M350-125/100", 120),
                            ("M350-125/125", 120),
                            ("M350-250/25", 120),
                            ("M350-250/30", 120),
                            ("M350-250/45", 120),
                            ("M350-250/50", 120),
                            ("M350-250/100", 120),
                            ("M350-250/125", 120)]

        for panel_name, thickness in panel_name_data:
            panel_thickness = data_handler.get_panel_thickness(panel_name)
            self.assertIsInstance(panel_thickness, float)
            self.assertEqual(panel_thickness, thickness)

    def test_get_min_panel_width(self):
        print("\n ========== Testing get_min_panel_width ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        default_min_panel_width = FormworkElement.MinPanelWidth.value
        min_panel_width = data_handler.get_min_panel_width()
        self.assertIsInstance(min_panel_width, float)
        self.assertLessEqual(min_panel_width, default_min_panel_width)

    def test_get_horizontal_lock(self):
        print("\n ========== Testing Get Horizontal Lock ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)

        for _ in range(50):
            wall_height = randint(0, 10750)
            if wall_height in range(1251, 1951):
                continue
        constellation = data_handler.get_height_constellation(wall_height)
        outside_horizontal_lock = data_handler.get_horizontal_lock(constellation)

        self.assertIsInstance(outside_horizontal_lock, tuple)
        for name in outside_horizontal_lock:
            self.assertIsInstance(name, str)

    def test_get_vertical_lock(self):
        print("\n ========== Testing Get Vertical Lock ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        for _ in range(50):
            wall_height = randint(0, 10750)
            if wall_height in range(1251, 1951):
                continue
        constellation = data_handler.get_height_constellation(wall_height)
        outside_vertical_lock = data_handler.get_vertical_lock(constellation)

        self.assertIsInstance(outside_vertical_lock, tuple)
        for name in outside_vertical_lock:
            self.assertIsInstance(name, str)

    def test_get_m_schalschloss_lock(self):
        print("\n ========== Testing get_m_schalschloss_lock ========== ")
        data_handler = DataHandler(build_ele=self.build_ele)
        check = data_handler._get_m_schalschloss_lock()
        self.assertIsInstance(check, tuple)
        self.assertGreater(len(check[0]), 0)

    def test_get_name_convert(self):
        print("\n ========== Testing Get Name Convert ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        name_convert = data_handler.get_name_convert()
        self.assertIsInstance(name_convert, dict)
        for name, symbol in zip(name_convert.keys(), name_convert.values()):
            self.assertIsInstance(name, str)
            self.assertIsInstance(symbol, str)

    def test_check_panel_by_element_name_mammut_350(self):
        print("\n ========== Testing check panel by element name Mammut 350 ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        data_test = [
            ("M350_InI_350x75",  True),
            ("M350_InI_350x250", True),
            ("M350_InI_350x25",  True),
            ("M350_InI_125x25",  True),
            ("M350_InI_125x45",  True),
            ("M350_InI_125x75",  True),
            ("M350_InI_250x55",  True),
            ("M350_InI_250x75",  True),
            ("M350_InI_IC350",   False),
            ("M350_InI_IC300",   False),
            ("M350_InI_IC250",   False),
            ("M350_InI_IC125",   False),
            ("M350_InI_OC350",   False),
            ("M_InI_AIC250",     False),
            ("M_InI_AIC125",     False),
            ("M_InI_AOC125",     False),
        ]
        for test_case in data_test:
            check = data_handler.check_panel_by_element_name(test_case[0])
            self.assertIsInstance(check, bool)
            self.assertEqual(check, test_case[1])

    def test_check_inside_corner_by_element_name_mammut_350(self):
        print("\n ========== Testing check inside corner by element name Mammut 350 ========== ")

        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        data_handler = DataHandler(build_ele=self.build_ele)
        data_test = [
            ("M350_InI_350x75",  False),
            ("M350_InI_350x250", False),
            ("M350_InI_350x25",  False),
            ("M350_InI_125x25",  False),
            ("M350_InI_125x45",  False),
            ("M350_InI_125x75",  False),
            ("M350_InI_250x55",  False),
            ("M350_InI_250x75",  False),
            ("M350_InI_IC350",   True),
            ("M350_InI_IC300",   True),
            ("M350_InI_IC250",   True),
            ("M350_InI_IC125",   True),
        ]
        for test_case in data_test:
            check = data_handler.check_inside_corner_by_element_name(test_case[0])
            self.assertIsInstance(check, bool)
            self.assertEqual(check, test_case[1])

    def test_get_tierod_objectid(self):
        print("\n ========== Testing Get TieRod Element ========== ")
        data_tests = [
            (MAMMUT_350, 1250.0, 1250.0, 'MEVA-TRID-060-135'),
            (MAMMUT_350, 2500.0, 1000.0, 'MEVA-TRID-060-100'),
            (MAMMUT_350, 2500.0, 1250.0, 'MEVA-TRID-060-095'),
            (MAMMUT_350, 3000.0, 1000.0, 'MEVA-TRID-060-060'),
            (MAMMUT_350, 3000.0, 1250.0, 'MEVA-TRID-060-055'),
            (MAMMUT_XT, 1250.0, 1250.0, 'MEVA-TRID-080-090'),
            (MAMMUT_XT, 2500.0, 750.0, 'MEVA-TRID-080-075'),
            (MAMMUT_XT, 2500.0, 1000.0, 'MEVA-TRID-080-070'),
            (MAMMUT_XT, 2500.0, 1250.0, 'MEVA-TRID-080-065'),
            (MAMMUT_XT, 3000.0, 1250.0, 'MEVA-TRID-080-040'),
        ]

        data_handler = DataHandler(build_ele=self.build_ele)
        for data_test in data_tests:
            self.interactor.modify_element_property(0, "System", data_test[0])
            self.interactor.modify_element_property(0, "SelectionMode", 2)
            oid_tierods = data_handler.get_tierod_objectid(data_test[1], data_test[2])
            self.assertIsInstance(oid_tierods, tuple)
            # for oid_tierod in oid_tierods:
            self.assertIsInstance(oid_tierods[0], str)
            self.assertEqual(oid_tierods[0], data_test[3])

    def test_get_tierod_dw15(self):
        print("\n ========== Testing Get Tie Rod Element Mammut 350 - Ankerstab DW15 ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)          
        for _ in range(50):
            wall_thickness = randint(0, 800)
            if wall_thickness in range(0, 149) or wall_thickness in range(651, 800):
                continue        
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        tie_rods = data_handler.get_tierod(wall_thickness, TIEROD_DW15)
        self.assertIsInstance(tie_rods, list)
        for dw15_tie_rod in tie_rods:
            dw15_prefix = "Acc_InI_tie_rod"
            self.assertIsInstance(dw15_tie_rod, str)
            self.assertIn(dw15_prefix, dw15_tie_rod)
            
    def test_get_tierod_dw20(self):
        print("\n ========== Testing Get Tie Rod Element Mammut 350 - Ankerstab DW20 ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        for _ in range(50):
            wall_thickness = randint(0, 800)
            if wall_thickness in range(0, 149) or wall_thickness in range(651, 800):
                continue
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        tie_rods = data_handler.get_tierod(wall_thickness, TIEROD_DW20)
        self.assertIsInstance(tie_rods, list)
        for dw20_tie_rod in tie_rods:
            dw20_prefix = "Acc_InI_tie_rod"
            self.assertIsInstance(dw20_tie_rod, str)
            self.assertIn(dw20_prefix, dw20_tie_rod)

    def test_get_tierod_xt_konusanker(self):
        print("\n ========== Testing Get Tie Rod Element Mammut XT - XT-Konusanker 20 ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        for _ in range(50):
            wall_thickness = randint(0, 800)
            if wall_thickness in range(0, 149) or wall_thickness in range(500, 800):
                continue       
        self.interactor.modify_element_property(0, "SelectionMode", 1)
        tie_rods = data_handler.get_tierod_mammut_xt(wall_thickness, XT_CONE_DW20)
        self.assertIsInstance(tie_rods, list)
        for xt_konusanker_tie_rod in tie_rods:
            xt_konusanker_prefix = "Acc_InI_taper_tie_23"
            self.assertIsInstance(xt_konusanker_tie_rod, str)
            self.assertIn(xt_konusanker_prefix, xt_konusanker_tie_rod)

    def test_get_tierod_xt_anker(self):
        print("\n ========== Testing Get Tie Rod Element Mammut XT - XT-Anker DW20 ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        for _ in range(50):
            wall_thickness = randint(0, 800)
            if wall_thickness in range(0, 149) or wall_thickness in range(500, 800):
                continue       
        self.interactor.modify_element_property(0, "SelectionMode", 1)
        tie_rods = data_handler.get_tierod_mammut_xt(wall_thickness, XT_TIE_DW20)
        self.assertIsInstance(tie_rods, list)
        for xt_anker_tie_rod in tie_rods:
            xt_anker_prefix = "Acc_InI_tie_DW20"
            self.assertIsInstance(xt_anker_tie_rod, str)
            self.assertIn(xt_anker_prefix, xt_anker_tie_rod)

    def test_get_tierod_length_dw15(self):
        print("\n ========== Testing Get Tie Rod Lenght Mammut 350 - Ankerstab DW15 ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        for _ in range(50):
            wall_thickness = randint(0, 800)
            if wall_thickness in range(0, 149) or wall_thickness in range(500, 800):
                continue       
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        tie_rod_lenghts = data_handler._get_tierod_length(wall_thickness, TIEROD_DW15)
        self.assertIsInstance(tie_rod_lenghts, list)
        for dw15_tierod_lenght in tie_rod_lenghts:
            dw15_prefix = "MEVA-AccOID-501"
            self.assertIsInstance(dw15_tierod_lenght, str)
            self.assertIn(dw15_prefix, dw15_tierod_lenght)
            
    def test_get_tierod_length_dw20(self):
        print("\n ========== Testing Get Tie Rod Lenght Mammut 350 - Ankerstab DW20 ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        for _ in range(50):
            wall_thickness = randint(0, 800)
            if wall_thickness in range(0, 149) or wall_thickness in range(500, 800):
                continue       
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        tie_rod_lenghts = data_handler._get_tierod_length(wall_thickness, TIEROD_DW20)
        self.assertIsInstance(tie_rod_lenghts, list)
        for dw20_tierod_lenght in tie_rod_lenghts:
            dw20_prefix = "MEVA-AccOID-501"
            self.assertIsInstance(dw20_tierod_lenght, str)
            self.assertIn(dw20_prefix, dw20_tierod_lenght)

    def test_get_tierod_length_both_single_and_two_sided(self):
        print("\n ========== Testing Get Both Single & Two Sided Tie Rod Lenght Mammut XT ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        for _ in range(50):
            wall_thickness = randint(0, 800)
            if wall_thickness in range(0, 149) or wall_thickness in range(500, 800):
                continue       
        self.interactor.modify_element_property(0, "SelectionMode", 1)
        system_set = [XT_CONE_DW20, XT_TIE_DW20, TIEROD_DW20]

        for system in system_set:
            tie_rods = data_handler._get_tierod_length_mammut_xt(wall_thickness, system)
            self.assertIsInstance(tie_rods, list)
            for tie_rod in tie_rods:
                tierod_prefix = "MEVA-AccOID-501"
                self.assertIsInstance(tie_rod, str)
                self.assertIn(tierod_prefix, tie_rod)

    def test_get_tierod_left_holes(self):
        print("\n ========== Testing Get tierod left holes ========== ")
        
        id_tierods = (
            'MEVA-TRID-060-005',
            'MEVA-TRID-060-010',
            'MEVA-TRID-060-015',
            'MEVA-TRID-060-020',
            'MEVA-TRID-060-025',
            'MEVA-TRID-060-030',
            'MEVA-TRID-060-035',
            'MEVA-TRID-060-040',
            'MEVA-TRID-060-045',
            'MEVA-TRID-060-050',
            'MEVA-TRID-060-055',
            'MEVA-TRID-060-060',
            'MEVA-TRID-060-065',
            'MEVA-TRID-060-070',
            'MEVA-TRID-060-075',
        )
        data_handler = DataHandler(build_ele=self.build_ele)
        tie_rods_left = data_handler.get_tierod_left_holes(id_tierods)
        self.assertIsInstance(tie_rods_left, tuple)
        for holes in tie_rods_left:
            self.assertIsInstance(holes, tuple)
            for hole in holes:
                self.assertIsInstance(hole, float)

    def test_get_tierod_middle_holes(self):
        print("\n ========== Testing Get tierod middle holes ========== ")
        
        id_tierods = (
            'MEVA-TRID-060-800',
            'MEVA-TRID-060-805',
            'MEVA-TRID-060-810',
            'MEVA-TRID-060-055',
            'MEVA-TRID-060-060',
            'MEVA-TRID-060-810',
            'MEVA-TRID-060-815',
            'MEVA-TRID-080-005',
            'MEVA-TRID-080-010',
            'MEVA-TRID-080-015',
            'MEVA-TRID-080-020',
            'MEVA-TRID-080-025',
            'MEVA-TRID-080-030',
            'MEVA-TRID-080-040',
            'MEVA-TRID-080-045',
            'MEVA-TRID-080-050',
            'MEVA-TRID-080-055',
            'MEVA-TRID-080-060',
        )
        data_handler = DataHandler(build_ele=self.build_ele)
        tie_rods_middle = data_handler.get_tierod_middle_holes(id_tierods)
        self.assertIsInstance(tie_rods_middle, tuple)
        for holes in tie_rods_middle:
            self.assertIsInstance(holes, tuple)
            for hole in holes:
                self.assertIsInstance(hole, float)

    def test_get_tierod_right_holes(self):
        print("\n ========== Testing Get tierod right holes ========== ")
        
        id_tierods = (
            'MEVA-TRID-060-080',
            'MEVA-TRID-060-085',
            'MEVA-TRID-060-090',
            'MEVA-TRID-060-095',
            'MEVA-TRID-060-100',
            'MEVA-TRID-060-105',
            'MEVA-TRID-060-110',
            'MEVA-TRID-060-115',
            'MEVA-TRID-060-120',
            'MEVA-TRID-060-125',
            'MEVA-TRID-060-130',
            'MEVA-TRID-060-135',
            'MEVA-TRID-060-140',
            'MEVA-TRID-060-145',
            'MEVA-TRID-060-150',
        )
        data_handler = DataHandler(build_ele=self.build_ele)
        tie_rods_right = data_handler.get_tierod_right_holes(id_tierods)
        self.assertIsInstance(tie_rods_right, tuple)
        for holes in tie_rods_right:
            self.assertIsInstance(holes, tuple)
            for hole in holes:
                self.assertIsInstance(hole, float)

    def test_get_flange_nut(self):
        print("\n ========== Testing Get Flange Nut Element ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)
        for _ in range(50):
            wall_thickness = randint(0, 800)
            if wall_thickness in range(0, 149) or wall_thickness in range(500, 800):
                continue       
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        flange_nuts = data_handler.get_flange_nut(wall_thickness, TIEROD_DW15)
        self.assertIsInstance(flange_nuts, list)
        for dw15_flange_nut in flange_nuts:
            self.assertIsInstance(dw15_flange_nut, str)

    def test_get_tierod_value_list(self):
        print("\n ========== Testing Get TieRod Value List ========== ")

        data_handler = DataHandler(build_ele=self.build_ele)

        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        results = data_handler.get_tierod_value_list()
        self.assertIsInstance(results, str)
        
    def test_get_tierod_constellation(self):
        print("\n ========== Testing Get Tierod Constellation ========== ")
        
        data_handler = DataHandler(build_ele=self.build_ele)
        tierod_constellation = data_handler._get_tierod_constellation()
        self.assertIsInstance(tierod_constellation, list)

    def test_check_sheet_name_database(self):
        print("\n ========== Testing Check Sheet Name Database ========== ")
        
        data_handler = DataHandler(build_ele=self.build_ele)
        sheet_name = 'ObjectID'
        data_sheet = data_handler._DataHandler__check_sheet_name_database(sheet_name)
        self.assertIsInstance(data_sheet, DataFrame)

    def test_get_inside_corner_width(self):
        print("\n ========== Testing Get Inside Corner Width ========== ")
        
        data_handler = DataHandler()
        for _ in range(50):
            wall_thickness = randint(0, 500)
            if wall_thickness in range(0, 151):
                continue
            inside_corner_width = data_handler.get_inside_corner_width(wall_thickness)
            self.assertIsInstance(inside_corner_width, float)

    def test_get_inside_corner_width_T_Shape_MammutXT(self):
        print("\n ========== Testing get inside corner width T Shape MammutXT ========== ")
        
        data_handler = DataHandler(build_ele=self.build_ele)
        self.interactor.modify_element_property(0, "System", MAMMUT_XT)
        for _ in range(50):
            wall_thickness = randint(0, 600)
            if wall_thickness in range(0, 150) or wall_thickness > 500:
                with self.assertRaises(ValueError):
                    data_handler.get_inside_corner_width_t_shape_mammutxt(float(wall_thickness))
                continue
            inside_corner_width = data_handler.get_inside_corner_width_t_shape_mammutxt(float(wall_thickness))
            self.assertIsInstance(inside_corner_width, float)        

    def test_get_outside_corner_width(self):
        print("\n ========== Testing Get Outside Corner Width ========== ")
        
        data_handler = DataHandler()
        for _ in range(50):
            wall_thickness = randint(0, 500)
            if wall_thickness in range(0, 151):
                continue
            inside_corner_width = data_handler.get_outside_corner_width(wall_thickness)
            self.assertIsInstance(inside_corner_width, float)

    def test_get_value_from_thickness(self):
        print("\n ========== Testing Get Value From Thickness ========== ")
        
        data_handler = DataHandler()
        for _ in range(50):
            wall_thickness = randint(0, 650)
            if wall_thickness in range(0, 149) or wall_thickness in range(501, 800):
                continue
            value_corner_mapping = {
                150: 350,
                200: 400,
                250: 350,
                300: 350,
                350: 400,
                400: 350,
                450: 400,
                500: 350
            }
            results = data_handler.get_value_from_thickness(value_corner_mapping, wall_thickness)
            self.assertIsInstance(results, float)
            if results > 350:
                self.assertEqual(results, 400)
            if results < 400:
                self.assertEqual(results, 350)

    def test_get_available_widths(self):
        print("\n ========== Testing Get available panel width ========== ")

        data_tests = [
            (MAMMUT_350, set({1250.0, 450.0, 2500.0, 550.0, 1000.0, 300.0, 750.0, 500.0, 250.0})),
            (MAMMUT_XT, set({1250.0, 2500.0, 1000.0, 750.0, 500.0, 250.0}))
        ]

        for data_test in data_tests:
            self.interactor.modify_element_property(0, "System", data_test[0])
            data_handler = DataHandler(build_ele=self.build_ele)
            all_widths = data_handler._get_available_widths((FormworkElement.Panel, FormworkElement.LargePanel))
            self.assertIsInstance(all_widths, set)
            self.assertEqual(all_widths, data_test[1])

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

    test_suite.addTest(unittest.makeSuite(TestDataHandler))

    return test_suite
