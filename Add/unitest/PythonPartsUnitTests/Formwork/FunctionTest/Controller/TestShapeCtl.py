# pyright: reportGeneralTypeIssues=false
# pyright: reportOptionalSubscript=false

import unittest
from collections import defaultdict

import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil
import NemAll_Python_Geometry as AllplanGeo

from Formwork.Data.DataHandler import DataHandler
from Formwork.Controller.ShapeCtl import ShapeCtl
from Formwork.Factories.BIM2WallFactory import BIM2WallFactory
from Formwork.Shape.Recognizer import ShapeRecognizer
from Formwork.BaseModules.Enumeration import FormworkElement
from Formwork.Utility.Shared import GeometryUtils as geo_utils
from Formwork.Utility.Utility import check_vectors_clockwise_oxy
from Formwork.Shape.Classes import Shape, LShape #, XShape, TShape, YShape, CShape, VShape, ShapeMember, ShapeMemberBuilder

from ..TestBase import TestBase, CONNECT_PATH

UNI_LOCKS_22 = "Uni-assembly lock 22"
UNI_LOCKS_28 = "Uni-assembly lock 28"
MAMMUT_XT = "Mammut XT"
MAMMUT_350 = "Mammut 350"
TIEROD_DW15  = "Ankerstab DW15" 
TIEROD_DW20  = "Ankerstab DW20"
XT_CONE_DW20 = "XT-Konusanker 20"
XT_TIE_DW20  = "XT-Anker DW20"


class TestShapeCtl(TestBase):

    @classmethod
    def setUpClass(cls):
        print(f"\n ========== Running {__name__} ========== ")

        cls.shape_dict = defaultdict(list)
        cls.data_handler = DataHandler()

        models_dict = defaultdict(list)

        l_shape  = (CONNECT_PATH + "LShape.sym",
                    CONNECT_PATH + "LShape_465.sym",)
        t_shape  = (CONNECT_PATH + "TShape.sym",)
        c_shape  = (CONNECT_PATH + "CShape.sym",)
        v_shape  = (CONNECT_PATH + "VShape_greater90.sym",
                    CONNECT_PATH + "VShape_smaller90.sym",)
        y_shape  = (CONNECT_PATH + "YShape.sym",)
        x_shape  = (CONNECT_PATH + "XShape.sym",)

        for shape in l_shape:
            models_dict["LShape"].append(cls._create_bim2walls(shape))
        for shape in v_shape:
            models_dict["VShape"].append(cls._create_bim2walls(shape))
        for shape in t_shape:
            models_dict["TShape"].append(cls._create_bim2walls(shape))
        for shape in y_shape:
            models_dict["YShape"].append(cls._create_bim2walls(shape))
        for shape in c_shape:
            models_dict["CShape"].append(cls._create_bim2walls(shape))
        for shape in x_shape:
            models_dict["XShape"].append(cls._create_bim2walls(shape))

        recognizer = ShapeRecognizer()

        for model_key in ("TShape", "YShape", "LShape", "VShape", "CShape", "XShape", "NoShape"):
            for walls in models_dict.get(model_key, []):
                bim2wall_1, bim2wall_2 = walls
                recognizer.recognize(bim2wall_1, bim2wall_2)
                shape = recognizer.create_shape()
                cls.shape_dict[model_key].append(shape)

    @classmethod
    def tearDownClass(cls):
        AllplanUtil.ClearUnitTestDocument()

    def test_create_controller(self):
        print("\n ========== Testing Create Controller ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} shapes ======== ")
            for shape in self.shape_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                controller = ShapeCtl(data_handler, shape, build_ele=self.build_ele)

                # Test instance
                self.assertIsInstance(controller, ShapeCtl)
                self.assertIsInstance(controller.shape, Shape)

                # Test attribute values
                self.assertIsInstance(controller.data_handler, DataHandler)
                self.assertEqual(controller.build_ele, self.build_ele)
                self.assertEqual(controller.timbers, [])
                self.assertEqual(controller.uni_assembly_lock, [])
                self.assertEqual(type(controller.local_str_table), type(self.build_ele.get_string_tables()[0]))
                self.assertEqual(controller._get_timber_fillers(), controller.timbers)
                
                # Test exception
                self.assertRaises(TypeError, setattr, controller, "shape", 10)
                self.assertRaises(TypeError, setattr, controller, "shape", 10.0)
                self.assertRaises(TypeError, setattr, controller, "shape", "LShape")
                self.assertRaises(TypeError, setattr, controller, "shape", LShape)

        for key in ("TShape", "YShape", "LShape", "VShape", "CShape", "XShape", "NoShape"):
            _test_each(key)

    def test_create_boundary(self):
        print("\n ========== Testing Create Boundary ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} shapes ======== ")
            for shape in self.shape_dict.get(model_key, []):
                controller = ShapeCtl(shape_obj = shape, build_ele=self.build_ele)

                # Test instance
                self.assertIsInstance(controller.create_boundary(), list)
                for element in controller.create_boundary():
                    self.assertIsInstance(element, AllplanBasisElements.ModelElement3D)

        for key in ("TShape", "YShape", "LShape", "VShape", "CShape", "XShape", "NoShape"):
            _test_each(key)

    def test_create_smart_symbol(self):
        print("\n ========== Testing Create SmartSymbol ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} shapes ======== ")
            for shape in self.shape_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                shape_controller, constellations = self._process_place_elements(
                    shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)

                # Test instance
                self.assertIsInstance(constellations, list)
                for height_constellation in constellations:
                    self.assertIsInstance(height_constellation, tuple)
                    self.assertIsInstance(shape_controller.create_smart_symbol(height_constellation), list)
                    for element in shape_controller.create_smart_symbol(height_constellation):
                        self.assertIsInstance(element, AllplanBasisElements.LibraryElement)

        for key in ("TShape", "YShape", "LShape", "VShape", "CShape", "XShape", "NoShape"):
            _test_each(key)

    def test_create_element(self):
        print("\n ========== Testing Create full element ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} shapes ======== ")
            for shape in self.shape_dict.get(model_key, []):
                build_ele = self.build_ele
                name_  = build_ele.pyp_file_name
                param_ = build_ele.get_params_list()
                hash_  = build_ele.get_hash()
                meta_data = (name_, param_, hash_)

                data_handler = DataHandler(build_ele=self.build_ele)
                shape_controller, constellations = self._process_place_elements(
                    shape, data_handler, build_ele, self.str_table_service, self.pyp_path, self.coord_input)

                elements = shape_controller.create_element(meta_data, constellations[0])
                self.assertIsInstance(elements, list)
                for element in elements:
                    self.assertTrue(isinstance(element, AllplanBasisElements.MacroElement) or\
                                    isinstance(element, AllplanBasisElements.MacroSlideElement) or\
                                    isinstance(element, AllplanBasisElements.MacroPlacementElement) or\
                                    isinstance(element, AllplanBasisElements.LibraryElement))

        for key in ("TShape", "YShape", "LShape", "VShape", "CShape", "XShape", "NoShape"):
            _test_each(key)
            
    def test_place_elements_mammut_350(self):
        print("\n ========== Testing Place Elements Mammut 350 ========== ")

        self.interactor.modify_element_property(0, "SelectionMode", 0)
        self.interactor.modify_element_property(0, "System", MAMMUT_350)
        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} shapes ======== ")
            for shape in self.shape_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                shape_controller, constellations = self._process_place_elements(
                    shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)
                
                self.assertIsInstance(constellations, list)
                for constellation in constellations:
                    self.assertIsInstance(constellation, tuple)
                    elements = shape_controller._place_elements_mammut_350(constellation)
                    self.assertIsInstance(elements, list)

        for key in ("LShape", "TShape", "CShape", "NoShape"):
            _test_each(key)
            
    def test_place_elements_mammut_xt(self):
        print("\n ========== Testing Place Elements Mammut XT ========== ")

        self.interactor.modify_element_property(0, "SelectionMode", 0)
        self.interactor.modify_element_property(0, "System", MAMMUT_XT)
        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} shapes ======== ")
            for shape in self.shape_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                shape_controller, constellations = self._process_place_elements(
                    shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)

                self.assertIsInstance(constellations, list)
                for constellation in constellations:
                    self.assertIsInstance(constellation, tuple)
                    elements = shape_controller._place_elements_mammut_xt(constellation)
                    self.assertIsInstance(elements, list)
                    self._process_check_timber_unilocks(shape_controller, elements)

        for key in ("LShape", "TShape", "NoShape"):
            _test_each(key)
        
    def test_place_elements_LShape(self):
        print("\n ========== Testing Place Elements LShape ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} shapes ======== ")
            for shape in self.shape_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                shape_controller, constellations = self._process_place_elements(
                    shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)

                elements = shape_controller._place_elements_l_shape(constellations[0])
                self.assertIsInstance(elements, list)
                for element in elements:
                    self.assertIsInstance(element, AllplanBasisElements.LibraryElement)

        for key in ("LShape", "VShape", "NoShape"):
            _test_each(key)

    def test_place_elements_TShape(self):
        print("\n ========== Testing Place Elements TShape ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} shapes ======== ")
            for shape in self.shape_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                shape_controller, constellations = self._process_place_elements(
                    shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)

                elements = shape_controller._place_elements_t_shape(constellations[0])
                self.assertIsInstance(elements, list)
                for element in elements:
                    self.assertIsInstance(element, AllplanBasisElements.LibraryElement)

        for key in ("TShape", "YShape", "NoShape"):
            _test_each(key)

    def test_place_elements_CShape(self):
        print("\n ========== Testing Place Elements TShape ========== ")

        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} shapes ======== ")
            for shape in self.shape_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                shape_controller, constellations = self._process_place_elements(
                    shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)

                elements = shape_controller._place_elements_c_shape(constellations[0])
                self.assertIsInstance(elements, list)
                for element in elements:
                    self.assertIsInstance(element, AllplanBasisElements.LibraryElement)

        for key in ("CShape", "NoShape"):
            _test_each(key)

    def test_place_elements_LShape_MXT(self):
        print("\n ========== Testing Place Elements LShape Mammut XT ========== ")

        self._select_mode_1_mammut_xt()
        def _test_each(model_key: str):
            print(f" ======== Test all {model_key} shapes ======== ")
            for shape in self.shape_dict.get(model_key, []):
                data_handler = DataHandler(build_ele=self.build_ele)
                shape_controller, constellations = self._process_place_elements(
                    shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)

                elements = shape_controller._place_elements_l_shape_mammutxt(constellations[0])
                self.assertIsInstance(elements, list)
                for element in elements:
                    self.assertIsInstance(element, AllplanBasisElements.LibraryElement)
                self._process_check_timber_unilocks(shape_controller, elements)

        for key in ("LShape", "NoShape"):
            _test_each(key)

    def test_place_elements_TShape_MXT(self):
        print("\n ========== Testing Place Elements TShape Mammut XT ========== ")

        self._select_mode_1_mammut_xt()
        model_key = "TShape"
        print(f" ======== Test all {model_key} shapes ======== ")
        for shape in self.shape_dict.get(model_key, []):
            data_handler = DataHandler(build_ele=self.build_ele)
            shape_controller, constellations = self._process_place_elements(
                shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)

            elements = shape_controller._place_elements_t_shape_mammutxt(constellations[0])
            self.assertIsInstance(elements, list)
            for element in elements:
                self.assertIsInstance(element, AllplanBasisElements.LibraryElement)
            self._process_check_timber_unilocks(shape_controller, elements)

    def test_place_elements_CShape_MXT(self):
        print("\n ========== Testing Place Elements CShape Mammut XT ========== ")

        self._select_mode_1_mammut_xt()
        model_key = "CShape"
        print(f" ======== Test all {model_key} shapes ======== ")
        for shape in self.shape_dict.get(model_key, []):
            data_handler = DataHandler(build_ele=self.build_ele)
            shape_controller, constellations = self._process_place_elements(
                shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)

            elements = shape_controller._place_elements_c_shape_mammutxt(constellations[0])
            self.assertIsInstance(elements, list)
            for element in elements:
                self.assertIsInstance(element, AllplanBasisElements.LibraryElement)
                
    def test_get_points_and_vectors_for_c_shape(self):
        print("\n ========== Testing get points and vectors for Cshape ========== ")

        self._select_mode_1_mammut_xt()
        model_key = "CShape"
        print(f" ======== Test all {model_key} shapes ======== ")
        for shape in self.shape_dict.get(model_key, []):
            data_handler = DataHandler(build_ele=self.build_ele)
            shape_controller, _constellations = self._process_place_elements(
                shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)

            elements = shape_controller._get_points_and_vectors_for_c_shape()
            for element in elements:
                self.assertIsInstance(element, list)

    def test_place_single_sided_tierod_general_case_for_cshape(self):
        print("\n ========== Testing place single sided tierod general case for Mammut XT CShape ========== ")
        
        self._select_mode_1_mammut_xt()
        model_key = "CShape"
        print(f" ======== Test all {model_key} shapes ======== ")
        for shape in self.shape_dict.get(model_key, []):     
            wall_1_width, wall_2_width = shape.first_wall.width, shape.second_wall.width
            self._check_wall_mammut_xt_accepts(wall_1_width, wall_2_width)
            data_handler = DataHandler(build_ele=self.build_ele)
            shape_controller, constellations = self._process_place_elements(
                shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)
            inter_thickness = 350.0
            
            inter_point = shape.intersect_point
            point_1 = shape.point_1
            point_2 = shape.point_2
            
            norm_dir_1 = AllplanGeo.Vector3D(shape.direction_1)
            norm_dir_2 = AllplanGeo.Vector3D(shape.direction_2)
            norm_dir_1.Normalize()
            norm_dir_2.Normalize()
            negative_z_vec = norm_dir_1*norm_dir_2
            rotation_line = AllplanGeo.Line3D(inter_point, negative_z_vec)
            norm_nor_1 = geo_utils.rotation(norm_dir_1, rotation_line, 180)
            norm_nor_2 = geo_utils.rotation(norm_dir_2, rotation_line, 180)
            
            panels_250_pnt_1 = point_1 + norm_dir_2 * inter_thickness
            panels_250_pnt_2 = point_1 + norm_nor_2 * (inter_thickness + wall_1_width)
            panels_250_pnt_3 = point_2 + norm_nor_1 * inter_thickness
            panels_250_pnt_4 = point_2 + norm_dir_1 * (inter_thickness + wall_2_width)
            
            elements = shape_controller._place_single_panel_250_general_case(
                constellations[0], panels_250_pnt_1, wall_1_width, [0, 0], norm_dir_2, norm_nor_1)
            elements.extend(shape_controller._place_single_panel_250_general_case(
                constellations[0], panels_250_pnt_2, wall_2_width, [0, 0], norm_nor_2, norm_nor_1))
            elements.extend(shape_controller._place_single_panel_250_general_case(
                constellations[0], panels_250_pnt_3, wall_1_width, [0, 0], norm_nor_1, norm_nor_2))
            elements.extend(shape_controller._place_single_panel_250_general_case(
                constellations[0], panels_250_pnt_4, wall_1_width, [0, 0], norm_dir_1, norm_nor_2))
            for element in elements:
                self.assertTrue(isinstance(element, AllplanBasisElements.MacroElement) or\
                                isinstance(element, AllplanBasisElements.MacroSlideElement) or\
                                isinstance(element, AllplanBasisElements.MacroPlacementElement) or\
                                isinstance(element, AllplanBasisElements.LibraryElement))
            self.assertIsInstance(elements, list)
            for element in elements:
                self.assertIsInstance(element, AllplanBasisElements.LibraryElement)

    def test_place_single_sided_tierod_general_case_for_tshape(self):
        print("\n ========== Testing place single sided tierod general case for Mammut XT TShape ========== ")
        
        self._select_mode_1_mammut_xt()
        model_key = "TShape"
        print(f" ======== Test all {model_key} shapes ======== ")
        for shape in self.shape_dict.get(model_key, []):     
            host_wall_width, guest_wall_width = shape.first_wall.width, shape.second_wall.width
            self._check_wall_mammut_xt_accepts(host_wall_width, guest_wall_width)
            data_handler = DataHandler(build_ele=self.build_ele)
            shape_controller, constellations = self._process_place_elements(
                shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)
            inter_thickness = data_handler.get_inside_corner_width_t_shape_mammutxt(guest_wall_width)
            _panels, filler, _panel_width = data_handler.get_suitable_panel_mammut_xt_for_tshape(constellations[0], guest_wall_width)
            if len(filler) == 1 and filler[0] > FormworkElement.MaximumFillerWidthOn1sideTShapeMXT.value:
                tmp_filler = tuple([float(filler[0]/2),float(filler[0]/2)])
                filler = tuple(tmp_filler)
            elif len(filler) == 1:
                tmp_filler = tuple([float(filler[0]), float(0)])
                filler = tuple(tmp_filler)

            vec_2nd = AllplanGeo.Vector3D(shape.second_wall.direction_close_far_side)
            vec_1st = AllplanGeo.Vector3D(shape.direction_hostface_one_hostface_two)
            # Do not use self.shape.first_wall.direction_close_far_side, direction can be opposite
            vec_1st.Normalize()
            vec_2nd.Normalize()
            line_3d = AllplanGeo.Line3D(AllplanGeo.Point3D(0.0, 0.0, 0.0), AllplanGeo.Vector3D(0.0, 0.0, 1.0))
            vec_2nd_reverted = geo_utils.rotation(vec_2nd, line_3d, 180.0)
            vec_1st_reverted = geo_utils.rotation(vec_1st, line_3d, 180.0)
            vec_1st_reverted.Normalize()
            vec_2nd_reverted.Normalize()
            check_clockwise = check_vectors_clockwise_oxy(
                shape.direction_hostface_one_hostface_two, shape.direction_closeface_farface)
            placement_point_panel = AllplanGeo.Point3D(shape.interior_point_2) + vec_2nd_reverted*host_wall_width
            placement_point_panel = AllplanGeo.Point3D(placement_point_panel) + vec_1st*(inter_thickness-filler[0])
            panel_250_base_pnt_1 = AllplanGeo.Point3D(placement_point_panel) + vec_1st*filler[0]
            panel_250_base_pnt_2 = AllplanGeo.Point3D(shape.interior_point_1) + vec_2nd_reverted*host_wall_width
            panel_250_base_pnt_2 = panel_250_base_pnt_2 + vec_1st_reverted*inter_thickness
            panel_250_base_pnt_3 = AllplanGeo.Point3D(shape.interior_point_2) + vec_2nd*inter_thickness
            
            elements = shape_controller._place_single_panel_250_general_case(
                constellations[0], panel_250_base_pnt_1, host_wall_width, filler, vec_1st, vec_2nd)        
            if filler[1] > 0:
                elements.extend(shape_controller._place_single_panel_250_general_case(
                    constellations[0], panel_250_base_pnt_2, host_wall_width, filler, vec_1st_reverted, vec_2nd))
            else:
                elements.extend(shape_controller._place_single_panel_250_general_case(
                    constellations[0], panel_250_base_pnt_2, host_wall_width, [0 , 0], vec_1st_reverted, vec_2nd))
            # Place the panel 250 for the guest wall
            if check_clockwise: # Check check_clockwise to keep the direction of the single sided tierods
                panel_250_base_pnt_3 = panel_250_base_pnt_3 - vec_1st*guest_wall_width
                elements.extend(shape_controller._place_single_panel_250_general_case(
                    constellations[0], panel_250_base_pnt_3, guest_wall_width, (0, 0), vec_2nd, vec_1st))
            else:
                elements.extend(shape_controller._place_single_panel_250_general_case(
                    constellations[0], panel_250_base_pnt_3, guest_wall_width, (0, 0), vec_2nd, vec_1st_reverted))
            
            self.assertIsInstance(elements, list)
            for element in elements:
                self.assertIsInstance(element, AllplanBasisElements.LibraryElement)

    def test_place_single_sided_tierod_general_case_for_lshape(self):
        print("\n ========== Testing place single sided tierod general case for Mammut XT LShape ========== ")
        
        self._select_mode_1_mammut_xt()
        model_key = "LShape"
        print(f" ======== Test all {model_key} shapes ======== ")
        for shape in self.shape_dict.get(model_key, []):
            wall_1_width, wall_2_width = shape.first_wall.width, shape.second_wall.width
            self._check_wall_mammut_xt_accepts(wall_1_width, wall_2_width)
            wall_width_max = max(wall_1_width, wall_2_width)
            data_handler = DataHandler(build_ele=self.build_ele)
            shape_controller, constellations = self._process_place_elements(
                shape, data_handler, self.build_ele, self.str_table_service, self.pyp_path, self.coord_input)
            inter_thickness_1 = inter_thickness_2 = data_handler.get_inside_corner_width(wall_width_max)
            outer_1_thickness = outer_2_thickness = data_handler.get_outside_corner_width(wall_width_max)
            panel_2_target = wall_1_width + inter_thickness_1
            panel_1_target = wall_2_width + inter_thickness_2
            _panels_1, filler_1, panels_1_width = data_handler.get_suitable_panel_mammut_xt(
                constellations[0], panel_1_target, outer_2_thickness)
            _panels_2, filler_2, panels_2_width = data_handler.get_suitable_panel_mammut_xt(
                constellations[0], panel_2_target, outer_1_thickness)

            vec_2nd = AllplanGeo.Vector3D(shape.second_wall.direction_close_far_side)
            vec_1st = AllplanGeo.Vector3D(shape.first_wall.direction_close_far_side)
            vec_1st.Normalize()
            vec_2nd.Normalize()
            vec_1st_reverse = AllplanGeo.Vector3D(vec_1st)
            vec_2nd_reverse = AllplanGeo.Vector3D(vec_2nd)
            vec_1st_reverse.Reverse()
            vec_2nd_reverse.Reverse()

            # Define all needed base points
            exter_base_pnt = shape.exterior_point
            ex_1_factor = outer_1_thickness + panels_1_width[0]
            ex_2_factor = outer_1_thickness + panels_2_width[0]
            if filler_1[0] > 0:
                panel_250_ex_1_pnt = exter_base_pnt + (vec_1st * (ex_1_factor + filler_1[0]))
            else:
                panel_250_ex_1_pnt = exter_base_pnt + (vec_1st * ex_1_factor)
            if filler_2[0] > 0:
                panel_250_ex_2_pnt = exter_base_pnt + (vec_2nd * (ex_2_factor + filler_2[0]))
            else:
                panel_250_ex_2_pnt = exter_base_pnt + (vec_2nd * ex_2_factor)
            elements = shape_controller._place_single_panel_250_general_case(
                constellations[0], panel_250_ex_1_pnt, wall_1_width, filler_1, vec_1st, vec_2nd)
            elements.extend(shape_controller._place_single_panel_250_general_case(
                constellations[0], panel_250_ex_2_pnt, wall_2_width, filler_2, vec_2nd, vec_1st))
            
            self.assertIsInstance(elements, list)
            for element in elements:
                self.assertIsInstance(element, AllplanBasisElements.LibraryElement)

    def _process_check_timber_unilocks(self, shape_controller, elements):
        # Timber fillers
        elements.extend(shape_controller._get_timber_fillers())
        macro_element = (elements[-2].create_model_ele())[0]
        macro_element_properties = macro_element.GetMacroProperties()
        timber_filler_name = macro_element_properties.Name
        self.assertEqual(timber_filler_name, "Timber Filler")
        # Uni-locks
        elements.extend(shape_controller._get_uni_assembly_lock())
        macro_element = (elements[-2].create_model_ele())[0]
        macro_element_properties = macro_element.GetMacroProperties()
        uni_locks_name = macro_element_properties.Name
        self.assertEqual(uni_locks_name, UNI_LOCKS_22)
                
    @staticmethod
    def _check_wall_mammut_xt_accepts(wall_1_width, wall_2_width):
        if not (150 <= wall_1_width <= 500 and 150 <= wall_2_width <= 500):
            return []
        else:
            return wall_1_width, wall_2_width
    
    def _select_mode_1_mammut_xt(self):
        self.interactor.modify_element_property(0, "SelectionMode", 0)
        self.interactor.modify_element_property(0, "System", MAMMUT_XT)
        self.interactor.modify_element_property(0, "TieRod", XT_TIE_DW20)
    
    @staticmethod
    def _process_place_elements(shape, data_handler, build_ele, str_table_service, pyp_path, coord_input):
        local_matrix = AllplanGeo.Matrix3D()
        shape_controller = ShapeCtl(data_handler, shape, local_matrix, str_table_service, \
            pyp_path, coord_input, build_ele=build_ele)
        constellations = shape_controller.get_combinations()
        
        return shape_controller, constellations
    
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

    test_suite.addTest(unittest.makeSuite(TestShapeCtl))

    return test_suite
