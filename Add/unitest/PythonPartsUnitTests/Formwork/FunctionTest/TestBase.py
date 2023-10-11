"""
    Implementation of the base class for unit tests
"""

import os
import unittest

import NemAll_Python_AllplanSettings as AllplanSettings

from TestHelper.PythonPartTestUtil import PythonPartTestUtil
from DocumentManager import DocumentManager

SINGLE_PATH = "Formwork\\SingleWall\\"
CONNECT_PATH = "Formwork\\ConnectionWalls\\"
SUB_PATH = "Library\\Construction\\Formwork\\Meva\\Accessories General"
PERI_SUB_PATH = "Library\\Construction\\Formwork\\Peri\\Accessories"

class TestBase(unittest.TestCase):
    """ implementation of the base class for the Formwork unit tests
    """

    def __init__(self, test: str):
        """ initialize

        Args:
            test: name of the test
        """

        super().__init__(test)

        self.interactor, self.palette, self.build_ele_list, self.coord_input = \
            PythonPartTestUtil.create_interactor(DocumentManager.get_instance().document, "\\Library\\PythonParts\\Formwork\\Formwork")

        self.build_ele         = self.build_ele_list[0]
        self.str_table, _      = self.build_ele.get_string_tables()
        self.palette_service   = self.interactor.palette_service
        self.str_table_service = self.interactor.str_table_service
        self.pyp_path          = self.interactor.pyp_path     


        self.bracket_2340_interactor, _, _, _ = \
            PythonPartTestUtil.create_interactor(DocumentManager.get_instance().document, os.path.join(AllplanSettings.AllplanPaths.GetPythonPartsEtcPath(), SUB_PATH, "StopEndBracket_2340"))
        self.unilock_22_interactor, _, _, _ = \
            PythonPartTestUtil.create_interactor(DocumentManager.get_instance().document, os.path.join(AllplanSettings.AllplanPaths.GetPythonPartsEtcPath(), SUB_PATH, "UniLock22"))
        self.unilock_28_interactor, _, _, _ = \
            PythonPartTestUtil.create_interactor(DocumentManager.get_instance().document, os.path.join(AllplanSettings.AllplanPaths.GetPythonPartsEtcPath(), SUB_PATH, "UniLock28"))
        self.sp_filler_interactor, _, _, _ = \
            PythonPartTestUtil.create_interactor(DocumentManager.get_instance().document, os.path.join(AllplanSettings.AllplanPaths.GetPythonPartsEtcPath(), SUB_PATH, "SupportFiller"))
        self.stopend_waler_interactor, _, _, _ = \
            PythonPartTestUtil.create_interactor(DocumentManager.get_instance().document, os.path.join(AllplanSettings.AllplanPaths.GetPythonPartsEtcPath(), PERI_SUB_PATH, "StopEndWaler"))
        self.align_coupler_bfd_interactor, _, _, _ = \
            PythonPartTestUtil.create_interactor(DocumentManager.get_instance().document, os.path.join(AllplanSettings.AllplanPaths.GetPythonPartsEtcPath(), PERI_SUB_PATH, "Align_Coup_BFD"))