# pyright: reportGeneralTypeIssues=false
# pyright: reportOptionalSubscript=false

import unittest
from collections import defaultdict

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Utility as AllplanUtil

from Formwork.Controller.ShapeCtl import ShapeCtl
from Formwork.Controller.FormingCtl import FormingCtl
from Formwork.Data.DataHandler import DataHandler
from Formwork.Shape.Recognizer import ShapeRecognizer
from Formwork.Factories.BIM2WallFactory import BIM2WallFactory
from Formwork.Factories.BIM2WallFactory import BIM2Wall

from ..TestBase import TestBase, SINGLE_PATH, CONNECT_PATH

WRONG_ID_ATTR = "Wrong ID of the NAME ATTRIBUTE"
WRONG_NAME_ATTR = "Wrong VALUE of the NAME ATTRIBUTE"
WRONG_ATTR = "Wrong TYPE output for ATTRIBUTES"
FORMWORK_ELEMENT = "Formwork Element"
MAMMUT_XT = "Mammut XT"
UNI_LOCKS_22 = "Uni-assembly lock 22"
UNI_LOCKS_28 = "Uni-assembly lock 28"


class TestSetAttributes(TestBase):

    @classmethod
    def setUpClass(cls):
        print(f"\n ========== Running {__name__} ========== ")
        cls.wall_dict = defaultdict(list)
        single_walls  = (SINGLE_PATH + "cut_wall_1_400.sym",
                         SINGLE_PATH + "cut_wall_1_550.sym",)

        for wall in single_walls:
            cls.wall_dict["SingleWalls"].append(cls._create_bim2walls(wall))

        # For connect walls
        cls.shape_dict = defaultdict(list)
        cls.data_handler = DataHandler()
        models_dict = defaultdict(list)
        l_shape  = (CONNECT_PATH + "LShape_MXT_UNI_22.sym",
                    CONNECT_PATH + "LShape_MXT_UNI_28.sym",)

        for shape in l_shape:
            models_dict["LShape"].append(cls._create_bim2walls(shape))
        recognizer = ShapeRecognizer()
        model_key = "LShape"
        for walls in models_dict.get("LShape", []):
            bim2wall_1, bim2wall_2 = walls
            recognizer.recognize(bim2wall_1, bim2wall_2)
            shape = recognizer.create_shape()
            cls.shape_dict[model_key].append(shape)

    @classmethod
    def tearDownClass(cls):
        AllplanUtil.ClearUnitTestDocument()

    def test_uni_lock_22_attributes(self):
        print("\n ========== Testing uni-assembly lock 22 attributes ========== ")
        shape_ = self.shape_dict.get("LShape", [])[0]
        target_name = UNI_LOCKS_22
        result_dict = {
            241   : "29-400-85",
            507   : "Acc_InI_uni_assembly_lock_22",
            1417  : FORMWORK_ELEMENT,
            18222 : "Uni-assembly lock 22"
        }
        elements = self.create_uni_locks_and_timbers_elements(target_name, shape_, 2)
        attr_list = elements[-1].get_attribute_list()
        self.assertIsInstance(attr_list, list, WRONG_ATTR + "LIST")
        self.assertIsInstance(attr_list[0], AllplanBaseElements.AttributeString, WRONG_ATTR + "STRING")
        self.check_attr_by_dict(attr_list, result_dict)

    def test_uni_lock_28_attributes(self):
        print("\n ========== Testing uni-assembly lock 28 attributes ========== ")
        shape_ = self.shape_dict.get("LShape", [])[-1]
        target_name = UNI_LOCKS_28
        result_dict = {
            241   : "29-400-90",
            507   : "Acc_InI_uni_assembly_lock_28",
            1417  : FORMWORK_ELEMENT,
            18222 : "Uni-assembly lock 28"
        }
        elements = self.create_uni_locks_and_timbers_elements(target_name, shape_, 2)
        attr_list = elements[-1].get_attribute_list()
        self.assertIsInstance(attr_list, list, WRONG_ATTR + "LIST")
        self.assertIsInstance(attr_list[0], AllplanBaseElements.AttributeString, WRONG_ATTR + "STRING")
        self.check_attr_by_dict(attr_list, result_dict)

    def test_stop_end_bracket_4060_attributes(self):
        print("\n ========== Testing stopend bracket 40/60 attributes ========== ")
        bim2wall = self.wall_dict.get("SingleWalls", [])[0]
        elements, controller = self.create_elements_freestanding_xt(bim2wall)
        elements.extend(controller._get_stop_end_bracket())
        self.assertIsInstance(elements, list)
        result_dict = {
            241   : "29-105-50",
            507   : "Acc_InI_stop_end_bracket_4060",
            1417  : FORMWORK_ELEMENT,
            18222 : "Stop End Bracket 40/60"
        }
        attr_list = elements[-1].get_attribute_list()
        self.assertIsInstance(attr_list, list, WRONG_ATTR + "LIST")
        self.assertIsInstance(attr_list[0], AllplanBaseElements.AttributeString, WRONG_ATTR + "STRING")
        self.check_attr_by_dict(attr_list, result_dict)

    def test_stop_end_bracket_6023_attributes(self):
        print("\n ========== Testing stopend bracket 60/23 attributes ========== ")
        bim2wall = self.wall_dict.get("SingleWalls", [])[1]
        elements, controller = self.create_elements_freestanding_xt(bim2wall)
        elements.extend(controller._get_stop_end_bracket())
        self.assertIsInstance(elements, list)
        result_dict = {
            241   : "29-105-60",
            507   : "Acc_InI_stop_end_bracket_6023",
            1417  : FORMWORK_ELEMENT,
            18222 : "Stop End Bracket 60/23"
        }
        attr_list = elements[-1].get_attribute_list()
        self.assertIsInstance(attr_list, list, WRONG_ATTR + "LIST")
        self.assertIsInstance(attr_list[0], AllplanBaseElements.AttributeString, WRONG_ATTR + "STRING")
        self.check_attr_by_dict(attr_list, result_dict)

    def test_timber_filler_attributes(self):
        print("\n ========== Testing timber filler attributes ========== ")        
        bim2wall = self.wall_dict.get("SingleWalls", [])[1]
        elements, controller = self.create_elements_freestanding_xt(bim2wall)
        elements.extend(controller._get_timber_fillers())
        self.assertIsInstance(elements, list)
        result_dict = {
            507   : "Timber Filler",
            1417  : FORMWORK_ELEMENT,
        }
        timber_attr = ((elements[-1].create_model_ele())[1].GetAttributesList()[0]).GetAttributes()
        self.assertIsInstance(timber_attr, list, WRONG_ATTR + "LIST")
        self.assertIsInstance(timber_attr[0], AllplanBaseElements.AttributeString, WRONG_ATTR + "STRING")
        self.check_attr_by_dict(timber_attr, result_dict)

    def test_support_filler_attributes(self):
        print("\n ========== Testing support filler attributes ========== ")
        elements = self.sp_filler_interactor
        attr_list = ((elements.create_model_ele()[1]).Attributes.GetAttributeSets()[0]).Attributes
        result_dict = {
            507   : "Timber Filler",
            1417  : FORMWORK_ELEMENT,
        }
        self.assertIsInstance(attr_list, list, WRONG_ATTR + "LIST")
        self.assertIsInstance(attr_list[0], AllplanBaseElements.AttributeString, WRONG_ATTR + "STRING")
        self.check_attr_by_dict(attr_list, result_dict)

    def test_stopend_waler_15_40_attributes(self):
        print("\n ========== Testing stop end waler MX 15-40 attributes ========== ")
        elements = self.stopend_waler_interactor
        result_dict = {
            241   : "127732",
            507   : "Acc_InI_stop_end_waler_15_40",
            1417  : FORMWORK_ELEMENT,
            18222 : "Stop End Waler MX 15-40"
        }
        attr_list = elements.get_attribute_list()
        self.assertIsInstance(attr_list, list, WRONG_ATTR + "LIST")
        self.assertIsInstance(attr_list[0], AllplanBaseElements.AttributeString, WRONG_ATTR + "STRING")
        self.check_attr_by_dict(attr_list, result_dict)

    def check_attr_by_dict(self, attr_list: list, dict_values: dict):
        for idx, id_key, value in \
            zip(range(len(attr_list)), dict_values.keys(), dict_values.values()):
            self.assertEqual(attr_list[idx].Id, id_key, WRONG_ID_ATTR)
            self.assertEqual(attr_list[idx].Value, value, WRONG_NAME_ATTR)

    @staticmethod
    def _process_place_elements(shape, data_handler, build_ele, str_table_service, pyp_path, coord_input):
        local_matrix = AllplanGeo.Matrix3D()
        shape_controller = ShapeCtl(data_handler, shape, local_matrix, str_table_service, \
            pyp_path, coord_input, build_ele=build_ele)
        constellations = shape_controller.get_combinations()
        
        return shape_controller, constellations

    def create_uni_locks_and_timbers_elements(self, target_name, shape_, target_num):
        self.interactor.modify_element_property(0, "SelectionMode", 0)
        self.interactor.modify_element_property(0, "System", MAMMUT_XT)
        data_handler = DataHandler(build_ele=self.build_ele)
        shape_controller, constellations = self._process_place_elements(
            shape_, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)
        # Test instance
        self.assertIsInstance(shape_controller, ShapeCtl)
        self.assertIsInstance(shape_controller.data_handler, DataHandler)
        # Test attribute values
        self.assertEqual(shape_controller.build_ele, self.build_ele)
        self.assertEqual(type(shape_controller.local_str_table), type(self.build_ele.get_string_tables()[0]))
        self.assertEqual(shape_controller.timbers, [])
        self.assertEqual(shape_controller.uni_assembly_lock, [])
        self.assertEqual(shape_controller._get_timber_fillers(), shape_controller.timbers)
        self.assertEqual(shape_controller._get_uni_assembly_lock(), shape_controller.uni_assembly_lock)
        
        self.assertIsInstance(constellations, list)
        for constellation in constellations:
            self.assertIsInstance(constellation, tuple)
            elements = shape_controller._place_elements_mammut_xt(constellation)
            self.assertIsInstance(elements, list)
            if target_num == 1:
                # Timber fillers
                elements.extend(shape_controller._get_timber_fillers())
                macro_element = (elements[-2].create_model_ele())[0]
                macro_element_properties = macro_element.GetMacroProperties()
                timber_filler_name = macro_element_properties.Name
                self.assertEqual(timber_filler_name, target_name)
            elif target_num == 2:
                # Uni-locks
                elements.extend(shape_controller._get_uni_assembly_lock())
                macro_ele = (elements[-2].create_model_ele())[0]
                macro_element_prop = macro_ele.GetMacroProperties()
                uni_locks_name = macro_element_prop.Name
                self.assertEqual(uni_locks_name, target_name)

        return elements
    
    def create_elements_freestanding_xt(self, bim2wall):
        self.interactor.modify_element_property(0, "System", MAMMUT_XT)
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        data_handler = DataHandler(build_ele=self.build_ele)
        input_height = bim2wall[0].height
        height_constellations = data_handler.get_height_constellation(input_height)
        local_matrix = AllplanGeo.Matrix3D()
        controller = FormingCtl(data_handler, bim2wall[0], build_ele=self.build_ele,
                                local_matrix=local_matrix, str_table_service=self.str_table_service,
                                pyp_path=self.pyp_path, coord_input=self.coord_input)
        # Test instance
        self.assertIsInstance(controller, FormingCtl)
        self.assertIsInstance(controller.bim2wall, BIM2Wall)
        self.assertIsInstance(controller.data_handler, DataHandler)
        # Test attribute values
        self.assertEqual(controller._bim2wall, bim2wall[0])
        self.assertEqual(controller.selected_formwork_elements, None)
        self.assertEqual(controller.build_ele, self.build_ele)
        self.assertEqual(controller._local_matrix, local_matrix)
        self.assertEqual(controller.coord_input, self.coord_input)
        self.assertEqual(controller.timbers, [])
        self.assertEqual(controller.stop_end_bracket, [])
        self.assertEqual(controller.uni_assembly_lock, [])
        self.assertEqual(controller.deleted_ele_list, [None, []])
        self.assertEqual(controller.doc, self.coord_input.GetInputViewDocument())
        self.assertEqual(type(controller.local_str_table), type(self.build_ele.get_string_tables()[0]))
        self.assertEqual(controller._get_timber_fillers(), controller.timbers)
        self.assertEqual(controller._get_deleted_ele_list(), controller.deleted_ele_list)

        for height_constellation in height_constellations:

            elements = controller._place_freestanding(height_constellation)
        return elements, controller    
    
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

    test_suite.addTest(unittest.makeSuite(TestSetAttributes))

    return test_suite
