# pyright: reportGeneralTypeIssues=false
# pyright: reportOptionalSubscript=false

import unittest
from collections import defaultdict

import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_Geometry as AllplanGeo

from Formwork.Controller.FormingCtl import FormingCtl
from Formwork.Controller.TimberCtl import TimberCtl
from Formwork.Controller.StopEndCtl import StopEndCtl
from Formwork.Data.DataHandler import DataHandler
from Formwork.Factories.BIM2WallFactory import BIM2WallFactory, BIM2Wall
from Formwork.BaseModules.Exception import DataNotSupport
from Formwork.BaseModules.Enumeration import FormworkElement
from Formwork.Data.DataHandler import DataHandler
from Formwork.Factories.BIM2WallFactory import BIM2Wall

from Formwork.Utility.Utility import(get_best_combination_without_fillers)

from ..TestBase import TestBase, SINGLE_PATH

MAMMUT_350 = "Mammut 350"
MAMMUT_XT  = "Mammut XT"


class TestFormingCtl(TestBase):

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

    def test_create_controller(self):
        print("\n ========== Testing Create Controller ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} ======== ")
            for bim2wall in self.wall_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                local_matrix = AllplanGeo.Matrix3D()
                controller = FormingCtl(data_handler, bim2wall[0], build_ele=self.build_ele, local_matrix=local_matrix,
                                        str_table_service=self.str_table_service, pyp_path=self.pyp_path, coord_input=self.coord_input)
                # Test instance
                self.assertIsInstance(controller, FormingCtl)
                self.assertIsInstance(controller.bim2wall, BIM2Wall)

                # Test attribute values
                self.assertIsInstance(controller.data_handler, DataHandler)
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

                # Test exception
                self.assertRaises(TypeError, setattr, controller, "bim2wall", 10)
                self.assertRaises(TypeError, setattr, controller, "bim2wall", 10.0)
                self.assertRaises(TypeError, setattr, controller, "bim2wall", "BIM2Wall")
                self.assertRaises(TypeError, setattr, controller, "bim2wall", BIM2Wall)
                self.assertRaises(TypeError, setattr, controller, "bim2wall", None)

        for key in ("SingleWalls",):
            _test_each(key)

    def check_list_library_elements(self, list_element) -> bool:
        if not isinstance(list_element, list):
            return False
        for element in list_element:
            if not isinstance(element, AllplanBasisElements.LibraryElement):
                return False
        if not list_element:
            return False
        return True

    def check_list_library_elements_is_pythonpart(self, list_element) -> bool:
        if not isinstance(list_element, list):
            return False
        for element in list_element:
            if not isinstance(element, AllplanBasisElements.LibraryElement):
                return False
            if element != AllplanElementAdapter.PythonPart_TypeUUID:
                return False
        return True

    def test_create_smart_symbol_350(self):
        print("\n ========== Testing Create SmartSymbol 350 ========== ")
        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} ======== ")
            for bim2wall in self.wall_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                input_height = bim2wall[0].height
                height_constellations = data_handler.get_height_constellation(input_height)
                local_matrix = AllplanGeo.Matrix3D()
                controller = FormingCtl(data_handler, bim2wall[0], build_ele=self.build_ele,
                                        local_matrix=local_matrix, str_table_service=self.str_table_service,
                                        pyp_path=self.pyp_path, coord_input=self.coord_input)

                for height_constellation in height_constellations:
                    # Test instance
                    self.assertEqual(self.check_list_library_elements(
                        controller.create_smart_symbol_350(height_constellation)), True)

        for key in ("SingleWalls",):
            _test_each(key)

    def test_create_smart_symbol_xt(self):
        print("\n ========== Testing Create SmartSymbol XT ========== ")
        self.interactor.modify_element_property(0, "System", MAMMUT_XT)
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} ======== ")
            for bim2wall in self.wall_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                input_height = bim2wall[0].height
                height_constellations = data_handler.get_height_constellation(input_height)
                local_matrix = AllplanGeo.Matrix3D()
                controller = FormingCtl(data_handler, bim2wall[0], build_ele=self.build_ele,
                                        local_matrix=local_matrix, str_table_service=self.str_table_service,
                                        pyp_path=self.pyp_path, coord_input=self.coord_input)

                for height_constellation in height_constellations:
                    # Test instance
                    self.assertEqual(self.check_list_library_elements(
                        controller.create_smart_symbol_xt(height_constellation)), True)

        for key in ("SingleWalls",):
            _test_each(key)

    def test_place_freestanding_350(self):
        print("\n ========== Testing Place Free Standing 350 ========== ")
        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} ======== ")
            for bim2wall in self.wall_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                input_height = bim2wall[0].height
                height_constellations = data_handler.get_height_constellation(input_height)
                local_matrix = AllplanGeo.Matrix3D()
                controller = FormingCtl(data_handler, bim2wall[0], build_ele=self.build_ele,
                                        local_matrix=local_matrix, str_table_service=self.str_table_service,
                                        pyp_path=self.pyp_path, coord_input=self.coord_input)

                for height_constellation in height_constellations:
                    # Test instance
                    self.assertEqual(self.check_list_library_elements(controller._place_freestanding(height_constellation)), True)

        for key in ("SingleWalls",):
            _test_each(key)

    def test_place_freestanding_xt(self):
        print("\n ========== Testing Place Free Standing XT ========== ")
        self.interactor.modify_element_property(0, "System", MAMMUT_XT)
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} ======== ")
            for bim2wall in self.wall_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                input_height = bim2wall[0].height
                height_constellations = data_handler.get_height_constellation(input_height)
                local_matrix = AllplanGeo.Matrix3D()
                controller = FormingCtl(data_handler, bim2wall[0], build_ele=self.build_ele,
                                        local_matrix=local_matrix, str_table_service=self.str_table_service,
                                        pyp_path=self.pyp_path, coord_input=self.coord_input)

                for height_constellation in height_constellations:
                    # Test instance
                    self.assertEqual(self.check_list_library_elements(controller._place_freestanding(height_constellation)), True)

        for key in ("SingleWalls",):
            _test_each(key)

    def test_place_panels_combination_without_filler(self):
        print("\n ========== Testing Place panels by best combination without filler ========== ")
        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} ======== ")
            for bim2wall in self.wall_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                best_combination, controller, height_constellations = self.process_freestanding_wall_element(
                    data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input, bim2wall)
                dir_vec_3rd, nor_vec_3rd, dir_vec_4th, nor_vec_4th = self.process_vector(bim2wall)
                for height_constellation in height_constellations:
                    filler_width = (sum(best_combination) - bim2wall[0].length)/2
                    start_point_3rd = bim2wall[0].start_point + dir_vec_4th*filler_width
                    start_point_4th = start_point_3rd + nor_vec_3rd*bim2wall[0].width

                    elements = controller._place_panels_combination_without_filler(height_constellation,
                                                                                    best_combination,
                                                                                    start_point_3rd,
                                                                                    start_point_4th,
                                                                                    dir_vec_3rd,
                                                                                    nor_vec_3rd,
                                                                                    nor_vec_4th)
                    # Test instance
                    self.assertEqual(self.check_list_library_elements(elements), True)

        for key in ("SingleWalls",):
            _test_each(key)

    def test_place_fixed_assembly_lock_by_combinations(self):
        print("\n ========== Testing Place panels by best combination without filler ========== ")
        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} ======== ")
            for bim2wall in self.wall_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                best_combination, controller, height_constellations = self.process_freestanding_wall_element(
                    data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input, bim2wall)
                dir_vec_3rd, nor_vec_3rd, dir_vec_4th, nor_vec_4th = self.process_vector(bim2wall)
                for height_constellation in height_constellations:
                    start_point_3rd = bim2wall[0].start_point
                    start_point_4th = start_point_3rd + nor_vec_3rd*bim2wall[0].width

                    elements = controller._place_fixed_assembly_lock_by_combinations(height_constellation,
                                                                                    best_combination,
                                                                                    start_point_3rd,
                                                                                    start_point_4th,
                                                                                    dir_vec_3rd,
                                                                                    dir_vec_4th,
                                                                                    nor_vec_3rd,
                                                                                    nor_vec_4th)
                    # Test instance
                    self.assertEqual(self.check_list_library_elements(elements), True)

        for key in ("SingleWalls",):
            _test_each(key)

    def test_place_tierod_element_freestanding_350_xt(self):
        print("\n ========== Testing Place Tie Rod Element Freestanding ========== ")
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} ======== ")
            for bim2wall in self.wall_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                best_combination, controller, height_constellations = self.process_freestanding_wall_element(
                    data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input, bim2wall)
                dir_vec_3rd, nor_vec_3rd, dir_vec_4th, nor_vec_4th = self.process_vector(bim2wall)
                for height_constellation in height_constellations:
                    filler_width = (sum(best_combination) - bim2wall[0].length)/2
                    start_point_3rd = bim2wall[0].start_point + dir_vec_4th*filler_width
                    self.interactor.modify_element_property(0, "System", MAMMUT_350)
                    elements_350 = controller._place_tierod_element_freestanding_350(height_constellation,
                                                                            best_combination,
                                                                            start_point_3rd,
                                                                            dir_vec_3rd,
                                                                            nor_vec_3rd,
                                                                            nor_vec_4th)
                    self.interactor.modify_element_property(0, "System", MAMMUT_XT)
                    panel_thickness = FormworkElement.Element_lenght.value
                    elements_xt = controller._place_tierod_element_freestanding_xt(height_constellation,
                                                                            best_combination,
                                                                            start_point_3rd,
                                                                            dir_vec_3rd,
                                                                            nor_vec_3rd,
                                                                            nor_vec_4th,
                                                                            panel_thickness)

                    self.assertEqual(self.check_list_library_elements(elements_350), True)
                    self.assertEqual(self.check_list_library_elements(elements_xt), True)

        for key in ("SingleWalls",):
            _test_each(key)

    def test_place_stop_end_timber_freestanding(self):
        print("\n ========== Testing Place stopend timber freestanding ========== ")
        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} ======== ")
            for bim2wall in self.wall_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                best_combination, controller, height_constellations = self.process_freestanding_wall_element(
                    data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input, bim2wall)
                dir_vec_3rd, nor_vec_3rd, dir_vec_4th, _nor_vec_4th = self.process_vector(bim2wall)
                for height_constellation in height_constellations:
                    filler_width = (sum(best_combination) - bim2wall[0].length)/2
                    panel_thickness = FormworkElement.Element_lenght.value
                    panel_width = FormworkElement.MinPanelFrame.value
                    start_point_3rd = bim2wall[0].start_point + dir_vec_4th*filler_width
                    start_point_4th = start_point_3rd + nor_vec_3rd*bim2wall[0].width
                    timber_pnt_1 = bim2wall[0].end_point
                    timber_pnt_2 = start_point_4th + dir_vec_3rd*filler_width
                    timber_ctl = TimberCtl(bim2wall[0].start_point,
                                            height_constellation,
                                            panel_width,
                                            panel_thickness,
                                            bim2wall[0].width,
                                            filler_width,
                                            str_table_service=self.str_table_service,
                                            pyp_path=self.pyp_path,
                                            coord_input=self.coord_input)

                    elements = controller._place_stop_end_timber(timber_ctl,
                                                                timber_pnt_1,
                                                                timber_pnt_2,
                                                                dir_vec_3rd,
                                                                nor_vec_3rd)

                    self.assertEqual(self.check_list_library_elements_is_pythonpart(elements), True)

        for key in ("SingleWalls",):
            _test_each(key)

    def test_place_stop_end_bracket_freestanding(self):
        print("\n ========== Testing Place stopend bracket freestanding ========== ")
        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        self.interactor.modify_element_property(0, "SelectionMode", 2)
        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} ======== ")
            for bim2wall in self.wall_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                best_combination, controller, height_constellations = self.process_freestanding_wall_element(
                    data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input, bim2wall)
                dir_vec_3rd, nor_vec_3rd, dir_vec_4th, nor_vec_4th = self.process_vector(bim2wall)
                for height_constellation in height_constellations:
                    panel_thickness = FormworkElement.Element_lenght.value
                    filler_width = (sum(best_combination) - bim2wall[0].length)/2
                    start_point_3rd = bim2wall[0].start_point + dir_vec_4th*filler_width
                    end_point_3rd = bim2wall[0].end_point + dir_vec_3rd*filler_width
                    bracket_constellation = self.data_handler.get_bracket_constellation(height_constellation)

                    bracket_pnt_1 = start_point_3rd + nor_vec_3rd*(bim2wall[0].width - panel_thickness)
                    bracket_pnt_2 = end_point_3rd - nor_vec_4th*panel_thickness
                    try:
                        bracket_type = data_handler.get_bracket_type(bim2wall[0].width)
                    except DataNotSupport:
                        return []
                    bracket_ctl = StopEndCtl(bim2wall[0].start_point, bracket_type, bracket_constellation,
                                             panel_thickness, bim2wall[0].width, filler_width,
                                             self.str_table_service, self.pyp_path, self.coord_input)

                    elements = controller._place_stop_end_bracket_freestanding(bracket_ctl,
                                                                               bracket_pnt_1,
                                                                               bracket_pnt_2,
                                                                               dir_vec_3rd,
                                                                               nor_vec_3rd,
                                                                               dir_vec_4th,
                                                                               nor_vec_4th)

                    self.assertEqual(self.check_list_library_elements_is_pythonpart(elements), True)

        for key in ("SingleWalls",):
            _test_each(key)

    @staticmethod
    def process_freestanding_wall_element(data_handler, build_ele, str_table_service, pyp_path, coord_input, bim2wall):
        input_height = bim2wall[0].height
        height_constellations = data_handler.get_height_constellation(input_height)
        all_widths = data_handler._get_available_widths((FormworkElement.Panel,))
        min_length = bim2wall[0].length + 100
        max_length = bim2wall[0].length + 450
        best_combination = get_best_combination_without_fillers(all_widths, 
                                                                min_length, 
                                                                max_length, 
                                                                False)
        local_matrix = AllplanGeo.Matrix3D()
        controller = FormingCtl(data_handler, bim2wall[0], build_ele=build_ele,
                                local_matrix=local_matrix, str_table_service=str_table_service,
                                pyp_path=pyp_path, coord_input=coord_input)
            
        return best_combination, controller, height_constellations
    
    @staticmethod
    def process_vector(bim2wall):                    
        # Define information of third_face (the face containing start_point and end_point) and fourth_face sides
        dir_vec_3rd = AllplanGeo.Vector3D(bim2wall[0].orientation)
        nor_vec_3rd = AllplanGeo.Vector3D(bim2wall[0].fourth_face.normal_vector)
        dir_vec_3rd.Normalize()
        nor_vec_3rd.Normalize()
        dir_vec_4th = AllplanGeo.Vector3D(bim2wall[0].orientation)
        nor_vec_4th = AllplanGeo.Vector3D(bim2wall[0].third_face.normal_vector)
        dir_vec_4th.Normalize()
        nor_vec_4th.Normalize()
        dir_vec_4th.Reverse()
        
        return dir_vec_3rd, nor_vec_3rd, dir_vec_4th, nor_vec_4th

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

    test_suite.addTest(unittest.makeSuite(TestFormingCtl))

    return test_suite
