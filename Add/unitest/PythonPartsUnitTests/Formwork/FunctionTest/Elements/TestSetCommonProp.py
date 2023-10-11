# pyright: reportGeneralTypeIssues=false
# pyright: reportOptionalSubscript=false

import unittest
from collections import defaultdict

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
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
WRONG_PROP = "Wrong TYPE output for PROPS"
MAMMUT_XT = "Mammut XT"
UNI_LOCKS_22 = "Uni-assembly lock 22"
UNI_LOCKS_28 = "Uni-assembly lock 28"
ALLIGN_BFD = "Alignment Coupler BFD"
TEXTURE_MEVA_03_STEEL = "Library\\\\Formwork\\\\Meva\\\\03-MEVA-STEEL"
TEXTURE_PERI_03_STEEL = "Library\\\\Formwork\\\\Peri\\\\03-PERI-STEEL"
TEXTURE_MEVA_05_GOLD  = "Library\\\\Formwork\\\\Meva\\\\05-MEVA-GOLD"
TEXTURE_MEVA_07_TIEROD  = "Library\\\\Formwork\\\\Meva\\\\07-MEVA-TIE-ROD"
class TestSetCommonProp(TestBase):

    @classmethod
    def setUpClass(cls):
        print(f"\n ========== Running {__name__} ========== ")
        cls.data_handler = DataHandler()
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

    def test_allign_bfd_common_prop(self):
        print("\n ========== Testing Allignment Coupler BFD common properties ========== ")
        
        elements = self.align_coupler_bfd_interactor
        com_prop = elements.get_common_prop()    
        self.assertIsInstance(com_prop, AllplanBaseElements.CommonProperties, WRONG_PROP)
        self.check_com_prop(com_prop)

    def test_allign_bfd_textures(self):
        print("\n ========== Testing Allignment Coupler BFD textures ========== ")

        elements = self.align_coupler_bfd_interactor
        geo_ele = elements.get_geometry_components()
        target_texture_list = [
            ['Lock_Static_Peri_22', TEXTURE_PERI_03_STEEL],
            ['Lock_Moving_Peri_22', TEXTURE_PERI_03_STEEL],
        ]
        self.check_texture_components(target_texture_list, geo_ele)

    def test_uni_lock_22_common_prop(self):
        print("\n ========== Testing uni lock 22 common properties ========== ")
        shape_ = self.shape_dict.get("LShape", [])[0]
        target_name = UNI_LOCKS_22
        # Check common properties from palette
        elements = self.create_uni_locks_and_timbers_elements(target_name, shape_, 2)     
        com_prop = elements[-1].get_common_prop()    
        self.assertIsInstance(com_prop, AllplanBaseElements.CommonProperties, WRONG_PROP)
        self.check_com_prop(com_prop)

    def test_uni_lock_22_textures(self):
        print("\n ========== Testing uni lock 22 textures ========== ")
        shape_ = self.shape_dict.get("LShape", [])[0]
        target_name = UNI_LOCKS_22
        elements = self.create_uni_locks_and_timbers_elements(target_name, shape_, 2)     
        geo_ele = elements[-1].get_geometry_components()
        target_texture_list = [
            ['UniAssemblyLock_D1', TEXTURE_MEVA_03_STEEL],
            ['UniAssemblyLock_D2', TEXTURE_MEVA_05_GOLD],
            ['UniAssemblyLock_22_S', TEXTURE_MEVA_03_STEEL],
        ]
        self.check_texture_components(target_texture_list, geo_ele)

    def test_uni_lock_28_common_prop(self):
        print("\n ========== Testing uni lock 28 common properties ========== ")
        shape_ = self.shape_dict.get("LShape", [])[-1]
        target_name = UNI_LOCKS_28
        # Check common properties from palette
        elements = self.create_uni_locks_and_timbers_elements(target_name, shape_, 2)
        com_prop = elements[-1].get_common_prop()
        self.assertIsInstance(com_prop, AllplanBaseElements.CommonProperties, WRONG_PROP)
        self.check_com_prop(com_prop)
        
    def test_uni_lock_28_textures(self):
        print("\n ========== Testing uni lock 28 textures ========== ")
        shape_ = self.shape_dict.get("LShape", [])[-1]
        target_name = UNI_LOCKS_28
        elements = self.create_uni_locks_and_timbers_elements(target_name, shape_, 2)     
        geo_ele = elements[-1].get_geometry_components()
        target_texture_list = [
            ['UniAssemblyLock_D1', TEXTURE_MEVA_03_STEEL],
            ['UniAssemblyLock_D2', TEXTURE_MEVA_05_GOLD],
            ['UniAssemblyLock_28_S', TEXTURE_MEVA_03_STEEL],
        ]
        self.check_texture_components(target_texture_list, geo_ele)
        
    def test_stop_end_bracket_2340_common_prop(self):
        print("\n ========== Testing stopend bracket 23/40 common properties ========== ")
        elements = self.bracket_2340_interactor
        # Check common properties from palette
        com_prop = elements.get_common_prop()       
        self.assertIsInstance(com_prop, AllplanBaseElements.CommonProperties, WRONG_PROP)
        self.check_com_prop(com_prop)

    def test_stop_end_bracket_2340_textures(self):
        print("\n ========== Testing stop end bracket 2340 textures ========== ")
        elements = self.bracket_2340_interactor
        geo_ele = elements.get_geometry_components()
        target_texture_list = [
            ['stop_end_bracket_S1_2340', TEXTURE_MEVA_03_STEEL],
            ['stop_end_bracket_S2_2340', TEXTURE_MEVA_03_STEEL],
            ['stop_end_bracket_S3_2340', TEXTURE_MEVA_05_GOLD],
            ['stop_end_bracket_S4_2340', TEXTURE_MEVA_07_TIEROD],
            ['stop_end_bracket_D_2340', TEXTURE_MEVA_03_STEEL],
        ]
        self.check_texture_components(target_texture_list, geo_ele)

    def test_stop_end_bracket_4060_common_prop(self):
        print("\n ========== Testing stopend bracket 40/60 common properties ========== ")
        bim2wall = self.wall_dict.get("SingleWalls", [])[0]
        elements, controller = self.create_elements_freestanding_xt(bim2wall)
        elements.extend(controller._get_stop_end_bracket())
        self.assertIsInstance(elements, list)
        com_prop = elements[-1].get_common_prop()        
        self.assertIsInstance(com_prop, AllplanBaseElements.CommonProperties, WRONG_PROP)
        self.check_com_prop(com_prop)
        
    def test_stopend_bracket_4060_textures(self):
        print("\n ========== Testing stopend bracket 40/60 textures ========== ")
        bim2wall = self.wall_dict.get("SingleWalls", [])[0]
        elements, controller = self.create_elements_freestanding_xt(bim2wall)
        elements.extend(controller._get_stop_end_bracket())
        geo_ele = elements[-1].get_geometry_components()
        target_texture_list = [
            ['stop_end_bracket_S1_4060', TEXTURE_MEVA_03_STEEL],
            ['stop_end_bracket_S2_4060', TEXTURE_MEVA_03_STEEL],
            ['stop_end_bracket_S3_4060', TEXTURE_MEVA_05_GOLD],
            ['stop_end_bracket_S4_4060', TEXTURE_MEVA_07_TIEROD],
            ['stop_end_bracket_D_4060', TEXTURE_MEVA_03_STEEL],
        ]
        self.check_texture_components(target_texture_list, geo_ele)

    def test_stop_end_bracket_6023_common_prop(self):
        print("\n ========== Testing stopend bracket 60/23 common properties ========== ")
        bim2wall = self.wall_dict.get("SingleWalls", [])[1]
        elements, controller = self.create_elements_freestanding_xt(bim2wall)
        elements.extend(controller._get_stop_end_bracket())
        self.assertIsInstance(elements, list)
        com_prop = elements[-1].get_common_prop()        
        self.assertIsInstance(com_prop, AllplanBaseElements.CommonProperties, WRONG_PROP)
        self.check_com_prop(com_prop)
            
    def test_stopend_bracket_6023_textures(self):
        print("\n ========== Testing stopend bracket 60/23 textures ========== ")
        bim2wall = self.wall_dict.get("SingleWalls", [])[1]
        elements, controller = self.create_elements_freestanding_xt(bim2wall)
        elements.extend(controller._get_stop_end_bracket())
        geo_ele = elements[-1].get_geometry_components()
        target_texture_list = [
            ['stop_end_bracket_S1_6023', TEXTURE_MEVA_03_STEEL],
            ['stop_end_bracket_S2_6023', TEXTURE_MEVA_03_STEEL],
            ['stop_end_bracket_S3_6023', TEXTURE_MEVA_05_GOLD],
            ['stop_end_bracket_S4_6023', TEXTURE_MEVA_07_TIEROD],
            ['stop_end_bracket_D_6023', TEXTURE_MEVA_03_STEEL],
        ]
        self.check_texture_components(target_texture_list, geo_ele)

    def test_timber_filler_common_prop(self):
        print("\n ========== Testing timber filler common properties ========== ")
        bim2wall = self.wall_dict.get("SingleWalls", [])[1]
        elements, controller = self.create_elements_freestanding_xt(bim2wall)
        elements.extend(controller._get_timber_fillers())
        self.assertIsInstance(elements, list)
        macro_placement_element = (elements[-1].create_model_ele())[1]
        self.assertIsInstance(macro_placement_element, AllplanBasisElements.MacroPlacementElement, WRONG_PROP)
        timber_com_props = (macro_placement_element.GetAttributesList()[0]).GetAttributes()
        attr_str_vec_value = timber_com_props[2].Value
        self.check_filler_com_prop(attr_str_vec_value)

    def test_suport_filler_common_prop(self):
        print("\n ========== Testing suport filler common properties ========== ")
        elements = self.sp_filler_interactor
        macro_placement_element = elements.create_model_ele()[1]
        self.assertIsInstance(macro_placement_element, AllplanBasisElements.MacroPlacementElement, WRONG_PROP)
        support_filler_com_props = (macro_placement_element.GetAttributesList()[0]).GetAttributes()
        attr_str_vec_value = support_filler_com_props[2].Value
        self.check_filler_com_prop(attr_str_vec_value)
            
    def test_stopend_waler_15_40_common_prop(self):
        print("\n ========== Testing stop end waler MX 15-40 common properties ========== ")
        elements = self.stopend_waler_interactor
        # Check common properties from palette
        com_prop = elements.get_common_prop()        
        self.assertIsInstance(com_prop, AllplanBaseElements.CommonProperties, WRONG_PROP)
        self.check_com_prop(com_prop)

    def test_stopend_waler_15_40_textures(self):
        print("\n ========== Testing stop end waler MX 15-40 textures ========== ")
        elements = self.stopend_waler_interactor
        geo_ele = elements.get_geometry_components()
        target_texture_list = [
            ['StopEndWaler_MX1540_S', TEXTURE_PERI_03_STEEL],
            ['StopEndWaler_MX1540_D', TEXTURE_PERI_03_STEEL],
        ]
        self.check_texture_components(target_texture_list, geo_ele)

    def check_texture_components(self, target_texture_list, geo_ele):
        for idx, key, value in \
            zip(range(len(target_texture_list)), geo_ele.keys(), geo_ele.values()):
            self.assertIsInstance(key, str, WRONG_PROP)
            self.assertEqual(key, (target_texture_list[idx])[0], WRONG_ID_ATTR)
            self.assertIsInstance(value, AllplanBasisElements.TextureDefinition, WRONG_PROP)
            self.assertEqual(value.SurfacePath, (target_texture_list[idx])[1], WRONG_ID_ATTR)

    def check_filler_com_prop(self, attr_str_vec):
        self.assertEqual(str(attr_str_vec[6]), "Pen=1\n", WRONG_ID_ATTR)
        self.assertEqual(str(attr_str_vec[8]), "Stroke=1\n", WRONG_NAME_ATTR)
        self.assertEqual(str(attr_str_vec[13]), "DrawOrder=5\n", WRONG_NAME_ATTR)
        
    def check_com_prop(self, com_prop):
        self.assertEqual(com_prop.Pen, 1, WRONG_ID_ATTR) # Pen Thickness 0.25
        self.assertEqual(com_prop.Color, 1, WRONG_NAME_ATTR) # Black
        self.assertEqual(com_prop.Layer, 0, WRONG_NAME_ATTR) # Default
        self.assertEqual(com_prop.DrawOrder, 5, WRONG_NAME_ATTR) # Sequence 5
        self.assertEqual(com_prop.Stroke, 1, WRONG_NAME_ATTR)

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

    test_suite.addTest(unittest.makeSuite(TestSetCommonProp))

    return test_suite
