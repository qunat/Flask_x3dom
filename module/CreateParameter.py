# -*- coding: utf-8 -*-
import os
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeRevol
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeChamfer
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax1, gp_Dir
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Builder, TopoDS_Compound, topods_CompSolid
from OCC.Extend.DataExchange import read_step_file, write_step_file
from OCC.Core.ChFi2d import ChFi2d_ChamferAPI
from OCC.Core.STEPControl import STEPControl_Reader, STEPControl_Writer
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Ax1, gp_Dir


class Create_boll_SCcrew_sfu(object):
    def __init__(self):  # 初始化参数
        pass
        # 螺母参数初始化---------------------------
        self.SFU01204_4_dict = {"d": 12, "I": 4, "Da": 2.500, "D": 24, "A": 40, "B": 10, "L": 40,
                                "W": 32, "H": 30, "X": 4.5, "Q": "-", "N": "1x4", "Ca": 902, "Coa": 1884,
                                "kgf/um": 26}  #
        self.SFU01604_4_dict = {"d": 16, "I": 4, "Da": 2.381, "D": 28, "A": 48, "B": 10, "L": 40,
                                "W": 38, "H": 40, "X": 5.5, "Q": "M6", "N": "1x4", "Ca": 973, "Coa": 2406,
                                "kgf/um": 32}  #
        self.SFU01605_4_dict = {"d": 16, "I": 5, "Da": 3.175, "D": 28, "A": 48, "B": 10, "L": 50,
                                "W": 38, "H": 40, "X": 5.5, "Q": "M6", "N": "1x4", "Ca": 1380, "Coa": 3052,
                                "kgf/um": 32}  #
        self.SFU01610_4_dict = {"d": 16, "I": 10, "Da": 3.175, "D": 28, "A": 48, "B": 10, "L": 57,
                                "W": 38, "H": 40, "X": 5.5, "Q": "M6", "N": "1x3", "Ca": 1103, "Coa": 2401,
                                "kgf/um": 26}  #
        self.SFU02004_4_dict = {"d": 20, "I": 4, "Da": 2.381, "D": 36, "A": 58, "B": 10, "L": 42,
                                "W": 47, "H": 44, "X": 6.6, "Q": "M6", "N": "1x4", "Ca": 1066, "Coa": 2987,
                                "kgf/um": 38}
        self.SFU02005_4_dict = {"d": 20, "I": 5, "Da": 3.175, "D": 36, "A": 58, "B": 10, "L": 51,
                                "W": 47, "H": 44, "X": 6.6, "Q": "M6", "N": "1x4", "Ca": 1551, "Coa": 3875,
                                "kgf/um": 39}
        self.SFU02504_4_dict = {"d": 25, "I": 4, "Da": 2.381, "D": 40, "A": 62, "B": 10, "L": 42,
                                "W": 51, "H": 48, "X": 6.6, "Q": "M6", "N": "1x4", "Ca": 1180, "Coa": 3795,
                                "kgf/um": 43}
        self.SFU02505_4_dict = {"d": 25, "I": 5, "Da": 3.175, "D": 40, "A": 62, "B": 10, "L": 51,
                                "W": 51, "H": 48, "X": 6.6, "Q": "M6", "N": "1x4", "Ca": 1724, "Coa": 4904,
                                "kgf/um": 45}
        self.SFU02506_4_dict = {"d": 25, "I": 6, "Da": 3.969, "D": 40, "A": 62, "B": 10, "L": 54,
                                "W": 51, "H": 48, "X": 6.6, "Q": "M6", "N": "1x4", "Ca": 2318, "Coa": 6057,
                                "kgf/um": 47}
        self.SFU02508_4_dict = {"d": 25, "I": 8, "Da": 4.762, "D": 40, "A": 62, "B": 10, "L": 63,
                                "W": 51, "H": 48, "X": 6.6, "Q": "M6", "N": "1x4", "Ca": 2963, "Coa": 7313,
                                "kgf/um": 49}
        self.SFU02510_4_dict = {"d": 25, "I": 10, "Da": 4.762, "D": 40, "A": 62, "B": 12, "L": 85,
                                "W": 51, "H": 48, "X": 6.6, "Q": "M6", "N": "1x4", "Ca": 2954, "Coa": 7295,
                                "kgf/um": 50}
        self.SFU03204_4_dict = {"d": 32, "I": 4, "Da": 2.381, "D": 50, "A": 80, "B": 12, "L": 44,
                                "W": 65, "H": 62, "X": 9.0, "Q": "M6", "N": "1x4", "Ca": 1296, "Coa": 4838,
                                "kgf/um": 51}
        self.SFU03205_4_dict = {"d": 32, "I": 5, "Da": 2.381, "D": 50, "A": 80, "B": 12, "L": 52,
                                "W": 65, "H": 62, "X": 9.0, "Q": "M6", "N": "1x4", "Ca": 1922, "Coa": 6343,
                                "kgf/um": 54}
        self.SFU03206_4_dict = {"d": 32, "I": 6, "Da": 3.969, "D": 50, "A": 80, "B": 12, "L": 57,
                                "W": 65, "H": 62, "X": 9.0, "Q": "M6", "N": "1x4", "Ca": 2632, "Coa": 7979,
                                "kgf/um": 57}
        self.SFU03208_4_dict = {"d": 32, "I": 8, "Da": 3.969, "D": 50, "A": 80, "B": 12, "L": 65,
                                "W": 65, "H": 62, "X": 9.0, "Q": "M6", "N": "1x4", "Ca": 3387, "Coa": 9622,
                                "kgf/um": 60}
        self.SFU03210_4_dict = {"d": 32, "I": 10, "Da": 3.969, "D": 50, "A": 80, "B": 12, "L": 90,
                                "W": 65, "H": 62, "X": 9.0, "Q": "M6", "N": "1x4", "Ca": 4805, "Coa": 12208,
                                "kgf/um": 61}
        self.SFU04005_4_dict = {"d": 40, "I": 5, "Da": 3.175, "D": 63, "A": 93, "B": 14, "L": 55,
                                "W": 78, "H": 70, "X": 9.0, "Q": "M6", "N": "1x4", "Ca": 2110, "Coa": 7988,
                                "kgf/um": 63}
        self.SFU04006_4_dict = {"d": 40, "I": 6, "Da": 3.969, "D": 63, "A": 93, "B": 14, "L": 60,
                                "W": 78, "H": 70, "X": 9.0, "Q": "M6", "N": "1x4", "Ca": 2873, "Coa": 9913,
                                "kgf/um": 66}
        self.SFU04008_4_dict = {"d": 40, "I": 8, "Da": 4.762, "D": 63, "A": 93, "B": 14, "L": 67,
                                "W": 78, "H": 70, "X": 9.0, "Q": "M6", "N": "1x4", "Ca": 3712, "Coa": 11947,
                                "kgf/um": 70}
        self.SFU04010_4_dict = {"d": 40, "I": 10, "Da": 6.325, "D": 63, "A": 93, "B": 14, "L": 93,
                                "W": 78, "H": 70, "X": 9.0, "Q": "M6", "N": "1x4", "Ca": 5399, "Coa": 15500,
                                "kgf/um": 73}
        self.SFU05010_4_dict = {"d": 50, "I": 10, "Da": 6.325, "D": 75, "A": 110, "B": 16, "L": 93,
                                "W": 93, "H": 85, "X": 11, "Q": "M6", "N": "1x4", "Ca": 6004, "Coa": 19614,
                                "kgf/um": 85}
        self.SFU05020_4_dict = {"d": 50, "I": 20, "Da": 7.144, "D": 75, "A": 110, "B": 16, "L": 138,
                                "W": 93, "H": 85, "X": 11, "Q": "M6", "N": "1x4", "Ca": 7142, "Coa": 22588,
                                "kgf/um": 94}
        self.SFU06310_4_dict = {"d": 63, "I": 10, "Da": 6.325, "D": 90, "A": 125, "B": 18, "L": 98,
                                "W": 108, "H": 95, "X": 11, "Q": "M6", "N": "1x4", "Ca": 6719, "Coa": 25358,
                                "kgf/um": 99}
        self.SFU06320_4_dict = {"d": 63, "I": 10, "Da": 9.525, "D": 95, "A": 135, "B": 20, "L": 149,
                                "W": 115, "H": 100, "X": 13.5, "Q": "M6", "N": "1x4", "Ca": 11444, "Coa": 36653,
                                "kgf/um": 112}
        self.SFU08010_4_dict = {"d": 80, "I": 10, "Da": 6.325, "D": 95, "A": 105, "B": 20, "L": 98,
                                "W": 125, "H": 110, "X": 13.5, "Q": "M6", "N": "1x4", "Ca": 7346, "Coa": 31953,
                                "kgf/um": 109}
        self.SFU08020_4_dict = {"d": 80, "I": 20, "Da": 9.525, "D": 125, "A": 165, "B": 25, "L": 154,
                                "W": 145, "H": 130, "X": 13.5, "Q": "M6", "N": "1x4", "Ca": 12911, "Coa": 47747,
                                "kgf/um": 138}
        self.SFU10020_4_dict = {"d": 100, "I": 20, "Da": 9.525, "D": 125, "A": 150, "B": 30, "L": 180,
                                "W": 170, "H": 155, "X": 13.5, "Q": "M6", "N": "1x4", "Ca": 14303, "Coa": 60698,
                                "kgf/um": 162}
        self.SFU_serise_dict = {"SFU01204-4": self.SFU01204_4_dict, "SFU01604-4": self.SFU01604_4_dict,
                                "SFU01605-4": self.SFU01605_4_dict,
                                "SFU01610-4": self.SFU01610_4_dict, "SFU02004-4": self.SFU02004_4_dict,
                                "SFU02005-4": self.SFU02005_4_dict,
                                "SFU02505-4": self.SFU02505_4_dict, "SFU02506-4": self.SFU02506_4_dict,
                                "SFU02508-4": self.SFU02508_4_dict,
                                "SFU02510-4": self.SFU02510_4_dict, "SFU03204-4": self.SFU03204_4_dict,
                                "SFU03205-4": self.SFU03205_4_dict,
                                "SFU03206-4": self.SFU03206_4_dict, "SFU03208-4": self.SFU03208_4_dict,
                                "SFU03210-4": self.SFU03210_4_dict,
                                "SFU04005-4": self.SFU04005_4_dict, "SFU04006-4": self.SFU04006_4_dict,
                                "SFU04008-4": self.SFU04008_4_dict, "SFU04010-4": self.SFU04010_4_dict,
                                "SFU05010-4": self.SFU05010_4_dict, "SFU05020-4": self.SFU05020_4_dict,
                                "SFU06310-4": self.SFU06310_4_dict,
                                "SFU06320-4": self.SFU06320_4_dict, "SFU08010-4": self.SFU08010_4_dict,
                                "SFU08020-4": self.SFU08020_4_dict,
                                "SFU10020-4": self.SFU10020_4_dict}
        self.series=self.SFU_serise_dict
        self.total_length=0
        self.asd=0
        # 丝杆参数初始化----------------------------------
        # -------------BKBF系列--------------------------
        self.BK_10_dict = {"D1": 8., "D2": 10., "D3": 12, "D4": 8, "D5": 7.0, "L1": 15, "L2": 16, "L3": 39, "L4": 10,
                           "L5": 7.9, "L6": 0.9, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.BK_12_dict = {"D1": 10., "D2": 12., "D3": 16, "D4": 10, "D5": 9.6, "L1": 15, "L2": 14, "L3": 39, "L4": 11,
                           "L5": 9.15, "L6": 1.15, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.BK_15_dict = {"D1": 12., "D2": 15., "D3": 20, "D4": 15, "D5": 14.3, "L1": 20, "L2": 12, "L3": 40, "L4": 13,
                           "L5": 10.15, "L6": 1.15, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.BK_17_dict = {"D1": 15., "D2": 17., "D3": 20, "D4": 17, "D5": 16.2, "L1": 23, "L2": 17, "L3": 53, "L4": 16,
                           "L5": 13.15, "L6": 1.15, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.BK_20_dict = {"D1": 17., "D2": 20., "D3": 25, "D4": 20, "D5": 16.2, "L1": 25, "L2": 15, "L3": 53, "L4": 16,
                           "L5": 13.35, "L6": 1.35, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.BK_25_dict = {"D1": 20., "D2": 25., "D3": 30, "D4": 25, "D5": 23.9, "L1": 30, "L2": 18, "L3": 65, "L4": 20,
                           "L5": 16.35, "L6": 1.35, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.BK_30_dict = {"D1": 25., "D2": 30., "D3": 35, "D4": 30, "D5": 28.6, "L1": 38, "L2": 25, "L3": 72, "L4": 21,
                           "L5": 17.75, "L6": 1.75, "C1": 0.5, "C2": 0.7, "C3": 1.0}  # ok
        self.BK_35_dict = {"D1": 30., "D2": 35., "D3": 40, "D4": 35, "D5": 33, "L1": 45, "L2": 28, "L3": 83, "L4": 22,
                           "L5": 18.75, "L6": 1.75, "C1": 0.5, "C2": 1.0, "C3": 1.0}  # ok
        self.BK_40_dict = {"D1": 35., "D2": 40., "D3": 50, "D4": 40, "D5": 38, "L1": 50, "L2": 35, "L3": 98, "L4": 23,
                           "L5": 19.95, "L6": 1.95, "C1": 0.5, "C2": 1.0, "C3": 1.0}  # ok
        self.BK_serise_dict = {"BKBF10": self.BK_10_dict, "BKBF12": self.BK_12_dict, "BKBF15": self.BK_15_dict,
                               "BKBF17": self.BK_17_dict,
                               "BKBF20": self.BK_20_dict, "BKBF25": self.BK_25_dict, "BKBF30": self.BK_30_dict,
                               "BKBF35": self.BK_35_dict,
                               "BKBF40": self.BK_40_dict}
        ####---------#######
        self.BF_10_dict={"D1":8,"E":10,"A":7.6,"B":0.9,"C":7.9}
        self.BF_12_dict={"D1":10,"E":11,"A":9.6,"B":1.15,"C":9.15}
        self.BF_15_dict = {"D1": 15, "E": 13, "A": 14.3, "B": 1.15, "C": 10.15}
        self.BF_17_dict = {"D1": 17, "E": 16, "A": 16.2, "B": 1.15, "C": 13.15}
        self.BF_20_dict = {"D1": 20, "E": 16, "A": 19, "B": 1.35, "C": 13.35}
        self.BF_25_dict = {"D1": 25, "E": 20, "A": 23.9, "B": 1.35, "C": 16.35}
        self.BF_30_dict = {"D1": 30, "E": 21, "A": 28.6, "B": 1.75, "C": 17.75}
        self.BF_35_dict = {"D1": 35, "E": 22, "A": 33, "B": 1.75, "C": 18.75}
        self.BF_40_dict = {"D1": 40, "E": 23, "A": 38, "B": 1.95, "C": 19.95}
        self.BF_serise_dict={"BF10":self.BF_10_dict,"BF12":self.BF_12_dict,"BF15":self.BF_15_dict,"BF17":self.BF_17_dict,
                             "BF20":self.BF_20_dict,"BF25":self.BF_25_dict,"BF30":self.BF_30_dict,"BF35":self.BF_35_dict,
                             "BF40":self.BF_40_dict}
        # -------------EKEF系列--------------------------
        self.EK_06_dict = {"D1": 4., "D2": 6., "D3": 6, "D4": 6, "D5": 5.7, "L1": 8, "L2": 10, "L3": 30, "L4": 9,
                           "L5": 6.8, "L6": 0.8, "C1": 0.3, "C2": 0.3, "C3": 0.3}  # ok
        self.EK_08_dict = {"D1": 6., "D2": 8., "D3": 10, "D4": 6, "D5": 5.7, "L1": 9, "L2": 10, "L3": 35, "L4": 9,
                           "L5": 6.8, "L6": 0.8, "C1": 0.3, "C2": 0.3, "C3": 0.3}  # ok
        self.EK_10_dict = {"D1": 8., "D2": 10., "D3": 12, "D4": 8, "D5": 7.6, "L1": 15, "L2": 11, "L3": 36, "L4": 10,
                           "L5": 7.9, "L6": 0.9, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.EK_12_dict = {"D1": 10., "D2": 12., "D3": 15, "D4": 10, "D5": 9.6, "L1": 15, "L2": 11, "L3": 36, "L4": 11,
                           "L5": 9.15, "L6": 1.15, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.EK_15_dict = {"D1": 12., "D2": 15., "D3": 18, "D4": 15, "D5": 14.3, "L1": 20, "L2": 11, "L3": 49, "L4": 13,
                           "L5": 10.15, "L6": 1.15, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.EK_20_dict = {"D1": 17., "D2": 20., "D3": 25, "D4": 20, "D5": 19, "L1": 25, "L2": 17, "L3": 64, "L4": 19,
                           "L5": 15.35, "L6": 1.35, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.EK_25_dict = {"D1": 20., "D2": 25., "D3": 32, "D4": 25, "D5": 23.9, "L1": 30, "L2": 18, "L3": 65, "L4": 20,
                           "L5": 16.35, "L6": 1.35, "C1": 0.5, "C2": 0.7, "C3": 0.1}  # ok
        self.EK_serise_dict = {"EKEF06": self.EK_06_dict, "EKEF08": self.EK_08_dict, "EKEF10": self.EK_10_dict,
                               "EKEF12": self.EK_12_dict,
                               "EKEF15": self.EK_15_dict, "EKEF20": self.EK_20_dict, "EKEF25": self.EK_25_dict}
        ####---------#######
        self.EF_6_dict={"D1":6,"E":9,"A":5.7,"B":0.8,"C":6.8}
        self.EF_8_dict = {"D1": 6, "E": 9, "A": 5.7, "B": 0.8, "C": 6.8}
        self.EF_10_dict = {"D1": 8, "E": 10, "A": 7.6, "B":0.9, "C": 7.9}
        self.EF_12_dict = {"D1": 10, "E": 11, "A": 9.6, "B": 1.15, "C": 9.15}
        self.EF_15_dict = {"D1": 15, "E": 13, "A": 14.3, "B": 1.15, "C": 10.15}
        self.EF_20_dict = {"D1": 20, "E": 19, "A": 19, "B": 1.35, "C": 15.35}
        self.EF_25_dict = {"D1": 25, "E": 20, "A": 23.9, "B": 1.35, "C": 16.35}
        self.EF_serise_dict={"EF6":self.EF_6_dict,"EF8":self.EF_8_dict,"EF10":self.EF_10_dict,"EF12":self.EF_12_dict,
                             "EF15":self.EF_15_dict,"EF20":self.EF_20_dict,"EF25":self.EF_25_dict}

        # -------------FKFF系列--------------------------
        self.FK_08_dict = {"D1": 6., "D2": 8., "D3": 10, "D4": 6, "D5": 5.7, "L1": 9, "L2": 15, "L3": 25, "L4": 9,
                           "L5": 6.8, "L6": 0.8, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_10_dict = {"D1": 8., "D2": 10., "D3": 12, "D4": 8, "D5": 5.6, "L1": 15, "L2": 11, "L3": 36, "L4": 10,
                           "L5": 7.9, "L6": 0.9, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_12_dict = {"D1": 10., "D2": 12., "D3": 15, "D4": 10, "D5": 9.6, "L1": 15, "L2": 11, "L3": 36, "L4": 11,
                           "L5": 9.15, "L6": 1.15, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_15_dict = {"D1": 12., "D2": 15., "D3": 18, "D4": 15, "D5": 14.3, "L1": 20, "L2": 13, "L3": 36, "L4": 13,
                           "L5": 10.15, "L6": 1.15, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_20_dict = {"D1": 17., "D2": 20., "D3": 25, "D4": 20, "D5": 19, "L1": 25, "L2": 17, "L3": 64, "L4": 19,
                           "L5": 15.75, "L6": 1.35, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_25_dict = {"D1": 20., "D2": 25., "D3": 32, "D4": 25, "D5": 23.9, "L1": 30, "L2": 20, "L3": 76, "L4": 20,
                           "L5": 16.35, "L6": 1.35, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_30_dict = {"D1": 25., "D2": 30., "D3": 40, "D4": 30, "D5": 28.6, "L1": 38, "L2": 25, "L3": 72, "L4": 21,
                           "L5": 17.75, "L6": 1.75, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_serise_dict = {"FKFF08": self.FK_08_dict, "FKFF10": self.FK_10_dict, "FKFF15": self.FK_15_dict,
                               "FKFF20": self.FK_20_dict,
                               "FKFF25": self.FK_25_dict, "FKFF30": self.FK_30_dict}
        ####---------#######
        self.FF_6_dict={"D1":6,"E":9,"A":5.7,"B":0.8,"C":6.8}
        self.FF_10_dict = {"D1": 8, "E": 10, "A": 7.6, "B": 0.9, "C": 7.9}
        self.FF_12_dict = {"D1": 10, "E": 11, "A": 9.6, "B": 1.15, "C": 9.15}
        self.FF_15_dict = {"D1": 15, "E": 13, "A": 14.3, "B": 1.15, "C": 10.15}
        self.FF_20_dict = {"D1": 20, "E": 19, "A": 19, "B": 1.35, "C": 15.35}
        self.FF_25_dict = {"D1": 25, "E": 20, "A": 23.9, "B": 1.35, "C": 16.35}
        self.FF_30_dict = {"D1": 30, "E": 21, "A": 28.6, "B": 1.75, "C": 17.75}
        self.FF_serise_dict={"FF6":self.FF_6_dict,"FF10":self.FF_10_dict,"FF12":self.FF_12_dict,"FF15":self.FF_15_dict,
                             "FF20":self.FF_20_dict,"FF25":self.FF_25_dict,"FF30":self.FF_30_dict}


        #---------------------------------------------------------------------------------------------------------

        # 复合体初始化---------------------------------
        self.shape = TopoDS_Shape()


    def Create_Bk(self, filename="SFU01204-4", ss="BKBF10", L=1000,suppor_side_type=""):
        pass
        self.new_build = TopoDS_Builder()  # 建立一个TopoDS_Builder()
        self.aCompound = TopoDS_Compound()  # 定义一个复合体
        self.new_build.MakeCompound(self.aCompound)  # 生成一个复合体DopoDS_shape
     
        "获取选择零件名称  获取路径"
        # 获取零件名称
        try:
            pass
            new_shape = TopoDS_Shape()
            #filename = "SFU01204-4"
            # 获取相应零件的路径***************************************
            self.partpath = os.getcwd()
            self.partpath = self.partpath + "/3Ddata" + "/STP" + "/" + filename + ".stp"
            self.shape = read_step_file(self.partpath)
            self.shape.Free(True)  # 先释放shape
            # self.new_build.Add(self.aCompound,shape123)#将shaoe添加入复合体
            self.new_build.Add(self.aCompound, self.shape)
            # 绘制丝杆**************************************************
            if int(filename[3:6]) == 12 or int(filename[3:6]) == 14 or int(filename[3:6]) == 15:
                ss = "BKBF10"
            elif int(filename[3:6]) == 14 or int(filename[3:6]) == 15 or int(filename[3:6]) == 16 or int(
                    filename[3:6]) == 18:
                pass
                ss = "BKBF12"
            elif int(filename[3:6]) == 18 or int(filename[3:6]) == 20:
                ss = "BKBF15"
            elif int(filename[3:6]) == 20 or int(filename[3:6]) == 25:
                ss = "BKBF17"
            elif int(filename[3:6]) == 25 or int(filename[3:6]) == 28:
                ss = "BKBF20"
            elif int(filename[3:6]) == 32 or int(filename[3:6]) == 36:
                ss = "BKBF25"
            elif int(filename[3:6]) == 36 or int(filename[3:6]) == 40:
                ss = "BKBF30"
            elif int(filename[3:6]) == 40 or int(filename[3:6]) == 45 or int(filename[3:6]) == 50:
                ss = "BKBF35"
            elif int(filename[3:6]) == 50 or int(filename[3:6]) == 55:
                ss = "BKBF40"
            if "BF" in suppor_side_type:
                F_para = self.BF_serise_dict[suppor_side_type]
            elif "EF" in suppor_side_type:
                F_para = self.EF_serise_dict[suppor_side_type]
            elif "FF" in suppor_side_type:
                F_para = self.FF_serise_dict[suppor_side_type]
            self.BK_serise_dict[ss]["D3"] = int(filename[3:6])  # 重新设置丝杆直径
            self.BK_serise_dict[ss]["D4"]=F_para["D1"]#支撑侧端部直径
            self.BK_serise_dict[ss]["D5"]=F_para["A"]#卡簧直径
            self.BK_serise_dict[ss]["L4"]=F_para["E"]#端部长度
            self.BK_serise_dict[ss]["L5"]=F_para["C"]#距离
            self.BK_serise_dict[ss]["L6"]=F_para["B"]#端部长度

            # PL = (L - 15 - 39 - 10) / 2
            L=L+self.BK_serise_dict[ss]["L1"]+self.BK_serise_dict[ss]["L3"]+self.BK_serise_dict[ss]["L4"]+self.series[filename]["L"]
            self.total_length=self.BK_serise_dict[ss]["L1"]+self.BK_serise_dict[ss]["L3"]+self.BK_serise_dict[ss]["L4"]+self.series[filename]["L"]
            PL = (L - self.BK_serise_dict[ss]["L1"] - self.BK_serise_dict[ss]["L3"] - self.BK_serise_dict[ss]["L4"]) / 2
            # Center_point=filename[0:]
            #PL = L / 2
            # P1 = [0, 0, PL + 39 + 15]
            P1 = [0, 0, PL + self.BK_serise_dict[ss]["L3"] + self.BK_serise_dict[ss]["L1"]]
            # P2 = [0, 4, PL + 39 + 15]
            P2 = [0, self.BK_serise_dict[ss]["D1"] / 2, PL + self.BK_serise_dict[ss]["L3"]
                  + self.BK_serise_dict[ss]["L1"]]
            # P3 = [0, 4, PL + 39]
            P3 = [0, self.BK_serise_dict[ss]["D1"] / 2, PL + self.BK_serise_dict[ss]["L3"]]
            # P4 = [0, 5, PL + 39]
            P4 = [0, self.BK_serise_dict[ss]["D2"] / 2, PL + self.BK_serise_dict[ss]["L3"]]
            # P5 = [0, 5, PL]
            P5 = [0, self.BK_serise_dict[ss]["D2"] / 2, PL]
            # P6 = [0, 6, PL]
            P6 = [0, self.BK_serise_dict[ss]["D3"] / 2, PL]
            # P7 = [0, 6, -PL]
            P7 = [0, self.BK_serise_dict[ss]["D3"] / 2, -PL]
            # P8 = [0, 4, -PL]
            P8 = [0, self.BK_serise_dict[ss]["D4"] / 2, -PL]
            # P9 = [0, 4, -PL - 7.9]
            P9 = [0, self.BK_serise_dict[ss]["D4"] / 2, -PL - self.BK_serise_dict[ss]["L5"]]
            # P10 = [0, 4 - 0.2, -PL - 7.9]
            P10 = [0, self.BK_serise_dict[ss]["D5"] / 2, -PL - self.BK_serise_dict[ss]["L5"]]
            # P11 = [0, 4 - 0.2, -PL - 7.9 - 0.8]
            P11 = [0, self.BK_serise_dict[ss]["D5"] / 2, -PL - self.BK_serise_dict[ss]["L5"] -
                   self.BK_serise_dict[ss]["L6"]]
            # P12 = [0, 4, -PL - 7.9 - 0.8]
            P12 = [0, self.BK_serise_dict[ss]["D4"] / 2, -PL - self.BK_serise_dict[ss]["L5"] -
                   self.BK_serise_dict[ss]["L6"]]
            # P13 = [0, 4, -PL - 10]
            P13 = [0, self.BK_serise_dict[ss]["D4"] / 2, -PL - self.BK_serise_dict[ss]["L4"]]
            # P14 = [0, 0, -PL - 10]
            P14 = [0, 0, -PL - self.BK_serise_dict[ss]["L4"]]
            E11 = BRepBuilderAPI_MakeEdge(gp_Pnt(P1[0], P1[1], P1[2]), gp_Pnt(P2[0], P2[1], P2[2])).Edge()
            E12 = BRepBuilderAPI_MakeEdge(gp_Pnt(P2[0], P2[1], P2[2]), gp_Pnt(P3[0], P3[1], P3[2])).Edge()
            E13 = BRepBuilderAPI_MakeEdge(gp_Pnt(P3[0], P3[1], P3[2]), gp_Pnt(P4[0], P4[1], P4[2])).Edge()
            E14 = BRepBuilderAPI_MakeEdge(gp_Pnt(P4[0], P4[1], P4[2]), gp_Pnt(P5[0], P5[1], P5[2])).Edge()
            E15 = BRepBuilderAPI_MakeEdge(gp_Pnt(P5[0], P5[1], P5[2]), gp_Pnt(P6[0], P6[1], P6[2])).Edge()
            E16 = BRepBuilderAPI_MakeEdge(gp_Pnt(P6[0], P6[1], P6[2]), gp_Pnt(P7[0], P7[1], P7[2])).Edge()
            E17 = BRepBuilderAPI_MakeEdge(gp_Pnt(P7[0], P7[1], P7[2]), gp_Pnt(P8[0], P8[1], P8[2])).Edge()
            E18 = BRepBuilderAPI_MakeEdge(gp_Pnt(P8[0], P8[1], P8[2]), gp_Pnt(P9[0], P9[1], P9[2])).Edge()
            E19 = BRepBuilderAPI_MakeEdge(gp_Pnt(P9[0], P9[1], P9[2]), gp_Pnt(P10[0], P10[1], P10[2])).Edge()
            E20 = BRepBuilderAPI_MakeEdge(gp_Pnt(P10[0], P10[1], P10[2]), gp_Pnt(P11[0], P11[1], P11[2])).Edge()
            E21 = BRepBuilderAPI_MakeEdge(gp_Pnt(P11[0], P11[1], P11[2]), gp_Pnt(P12[0], P12[1], P12[2])).Edge()
            E22 = BRepBuilderAPI_MakeEdge(gp_Pnt(P12[0], P12[1], P12[2]), gp_Pnt(P13[0], P13[1], P13[2])).Edge()
            E23 = BRepBuilderAPI_MakeEdge(gp_Pnt(P13[0], P13[1], P13[2]), gp_Pnt(P14[0], P14[1], P14[2])).Edge()
            E24 = BRepBuilderAPI_MakeEdge(gp_Pnt(P14[0], P14[1], P14[2]), gp_Pnt(P1[0], P1[1], P1[2])).Edge()
            new_charme = ChFi2d_ChamferAPI()
            new_charme.Init(E11, E12)
            new_charme.Perform()
            E25 = new_charme.Result(E11, E12, self.BK_serise_dict[ss]["C1"], self.BK_serise_dict[ss]["C1"])  # 倒角1

            new_charme.Init(E13, E14)
            new_charme.Perform()
            E26 = new_charme.Result(E13, E14, self.BK_serise_dict[ss]["C2"], self.BK_serise_dict[ss]["C2"])  # 倒角2

            new_charme.Init(E15, E16)
            new_charme.Perform()
            E27 = new_charme.Result(E15, E16, self.BK_serise_dict[ss]["C3"], self.BK_serise_dict[ss]["C3"])  # 倒角3

            new_charme.Init(E16, E17)
            new_charme.Perform()
            E28 = new_charme.Result(E16, E17, self.BK_serise_dict[ss]["C3"], self.BK_serise_dict[ss]["C3"])  # 倒角4

            new_charme.Init(E22, E23)
            new_charme.Perform()
            E29 = new_charme.Result(E22, E23, self.BK_serise_dict[ss]["C1"], self.BK_serise_dict[ss]["C1"])  # 倒角5

            # print(type(E11))
            # print(E29.IsNull())

            W1 = BRepBuilderAPI_MakeWire(E11, E25, E12).Wire()
            W2 = BRepBuilderAPI_MakeWire(E13, E26, E14).Wire()
            W3 = BRepBuilderAPI_MakeWire(E15, E27, E16).Wire()
            W4 = BRepBuilderAPI_MakeWire(E16, E28, E17).Wire()
            W5 = BRepBuilderAPI_MakeWire(E18, E19, E20, E21).Wire()
            W6 = BRepBuilderAPI_MakeWire(E22, E29, E23, E24).Wire()
            # print("succeed")

            mkWire = BRepBuilderAPI_MakeWire()
            mkWire.Add(W1)
            mkWire.Add(W2)
            mkWire.Add(W3)
            mkWire.Add(W4)
            mkWire.Add(W5)
            mkWire.Add(W6)
            Rob = BRepPrimAPI_MakeRevol(BRepBuilderAPI_MakeFace(mkWire.Wire()).Face(),
                                        gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))).Shape()
            # 倒角-----------------------------
            # MF=BRepFilletAPI_MakeChamfer(Rob)
            # MF.Add()
            # 移动

            ls_filename = filename
            move_distance = 0.5 * L - (L - float(self.series[ls_filename]["L"])) / 2
            cone = TopoDS_Shape(Rob)
            T = gp_Trsf()
            T.SetTranslation(gp_Vec(0, 0, -move_distance))
            loc = TopLoc_Location(T)
            cone.Location(loc)
            self.new_build.Add(self.aCompound, cone)
            print(type(self.aCompound))
            return self.aCompound


        except Exception as e:
            print(e)
            return False

    def Create_Ek(self, filename="SFU01204-4", ss="EKEF10", L=100,suppor_side_type=""):
        pass
        self.total_length = 0
        self.new_build = TopoDS_Builder()  # 建立一个TopoDS_Builder()
        self.aCompound = TopoDS_Compound()  # 定义一个复合体
        self.new_build.MakeCompound(self.aCompound)  # 生成一个复合体DopoDS_shape
        if int(filename[3:6]) == 6 or int(filename[3:6]) == 8:
            ss = "EKEF06"
        elif int(filename[3:6]) == 10 or int(filename[3:6]) == 12:
            ss = "EKEF08"
        elif int(filename[3:6]) == 12 or int(filename[3:6]) == 14 or int(filename[3:6]) == 15:
            ss = "EKEF10"
        elif int(filename[3:6]) == 14 or int(filename[3:6]) == 15 or int(filename[3:6]) == 16:
            ss = "EKEF12"
        elif int(filename[3:6]) == 18 or int(filename[3:6]) == 20:
            ss = "EKEF15"
        elif int(filename[3:6]) == 25 or int(filename[3:6]) == 28 or int(filename[3:6]) == 32:
            ss = "EKEF20"
        elif int(filename[3:6]) == 32 or int(filename[3:6]) == 36:
            ss = "EKEF25"
        #"获取选择零件名称  获取路径"
        # 获取零件名称
        print("ok1")
        try:
            pass
            new_shape = TopoDS_Shape()
            # filename = "SFU2005-4"
            # 获取相应零件的路径***************************************
            self.partpath = os.getcwd()
            self.partpath = self.partpath + "\\3Ddata" + "\\STP" + "\\" + filename + ".stp"
            self.shape = read_step_file(self.partpath)
            self.shape.Free(True)  # 先释放shape
            # self.new_build.Add(self.aCompound,shape123)#将shaoe添加入复合体
            self.new_build.Add(self.aCompound, self.shape)
            # 绘制丝杆**************************************************
            if "BF" in suppor_side_type:
                F_para = self.BF_serise_dict[suppor_side_type]
            elif "EF" in suppor_side_type:
                F_para = self.EF_serise_dict[suppor_side_type]
            elif "FF" in suppor_side_type:
                F_para = self.FF_serise_dict[suppor_side_type]
            self.EK_serise_dict[ss]["D3"] = int(filename[3:6])  # 重新设置丝杆直径
            self.EK_serise_dict[ss]["D4"] = F_para["D1"]  # 支撑侧端部直径
            self.EK_serise_dict[ss]["D5"] = F_para["A"]  # 卡簧直径
            self.EK_serise_dict[ss]["L4"] = F_para["E"]  # 端部长度
            self.EK_serise_dict[ss]["L5"] = F_para["C"]  # 距离
            self.EK_serise_dict[ss]["L6"] = F_para["B"]  # 端部长度
            # print(filename[3:6])
            # PL = (L - 15 - 39 - 10) / 2
            L=L+self.EK_serise_dict[ss]["L1"]+self.EK_serise_dict[ss]["L3"]+self.EK_serise_dict[ss]["L4"]+self.series[filename]["L"]
            self.total_length = self.EK_serise_dict[ss]["L1"]+self.EK_serise_dict[ss]["L3"]+self.EK_serise_dict[ss]["L4"]+self.series[filename]["L"]
            PL = (L - self.EK_serise_dict[ss]["L1"] - self.EK_serise_dict[ss]["L2"]
                  - self.EK_serise_dict[ss]["L4"]) / 2
            # P1 = [0, 0, PL + 39 + 15]
            P1 = [0, 0, PL + self.EK_serise_dict[ss]["L3"] + self.EK_serise_dict[ss]["L1"]]
            # P2 = [0, 4, PL + 39 + 15]
            P2 = [0, self.EK_serise_dict[ss]["D1"] / 2, PL + self.EK_serise_dict[ss]["L3"]
                  + self.EK_serise_dict[ss]["L1"]]
            # P3 = [0, 4, PL + 39]
            P3 = [0, self.EK_serise_dict[ss]["D1"] / 2, PL + self.EK_serise_dict[ss]["L3"]]
            # P4 = [0, 5, PL + 39]
            P4 = [0, self.EK_serise_dict[ss]["D2"] / 2, PL + self.EK_serise_dict[ss]["L3"]]
            # P5 = [0, 5, PL]
            P5 = [0, self.EK_serise_dict[ss]["D2"] / 2, PL]
            # P6 = [0, 6, PL]
            P6 = [0, self.EK_serise_dict[ss]["D3"] / 2, PL]
            # P7 = [0, 6, -PL]
            P7 = [0, self.EK_serise_dict[ss]["D3"] / 2, -PL]
            # P8 = [0, 4, -PL]
            P8 = [0, self.EK_serise_dict[ss]["D1"] / 2, -PL]
            # P9 = [0, 4, -PL - 7.9]
            P9 = [0, self.EK_serise_dict[ss]["D1"] / 2, -PL - self.EK_serise_dict[ss]["L5"]]
            # P10 = [0, 4 - 0.2, -PL - 7.9]
            P10 = [0, self.EK_serise_dict[ss]["D5"] / 2, -PL - self.EK_serise_dict[ss]["L5"]]
            # P11 = [0, 4 - 0.2, -PL - 7.9 - 0.8]
            P11 = [0, self.EK_serise_dict[ss]["D5"] / 2, -PL - self.EK_serise_dict[ss]["L5"] -
                   self.EK_serise_dict[ss]["L6"]]
            # P12 = [0, 4, -PL - 7.9 - 0.8]
            P12 = [0, self.EK_serise_dict[ss]["D1"] / 2, -PL - self.EK_serise_dict[ss]["L5"] -
                   self.EK_serise_dict[ss]["L6"]]
            # P13 = [0, 4, -PL - 10]
            P13 = [0, self.EK_serise_dict[ss]["D1"] / 2, -PL - self.EK_serise_dict[ss]["L4"]]
            # P14 = [0, 0, -PL - 10]
            P14 = [0, 0, -PL - self.EK_serise_dict[ss]["L4"]]
            E11 = BRepBuilderAPI_MakeEdge(gp_Pnt(P1[0], P1[1], P1[2]), gp_Pnt(P2[0], P2[1], P2[2])).Edge()
            E12 = BRepBuilderAPI_MakeEdge(gp_Pnt(P2[0], P2[1], P2[2]), gp_Pnt(P3[0], P3[1], P3[2])).Edge()
            E13 = BRepBuilderAPI_MakeEdge(gp_Pnt(P3[0], P3[1], P3[2]), gp_Pnt(P4[0], P4[1], P4[2])).Edge()
            E14 = BRepBuilderAPI_MakeEdge(gp_Pnt(P4[0], P4[1], P4[2]), gp_Pnt(P5[0], P5[1], P5[2])).Edge()
            E15 = BRepBuilderAPI_MakeEdge(gp_Pnt(P5[0], P5[1], P5[2]), gp_Pnt(P6[0], P6[1], P6[2])).Edge()
            E16 = BRepBuilderAPI_MakeEdge(gp_Pnt(P6[0], P6[1], P6[2]), gp_Pnt(P7[0], P7[1], P7[2])).Edge()
            E17 = BRepBuilderAPI_MakeEdge(gp_Pnt(P7[0], P7[1], P7[2]), gp_Pnt(P8[0], P8[1], P8[2])).Edge()
            E18 = BRepBuilderAPI_MakeEdge(gp_Pnt(P8[0], P8[1], P8[2]), gp_Pnt(P9[0], P9[1], P9[2])).Edge()
            E19 = BRepBuilderAPI_MakeEdge(gp_Pnt(P9[0], P9[1], P9[2]), gp_Pnt(P10[0], P10[1], P10[2])).Edge()
            E20 = BRepBuilderAPI_MakeEdge(gp_Pnt(P10[0], P10[1], P10[2]), gp_Pnt(P11[0], P11[1], P11[2])).Edge()
            E21 = BRepBuilderAPI_MakeEdge(gp_Pnt(P11[0], P11[1], P11[2]), gp_Pnt(P12[0], P12[1], P12[2])).Edge()
            E22 = BRepBuilderAPI_MakeEdge(gp_Pnt(P12[0], P12[1], P12[2]), gp_Pnt(P13[0], P13[1], P13[2])).Edge()
            E23 = BRepBuilderAPI_MakeEdge(gp_Pnt(P13[0], P13[1], P13[2]), gp_Pnt(P14[0], P14[1], P14[2])).Edge()
            E24 = BRepBuilderAPI_MakeEdge(gp_Pnt(P14[0], P14[1], P14[2]), gp_Pnt(P1[0], P1[1], P1[2])).Edge()

            new_charme = ChFi2d_ChamferAPI()
            new_charme.Init(E11, E12)
            new_charme.Perform()
            E25 = new_charme.Result(E11, E12, self.EK_serise_dict[ss]["C1"], self.EK_serise_dict[ss]["C1"])  # 倒角1

            new_charme.Init(E13, E14)
            new_charme.Perform()
            E26 = new_charme.Result(E13, E14, self.EK_serise_dict[ss]["C2"], self.EK_serise_dict[ss]["C2"])  # 倒角2

            new_charme.Init(E15, E16)
            new_charme.Perform()
            E27 = new_charme.Result(E15, E16, self.EK_serise_dict[ss]["C3"], self.EK_serise_dict[ss]["C3"])  # 倒角3

            new_charme.Init(E16, E17)
            new_charme.Perform()
            E28 = new_charme.Result(E16, E17, self.EK_serise_dict[ss]["C3"], self.EK_serise_dict[ss]["C3"])  # 倒角4

            new_charme.Init(E22, E23)
            new_charme.Perform()
            E29 = new_charme.Result(E22, E23, self.EK_serise_dict[ss]["C1"], self.EK_serise_dict[ss]["C1"])  # 倒角5

            # print(type(E11))
            # print(E29.IsNull())
            W1 = BRepBuilderAPI_MakeWire(E11, E25, E12).Wire()
            W2 = BRepBuilderAPI_MakeWire(E13, E26, E14).Wire()
            W3 = BRepBuilderAPI_MakeWire(E15, E27, E16).Wire()
            W4 = BRepBuilderAPI_MakeWire(E16, E28, E17).Wire()
            W5 = BRepBuilderAPI_MakeWire(E18, E19, E20, E21).Wire()
            W6 = BRepBuilderAPI_MakeWire(E22, E29, E23, E24).Wire()
            # print("succeed")

            mkWire = BRepBuilderAPI_MakeWire()
            mkWire.Add(W1)
            mkWire.Add(W2)
            mkWire.Add(W3)
            mkWire.Add(W4)
            mkWire.Add(W5)
            mkWire.Add(W6)
            Rob = BRepPrimAPI_MakeRevol(BRepBuilderAPI_MakeFace(mkWire.Wire()).Face(),
                                        gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))).Shape()
            # 倒角-----------------------------
            # MF=BRepFilletAPI_MakeChamfer(Rob)
            # MF.Add()
            # 移动
            ls_filename = filename
            move_distance = 0.5 * L - (L - float(self.series[ls_filename]["L"])) / 2
            cone = TopoDS_Shape(Rob)
            T = gp_Trsf()
            T.SetTranslation(gp_Vec(0, 0, -move_distance))
            loc = TopLoc_Location(T)
            cone.Location(loc)
            self.new_build.Add(self.aCompound, cone)
            #print(type(self.aCompound))
            return self.aCompound

        except Exception as e:
            print(e)
            print("error")
            return False

    def Create_Fk(self, filename="SFU01204-4", ss="FKFF8", L=100,suppor_side_type=""):
        pass
        self.total_length = 0
        self.new_build = TopoDS_Builder()  # 建立一个TopoDS_Builder()
        self.aCompound = TopoDS_Compound()  # 定义一个复合体
        self.new_build.MakeCompound(self.aCompound)  # 生成一个复合体DopoDS_shape
        if int(filename[3:6]) == 10 or int(filename[3:6]) == 12:
            ss = "FKFF08"
        if int(filename[3:6]) == 12 or int(filename[3:6]) == 14 or int(filename[3:6]) == 15:
            ss = "FKFF10"
        if int(filename[3:6]) == 14 or int(filename[3:6]) == 15 or int(filename[3:6]) == 16:
            ss = "FKFF12"
        if int(filename[3:6]) == 18 or int(filename[3:6]) == 20:
            ss = "FKFF15"
        if int(filename[3:6]) == 25 or int(filename[3:6]) == 28:
            ss = "FKFF20"
        if int(filename[3:6]) == 32 or int(filename[3:6]) == 36:
            ss = "FKFF25"
        if int(filename[3:6]) == 40 or int(filename[3:6]) == 50:
            ss = "FKFF30"
        #"获取选择零件名称  获取路径"
        # 获取零件名称
        try:
            pass
            new_shape = TopoDS_Shape()
            # filename = "SFU2005-4"
            # 获取相应零件的路径***************************************
            self.partpath = os.getcwd()
            self.partpath = self.partpath + "\\3Ddata" + "\\STP" + "\\" + filename + ".stp"
            self.shape = read_step_file(self.partpath)
            self.shape.Free(True)  # 先释放shape
            # self.new_build.Add(self.aCompound,shape123)#将shaoe添加入复合体
            self.new_build.Add(self.aCompound, self.shape)
            # 绘制丝杆**************************************************
            if "BF" in suppor_side_type:
                F_para = self.BF_serise_dict[suppor_side_type]
            elif "EF" in suppor_side_type:
                F_para = self.EF_serise_dict[suppor_side_type]
            elif "FF" in suppor_side_type:
                F_para = self.FF_serise_dict[suppor_side_type]
            self.FK_serise_dict[ss]["D3"] = int(filename[3:6])  # 重新设置丝杆直径
            self.FK_serise_dict[ss]["D4"] = F_para["D1"]  # 支撑侧端部直径
            self.FK_serise_dict[ss]["D5"] = F_para["A"]  # 卡簧直径
            self.FK_serise_dict[ss]["L4"] = F_para["E"]  # 端部长度
            self.FK_serise_dict[ss]["L5"] = F_para["C"]  # 距离
            self.FK_serise_dict[ss]["L6"] = F_para["B"]  # 端部长度
            # print(filename[3:6])
            # PL = (L - 15 - 39 - 10) / 2
            L=L+self.FK_serise_dict[ss]["L1"]+self.FK_serise_dict[ss]["L3"]+self.FK_serise_dict[ss]["L4"]+self.series[filename]["L"]
            self.total_length = self.FK_serise_dict[ss]["L1"]+self.FK_serise_dict[ss]["L3"]+self.FK_serise_dict[ss]["L4"]+self.series[filename]["L"]
            PL = (L - self.FK_serise_dict[ss]["L1"] - self.FK_serise_dict[ss]["L2"]
                  - self.FK_serise_dict[ss]["L4"]) / 2
            # P1 = [0, 0, PL + 39 + 15]
            P1 = [0, 0, PL + self.FK_serise_dict[ss]["L3"] + self.FK_serise_dict[ss]["L1"]]
            # P2 = [0, 4, PL + 39 + 15]
            P2 = [0, self.FK_serise_dict[ss]["D1"] / 2, PL + self.FK_serise_dict[ss]["L3"]
                  + self.FK_serise_dict[ss]["L1"]]
            # P3 = [0, 4, PL + 39]
            P3 = [0, self.FK_serise_dict[ss]["D1"] / 2, PL + self.FK_serise_dict[ss]["L3"]]
            # P4 = [0, 5, PL + 39]
            P4 = [0, self.FK_serise_dict[ss]["D2"] / 2, PL + self.FK_serise_dict[ss]["L3"]]
            # P5 = [0, 5, PL]
            P5 = [0, self.FK_serise_dict[ss]["D2"] / 2, PL]
            # P6 = [0, 6, PL]
            P6 = [0, self.FK_serise_dict[ss]["D3"] / 2, PL]
            # P7 = [0, 6, -PL]
            P7 = [0, self.FK_serise_dict[ss]["D3"] / 2, -PL]
            # P8 = [0, 4, -PL]
            P8 = [0, self.FK_serise_dict[ss]["D1"] / 2, -PL]
            # P9 = [0, 4, -PL - 7.9]
            P9 = [0, self.FK_serise_dict[ss]["D1"] / 2, -PL - self.FK_serise_dict[ss]["L5"]]
            # P10 = [0, 4 - 0.2, -PL - 7.9]
            P10 = [0, self.FK_serise_dict[ss]["D5"] / 2, -PL - self.FK_serise_dict[ss]["L5"]]
            # P11 = [0, 4 - 0.2, -PL - 7.9 - 0.8]
            P11 = [0, self.FK_serise_dict[ss]["D5"] / 2, -PL - self.FK_serise_dict[ss]["L5"] -
                   self.FK_serise_dict[ss]["L6"]]
            # P12 = [0, 4, -PL - 7.9 - 0.8]
            P12 = [0, self.FK_serise_dict[ss]["D1"] / 2, -PL - self.FK_serise_dict[ss]["L5"] -
                   self.FK_serise_dict[ss]["L6"]]
            # P13 = [0, 4, -PL - 10]
            P13 = [0, self.FK_serise_dict[ss]["D1"] / 2, -PL - self.FK_serise_dict[ss]["L4"]]
            # P14 = [0, 0, -PL - 10]
            P14 = [0, 0, -PL - self.FK_serise_dict[ss]["L4"]]
            E11 = BRepBuilderAPI_MakeEdge(gp_Pnt(P1[0], P1[1], P1[2]), gp_Pnt(P2[0], P2[1], P2[2])).Edge()
            E12 = BRepBuilderAPI_MakeEdge(gp_Pnt(P2[0], P2[1], P2[2]), gp_Pnt(P3[0], P3[1], P3[2])).Edge()
            E13 = BRepBuilderAPI_MakeEdge(gp_Pnt(P3[0], P3[1], P3[2]), gp_Pnt(P4[0], P4[1], P4[2])).Edge()
            E14 = BRepBuilderAPI_MakeEdge(gp_Pnt(P4[0], P4[1], P4[2]), gp_Pnt(P5[0], P5[1], P5[2])).Edge()
            E15 = BRepBuilderAPI_MakeEdge(gp_Pnt(P5[0], P5[1], P5[2]), gp_Pnt(P6[0], P6[1], P6[2])).Edge()
            E16 = BRepBuilderAPI_MakeEdge(gp_Pnt(P6[0], P6[1], P6[2]), gp_Pnt(P7[0], P7[1], P7[2])).Edge()
            E17 = BRepBuilderAPI_MakeEdge(gp_Pnt(P7[0], P7[1], P7[2]), gp_Pnt(P8[0], P8[1], P8[2])).Edge()
            E18 = BRepBuilderAPI_MakeEdge(gp_Pnt(P8[0], P8[1], P8[2]), gp_Pnt(P9[0], P9[1], P9[2])).Edge()
            E19 = BRepBuilderAPI_MakeEdge(gp_Pnt(P9[0], P9[1], P9[2]), gp_Pnt(P10[0], P10[1], P10[2])).Edge()
            E20 = BRepBuilderAPI_MakeEdge(gp_Pnt(P10[0], P10[1], P10[2]), gp_Pnt(P11[0], P11[1], P11[2])).Edge()
            E21 = BRepBuilderAPI_MakeEdge(gp_Pnt(P11[0], P11[1], P11[2]), gp_Pnt(P12[0], P12[1], P12[2])).Edge()
            E22 = BRepBuilderAPI_MakeEdge(gp_Pnt(P12[0], P12[1], P12[2]), gp_Pnt(P13[0], P13[1], P13[2])).Edge()
            E23 = BRepBuilderAPI_MakeEdge(gp_Pnt(P13[0], P13[1], P13[2]), gp_Pnt(P14[0], P14[1], P14[2])).Edge()
            E24 = BRepBuilderAPI_MakeEdge(gp_Pnt(P14[0], P14[1], P14[2]), gp_Pnt(P1[0], P1[1], P1[2])).Edge()

            new_charme = ChFi2d_ChamferAPI()
            new_charme.Init(E11, E12)
            new_charme.Perform()
            E25 = new_charme.Result(E11, E12, 1.0, 1.0)  # 倒角1

            new_charme.Init(E13, E14)
            new_charme.Perform()
            E26 = new_charme.Result(E13, E14, 0.5, 0.5)  # 倒角2

            new_charme.Init(E15, E16)
            new_charme.Perform()
            E27 = new_charme.Result(E15, E16, 0.5, 0.5)  # 倒角3

            new_charme.Init(E16, E17)
            new_charme.Perform()
            E28 = new_charme.Result(E16, E17, 0.5, 0.5)  # 倒角4

            new_charme.Init(E22, E23)
            new_charme.Perform()
            E29 = new_charme.Result(E22, E23, 0.5, 0.5)  # 倒角5

            # print(type(E11))
            # print(E29.IsNull())

            W1 = BRepBuilderAPI_MakeWire(E11, E25, E12).Wire()
            W2 = BRepBuilderAPI_MakeWire(E13, E26, E14).Wire()
            W3 = BRepBuilderAPI_MakeWire(E15, E27, E16).Wire()
            W4 = BRepBuilderAPI_MakeWire(E16, E28, E17).Wire()
            W5 = BRepBuilderAPI_MakeWire(E18, E19, E20, E21).Wire()
            W6 = BRepBuilderAPI_MakeWire(E22, E29, E23, E24).Wire()
            # print("succeed")

            mkWire = BRepBuilderAPI_MakeWire()
            mkWire.Add(W1)
            mkWire.Add(W2)
            mkWire.Add(W3)
            mkWire.Add(W4)
            mkWire.Add(W5)
            mkWire.Add(W6)
            Rob = BRepPrimAPI_MakeRevol(BRepBuilderAPI_MakeFace(mkWire.Wire()).Face(),
                                        gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))).Shape()
            # 倒角-----------------------------
            # MF=BRepFilletAPI_MakeChamfer(Rob)
            # MF.Add()
            # 移动
            ls_filename = filename
            move_distance = 0.5 * L - (L - float(self.series[ls_filename]["L"])) / 2
            cone = TopoDS_Shape(Rob)
            T = gp_Trsf()
            T.SetTranslation(gp_Vec(0, 0, -move_distance))
            loc = TopLoc_Location(T)
            cone.Location(loc)
            self.new_build.Add(self.aCompound, cone)
            #print(type(self.aCompound))
            return self.aCompound

        except:
            return False

    def Create_combox_list(self):
        combox_list=[]#单个选型的列表
        all_combox_list=[]#所有不同选项的列表
        all_combox_list.append({"精度等级":["C"]})
        length_list=[str(x) for x in range(100,1200,10)]#有效行程列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0,"  ")
        dict_combox={"型号":combox_list}
        all_combox_list.append(dict_combox)
        all_combox_list.append({"固定侧": ["  "," 方型：BK型 ","方型：EK型","法兰型：FK型"]})
        all_combox_list.append({"支撑侧": ["  "," 方型：BF型 ", "方型：EF型", "方型：FF型"]})
        all_combox_list.append({"有效行程S(mm)": length_list})
        all_combox_list.append(["丝杆轴材质","SCM415H"])
        all_combox_list.append(["丝杆轴硬度","滲碳58-62HRC"])
        all_combox_list.append(["螺母材质","SCM415H"])
        all_combox_list.append(["螺母轴硬度","滲碳58-62HRC"])
        all_combox_list.append(["螺母循环方式","内循环"])
        all_combox_list.append(["螺母类型","回流盖式"])
        all_combox_list.append(["丝杆总长(mm)",""])
        all_combox_list.append(["订货代码",""])
        return all_combox_list



class Create_boll_SCcrew_sfy(Create_boll_SCcrew_sfu):
        def __init__(self):
            super(Create_boll_SCcrew_sfy, self).__init__()
            self.SFY01616_3_6_dict = {"d": 16, "I": 16, "Da": 2.778, "D": 32, "A": 53,"E":10.4, "B": 10, "L":45,
                                    "W": 42, "H": 34, "X": 4.5, "Q": "M6", "N": "1.8x2", "Ca":1073, "Coa":2551,
                                    "kgf/um":31}  #
            self.SFY01616_5_6_dict = {"d": 16, "I": 16, "Da": 2.778, "D": 32, "A": 53, "E": 10.4, "B": 10, "L": 61,
                                      "W": 42, "H": 34, "X": 4.5, "Q": "M6", "N": "2.8x2", "Ca": 1568, "Coa": 3968,
                                      "kgf/um": 47}  #
            self.SFY02020_3_6_dict = {"d": 20, "I": 20, "Da": 3.175, "D": 39, "A": 62, "E": 13, "B": 10, "L": 52,
                                      "W": 50, "H": 41, "X": 5.5, "Q": "M6", "N": "1.8x2", "Ca": 1387, "Coa": 2515,
                                      "kgf/um": 37}  #
            self.SFY02020_5_6_dict = {"d": 20, "I": 20, "Da": 3.175, "D": 39, "A": 62, "E": 13, "B": 10, "L": 72,
                                      "W": 50, "H": 41, "X": 5.5, "Q": "M6", "N": "2.8x2", "Ca": 2029, "Coa": 5468,
                                      "kgf/um": 56}  #
            self.SFY02525_3_6_dict = {"d": 25, "I": 25, "Da": 3.969, "D": 47, "A": 74, "E": 15, "B": 12, "L": 64,
                                      "W": 60, "H": 49, "X": 6.6, "Q": "M6", "N": "1.8x2", "Ca": 2047, "Coa": 5494,
                                      "kgf/um": 45}  #
            self.SFY02525_5_6_dict = {"d": 25, "I": 25, "Da": 3.969, "D": 47, "A": 74, "E": 15, "B": 12, "L": 89,
                                      "W": 60, "H": 49, "X": 6.6, "Q": "M6", "N": "2.8x2", "Ca": 2032, "Coa": 8546,
                                      "kgf/um": 58}  #
            self.SFY03232_3_6_dict = {"d": 32, "I": 32, "Da": 4.762, "D": 58, "A": 92, "E": 17, "B": 12, "L": 78,
                                      "W": 74, "H": 40, "X": 9, "Q": "M6", "N": "1.8x2", "Ca": 3021, "Coa": 8690,
                                      "kgf/um": 58}  #
            self.SFY03232_5_6_dict = {"d": 32, "I": 32, "Da": 4.762, "D": 58, "A": 92, "E": 17, "B": 12, "L": 110,
                                      "W": 74, "H": 40, "X": 9, "Q": "M6", "N": "2.8x2", "Ca": 4417, "Coa": 3517,
                                      "kgf/um": 88}  #
            self.SFY04040_3_6_dict = {"d": 40, "I": 40, "Da": 6.35, "D": 73, "A": 114, "E": 19.5, "B": 15, "L": 99,
                                      "W": 93, "H": 75, "X": 11, "Q": "M6", "N": "1.8x2", "Ca": 4831, "Coa": 14062,
                                      "kgf/um": 70}  #
            self.SFY04040_5_6_dict = {"d": 40, "I": 40, "Da": 6.35, "D": 73, "A": 114, "E": 19.5, "B": 15, "L": 139,
                                      "W": 93, "H": 75, "X": 11, "Q": "M6", "N": "2.8x2", "Ca": 7065, "Coa": 21874,
                                      "kgf/um": 106}  #
            self.SFY05050_3_6_dict = {"d": 50, "I": 50, "Da": 7.938, "D": 90, "A": 135, "E": 21.5, "B": 20, "L": 117,
                                      "W": 192, "H": 92, "X": 14, "Q": "M6", "N": "1.8x2", "Ca": 7220, "Coa": 21974,
                                      "kgf/um": 86}  #
            self.SFY05050_5_6_dict = {"d": 50, "I": 50, "Da": 7.938, "D": 90, "A": 135, "E": 21.5, "B": 20, "L": 167,
                                      "W": 192, "H": 92, "X": 14, "Q": "M6", "N": "2.8x2", "Ca": 10558, "Coa": 34182,
                                      "kgf/um": 131}  #
            #--------------------------------两倍导程---------------------------------------------------------------
            self.SFY01632_1_6_dict = {"d": 16, "I": 32, "Da": 2.778, "D": 32, "A": 53, "E": 10.4, "B": 10, "L": 74.5,
                                      "W": 42, "H": 34, "X": 4.5, "Q": "M6", "N": "0.8x2", "Ca": 493, "Coa": 1116,
                                      "kgf/um": 11}  #
            self.SFY01632_3_6_dict = {"d": 16, "I": 32, "Da": 2.778, "D": 32, "A": 53, "E": 10.4, "B": 10, "L": 61,
                                      "W": 42, "H": 34, "X": 4.5, "Q": "M6", "N": "2.8x2", "Ca": 1568, "Coa": 3968,
                                      "kgf/um": 23}  #
            self.SFY02040_1_6_dict = {"d": 20, "I": 40, "Da": 3.175, "D": 39, "A": 62, "E": 13, "B": 10, "L": 48,
                                      "W": 50, "H": 41, "X": 5.5, "Q": "M6", "N": "0.8x2", "Ca": 653, "Coa": 1597,
                                      "kgf/um": 15}  #
            self.SFY02040_3_6_dict = {"d": 20, "I": 40, "Da": 3.175, "D": 39, "A": 62, "E": 13, "B": 10, "L": 88,
                                      "W": 50, "H": 41, "X": 5.5, "Q": "M6", "N": "1.8x2", "Ca": 1311, "Coa": 3592,
                                      "kgf/um": 30}  #
            self.SFY02550_1_6_dict = {"d": 25, "I": 50, "Da": 3.969, "D": 47, "A": 74, "E": 15, "B": 12, "L": 58,
                                      "W": 60, "X": 6.6, "H": 49, "Q": "M6", "N": "0.8x2", "Coa": 976, "Ca": 2495,
                                      "kgf/um": 19}  #
            self.SFY02550_3_6_dict = {"d": 25, "I": 50, "Da": 3.969, "D": 47, "A": 74, "E": 15, "B": 12, "L": 108,
                                      "W": 60, "H": 49, "X": 6.6, "Q": "M6", "N": "1.8x2", "Ca": 1960, "Coa": 5614,
                                      "kgf/um": 32}  #ok
            self.SFY03264_1_6_dict = {"d": 32, "I": 62, "Da": 4.762, "D": 58, "A": 92, "E": 17, "B": 12, "L": 71,
                                      "W": 74, "H": 40, "X": 9, "Q": "M6", "N": "0.8x2", "Ca": 1374, "Coa": 3571,
                                      "kgf/um": 22}  #
            self.SFY03264_3_6_dict = {"d": 32, "I": 62, "Da": 4.762, "D": 58, "A": 92, "E": 17, "B": 12, "L": 135,
                                      "W": 74, "H": 40, "X": 9, "Q": "M6", "N": "1.8x2", "Ca": 2759, "Coa": 8441,
                                      "kgf/um": 46}  #ok
            self.SFY04080_1_6_dict = {"d": 40, "I": 80, "Da": 6.35, "D": 73, "A": 114, "E": 19.5, "B": 15, "L": 90,
                                      "W": 93, "H": 75, "X": 11, "Q": "M6", "N": "0.8x2", "Ca": 2273, "Coa": 6387,
                                      "kgf/um": 29}  #
            self.SFY04080_3_6_dict = {"d": 40, "I": 80, "Da": 6.35, "D": 73, "A": 114, "E": 19.5, "B": 15, "L": 117,
                                      "W": 93, "H": 75, "X": 11, "Q": "M6", "N": "1.8x2", "Ca": 4566, "Coa": 14370,
                                      "kgf/um": 50}  #
            self.SFY050100_1_6_dict = {"d": 50, "I": 100, "Da": 7.938, "D": 90, "A": 135, "E": 21.5, "B": 20, "L": 111,
                                      "W": 192, "H": 92, "X": 14, "Q": "M6", "N": "1.8x2", "Ca": 3398, "Coa": 9980,
                                      "kgf/um": 35}  #
            self.SFY050100_3_6_dict = {"d": 50, "I": 100, "Da": 7.938, "D": 90, "A": 135, "E": 21.5, "B": 20, "L": 211,
                                      "W": 192, "H": 92, "X": 14, "Q": "M6", "N": "2.8x2", "Ca": 6824, "Coa": 22455,
                                      "kgf/um": 72}  #


            self.SFY_serise_dict = {"SFY01616-3.6": self.SFY01616_3_6_dict, "SFY01616-5.6": self.SFY01616_5_6_dict,
                                    "SFY02020-3.6":self.SFY02020_3_6_dict,"SFY02020-5.6":self.SFY02020_5_6_dict,
                                    "SFY02525-3.6":self.SFY02525_3_6_dict,"SFY02525-5.6":self.SFY02525_5_6_dict,
                                    "SFY03232-3.6":self.SFY03232_3_6_dict,"SFY03232-5.6":self.SFY03232_5_6_dict,
                                    "SFY04040-3.6":self.SFY04040_3_6_dict,"SFY04040-5.6":self.SFY04040_5_6_dict,
                                    "SFY05050-3.6":self.SFY05050_3_6_dict,"SFY05050-5.6":self.SFY05050_5_6_dict,
                                    "SFY01632-1.6":self.SFY01632_1_6_dict,"SFY01632-3.6":self.SFY01632_3_6_dict,
                                    "SFY02040-1.6":self.SFY02040_1_6_dict,"SFY02040-3.6":self.SFY02040_3_6_dict,
                                    "SFY02550-1.6":self.SFY02550_1_6_dict,"SFY02550-3.6":self.SFY02550_3_6_dict,
                                    "SFY03264-1.6":self.SFY03264_1_6_dict,"SFY03264-3.6":self.SFY03264_3_6_dict,
                                    "SFY04080-1.6":self.SFY04080_1_6_dict,"SFY04080-3.6":self.SFY04080_3_6_dict,
                                    "SFY050100-1.6":self.SFY050100_1_6_dict,"SFY050100-3.6":self.SFY050100_3_6_dict
                                  }
            self.series=self.SFY_serise_dict
            self.total_length=0


class Create_boll_SCcrew_sfh(Create_boll_SCcrew_sfu):
    def __init__(self):
        super(Create_boll_SCcrew_sfh, self).__init__()
        self.SFH01205_2_8_dict = {"d": 12, "I": 5, "Da": 2.5, "D": 24, "A": 40, "E": 5, "B": 10, "L": 30,
                                  "W": 32, "H": 30, "X": 4.5, "Q": "-", "N": "2.8x1", "Ca": 661, "Coa": 1316,
                                  "kgf/um": 19}  #
        self.SFH01210_2_8_dict = {"d": 12, "I": 10, "Da": 2.5, "D": 24, "A": 40, "E": 5, "B": 10, "L": 45,
                                 "W": 32, "H": 30, "X": 4.5, "Q": "-", "N": "2.8x1", "Ca": 642, "Coa": 1287,
                                 "kgf/um": 19}  #
        self.SFH01605_3_8_dict = {"d": 16, "I": 5, "Da": 2.778, "D": 28, "A": 48, "E": 5, "B": 10, "L": 37,
                                 "W": 38, "H": 40, "X": 5.5, "Q": "M6", "N": "3.8x1", "Ca": 1112, "Coa": 2507,
                                 "kgf/um": 30}  #
        self.SFH01610_2_8_dict = {"d": 16, "I": 10, "Da": 2.778, "D": 28, "A": 48, "E": 5, "B": 10, "L": 45,
                                 "W": 38, "H": 40, "X": 5.5, "Q": "M6", "N": "2.8x1", "Ca": 839, "Coa": 1821,
                                 "kgf/um": 23}  #
        self.SFH01616_1_8_dict = {"d": 16, "I": 16, "Da": 2.778, "D": 28, "A": 48, "E": 5, "B": 10, "L": 45,
                                "W": 38, "H": 40, "X": 5.5, "Q": "M6", "N": "1.8x1", "Ca": 552, "Coa": 1137,
                                "kgf/um": 14}  #
        self.SFH01616_2_8_dict = {"d": 16, "I": 16, "Da": 2.778, "D": 28, "A": 48, "E": 5, "B": 10, "L": 61,
                                 "W": 38, "H": 40, "X": 5.5, "Q": "M6", "N": "2.8x1", "Ca": 808, "Coa": 1769,
                                 "kgf/um": 22}  #
        self.SFH01620_1_8_dict = {"d": 16, "I": 20, "Da": 2.778, "D": 28, "A": 48, "E": 7, "B": 10, "L": 58,
                                 "W": 38, "H": 40, "X": 5.5, "Q": "M6", "N": "1.8x1", "Ca": 554, "Coa": 1170,
                                 "kgf/um": 14}  #
        self.SFH02005_3_8_dict = {"d": 20, "I": 5, "Da": 3.175, "D": 36, "A": 58, "E": 7, "B": 10, "L": 37,
                                 "W": 47, "H": 44, "X": 6.6, "Q": "M6", "N": "3.8x1", "Ca": 1484, "Coa": 3681,
                                 "kgf/um": 37}  #
        self.SFH02010_3_8_dict = {"d": 20, "I": 10, "Da": 3.175, "D": 36, "A": 58, "E": 7, "B": 10, "L": 55,
                                 "W": 47, "H": 44, "X": 6.6, "Q": "M6", "N": "3.8x1", "Ca": 1516, "Coa": 3833,
                                 "kgf/um": 40}  #
        self.SFH02020_1_8_dict = {"d": 20, "I": 20, "Da": 3.175, "D": 36, "A": 58, "E": 7, "B": 10, "L": 54,
                                 "W": 47, "H": 44, "X": 6.6, "Q": "M6", "N": "1.8x1", "Ca": 764, "Coa": 1758,
                                 "kgf/um": 19}  #
        self.SFH02020_2_8_dict = {"d": 20, "I": 20, "Da": 3.175, "D": 36, "A": 58, "E": 7, "B": 10, "L": 74,
                                 "W": 47, "H": 44, "X": 6.6, "Q": "M6", "N": "2.8x1", "Ca": 1118, "Coa": 2734,
                                 "kgf/um": 29}  #
        self.SFH02505_3_8_dict = {"d": 25, "I": 5, "Da": 3.175, "D": 40, "A": 62, "E": 7, "B": 10, "L": 37,
                                 "W": 51, "H": 48, "X": 6.6, "Q": "M6", "N": "3.8x1", "Ca": 1650, "Coa": 4658,
                                 "kgf/um": 43}  #
        self.SFH02510_3_8_dict = {"d": 25, "I": 10, "Da": 3.175, "D": 40, "A": 62, "E": 7, "B": 12, "L": 55,
                                 "W": 51, "H": 48, "X": 6.6, "Q": "M6", "N": "3.8x1", "Ca": 1638, "Coa": 4633,
                                 "kgf/um": 45}  #
        self.SFH02525_1_8_dict = {"d": 25, "I": 25, "Da": 3.175, "D": 40, "A": 62, "E": 7, "B": 12, "L": 64,
                                 "W": 51, "H": 48, "X": 6.6, "Q": "M6", "N": "1.8x1", "Ca": 843, "Coa": 2199,
                                 "kgf/um": 22}  #
        self.SFH02525_2_8_dict = {"d": 25, "I": 25, "Da": 3.175, "D": 40, "A": 2, "E": 7, "B": 12, "L": 89,
                                 "W": 51, "H": 48, "X": 6.6, "Q": "M6", "N": "2.8x1", "Ca": 1232, "Coa": 3421,
                                 "kgf/um": 34}  #
        self.SFH03205_3_8_dict = {"d": 32, "I": 5, "Da": 3.175, "D": 50, "A": 80, "E": 9, "B": 12, "L": 37,
                                 "W": 65, "H": 62, "X": 9, "Q": "M6", "N": "3.8x1", "Ca": 1839, "Coa": 6026,
                                 "kgf/um": 51}  #
        self.SFH03210_3_8_dict = {"d": 32, "I": 10, "Da": 3.969, "D": 50, "A": 80, "E": 9, "B": 12, "L": 57,
                                 "W": 65, "H": 62, "X": 9, "Q": "M6", "N": "3.8x1", "Ca": 2460, "Coa": 7255,
                                 "kgf/um": 55}  #
        self.SFH03220_2_8_dict = {"d": 32, "I": 20, "Da": 3.969, "D": 50, "A": 80, "E": 9, "B": 12, "L": 76,
                                  "W": 65, "H": 62, "X": 9, "Q": "M6", "N": "2.8x1", "Ca": 1907, "Coa": 5482,
                                  "kgf/um": 43}  #
        self.SFH03232_1_8_dict = {"d": 32, "I": 32, "Da": 3.969, "D": 50, "A": 80, "E": 9, "B": 12, "L":80,
                                  "W": 65, "H": 62, "X": 9, "Q": "M6", "N": "1.8x1", "Ca": 1257, "Coa": 3426,
                                  "kgf/um": 27}  #
        self.SFH03232_2_8_dict = {"d": 32, "I": 32, "Da": 3.969, "D": 50, "A": 80, "E": 9, "B": 12, "L": 112,
                                  "W": 65, "H": 62, "X": 9, "Q": "M6", "N": "2.8x1", "Ca": 1838, "Coa": 5329,
                                  "kgf/um": 42}  #
        self.SFH04005_3_8_dict = {"d": 40, "I": 5, "Da": 3.175, "D": 63, "A": 93, "E": 9, "B": 15, "L": 42,
                                  "W": 78, "H": 70, "X": 9, "Q": "M8", "N": "3.8x1", "Ca": 2018, "Coa": 7589,
                                  "kgf/um": 60}  #
        self.SFH04010_3_8_dict = {"d": 40, "I": 10, "Da": 6.35, "D": 63, "A": 93, "E": 9, "B": 14, "L": 60,
                                  "W": 78, "H": 70, "X": 9, "Q": "M8", "N": "3.8x1", "Ca": 5035, "Coa": 13943,
                                  "kgf/um": 67}  #
        self.SFH04020_2_8_dict = {"d": 40, "I": 20, "Da": 6.35, "D": 63, "A": 93, "E": 9, "B": 14, "L": 80,
                                  "W": 78, "H": 70, "X": 9, "Q": "M8", "N": "2.8x1", "Ca": 3959, "Coa": 10715,
                                  "kgf/um": 54}  #
        self.SFH04040_1_8_dict = {"d": 40, "I": 40, "Da": 6.35, "D": 63, "A": 93, "E": 9, "B": 14, "L": 98,
                                  "W": 78, "H": 70, "X": 9, "Q": "M8", "N": "1.8x1", "Ca": 2585, "Coa": 6648,
                                  "kgf/um": 34}  #
        self.SFH04040_2_8_dict = {"d": 40, "I": 40, "Da": 6.35, "D": 63, "A": 93, "E": 9, "B": 14, "L": 138,
                                  "W": 78, "H": 70, "X": 9, "Q": "M8", "N": "2.8x1", "Ca": 3780, "Coa": 10341,
                                  "kgf/um": 52}  #
        self.SFH05005_3_8_dict = {"d": 50, "I": 5, "Da": 3.175, "D": 75, "A": 110, "E": 105, "B": 15, "L": 42,
                                  "W": 93, "H": 85, "X": 11, "Q": "M8", "N": "3.8x1", "Ca": 2207, "Coa": 9542,
                                  "kgf/um": 68}  #
        self.SFH05010_3_8_dict = {"d": 50, "I": 10, "Da": 6.35, "D": 75, "A": 110, "E": 105, "B": 18, "L": 60,
                                  "W": 93, "H": 85, "X": 11, "Q": "M8", "N": "3.8x1", "Ca": 5638, "Coa": 17852,
                                  "kgf/um": 79}  #
        self.SFH05020_3_8_dict = {"d": 50, "I": 20, "Da": 6.35, "D": 75, "A": 110, "E": 105, "B": 18, "L": 100,
                                  "W": 93, "H": 85, "X": 11, "Q": "M8", "N": "3.8x1", "Ca": 5749, "Coa": 18485,
                                  "kgf/um": 87}  #
        self.SFH05050_1_8_dict = {"d": 50, "I": 50, "Da": 6.35, "D": 75, "A": 110, "E": 105, "B": 18, "L": 120,
                                  "W": 93, "H": 85, "X": 11, "Q": "M8", "N": "1.8x1", "Ca": 2946, "Coa": 8749,
                                  "kgf/um": 42}  #
        self.SFH05050_1_8_dict = {"d": 50, "I": 50, "Da": 6.35, "D": 75, "A": 110, "E": 105, "B": 18, "L": 170,
                                  "W": 93, "H": 85, "X": 11, "Q": "M8", "N": "2.8x1", "Ca": 4308, "Coa": 13610,
                                  "kgf/um": 65}  #

        self.SFH_serise_dict = {"SFH01205-2.8": self.SFH01205_2_8_dict, "SFH01210-2.8": self.SFH01210_2_8_dict,
                                "SFH01605-3.8": self.SFH01605_3_8_dict,"SFH01610-2.8":self.SFH01610_2_8_dict,
                                "SFH01616-1.8":self.SFH01616_1_8_dict,"SFH01616-2.8":self.SFH01616_2_8_dict,
                                "SFH01620-1.8":self.SFH01620_1_8_dict,"SFH02005-3.8":self.SFH02005_3_8_dict,
                                "SFH02010-3.8":self.SFH02010_3_8_dict,"SFH02020-1.8":self.SFH02020_1_8_dict,
                                "SFH02020-2.8":self.SFH02020_2_8_dict,"SFH02505-3.8":self.SFH02505_3_8_dict,
                                "SFH02510-3.8":self.SFH02510_3_8_dict,"SFH02525-1.8":self.SFH02525_1_8_dict,
                                "SFH02525-2.8":self.SFH02525_2_8_dict,"SFH03205-3.8":self.SFH03205_3_8_dict,
                                "SFH03210-3.8":self.SFH03210_3_8_dict,"SFH03220-2.8":self.SFH03220_2_8_dict,
                                "SFH03232-1.8":self.SFH03232_1_8_dict,"SFH03232-2.8":self.SFH03232_2_8_dict,
                                "SFH04005-3.8":self.SFH04005_3_8_dict,"SFH04010-3.8":self.SFH04010_3_8_dict,
                                "SFH04020-2.8":self.SFH04020_2_8_dict,"SFH04040-1.8":self.SFH04040_1_8_dict,
                                "SFH04040-2.8":self.SFH04040_2_8_dict,"SFH05005-3.8":self.SFH05005_3_8_dict,
                                "SFH05010-3.8":self.SFH05010_3_8_dict,"SFH05020-3.8":self.SFH05020_3_8_dict,
                                "SFH05050-1.8":self.SFH05050_1_8_dict,"SFH05050-1.8":self.SFH05050_1_8_dict
                                }

        self.series=self.SFH_serise_dict
        self.total_length=0
 
class Create_boll_SCcrew_dfu(Create_boll_SCcrew_sfu):
    def __init__(self):
        super(Create_boll_SCcrew_dfu, self).__init__()
        pass
        self.DFU01604_4_dict = {"d": 16, "I": 4, "Da": 2.381, "D": 28, "A": 48, "B": 10, "L": 80,
                                  "W": 38, "H": 40, "X": 5.5, "Q": "M6", "N": "1x4", "Ca": 973, "Coa": 2406,
                                  "kgf/um": 43}  #

        self.DFU02004_4_dict = {"d": 20, "I": 4, "Da": 2.381, "D": 36, "A": 58, "B": 10, "L": 80,
                                "W": 47, "H": 44, "X": 6.6, "Q": "M6", "N": "1x4", "Ca": 1066, "Coa": 2987,
                                "kgf/um": 51}  #

        self.DFU02504_4_dict = {"d": 25, "I": 4, "Da": 2.381, "D": 40, "A": 62, "B": 10, "L": 80,
                                "W": 51, "H": 48, "X": 6.6, "Q": "M6", "N": "1x4", "Ca": 1180, "Coa": 3795,
                                "kgf/um": 60}  #

        self.DFU02506_4_dict = {"d": 25, "I": 6, "Da": 3.969, "D": 40, "A": 62, "B": 10, "L": 105,
                                "W": 51, "H": 48, "X": 6.6, "Q": "M6", "N": "1x4", "Ca": 2381, "Coa": 6057,
                                "kgf/um": 64}  #

        self.DFU02508_4_dict = {"d": 25, "I": 8, "Da": 4.762, "D": 40, "A": 62, "B": 10, "L": 120,
                                "W": 51, "H": 48, "X": 6.6, "Q": "M6", "N": "1x4", "Ca": 2963, "Coa": 7313,
                                "kgf/um": 67}  #

        self.DFU03204_4_dict = {"d": 32, "I": 4, "Da": 2.381, "D": 50, "A": 80, "B": 12, "L": 80,
                                "W": 65, "H": 62, "X": 9, "Q": "M6", "N": "1x4", "Ca": 1296, "Coa": 4838,
                                "kgf/um": 71}  #

        self.DFU03206_4_dict = {"d": 32, "I": 4, "Da": 3.969, "D": 50, "A": 80, "B": 12, "L": 105,
                                "W": 65, "H": 62, "X": 9, "Q": "M6", "N": "1x4", "Ca": 2632, "Coa": 7979,
                                "kgf/um": 78}  #

        self.DFU03208_4_dict = {"d": 32, "I": 8, "Da": 4.762, "D": 50, "A": 80, "B": 12, "L": 122,
                                "W": 65, "H": 62, "X": 9, "Q": "M6", "N": "1x4", "Ca": 3387, "Coa": 9622,
                                "kgf/um": 82}  #

        self.DFU04006_4_dict = {"d": 40, "I": 6, "Da": 3.969, "D": 63, "A": 93, "B": 14, "L": 108,
                                "W": 78, "H": 70, "X": 9, "Q": "M6", "N": "1x4", "Ca": 2873, "Coa": 9913,
                                "kgf/um": 91}  #

        self.DFU04008_4_dict = {"d": 40, "I": 8, "Da": 4.762, "D": 63, "A": 93, "B": 14, "L": 132,
                                "W": 78, "H": 70, "X": 9, "Q": "M6", "N": "1x4", "Ca": 3712, "Coa": 11947,
                                "kgf/um": 96}  #.

        self.DFU05020_4_dict = {"d": 50, "I": 20, "Da": 7.144, "D": 75, "A": 110, "B": 16, "L": 280,
                                "W": 93, "H": 85, "X": 11, "Q": "M8", "N": "1x4", "Ca": 7142, "Coa": 22588,
                                "kgf/um": 126}  #

        self.DFU06320_4_dict = {"d": 63, "I": 20, "Da": 9.525, "D": 95, "A": 135, "B": 20, "L": 290,
                                "W":115, "H": 100, "X": 13.5, "Q": "M8", "N": "1x4", "Ca": 11444, "Coa": 36653,
                                "kgf/um": 152}  #

        self.DFU08020_4_dict = {"d": 80, "I": 20, "Da": 9.525, "D": 125, "A": 165, "B": 25, "L": 295,
                                "W": 145, "H": 130, "X": 13.5, "Q": "M8", "N": "1x4", "Ca": 12911, "Coa": 47747,
                                "kgf/um": 187}  #

        self.DFU10020_4_dict = {"d": 100, "I": 20, "Da": 9.525, "D": 150, "A": 202, "B": 30, "L": 340,
                                "W": 170, "H": 155, "X": 17.5, "Q": "M8", "N": "1x4", "Ca": 14303, "Coa": 60698,
                                "kgf/um": 222}  #
        self.DFU_serise_dict={"DFU01604-4":self.DFU01604_4_dict,"DFU02004-4":self.DFU02004_4_dict,"DFU02504-4":self.DFU02504_4_dict,
                              "DFU02506-4":self.DFU02506_4_dict,"DFU02508-4":self.DFU02508_4_dict,"DFU03204-4":self.DFU03204_4_dict,
                              "DFU03206-4":self.DFU03206_4_dict,"DFU03208-4":self.DFU03208_4_dict,"DFU04006-4":self.DFU04006_4_dict,
                              "DFU04008-4":self.DFU04008_4_dict,"DFU05020-4":self.DFU05020_4_dict,"DFU06320-4":self.DFU06320_4_dict,
                              "DFU08020-4":self.DFU08020_4_dict,"DFU10020-4":self.DFU10020_4_dict}

        self.series=self.DFU_serise_dict
        self.total_length=0


class Create_Liner_guide_TRH_V(object):
    def __init__(self):
        pass
        self.TRH15VN_dict = {"组装规格(mm)":" ","H":28,"W2":9.5,"E":3.2,"滑块尺寸(mm)":" ","W":34,"B":26,"J":26,
                             "L":56.9,"L1":39.5,"Qxl":"M4*8","T1":"9.5","油孔":"M4*0.7","N":7,"滑轨(mm)":" ",
                             "W1":15,"H1":13,"ΦD":"7.5","h":6,"Φd":4.5,"F":60}  #
        self.TRH15VL_dict = {"组装规格(mm)": " ", "H": 28, "W2": 9.5, "E": 3.2, "滑块尺寸(mm)": " ", "W": 34, "B": 26, "J": 26,
                           "L": 65.4, "L1": 48, "Qxl": "M4*8", "T1": "9.5", "油孔": "M4*0.7", "N": 7, "滑轨(mm)": " ",
                           "W1": 15, "H1": 13, "ΦD": "7.5", "h": 6, "Φd": 4.5, "F": 60}  #
        self.TRH20VN_dict = {"组装规格(mm)": " ", "H": 30, "W2": 12, "E": 3.6, "滑块尺寸(mm)": " ", "W": 44, "B": 32, "J": 36,
                             "L": 75.6, "L1": 54, "Qxl": "M5*7", "T1": "6.5", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 20, "H1": 16.5, "ΦD": "9.5", "h": 8.5, "Φd": 6, "F": 60}  #
        self.TRH20VE_dict = {"组装规格(mm)": " ", "H": 30, "W2": 12, "E": 3.6, "滑块尺寸(mm)": " ", "W": 44, "B": 32, "J": 50,
                             "L": 99.6, "L1": 78, "Qxl": "M5*7", "T1": 6.5, "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 20, "H1": 16.5, "ΦD": "9.5", "h": 8.5, "Φd": 6, "F": 60}  #
        self.TRH25VN_dict = {"组装规格(mm)": " ", "H": 40, "W2": 12.5, "E": 5.8, "滑块尺寸(mm)": " ", "W": 48, "B": 35, "J": 35,
                             "L": 81, "L1": 59, "Qxl": "M6*8", "T1": 11.5,"油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 23, "H1": 20, "ΦD": "11", "h": 9, "Φd": 7, "F": 60}  #
        self.TRH25VE_dict = {"组装规格(mm)": " ", "H": 40, "W2": 12.5, "E": 5.8, "滑块尺寸(mm)": " ", "W": 48, "B": 35, "J": 50,
                             "L": 110, "L1": 88, "Qxl": "M6*8", "T1": 11.5, "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 23, "H1": 20, "ΦD": "11", "h": 9, "Φd": 7, "F": 60}  #
        self.TRH30VN_dict = {"组装规格(mm)": " ", "H": 45, "W2": 16, "E": 7, "滑块尺寸(mm)": " ", "W":60 , "B": 40, "J": 40,
                             "L": 96.3, "L1": 69.3, "Qxl": "M8*10", "T1": 11, "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 28, "H1": 23, "ΦD": "14", "h": 12, "Φd": 9, "F": 80}  #
        self.TRH30VE_dict = {"组装规格(mm)": " ", "H": 45, "W2": 16, "E": 7, "滑块尺寸(mm)": " ", "W": 60, "B": 40, "J": 60,
                             "L": 132, "L1": 105, "Qxl": "M8*10", "T1": 11, "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 28, "H1": 23, "ΦD": "14", "h": 12, "Φd": 9, "F": 80}  #
        self.TRH35VN_dict = {"组装规格(mm)": " ", "H": 55, "W2": 18, "E": 7.5, "滑块尺寸(mm)": " ", "W": 70, "B": 50, "J": 50,
                             "L": 109, "L1": 79, "Qxl": "M8*10", "T1": 15, "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 34, "H1": 26, "ΦD": "14", "h": 12, "Φd": 9, "F": 80}  #
        self.TRH35VE_dict = {"组装规格(mm)": " ", "H": 55, "W2": 18, "E": 7.5, "滑块尺寸(mm)": " ", "W": 70, "B": 50, "J": 72,
                             "L": 153, "L1": 123, "Qxl": "M8*10", "T1": 15, "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 34, "H1": 26, "ΦD": "14", "h": 12, "Φd": 9, "F": 80}  #
        self.TRH45VL_dict = {"组装规格(mm)": " ", "H": 70, "W2": 20.5, "E": 8.9, "滑块尺寸(mm)": " ", "W": 85.5, "B": 60, "J": 60,
                             "L": 140, "L1": 106, "Qxl": "M10*15", "T1": 20.5, "油孔": "PT1/8", "N": 12.5, "滑轨(mm)": " ",
                             "W1": 45, "H1": 32, "ΦD": "20", "h": 17, "Φd": 14, "F": 105}  #
        self.TRH45VE_dict = {"组装规格(mm)": " ", "H": 70, "W2": 20.5, "E": 8.9, "滑块尺寸(mm)": " ", "W": 85.5, "B": 60,
                             "J": 80,"L": 174, "L1": 140, "Qxl": "M10*15", "T1": 20.5, "油孔": "PT1/8", "N": 12.5, "滑轨(mm)": " ",
                             "W1": 45, "H1": 32, "ΦD": "20", "h": 17, "Φd": 14, "F": 105}  #
        self.TRH55VL_dict = {"组装规格(mm)": " ", "H": 80, "W2": 23.5, "E": 13, "滑块尺寸(mm)": " ", "W": 100, "B": 75,
                             "J": 75, "L": 162, "L1": 118, "Qxl": "M12*18", "T1": 21, "油孔": "PT1/8", "N": 12.5,
                             "滑轨(mm)": " ",
                             "W1": 53, "H1": 44, "ΦD": "23", "h": 20, "Φd": 16, "F": 120}  #
        self.TRH55VE_dict = {"组装规格(mm)": " ", "H": 80, "W2": 23.5, "E": 13, "滑块尺寸(mm)": " ", "W": 100, "B": 75,
                             "J": 95, "L": 200.1, "L1": 156.1, "Qxl": "M12*18", "T1": 21, "油孔": "PT1/8", "N": 12.5,
                             "滑轨(mm)": " ",
                             "W1": 53, "H1": 44, "ΦD": "23", "h": 20, "Φd": 16, "F": 120}  #
        self.TRH65VL_dict = {"组装规格(mm)": " ", "H": 90, "W2": 31.5, "E": 14, "滑块尺寸(mm)": " ", "W": 126, "B": 76,
                             "J": 70, "L": 197, "L1": 147, "Qxl": "M16*20", "T1": 19, "油孔": "PT1/8", "N": 12.5,
                             "滑轨(mm)": " ",
                             "W1": 63, "H1": 53, "ΦD": "26", "h": 22, "Φd": 18, "F": 150}  #
        self.TRH65VE_dict = {"组装规格(mm)": " ", "H": 90, "W2": 31.5, "E": 14, "滑块尺寸(mm)": " ", "W": 126, "B": 76,
                             "J": 120, "L": 256.5, "L1": 206.5, "Qxl": "M16*20", "T1": 19, "油孔": "PT1/8", "N": 12.5,
                             "滑轨(mm)": " ",
                             "W1": 63, "H1": 53, "ΦD": "26", "h": 22, "Φd": 18, "F": 150}  #
        self.TRH_series_dict = {"TRH15VN":self.TRH15VN_dict,"TRH20VL": self.TRH15VL_dict,"TRH20VN":self.TRH20VN_dict,"TRH20VE":self.TRH20VE_dict,
                                "TRH25VN":self.TRH25VN_dict,"TRH25VE":self.TRH25VE_dict,"TRH30VN":self.TRH30VN_dict,"TRH30VE":self.TRH30VE_dict,
                                "TRH35VN":self.TRH35VN_dict,"TRH35VE":self.TRH35VE_dict,"TRH45VL":self.TRH45VL_dict,"TRH45VE":self.TRH45VE_dict,
                                "TRH55VL":self.TRH55VL_dict,"TRH55VE":self.TRH20VN_dict,"TRH65VL":self.TRH65VL_dict,"TRH65VE":self.TRH65VE_dict
                                }

        self.series = self.TRH_series_dict
    def Create_shape(self,filename):
        pass
        try:
            filepath="./3Ddata/STP/"+filename+".stp"
            self.acompoud=read_step_file(filepath)
            return self.acompoud
        except:
            filepath = "./3Ddata/STP/" + filename + ".step"
            self.acompoud = read_step_file(filepath)
            return self.acompoud

    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")#导轨高度列表
        dict_combox = {"滑块型号": ["","15","20","25","30","35","45","55","65"]}#
        all_combox_list.append(["滑轨","标准型"])
        all_combox_list.append(["组装高度","高组装系列"])
        all_combox_list.append(["硬度","58～62HRC"])
        all_combox_list.append(["滑轨材料","S55C"])
        all_combox_list.append(["滑块材料","SCM420"])
        all_combox_list.append(["精度等级","普通"])
        all_combox_list.append(dict_combox)#导轨高度列表
        all_combox_list.append({"滑块法兰式": ["  ", "V:无法兰"]})
        all_combox_list.append({"滑块长度": ["  ", "N:标准型 ", "S:短型", "L:长型","E:加长型"]})
        all_combox_list.append(["滑轨长度L(mm)", "600"])
        all_combox_list.append(["订货代码", ""])

        return all_combox_list

class Create_Liner_guide_TRH_F(object):
    def __init__(self):
        pass
        self.TRH15FN_dict = {"组装规格(mm)":" ","H":24,"W2":16,"E":3.2,"滑块尺寸(mm)":" ","W":47,"B":38,"J":30,"t":8,
                             "L":56.9,"L1":39.5,"Qxl":"M5*8","T1":"5.5","油孔":"M4*0.7","N":7,"滑轨(mm)":" ",
                             "W1":15,"H1":13,"ΦD":"7.5","h":6,"Φd":4.5,"F":60}  #
        self.TRH15FL_dict = {"组装规格(mm)": " ", "H": 24, "W2": 16, "E": 3.2, "滑块尺寸(mm)": " ", "W": 47, "B": 38, "J": 30,"t":8,
                             "L": 65.4, "L1": 48, "Qxl": "M5*8", "T1": "9.5", "油孔": "M4*0.7", "N": 7, "滑轨(mm)": " ",
                             "W1": 15, "H1": 13, "ΦD": "7.5", "h": 6, "Φd": 4.5, "F": 60}  #
        self.TRH20FN_dict = {"组装规格(mm)": " ", "H": 30, "W2": 21.5, "E": 4.6, "滑块尺寸(mm)": " ", "W": 63, "B": 53, "J": 40,"t":10,
                             "L": 75.6, "L1": 54, "Qxl": "M6*10", "T1": "6.5", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 20, "H1": 16.5, "ΦD": "9.5", "h": 8.5, "Φd": 6, "F": 60} #
        self.TRH20FE_dict = {"组装规格(mm)": " ", "H": 30, "W2": 21.5, "E": 4.6, "滑块尺寸(mm)": " ", "W": 63, "B": 53, "J": 40,"t": 10,
                             "L": 99.6, "L1": 78, "Qxl": "M6*10", "T1": "6.5", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 20, "H1": 16.5, "ΦD": "9.5", "h": 8.5, "Φd": 6, "F": 60}  #
        self.TRH25FN_dict = {"组装规格(mm)": " ", "H": 36, "W2": 23.5, "E": 5.8, "滑块尺寸(mm)": " ", "W": 70, "B": 57, "J": 45,"t":12,
                             "L": 81, "L1": 59, "Qxl": "M8*12", "T1": 7.5, "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 23, "H1": 20, "ΦD": "11", "h": 9, "Φd": 7, "F": 60}  #
        self.TRH25FE_dict = {"组装规格(mm)": " ", "H": 36, "W2": 23.5, "E": 5.8, "滑块尺寸(mm)": " ", "W": 70, "B": 57, "J": 45,"t": 12,
                             "L": 110, "L1": 88, "Qxl": "M8*12", "T1": 7.5, "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 23, "H1": 20, "ΦD": "11", "h": 9, "Φd": 7, "F": 60}  #
        self.TRH30FN_dict = {"组装规格(mm)": " ", "H": 42, "W2": 31, "E": 7, "滑块尺寸(mm)": " ", "W": 90, "B": 52, "J": 52,
                             "L": 96.3, "L1": 69.3, "Qxl": "M10*15", "T1": 8, "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 28, "H1": 23, "ΦD": "14", "h": 12, "Φd": 9, "F": 80}  #
        self.TRH30FE_dict = {"组装规格(mm)": " ", "H": 42, "W2": 31, "E": 7, "滑块尺寸(mm)": " ", "W": 90, "B": 52, "J": 52,
                             "L": 132, "L1": 105, "Qxl": "M10*15", "T1": 8, "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 28, "H1": 23, "ΦD": "14", "h": 12, "Φd": 9, "F": 80}  #
        self.TRH35FN_dict = {"组装规格(mm)": " ", "H": 48, "W2": 33, "E": 7.5, "滑块尺寸(mm)": " ", "W": 100, "B": 82, "J": 62,"t":15,
                             "L": 109, "L1": 79, "Qxl": "M10*15", "T1": 8, "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 34, "H1": 26, "ΦD": "14", "h": 12, "Φd": 9, "F": 80}  #
        self.TRH35FE_dict = {"组装规格(mm)": " ", "H": 48, "W2": 33, "E": 7.5, "滑块尺寸(mm)": " ", "W": 100, "B": 82, "J": 62,"t": 15,
                             "L": 153, "L1": 123, "Qxl": "M10*15", "T1": 8, "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 34, "H1": 26, "ΦD": "14", "h": 12, "Φd": 9, "F": 80}  #
        self.TRH45FL_dict = {"组装规格(mm)": " ", "H": 60, "W2": 37.5, "E": 8.9, "滑块尺寸(mm)": " ", "W": 120, "B": 100,"J": 80,"t":18,
                             "L": 140, "L1": 106, "Qxl": "M12*18", "T1": 10.5, "油孔": "PT1/8", "N": 12.5, "滑轨(mm)": " ",
                             "W1": 45, "H1": 32, "ΦD": "20", "h": 17, "Φd": 14, "F": 105}  #
        self.TRH45FE_dict = {"组装规格(mm)": " ", "H": 60, "W2": 37.5, "E": 8.9, "滑块尺寸(mm)": " ", "W": 120, "B": 100,"J": 80, "t": 18,
                             "L": 174, "L1": 140, "Qxl": "M12*18", "T1": 10.5, "油孔": "PT1/8", "N": 12.5, "滑轨(mm)": " ",
                             "W1": 45, "H1": 32, "ΦD": "20", "h": 17, "Φd": 14, "F": 105}  #
        self.TRH55FL_dict = {"组装规格(mm)": " ", "H": 70, "W2": 43.5, "E": 13, "滑块尺寸(mm)": " ", "W": 140, "B": 116,
                             "J": 95, "t":23.5,"L": 162, "L1": 118, "Qxl": "M14*17", "T1": 11, "油孔": "PT1/8", "N": 12.5,"滑轨(mm)": " ",
                             "W1": 53, "H1": 44, "ΦD": "23", "h": 20, "Φd": 16, "F": 120}  #
        self.TRH55FE_dict = {"组装规格(mm)": " ", "H": 70, "W2": 43.5, "E": 13, "滑块尺寸(mm)": " ", "W": 140, "B": 116,
                             "J": 95, "t": 23.5, "L": 200.1, "L1": 156.1, "Qxl": "M14*17", "T1": 11, "油孔": "PT1/8",
                             "N": 12.5, "滑轨(mm)": " ",
                             "W1": 53, "H1": 44, "ΦD": "23", "h": 20, "Φd": 16, "F": 120}  #
        self.TRH65FL_dict = {"组装规格(mm)": " ", "H": 90, "W2": 53.5, "E": 14, "滑块尺寸(mm)": " ", "W": 170, "B": 142,
                             "J": 110,"t":37,"L": 197, "L1": 147, "Qxl": "M16*23", "T1": 11, "油孔": "PT1/8", "N": 12.5,"滑轨(mm)": " ",
                             "W1": 63, "H1": 53, "ΦD": "26", "h": 22, "Φd": 18, "F": 150}  #
        self.TRH65FE_dict = {"组装规格(mm)": " ", "H": 90, "W2": 53.5, "E": 14, "滑块尺寸(mm)": " ", "W": 170, "B": 142,
                             "J": 110, "t": 37, "L": 256.5, "L1": 206.5, "Qxl": "M16*23", "T1": 11, "油孔": "PT1/8",
                             "N": 12.5, "滑轨(mm)": " ",
                             "W1": 63, "H1": 53, "ΦD": "26", "h": 22, "Φd": 18, "F": 150}  #

        self.TRH_series_dict = {"TRH15FN":self.TRH15FN_dict,"TRH15FL":self.TRH15FL_dict,"TRH20FN":self.TRH20FN_dict,"TRH20FE":self.TRH20FE_dict,
                                "TRH25FN":self.TRH25FN_dict,"TRH25FE":self.TRH25FE_dict,"TRH30FN":self.TRH30FN_dict,"TRH30FE":self.TRH30FE_dict,
                                "TRH35FN":self.TRH35FN_dict,"TRH35FE":self.TRH35FE_dict,"TRH45FL":self.TRH45FL_dict,"TRH45FE":self.TRH45FE_dict,
                                "TRH55FL":self.TRH55FL_dict,"TRH55FE":self.TRH55FE_dict,"TRH65FL":self.TRH65FL_dict,"TRH65FE":self.TRH65FE_dict
                                }

        self.series = self.TRH_series_dict
    def Create_shape(self,filename):
        pass
        try:
            filepath="./3Ddata/STP/"+filename+".stp"
            self.acompoud=read_step_file(filepath)
            return self.acompoud
        except:
            filepath = "./3Ddata/STP/" + filename + ".step"
            self.acompoud = read_step_file(filepath)
            return self.acompoud

    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")#导轨高度列表
        dict_combox = {"滑块型号": ["","15","20","25","30","35","45","55","65"]}#
        all_combox_list.append(["滑轨","标准型"])
        all_combox_list.append(["组装高度","高组装系列"])
        all_combox_list.append(["硬度","58～62HRC"])
        all_combox_list.append(["滑轨材料","S55C"])
        all_combox_list.append(["滑块材料","SCM420"])
        all_combox_list.append(["精度等级","普通"])
        all_combox_list.append(dict_combox)#导轨高度列表
        all_combox_list.append({"滑块法兰式": ["  ", "F:有法兰"]})
        all_combox_list.append({"滑块长度": ["  ", "N:标准型 ", "S:短型", "L:长型","E:加长型"]})
        all_combox_list.append(["滑轨长度L(mm)", "600"])
        all_combox_list.append(["订货代码", ""])

        return all_combox_list

class Create_Liner_guide_TRS_V(object):
    def __init__(self):
        pass
        self.TRS15VS_dict = {"组装规格(mm)":" ","H":24,"W2":9.5,"E":3.2,"滑块尺寸(mm)":" ","W":34,"B":26,"J":"-",
                             "L":40.3,"L1":22.9,"Qxl":"M4*5","T1":"5.5","油孔":"M4*0.7","N":7,"滑轨(mm)":" ",
                             "W1":15,"H1":13,"ΦD":"7.5","h":6,"Φd":4.5,"F":60}  #
        self.TRS15VN_dict = {"组装规格(mm)": " ", "H": 24, "W2": 9.5, "E": 3.2, "滑块尺寸(mm)": " ", "W": 34, "B": 26, "J": 26,
                             "L": 56.9, "L1": 39.5, "Qxl": "M4*5", "T1": "5.5", "油孔": "M4*0.7", "N": 7, "滑轨(mm)": " ",
                             "W1": 15, "H1": 13, "ΦD": "7.5", "h": 6, "Φd": 4.5, "F": 60}  #
        self.TRS20VS_dict = {"组装规格(mm)": " ", "H": 28, "W2": 11, "E": 4.6, "滑块尺寸(mm)": " ", "W": 42, "B": 32, "J": "-",
                             "L": 49.4, "L1": 27.8, "Qxl": "M5*6", "T1": "4.5", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 20, "H1": 16.5, "ΦD": "9.5", "h": 8.5, "Φd": 6, "F": 60}  #
        self.TRS20VN_dict = {"组装规格(mm)": " ", "H": 28, "W2": 11, "E": 4.6, "滑块尺寸(mm)": " ", "W": 42, "B": 32, "J": 32,
                             "L": 68.3, "L1": 46.7, "Qxl": "M5*6", "T1": "4.5", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 20, "H1": 16.5, "ΦD": "9.5", "h": 8.5, "Φd": 6, "F": 60}  #
        self.TRS25VS_dict = {"组装规格(mm)": " ", "H": 33, "W2": 12.5, "E": 5.8, "滑块尺寸(mm)": " ", "W": 48, "B": 35, "J": "-",
                             "L": 57.2, "L1": 35.2, "Qxl": "M6*6.5", "T1": "4.5", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 23, "H1": 20, "ΦD": "11", "h": 9, "Φd": 7, "F": 60}  #
        self.TRS25VN_dict = {"组装规格(mm)": " ", "H": 33, "W2": 12.5, "E": 5.8, "滑块尺寸(mm)": " ", "W": 48, "B": 35,
                             "J": "35",
                             "L": 81, "L1": 59, "Qxl": "M6*6.5", "T1": "4.5", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 23, "H1": 20, "ΦD": "11", "h": 9, "Φd": 7, "F": 60}  #
        self.TRS30VS_dict = {"组装规格(mm)": " ", "H": 42, "W2": 16, "E": 7, "滑块尺寸(mm)": " ", "W": 60, "B": 40,
                             "J": "-",
                             "L": 67.4, "L1": 40.4, "Qxl": "M8*8", "T1": "8", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 28, "H1": 23, "ΦD": "14", "h": 12, "Φd": 9, "F": 80}  #
        self.TRS30VN_dict = {"组装规格(mm)": " ", "H": 42, "W2": 16, "E": 7, "滑块尺寸(mm)": " ", "W": 60, "B": 40,
                             "J": 40,
                             "L": 96.3, "L1": 69.3, "Qxl": "M8*8", "T1": "8", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 28, "H1": 23, "ΦD": "14", "h": 12, "Φd": 9, "F": 80}  #
        self.TRS35VN_dict = {"组装规格(mm)": " ", "H": 48, "W2": 18, "E": 7.5, "滑块尺寸(mm)": " ", "W": 70, "B": 50,
                             "J": 50,
                             "L": 109, "L1": 79, "Qxl": "M8*8", "T1": "8", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 34, "H1": 26, "ΦD": "14", "h": 12, "Φd": 9, "F": 80}  #
        self.TRS35VE_dict = {"组装规格(mm)": " ", "H": 48, "W2": 18, "E": 7.5, "滑块尺寸(mm)": " ", "W": 70, "B": 50,
                             "J": 72,
                             "L": 153, "L1": 123, "Qxl": "M8*8", "T1": "8", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 34, "H1": 26, "ΦD": "14", "h": 12, "Φd": 9, "F": 80}  #
        self.TRS45VE_dict = {"组装规格(mm)": " ", "H": 60, "W2": 20.5, "E": 8.9, "滑块尺寸(mm)": " ", "W": 86, "B": 60,
                             "J": 60,
                             "L": 124.5, "L1": 90.5, "Qxl": "M10*15", "T1": "10.5", "油孔": "PT1/8", "N": 12.5, "滑轨(mm)": " ",
                             "W1": 45, "H1": 32, "ΦD": "20", "h": 17, "Φd": 14, "F": 105}  #


        self.TRH_series_dict = {"TRS15VS":self.TRS15VS_dict,"TRS15VN":self.TRS15VN_dict,"TRS20VS":self.TRS20VS_dict,"TRS20VN":self.TRS20VN_dict,
                                "TRS25VS":self.TRS25VS_dict,"TRS25VN":self.TRS25VN_dict,"TRS30VS":self.TRS30VS_dict,"TRS30VN":self.TRS30VN_dict,
                                "TRS35VN":self.TRS35VN_dict,"TRS35VE":self.TRS35VE_dict,"TRS45VE":self.TRS45VE_dict
                                }

        self.series = self.TRH_series_dict
    def Create_shape(self,filename):
        pass
        try:
            filepath="./3Ddata/STP/"+filename+".stp"
            self.acompoud=read_step_file(filepath)
            return self.acompoud
        except:
            filepath = "./3Ddata/STP/" + filename + ".step"
            self.acompoud = read_step_file(filepath)
            return self.acompoud

    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")#导轨高度列表
        dict_combox = {"滑块型号": ["","15","20","25","30","35","45"]}#
        all_combox_list.append(["滑轨","标准型"])
        all_combox_list.append(["组装高度","低组装系列"])
        all_combox_list.append(["硬度","58～62HRC"])
        all_combox_list.append(["滑轨材料","S55C"])
        all_combox_list.append(["滑块材料","SCM420"])
        all_combox_list.append(["精度等级","普通"])
        all_combox_list.append(dict_combox)#导轨高度列表
        all_combox_list.append({"滑块法兰式": ["  ", "V:无法兰"]})
        all_combox_list.append({"滑块长度": ["  ", "N:标准型 ", "S:短型", "L:长型","E:加长型"]})
        all_combox_list.append(["滑轨长度L(mm)", "600"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list
class Create_Liner_guide_TRS_F(object):
    def __init__(self):
        pass
        self.TRS15FS_dict = {"组装规格(mm)":" ","H":24,"W2":18.5,"E":3.2,"滑块尺寸(mm)":" ","W":52,"B":41,"J":"-","t":7,
                             "L":40.3,"L1":22.9,"Qxl":"M5*7","T1":"5.5","油孔":"M4*0.7","N":7,"滑轨(mm)":" ",
                             "W1":15,"H1":13,"ΦD":"7.5","h":6,"Φd":4.5,"F":60}  #

        self.TRS15FN_dict = {"组装规格(mm)": " ", "H": 24, "W2": 18.5, "E": 3.2, "滑块尺寸(mm)": " ", "W": 52, "B": 41, "J": 26,"t":7,
                             "L": 56.9, "L1": 39.5, "Qxl": "M5*7", "T1": "5.5", "油孔": "M4*0.7", "N": 7, "滑轨(mm)": " ",
                             "W1": 15, "H1": 13, "ΦD": "7.5", "h": 6, "Φd": 4.5, "F": 60}  #

        self.TRS20FS_dict = {"组装规格(mm)": " ", "H": 28, "W2": 19.5, "E": 4.6, "滑块尺寸(mm)": " ", "W": 59, "B": 49, "J": "-","t":9,
                             "L": 49.4, "L1": 27.8, "Qxl": "M6*9", "T1": "4.5", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 20, "H1": 16.5, "ΦD": "9.5", "h": 8.5, "Φd": 6, "F": 60}  #

        self.TRS20FN_dict = {"组装规格(mm)": " ", "H": 28, "W2": 19.5, "E": 4.6, "滑块尺寸(mm)": " ", "W": 59, "B": 49, "J": 32,"t":9,
                             "L": 68.3, "L1": 46.7, "Qxl": "M6*9", "T1": "4.5", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 20, "H1": 16.5, "ΦD": "9.5", "h": 8.5, "Φd": 6, "F": 60}  #

        self.TRS25FN_dict = {"组装规格(mm)": " ", "H": 33, "W2": 25, "E": 5.8, "滑块尺寸(mm)": " ", "W": 73, "B": 60, "J": 35,"t":10,
                             "L": 81, "L1": 59, "Qxl": "M8*10", "T1": "4.5", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 23, "H1": 20, "ΦD": "11", "h": 9, "Φd": 7, "F": 60}  #

        self.TRS25VE_dict = {"组装规格(mm)": " ", "H": 36, "W2": 12.5, "E": 5.8, "滑块尺寸(mm)": " ", "W": 48, "B": 35,
                             "J": "50",
                             "L": 110, "L1": 88, "Qxl": "M6*6.5", "T1": "7.5", "油孔": "M6*1", "N": 14, "滑轨(mm)": " ",
                             "W1": 23, "H1": 20, "ΦD": "11", "h": 9, "Φd": 7, "F": 60}  #



        self.TRS_series_dict = {"TRS15FS":self.TRS15FS_dict,"TRS15FN":self.TRS15FN_dict,"TRS20FS":self.TRS20FS_dict,"TRS20FN":self.TRS20FN_dict,
                                "TRS25FN":self.TRS25FN_dict,"TRS25VE":self.TRS25VE_dict
                                }

        self.series = self.TRS_series_dict
    def Create_shape(self,filename):
        pass
        try:
            filepath="./3Ddata/STP/"+filename+".stp"
            self.acompoud=read_step_file(filepath)
            return self.acompoud
        except:
            filepath = "./3Ddata/STP/" + filename + ".step"
            self.acompoud = read_step_file(filepath)
            return self.acompoud

    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")#导轨高度列表
        dict_combox = {"滑块型号": ["","15","20","25"]}#
        all_combox_list.append(["滑轨","标准型"])
        all_combox_list.append(["组装高度","低组装系列"])
        all_combox_list.append(["硬度","58～62HRC"])
        all_combox_list.append(["滑轨材料","S55C"])
        all_combox_list.append(["滑块材料","SCM420"])
        all_combox_list.append(["精度等级","普通"])
        all_combox_list.append(dict_combox)#导轨高度列表
        all_combox_list.append({"滑块法兰式": ["  ", "F:有法兰"]})
        all_combox_list.append({"滑块长度": ["  ", "N:标准型 ", "S:短型", "L:长型","E:加长型"]})
        all_combox_list.append(["滑轨长度L(mm)", "600"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list
class Create_Liner_guide_TM_N(object):
    def __init__(self):
        pass
        self.TM07NN_dict = {"组装规格(mm)":" ","H":8,"W2":5,"E":1.2,"滑块尺寸(mm)":" ","W":17,"B":12,"J":8,"T":2.25,
                             "L":22.8,"L1":12.3,"Qxl":"M2*2","Φ":1.3,"滑轨(mm)":" ",
                             "W1":7,"H1":4.7,"ΦD":"4.2","h":2.3,"Φd":2.4,"F":15}  #

        self.TM07NL_dict = {"组装规格(mm)": " ", "H": 8, "W2": 5, "E": 1.2, "滑块尺寸(mm)": " ", "W": 17, "B": 12, "J": 13,"T": 2.25,
                            "L": 30.8, "L1": 20.3, "Qxl": "M2*2", "Φ": 1.3, "滑轨(mm)": " ",
                            "W1": 7, "H1": 4.7, "ΦD": "4.2", "h": 2.3, "Φd": 2.4, "F": 15}  #

        self.TM09NN_dict = {"组装规格(mm)": " ", "H": 10, "W2": 5.5, "E": 1.9, "滑块尺寸(mm)": " ", "W": 20, "B": 15, "J": 10,
                            "T": 3.62,
                            "L": 30.4, "L1": 19.8, "Qxl": "M3*3", "Φ": 1.3, "滑轨(mm)": " ",
                            "W1": 9, "H1": 5.5, "ΦD": "6", "h": 3.3, "Φd": 3.5, "F": 20}  #
        self.TM09NL_dict = {"组装规格(mm)": " ", "H": 10, "W2": 5.5, "E": 1.9, "滑块尺寸(mm)": " ", "W": 20, "B": 15, "J": 16,
                            "T": 3.62,
                            "L": 40.7, "L1": 31.1, "Qxl": "M3*3", "Φ": 1.3, "滑轨(mm)": " ",
                            "W1": 9, "H1": 5.5, "ΦD": "6", "h": 3.3, "Φd": 3.5, "F": 20}  #

        self.TM12NN_dict = {"组装规格(mm)": " ", "H": 13, "W2": 7.5, "E": 2.7, "滑块尺寸(mm)": " ", "W": 27, "B": 20, "J": 15,
                            "T": 4.54,
                            "L": 34.4, "L1": 20.6, "Qxl": "M3*3.5", "Φ": 1.3, "滑轨(mm)": " ",
                            "W1": 12, "H1": 7.5, "ΦD": "6", "h": 4.5, "Φd": 3.5, "F": 25}  #
        self.TM12NL_dict = {"组装规格(mm)": " ", "H": 13, "W2": 7.5, "E": 2.7, "滑块尺寸(mm)": " ", "W": 27, "B": 20, "J": 20,
                            "T": 4.54,
                            "L": 34.4, "L1": 20.6, "Qxl": "M3*3.5", "Φ": 1.3, "滑轨(mm)": " ",
                            "W1": 12, "H1": 7.5, "ΦD": "6", "h": 4.5, "Φd": 3.5, "F": 25}  #
        self.TM15NN_dict = {"组装规格(mm)": " ", "H": 16, "W2": 8.5, "E": 3.7, "滑块尺寸(mm)": " ", "W": 32, "B": 25, "J": 20,
                            "T": 5.86,
                            "L": 42.4, "L1": 27, "Qxl": "M3*5", "Φ": 1.3, "滑轨(mm)": " ",
                            "W1": 15, "H1": 9.5, "ΦD": "6", "h": 4.5, "Φd": 3.5, "F": 40}  #
        self.TM15NL_dict = {"组装规格(mm)": " ", "H": 16, "W2": 8.5, "E": 3.7, "滑块尺寸(mm)": " ", "W": 32, "B": 25, "J": 25,
                            "T": 5.86,
                            "L": 59.4, "L1": 44, "Qxl": "M3*5", "Φ": 1.3, "滑轨(mm)": " ",
                            "W1": 15, "H1": 9.5, "ΦD": "6", "h": 4.5, "Φd": 3.5, "F": 40}  #




        self.TRH_series_dict = {"TM07NN":self.TM07NN_dict,"TM07NL":self.TM07NL_dict,"TM09NN":self.TM09NN_dict,"TM09NL":self.TM09NL_dict,
                                "TM12NN":self.TM12NN_dict,"TM12NL":self.TM12NL_dict,"TM15NN":self.TM15NN_dict,"TM15NL":self.TM15NL_dict
                                }



        self.series = self.TRH_series_dict
    def Create_shape(self,filename):
        pass
        try:
            filepath="./3Ddata/STP/"+filename+".stp"
            self.acompoud=read_step_file(filepath)
            return self.acompoud
        except:
            filepath = "./3Ddata/STP/" + filename + ".step"
            self.acompoud = read_step_file(filepath)
            return self.acompoud

    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")#导轨高度列表
        dict_combox = {"滑块型号": ["","07","09","12","15"]}#
        all_combox_list.append(["滑轨","微小型"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度","58～62HRC"])
        all_combox_list.append(["滑轨材料","S55C"])
        all_combox_list.append(["滑块材料","SCM420"])
        all_combox_list.append(["精度等级","普通"])
        all_combox_list.append(dict_combox)#导轨高度列表
        all_combox_list.append({"滑轨宽度": ["  ", "N:标准型"]})
        all_combox_list.append({"滑块长度": ["  ", "N:标准型 ", "L:长型"]})
        all_combox_list.append(["滑轨长度L(mm)", "600"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Liner_guide_TM_W(object):
        def __init__(self):
            pass
            self.TM09WN_dict = {"组装规格(mm)": " ", "H": 12, "W2": 6, "E": 3, "滑块尺寸(mm)": " ", "W": 30, "B": 21,
                                "J": 12,
                                "T": 4,
                                "L": 39.1, "L1": 26.7, "Qxl": "M3*3", "Φ": 1.3, "滑轨(mm)": " ",
                                "W1": 18, "H1": 7.3, "ΦD": "6", "h": 4.5, "Φd": 3.5, "F": 30}  #
            self.TM09WL_dict = {"组装规格(mm)": " ", "H": 12, "W2": 6, "E": 3, "滑块尺寸(mm)": " ", "W": 30, "B": 23,
                                "J": 24,
                                "T": 4,
                                "L": 50.7, "L1": 38.3, "Qxl": "M3*3", "Φ": 1.3, "滑轨(mm)": " ",
                                "W1": 18, "H1": 7.3, "ΦD": "6", "h": 4.5, "Φd": 3.5, "F": 30}  #

            self.TM12WN_dict = {"组装规格(mm)": " ", "H": 14, "W2": 8, "E": 3.5, "滑块尺寸(mm)": " ", "W": 40, "B": 28,
                                "J": 15,
                                "T": 4.5,
                                "L": 46.2, "L1": 29, "Qxl": "M3*3.5", "Φ": 1.3, "滑轨(mm)": " ",
                                "W1": 24, "H1": 8.5, "ΦD": "8", "h": 4.5, "Φd": 4.5, "F": 40}  #
            self.TM12WL_dict = {"组装规格(mm)": " ", "H": 14, "W2": 8, "E": 3.5, "滑块尺寸(mm)": " ", "W": 40, "B": 28,
                                "J": 28,
                                "T": 4.5,
                                "L": 61.2, "L1": 44, "Qxl": "M3*3.5", "Φ": 1.3, "滑轨(mm)": " ",
                                "W1": 24, "H1": 8.5, "ΦD": "8", "h": 4.5, "Φd": 4.5, "F": 40}  #
            self.TM15WN_dict = {"组装规格(mm)": " ", "H": 16, "W2": 9, "E": 3.6, "滑块尺寸(mm)": " ", "W": 60, "B": 45,
                                "J": 20,
                                "T": 4.8,
                                "L": 55.1, "L1": 38.5, "Qxl": "M4*4.5", "Φ": 1.3, "滑轨(mm)": " ",
                                "W1": 42, "H1": 9.5, "ΦD": "8", "h": 4.5, "Φd": 4.5, "F": 40,"P":23}  #
            self.TM15L_dict = {"组装规格(mm)": " ", "H": 16, "W2": 9, "E": 3.6, "滑块尺寸(mm)": " ", "W": 60, "B": 45,
                                "J": 35,
                                "T": 4.8,
                                "L": 74.4, "L1": 57.6, "Qxl": "M4*4.5", "Φ": 1.3, "滑轨(mm)": " ",
                                "W1": 42, "H1": 9.5, "ΦD": "8", "h": 4.5, "Φd": 4.5, "F": 40, "P": 23}  #


            self.TRH_series_dict = {"TM09WN":self.TM09WN_dict,"TM09WL":self.TM09WL_dict,"TM12WN":self.TM12WN_dict,"TM12WL":self.TM12WL_dict,
                                    "TM15WN":self.TM15WN_dict,"TM15L":self.TM15L_dict}

            self.series = self.TRH_series_dict

        def Create_shape(self, filename):
            pass
            try:
                filepath = "./3Ddata/STP/" + filename + ".stp"
                self.acompoud = read_step_file(filepath)
                return self.acompoud
            except:
                filepath = "./3Ddata/STP/" + filename + ".step"
                self.acompoud = read_step_file(filepath)
                return self.acompoud

        def Create_combox_list(self):
            combox_list = []  # 单个选型的列,
            all_combox_list = []  # 所有不同选项的列表
            for i in self.series.keys():
                combox_list.append(i)
            combox_list.insert(0, "  ")  # 导轨高度列表
            dict_combox = {"滑块型号": ["", "09", "12", "15"]}  #
            all_combox_list.append(["滑轨", "微小型"])
            all_combox_list.append(["组装高度", "-"])
            all_combox_list.append(["硬度", "58～62HRC"])
            all_combox_list.append(["滑轨材料", "S55C"])
            all_combox_list.append(["滑块材料", "SCM420"])
            all_combox_list.append(["精度等级", "普通"])
            all_combox_list.append(dict_combox)  # 导轨高度列表
            all_combox_list.append({"滑轨宽度": ["  ", "W:宽轨型"]})
            all_combox_list.append({"滑块长度": ["  ", "N:标准型 ", "L:长型"]})
            all_combox_list.append(["滑轨长度L(mm)", "600"])
            all_combox_list.append(["订货代码", ""])
            return all_combox_list

class Create_Ball_Srew_BK(object):#支撑座BK
        def __init__(self):
            pass
            self.BK10_dict = {"A":60,"B":46,"C":34,"C1":13,"C2":6,"E":30,"H1":32.5,"h":22,"H":39,
                              "L":25,"L1":5,"L2":29,"L3":5,"T":16,"P":5.5,"N":15,"M":"M3","X":6.6,"Y":11,"Z":5}  #

            self.BK12_dict = {"A": 60, "B": 46, "C": 35, "C1": 13, "C2": 6, "E": 30, "H1": 32.5, "h": 25, "H": 43,
                              "L":25,"L1":5,"L2":29,"L3":5,"T":19,"P":5.5,"N":15,"M":"M3","X":6.6,"Y":11,"Z":1.5}  #

            self.BK15_dict = {"A": 70, "B": 54, "C": 40, "C1": 15, "C2": 6, "E": 35, "H1": 38, "h": 28, "H": 48,
                              "L":27,"L1":6,"L2":32,"L3":6,"T":22,"P":5.5,"N":18,"M":"M3","X":6.6,"Y":11,"Z":6.5}  #

            self.BK17_dict = {"A": 86, "B": 68, "C": 50, "C1": 19, "C2": 8, "E": 43, "H1": 55, "h": 39, "H": 64,
                              "L":35,"L1":8,"L2":44,"L3":7,"T":24,"P":6.6,"N":28,"M":"M4","X":9,"Y":14,"Z":8.5}  #

            self.BK20_dict = {"A": 88, "B": 70, "C": 52, "C1": 19, "C2": 8, "E": 44, "H1": 50, "h": 34, "H": 60,
                              "L":35,"L1":8,"L2":43,"L3":8,"T":30,"P":6.6,"N":22,"M":"M4","X":9,"Y":14,"Z":8.5}  #

            self.BK25_dict = {"A": 106, "B": 85, "C": 64, "C1": 22, "C2": 10, "E": 53, "H1": 70, "h": 48, "H": 80,
                             "L": 42, "L1": 12, "L2": 54, "L3": 9, "T": 35, "P": 9, "N": 33, "M": "M5", "X": 11,
                             "Y": 17.5, "Z": 11}  #
            self.BK30_dict = {"A": 128, "B": 102, "C": 76, "C1": 23, "C2": 11, "E": 64, "H1": 78, "h": 51, "H":89,
                              "L": 45, "L1": 14, "L2": 61, "L3":9, "T": 40, "P":11, "N": 33, "M": "M6", "X": 14,
                              "Y": 20, "Z": 13}  #

            self.BK35_dict = {"A": 140, "B": 114, "C": 88, "C1": 26, "C2": 12, "E": 70, "H1": 79, "h": 52, "H": 96,
                              "L": 50, "L1": 14, "L2": 67, "L3": 12, "T": 50, "P": 11, "N": 35, "M": "M8", "X": 14,
                              "Y": 20, "Z": 13}  #

            self.BK40_dict = {"A": 160, "B": 130, "C": 100, "C1": 33, "C2": 14, "E": 80, "H1": 90, "h": 60, "H": 110,
                              "L": 61, "L1": 18, "L2": 76, "L3": 15, "T": 50, "P": 14, "N": 37, "M": "M8", "X": 18,
                              "Y": 26, "Z": 17.5}  #

            self.BK_series_dict = {"BK10":self.BK10_dict,"BK12":self.BK12_dict,"BK15":self.BK15_dict,"BK17":self.BK17_dict,
                                    "BK20":self.BK20_dict,"BK25":self.BK25_dict,"BK30":self.BK30_dict,"BK35":self.BK35_dict,
                                    "BK40":self.BK40_dict }
            self.series = self.BK_series_dict

        def Create_shape(self, filename):
            pass
            try:
                filepath = "./3Ddata/STP/" + filename + ".stp"
                self.acompoud = read_step_file(filepath)
                return self.acompoud
            except:
                filepath = "./3Ddata/STP/" + filename + ".step"
                self.acompoud = read_step_file(filepath)
                return self.acompoud

        def Create_combox_list(self):
            combox_list = []  # 单个选型的列,
            all_combox_list = []  # 所有不同选项的列表
            for i in self.series.keys():
                combox_list.append(i)
            combox_list.insert(0, "  ")  #
            dict_combox = {"轴径D1": ["", "10", "12", "15","17","20","25","30","35","40"]}  #
            all_combox_list.append(["材质", "S45C"])
            all_combox_list.append(["表面处理", "无电解镀镍"])
            all_combox_list.append(["轴承类型", "普通型"])
            all_combox_list.append(dict_combox)  # 轴径列表
            all_combox_list.append(["订货代码", ""])
            return all_combox_list


class Create_Ball_Srew_BF(object):#支撑座BF
    def __init__(self):
        pass
        self.BF10_dict = {"A": 60, "B": 46, "C": 34, "E": 30, "H1": 32.5, "h": 22, "H": 39,
                          "L": 20, "N": 15,"P":5.5, "M": "M3", "X": 6.6, "Y": 11,
                          "Z": 5,"C型扣环":"C8"}  #

        self.BF12_dict = {"A": 60, "B": 46, "C": 35,"E": 30, "H1": 32.5, "h": 25, "H": 43,
                          "L": 20, "N": 18, "P":5.5, "X": 6.6, "Y": 11,
                          "Z": 1.5,"C型扣环":"C10"}  #

        self.BF15_dict = {"A": 70, "B": 54, "C": 40,"E": 35, "H1": 38, "h": 28, "H": 48,
                          "L": 20, "N": 18,"P":5.5, "X": 6.6, "Y": 11,
                          "Z": 6.5,"C型扣环":"C15"}  #

        self.BF17_dict = {"A": 86, "B": 68, "C": 50,"E": 43, "H1": 55, "h": 39, "H": 64,
                          "L": 23, "P": 6.6, "N": 28, "X": 9, "Y": 14,
                          "Z": 8.5,"C型扣环":"C17"}  #

        self.BF20_dict = {"A": 88, "B": 70, "C": 52,"E": 44, "H1": 50, "h": 34, "H": 60,
                          "L": 26, "P": 6.6, "N": 22, "X": 9, "Y": 14,
                          "Z": 8.5,"C型扣环":"C20"}  #

        self.BF25_dict = {"A": 106, "B": 85, "C": 64, "E": 53, "H1": 70, "h": 48, "H": 80,
                          "L": 30, "P": 9, "N": 33, "X": 11,
                          "Y": 17.5, "Z": 11,"C型扣环":"C25"}  #

        self.BF30_dict = {"A": 128, "B": 102, "C": 76,"E": 64, "H1": 78, "h": 51, "H": 89,
                          "L": 32, "P": 11, "N": 33, "X": 14,
                          "Y": 20, "Z": 13,"C型扣环":"C30"}  #

        self.BF35_dict = {"A": 140, "B": 114, "C": 88,"E": 70, "H1": 79, "h": 52, "H": 96,
                          "L": 32,"P": 11, "N": 35, "X": 14,
                          "Y": 20, "Z": 13,"C型扣环":"C35"}  #

        self.BF40_dict = {"A": 160, "B": 130, "C": 100,"E": 80, "H1": 90, "h": 60, "H": 110,
                          "L": 37,"P": 14, "N": 37,"X": 18,
                          "Y": 26, "Z": 17.5,"C型扣环":"C35"}  #

        self.BF_series_dict = {"BF8": self.BF10_dict, "BF10": self.BF12_dict, "BF15": self.BF10_dict,
                                "BF17": self.BF17_dict,
                                "BF20": self.BF20_dict, "BF25": self.BF25_dict, "BF30": self.BF30_dict,
                                "BF35": self.BF35_dict,
                                "BF40": self.BF40_dict}
        self.series = self.BF_series_dict

    def Create_shape(self, filename):
        pass
        try:
            filepath = "./3Ddata/STP/" + filename + ".stp"
            self.acompoud = read_step_file(filepath)
            return self.acompoud
        except:
            filepath = "./3Ddata/STP/" + filename + ".step"
            self.acompoud = read_step_file(filepath)
            return self.acompoud

    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  #
        dict_combox = {"轴径D1": ["", "8", "10", "15", "17", "20", "25", "30", "35", "40"]}  #
        all_combox_list.append(["材质", "S45C"])
        all_combox_list.append(["表面处理", "无电解镀镍"])
        all_combox_list.append(["轴承类型", "普通型"])
        all_combox_list.append(dict_combox)  # 轴径列表
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Ball_Srew_EK(object):#固定座EK
        def __init__(self):
            pass
            self.EK6_dict = {"A":42,"B":30,"C":18,"E":21,"H1":20,"h":13,"H":25,
                              "L":20,"L1":5.5,"L2":22,"L3":3.5,"M":"M3","X":5.5,"Y":9.5,"Z":11,"T":12}  #

            self.EK8_dict = {"A": 52, "B": 38, "C": 25, "E": 26, "H1": 26, "h": 17, "H": 32,
                             "L": 23, "L1": 7, "L2": 26, "L3": 4, "M": "M3", "X": 6.6, "Y": 11, "Z": 12,
                             "T": 14}  #

            self.EK10_dict = {"A": 70, "B": 52, "C": 36, "E": 35, "H1":24, "h": 25, "H": 43,
                             "L": 24, "L1": 6, "L2": 29.5, "L3": 6, "M": "M3", "X": 9, "Y": "-", "Z": "-",
                             "T": 16}  #

            self.EK12_dict = {"A": 70, "B": 52, "C": 36, "E": 35, "H1": 24, "h": 25, "H": 43,
                              "L": 24, "L1": 6, "L2": 29.5, "L3": 6, "M": "M3", "X": 9, "Y": "-", "Z": "-",
                              "T": 19}  #

            self.EK15_dict = {"A": 80, "B": 60, "C": 41, "E": 40, "H1": 25, "h": 30, "H": 49,
                              "L": 25, "L1": 6, "L2": 36, "L3": 5, "M": "M3", "X": 11, "Y": "-", "Z": "-",
                              "T": 22}  #

            self.EK20_dict = {"A": 95, "B": 75, "C": 56, "E": 47.5, "H1": 25, "h": 30,"C1":"-","C2":"-", "H": 58,
                              "L": 42, "L1": 10, "L2": 50, "L3": 10, "M": "M4", "X": 11, "Y": "-", "Z": "-",
                              "T": 30}  #

            self.EK25_dict = {"A": 105, "B": 85, "C": 66, "E": 52.5, "H1": 25, "h": 30, "C1": "9", "C2": "30", "H": 68,
                              "L": 48, "L1": 13, "L2": 60, "L3": 14, "M": "M5", "X": 11, "Y": "-", "Z": "-",
                              "T": 35}  #


            self.EK_series_dict = {"EK6":self.EK6_dict,"EK8":self.EK8_dict,"EK10":self.EK10_dict,"EK12":self.EK12_dict,
                                    "EK15":self.EK15_dict,"EK20":self.EK20_dict,"EK25":self.EK25_dict}

            self.series = self.EK_series_dict

        def Create_shape(self, filename):
            pass
            try:
                filepath = "./3Ddata/STP/" + filename + ".stp"
                self.acompoud = read_step_file(filepath)
                return self.acompoud
            except:
                filepath = "./3Ddata/STP/" + filename + ".step"
                self.acompoud = read_step_file(filepath)
                return self.acompoud

        def Create_combox_list(self):
            combox_list = []  # 单个选型的列,
            all_combox_list = []  # 所有不同选项的列表
            for i in self.series.keys():
                combox_list.append(i)
            combox_list.insert(0, "  ")  #
            dict_combox = {"轴径D1": ["", "6", "8", "10","12","15","20","25"]}  #
            all_combox_list.append(["材质", "S45C"])
            all_combox_list.append(["表面处理", "无电解镀镍"])
            all_combox_list.append(["轴承类型", "普通型"])
            all_combox_list.append(dict_combox)  # 轴径列表
            all_combox_list.append(["订货代码", ""])
            return all_combox_list

class Create_Ball_Srew_EF(object):#支撑座EF
        def __init__(self):
            pass
            self.EF8_dict = {"A":52,"B":38,"C":25,"E":26,"H1":26,"h":17,"H":32,
                              "L":14,"X":6.6,"Y":11,"Z":12,"C型扣环":"C6","轴承型号":"606ZZ"}  #

            self.EF10_dict = {"A": 70, "B": 52, "C": 36, "E": 35, "H1": 24, "h": 25, "H": 43,
                             "L": 20, "X": 9, "Y": "-", "Z": "-", "C型扣环": "C8", "轴承型号": "608ZZ"}  #

            self.EF12_dict = {"A": 70, "B": 52, "C": 36, "E": 35, "H1": 24, "h": 25, "H": 43,
                              "L": 20, "X": 9, "Y": "-", "Z": "-", "C型扣环": "C10", "轴承型号": "6002ZZ"}  #

            self.EF15_dict = {"A": 80, "B": 60, "C": 41, "E": 40, "H1": 25, "h": 30, "H": 49,
                              "L": 20, "X": 9, "Y": "-", "Z": "-", "C型扣环": "C15", "轴承型号": "6002ZZ"}  #

            self.EF20_dict = {"A": 96, "B": 75, "C": 56, "E": 47.5, "H1": 25, "h": 30, "H": 58,
                              "L": 26, "X": 11, "Y": "-", "Z": "-", "C型扣环": "C20", "轴承型号": "6204ZZ"}  #

            self.EF25_dict = {"A": 105, "B": 85, "C": 66, "E": 52.5, "H1": 25, "h": 35, "H": 68,
                              "L": 30, "X": "-", "Y": "11", "Z": "-", "C型扣环": "C25", "轴承型号": "6205ZZ"}  #



            self.EF_series_dict = {"EF8":self.EF8_dict,"EF10":self.EF10_dict,"EF12":self.EF12_dict,"EF15":self.EF15_dict,
                                    "EF20":self.EF20_dict,"EF25":self.EF25_dict}

            self.series = self.EF_series_dict

        def Create_shape(self, filename):
            pass
            try:
                filepath = "./3Ddata/STP/" + filename + ".stp"
                self.acompoud = read_step_file(filepath)
                return self.acompoud
            except:
                filepath = "./3Ddata/STP/" + filename + ".step"
                self.acompoud = read_step_file(filepath)
                return self.acompoud

        def Create_combox_list(self):
            combox_list = []  # 单个选型的列,
            all_combox_list = []  # 所有不同选项的列表
            for i in self.series.keys():
                combox_list.append(i)
            combox_list.insert(0, "  ")  #
            dict_combox = {"轴径D1": ["",  "8", "10","15","20","25"]}  #
            all_combox_list.append(["材质", "S45C"])
            all_combox_list.append(["表面处理", "无电解镀镍"])
            all_combox_list.append(["轴承类型", "普通型"])
            all_combox_list.append(dict_combox)  # 轴径列表
            all_combox_list.append(["订货代码", ""])
            return all_combox_list

class Create_Ball_Srew_FK(object):#固定座FK
        def __init__(self):
            pass
            self.FK8_dict = {"A":43,"F":14,"L":23,"E":26,"H":9,
                              "PCD":35,"M":"M3","L1":7,"T1":4,"L2":8,"T2":5,"X":3.4,"Y":6.5,"Z":4,"T":14}  #

            self.FK10_dict = {"A": 52, "F": 17, "L": 27, "E": 29.5,"Dg6":34, "H": 10,
                             "PCD": 42, "M": "M3","B":42, "L1": 7.5, "T1": 5, "L2": 8.5, "T2": 6, "X": 4.5, "Y": 8, "Z": 4,
                             "T": 16}  #
            self.FK12_dict = {"A": 54, "F": 17, "L": 27, "E": 29.5, "Dg6": 36, "H": 10,
                              "PCD": 44, "M": "M3", "B": 44, "L1": 7.5, "T1": 5, "L2": 8.5, "T2": 6, "X": 4.5, "Y": 8,
                              "Z": 4,
                              "T": 19}  #
            self.FK15_dict = {"A": 63, "F": 17, "L": 32, "E": 36, "Dg6": 40, "H": 15,
                              "PCD": 50, "M": "M3", "B": 52, "L1": 10, "T1": 6, "L2": 12, "T2": 8, "X": 5.5, "Y": 9.5,
                              "Z": 6,
                              "T": 22}  #
            self.FK20_dict = {"A": 85, "F": 30, "L": 52, "E": 50, "Dg6": 57, "H": 22,
                              "PCD": 70, "M": "M4", "B": 68, "L1": 8, "T1": 10, "L2": 12, "T2": 14, "X": 6.6, "Y": 11,
                              "Z": 10,
                              "T": 30}  #
            self.FK25_dict = {"A": 98, "F": 30, "L": 57, "E": 60, "Dg6": 63, "H": 27,
                              "PCD": 80, "M": "M5", "B": 79, "L1": 13, "T1": 10, "L2": 20, "T2": 17, "X": 9, "Y": 15,
                              "Z": 13,
                              "T": 35}  #
            self.FK30_dict = {"A": 117, "F": 32, "L": 62, "E": 61, "Dg6": 75, "H": 30,
                              "PCD": 95, "M": "M6", "B": 93, "L1": 14, "T1": 12, "L2": 17, "T2": 18, "X": 11, "Y": 17.5,
                              "Z": 15,
                              "T": 40}  #



            self.FK_series_dict = {"FK8":self.FK8_dict,"FK10":self.FK10_dict,"FK12":self.FK12_dict,"FK15":self.FK15_dict,
                                    "FK20":self.FK20_dict,"FK25":self.FK25_dict,"FK30":self.FK30_dict}

            self.series = self.FK_series_dict

        def Create_shape(self, filename):
            pass
            try:
                filepath = "./3Ddata/STP/" + filename + ".stp"
                self.acompoud = read_step_file(filepath)
                return self.acompoud
            except:
                filepath = "./3Ddata/STP/" + filename + ".step"
                self.acompoud = read_step_file(filepath)
                return self.acompoud

        def Create_combox_list(self):
            combox_list = []  # 单个选型的列,
            all_combox_list = []  # 所有不同选项的列表
            for i in self.series.keys():
                combox_list.append(i)
            combox_list.insert(0, "  ")  #
            dict_combox = {"轴径D1": ["", "8", "10", "12","15","20","25","30"]}  #
            all_combox_list.append(["材质", "S45C"])
            all_combox_list.append(["表面处理", "无电解镀镍"])
            all_combox_list.append(["轴承类型", "普通型"])
            all_combox_list.append(dict_combox)  #轴径列表
            all_combox_list.append(["订货代码", ""])
            return all_combox_list

class Create_Ball_Srew_FF(object):#支撑座FF
        def __init__(self):
            pass
            self.FF6_dict = {"L":10,"H":6,"F":4,"Dg6":22,"A":36,"PCD":28,"B":28,"X":3.4,"Y":6.5,"Z":4,"C型扣环":"C6","轴承型号":"606ZZ"}

            self.FF10_dict = {"L": 12, "H": 7, "F": 5, "Dg6": 28, "A": 43, "PCD": 35, "B": 35, "X": 3.4, "Y": 6.5,
                             "Z": 4, "C型扣环": "C8", "轴承型号": "608ZZ"}

            self.FF12_dict = {"L": 15, "H": 7, "F": 8, "Dg6": 34, "A": 52, "PCD": 42, "B": 42, "X": 4.5, "Y": 8,
                              "Z": 4, "C型扣环": "C10", "轴承型号": "6000ZZ"}

            self.FF15_dict = {"L": 17, "H": 9, "F": 8, "Dg6": 40, "A": 63, "PCD": 50, "B": 52, "X": 5.5, "Y": 9.5,
                              "Z": 5.5, "C型扣环": "C15", "轴承型号": "6002ZZ"}

            self.FF20_dict = {"L": 20, "H": 11, "F": 9 ,"Dg6": 57, "A": 85, "PCD": 70, "B": 68, "X": 6.6, "Y": 11,
                              "Z": 6.5, "C型扣环": "C20", "轴承型号": "6204ZZ"}

            self.FF25_dict = {"L": 24, "H": 14, "F": 10, "Dg6": 63, "A": 98, "PCD": 80, "B": 79 ,"X": 9, "Y": 14,
                              "Z": 8.5, "C型扣环": "C25", "轴承型号": "6205ZZ"}

            self.FF30_dict = {"L": 27, "H": 18, "F": 9, "Dg6": 75, "A": 117, "PCD": 95, "B": 93, "X": 11, "Y": 17.5,
                              "Z": 11, "C型扣环": "C30", "轴承型号": "6206ZZ"}






            self.FF_series_dict = {"FF6":self.FF6_dict,"FF8":self.FF10_dict,"FF10":self.FF12_dict,"FF15":self.FF15_dict,
                                    "FF20":self.FF20_dict,"FF25":self.FF25_dict,"FF30_dict":self.FF30_dict}

            self.series = self.FF_series_dict

        def Create_shape(self, filename):
            pass
            try:
                filepath = "./3Ddata/STP/" + filename + ".stp"
                self.acompoud = read_step_file(filepath)
                return self.acompoud
            except:
                filepath = "./3Ddata/STP/" + filename + ".step"
                self.acompoud = read_step_file(filepath)
                return self.acompoud

        def Create_combox_list(self):
            combox_list = []  # 单个选型的列,
            all_combox_list = []  # 所有不同选项的列表
            for i in self.series.keys():
                combox_list.append(i)
            combox_list.insert(0, "  ")  #
            dict_combox = {"轴径D1": ["", "6", "8", "10","15","20","25","30"]}  #
            all_combox_list.append(["材质", "S45C"])
            all_combox_list.append(["表面处理", "无电解镀镍"])
            all_combox_list.append(["轴承类型", "普通型"])
            all_combox_list.append(dict_combox)  # 轴径列表
            all_combox_list.append(["订货代码", ""])
            return all_combox_list

class Create_Liner_guide_MGN(object):
    def __init__(self):
        pass
        self.MGN5C_dict = {"组件尺寸(mm)":" ","H":6,"H1":1.5,"N":3.5,
                           "滑块尺寸(mm)":" ","W":12,"B":8,"B1":2,"C":"-","L1":9.6,"L":16,"G":"-","Gn":0.8,"MXl":"M2X1.5",
                           "H2":1,
                           "滑轨(mm)":" ","WR":5,"HR":3.6,"D":"3.6","h":0.8,"d":2.4,"P15":15,"E":5,
                           "滑轨螺栓尺寸":"M2X6","基本动额定负载":"0.54",
                           "基本静额定负载":"0.84",
                           "容许静力矩":"","MR":"2","MP":"1.3","MY":"1.3"}  #

        self.MGN7C_dict = {"组件尺寸(mm)": " ", "H": 8, "H1": 1.5, "N": 5,
                           "滑块尺寸(mm)": " ", "W": 17, "B": 12, "B1": 2.5, "C": "8", "L1": 13.5, "L": 22.5, "G": "-", "Gn": "Φ1.2",
                           "M*l": "M2X2.5","H2":1.5,
                           "滑轨(mm)": " ", "WR": 7, "HR": 4.8, "D": "4.2", "h": 2.3, "d": 2.4, "P": 15, "E": 5,
                           "滑轨螺栓尺寸": "M2X6", "基本动额定负载": "0.98",
                           "基本静额定负载": "1.24",
                           "容许静力矩": "", "MR": "4.7", "MP": "2.84", "MY": "2.84"}  #

        self.MGN7H_dict = {"组件尺寸(mm)": " ", "H": 8, "H1": 1.5, "N": 5,
                           "滑块尺寸(mm)": " ", "W": 17, "B": 12, "B1": 2.5, "C": "13", "L1": 21.8, "L": 30.8, "G": "-",
                           "Gn": "Φ1.2",
                           "M*l": "M2X2.5","H2":1.5,
                           "滑轨(mm)": " ", "WR": 7, "HR": 4.8, "D": "4.2", "h": 2.3, "d": 2.4, "P": 15, "E": 5,
                           "滑轨螺栓尺寸": "M2X6", "基本动额定负载": "1.37",
                           "基本静额定负载": "1.96",
                           "容许静力矩": "", "MR": "7.64", "MP": "4.80", "MY": "4.80"}  #

        self.MGN9C_dict = {"组件尺寸(mm)": " ", "H": 10, "H1": 2, "N": 5.5,
                           "滑块尺寸(mm)": " ", "W": 20, "B": 15, "B1": 2.5, "C": "10", "L1": 18.9, "L": 28.9, "G": "-",
                           "Gn": "Φ1.4",
                           "M*l": "M3X3","H2":1.8,
                           "滑轨(mm)": " ", "WR": 9, "HR": 6.5, "D": "6", "h": 3.5, "d": 3.5, "P": 20, "E":7.5,
                           "滑轨螺栓尺寸": "M3X8", "基本动额定负载": "1.86",
                           "基本静额定负载": "2.55",
                           "容许静力矩": "", "MR": "11.76", "MP": "7.35", "MY": "7.35"}  #

        self.MGN9H_dict = {"组件尺寸(mm)": " ", "H": 10, "H1": 2, "N": 5.5,
                           "滑块尺寸(mm)": " ", "W": 20, "B": 15, "B1": 2.5, "C": "16", "L1": 29.9, "L": 39.9, "G": "-",
                           "Gn": "Φ1.4",
                           "M*l": "M3X3", "H2": 1.8,
                           "滑轨(mm)": " ", "WR": 9, "HR": 6.5, "D": "6", "h": 3.5, "d": 3.5, "P": 20, "E": 7.5,
                           "滑轨螺栓尺寸": "M3X8", "基本动额定负载": "2.55",
                           "基本静额定负载": "4.02",
                           "容许静力矩": "", "MR": "19.6", "MP": "18.62", "MY": "18.62"}  #

        self.MGN12C_dict = {"组件尺寸(mm)": " ", "H": 13, "H1": 3, "N": 7.5,
                           "滑块尺寸(mm)": " ", "W": 27, "B": 20, "B1": 3.5, "C": "15", "L1": 21.7, "L": 34.7, "G": "-",
                           "Gn": "Φ2",
                           "M*l": "M3X3.5", "H2": 2.5,
                           "滑轨(mm)": " ", "WR": 12, "HR": 8, "D": "6", "h": 4.5, "d": 3.5, "P15": 25, "E": 10,
                           "滑轨螺栓尺寸": "M3X8", "基本动额定负载": "2.84",
                           "基本静额定负载": "3.92",
                           "容许静力矩": "", "MR": "25.48", "MP": "13.72", "MY": "13.72"}  #

        self.MGN12H_dict = {"组件尺寸(mm)": " ", "H": 13, "H1": 3, "N": 7.5,
                            "滑块尺寸(mm)": " ", "W": 27, "B": 20, "B1": 3.5, "C": "20", "L1": 32.4, "L": 45.4, "G": "-",
                            "Gn": "Φ2",
                            "M*l": "M3X3.5", "H2": 2.5,
                            "滑轨(mm)": " ", "WR": 12, "HR": 8, "D": "6", "h": 4.5, "d": 3.5, "P": 25, "E": 10,
                            "滑轨螺栓尺寸": "M3X8", "基本动额定负载": "3.72",
                            "基本静额定负载": "5.88",
                            "容许静力矩": "", "MR": "38.2", "MP": "36.26", "MY": "36.26"}  #

        self.MGN15C_dict = {"组件尺寸(mm)": " ", "H": 16, "H1": 4, "N": 8.5,
                            "滑块尺寸(mm)": " ", "W": 32, "B": 25, "B1": 3.5, "C": "20", "L1": 26.7, "L": 42.1, "G": "4.5",
                            "Gn": "M3",
                            "M*l": "M3X4", "H2": 3,
                            "滑轨(mm)": " ", "WR": 15, "HR":10, "D": "6", "h": 4.5, "d": 3.5, "P": 40, "E": 15,
                            "滑轨螺栓尺寸": "M3X10", "基本动额定负载": "4.61",
                            "基本静额定负载": "5.59",
                            "容许静力矩": "", "MR": "45.08", "MP": "21.56", "MY": "21.56"}  #

        self.MGN15H_dict = {"组件尺寸(mm)": " ", "H": 16, "H1": 4, "N": 8.5,
                           "滑块尺寸(mm)": " ", "W": 32, "B": 25, "B1": 3.5, "C": "25", "L1": 43.4, "L": 58.5, "G": "4.5",
                           "Gn": "M3",
                           "M*l": "M3X4", "H2": 3,
                           "滑轨(mm)": " ", "WR": 15, "HR": 10, "D": "6", "h": 4.5, "d": 3.5, "P": 40, "E": 15,
                           "滑轨螺栓尺寸": "M3*10", "基本动额定负载": "6.37",
                           "基本静额定负载": "9.11",
                           "容许静力矩": "", "MR": "73.5", "MP": "57.82", "MY": "57.82"}  #



        self.MGN_series_dict = {"MGN5C":self.MGN5C_dict,"MGN7C":self.MGN7C_dict,"MGN7H_dict":self.MGN7H_dict,
                                "MGN9C_dict":self.MGN9C_dict,"MGN9H_dict":self.MGN9H_dict,"MGN12C":self.MGN12C_dict,
                                "MGN12H":self.MGN12H_dict,"MGN15C":self.MGN15C_dict,"MGN15H_dict":self.MGN15H_dict
                                }



        self.series = self.MGN_series_dict
    def Create_shape(self,filename):
        pass
        try:
            filepath="./3Ddata/STP/"+filename+".stp"
            self.acompoud=read_step_file(filepath)
            return self.acompoud
        except:
            filepath = "./3Ddata/STP/" + filename + ".step"
            self.acompoud = read_step_file(filepath)
            return self.acompoud

    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")#导轨高度列表
        dict_combox = {"滑块型号": ["","5","7","9","12","15"]}#
        all_combox_list.append(["滑轨","微小型"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度","58～62HRC"])
        all_combox_list.append(["滑轨材料","S55C"])
        all_combox_list.append(["滑块材料","SCM420"])
        all_combox_list.append(["精度等级","普通"])
        all_combox_list.append(dict_combox)#导轨高度列表
        all_combox_list.append({"负荷型式": ["  ", "C:标准型 ", "H:长型"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list


class Create_Liner_guide_MGW(object):
    def __init__(self):
        pass
        self.MGW5C_dict = {"组件尺寸(mm)":" ","H":6.5,"H1":1.5,"N":3.5,
                           "滑块尺寸(mm)":" ","W":17,"B":13,"B1":2,"C":"-","L1":14.1,"L":20.5,"G":"-","Gn":"Φ0.8","MXl":"M2.5X1.5",
                           "H2":1,
                           "滑轨(mm)":" ","WR":10,"WB":"-","HR":4,"D":"5.5","h":1.6,"d":3,"P":20,"E":5,
                           "滑轨螺栓尺寸":"M2.5X7","基本动额定负载":"0.68",
                           "基本静额定负载":"1.18",
                           "容许静力矩":"","MR":"5.5","MP":"2.7","MY":"2.7"}  #

        self.MGW7C_dict = {"组件尺寸(mm)": " ", "H": 9, "H1": 1.9, "N": 5.5,
                           "滑块尺寸(mm)": " ", "W": 25, "B": 19, "B1": 3, "C": "10", "L1": 21, "L": 31.2, "G": "-",
                           "Gn": "Φ1.2", "MXl": "M3X3",
                           "H2": 1.85,
                           "滑轨(mm)": " ", "WR": 14, "WB": "-", "HR": 5.2, "D": "6", "h": 3.2, "d": 3.5, "P": 30, "E": 10,
                           "滑轨螺栓尺寸": "M3X6", "基本动额定负载": "1.37",
                           "基本静额定负载": "2.06",
                           "容许静力矩": "", "MR": "15.70", "MP": "7.14", "MY": "7.14"}  #

        self.MGW7H_dict = {"组件尺寸(mm)": " ", "H": 9, "H1": 1.9, "N": 5.5,
                           "滑块尺寸(mm)": " ", "W": 25, "B": 19, "B1": 3, "C": "19", "L1": 30.8, "L": 41, "G": "-",
                           "Gn": "Φ1.2", "MXl": "M3X3",
                           "H2": 1.85,
                           "滑轨(mm)": " ", "WR": 14, "WB": "-", "HR": 5.2, "D": "6", "h": 3.2, "d": 3.5, "P": 30,
                           "E": 10,
                           "滑轨螺栓尺寸": "M3X6", "基本动额定负载": "1.77",
                           "基本静额定负载": "3.14",
                           "容许静力矩": "", "MR": "23.45", "MP": "15.53", "MY": "15.53"}  #

        self.MGW9C_dict = {"组件尺寸(mm)": " ", "H": 12, "H1": 2.9, "N": 6,
                           "滑块尺寸(mm)": " ", "W": 30, "B": 21, "B1": 4.5, "C": "12", "L1": 27.5, "L": 39.3, "G": "-",
                           "Gn": "Φ1.2", "MXl": "M3X3",
                           "H2": 2.4,
                           "滑轨(mm)": " ", "WR": 18, "WB": "-", "HR": 7, "D": "6", "h": 4.5, "d": 3.5, "P": 30,
                           "E": 10,
                           "滑轨螺栓尺寸": "M3X8", "基本动额定负载": "2.75",
                           "基本静额定负载": "4.12",
                           "容许静力矩": "", "MR": "40.12", "MP": "18.96", "MY": "18.96"}  #

        self.MGW9H_dict = {"组件尺寸(mm)": " ", "H": 12, "H1": 2.9, "N": 6,
                           "滑块尺寸(mm)": " ", "W": 30, "B": 23, "B1": 3.5, "C": "24", "L1": 38.5, "L": 50.7, "G": "-",
                           "Gn": "Φ1.2", "MXl": "M3X3",
                           "H2": 2.4,
                           "滑轨(mm)": " ", "WR": 18, "WB": "-", "HR": 7, "D": "6", "h": 4.5, "d": 3.5, "P": 30,
                           "E": 10,
                           "滑轨螺栓尺寸": "M3X8", "基本动额定负载": "3.43",
                           "基本静额定负载": "5.89",
                           "容许静力矩": "", "MR": "54.54", "MP": "34", "MY": "34"}  #

        self.MGW12C_dict = {"组件尺寸(mm)": " ", "H": 14, "H1": 3.4, "N": 8,
                           "滑块尺寸(mm)": " ", "W": 40, "B": 28, "B1": 6, "C": "15", "L1": 31.3, "L": 46.1, "G": "-",
                           "Gn": "Φ1.2", "MXl": "M3X3.6",
                           "H2": 2.8,
                           "滑轨(mm)": " ", "WR": 24, "WB": "-", "HR": 8.5, "D": "8", "h": 4.5, "d": 4.5, "P": 40,
                           "E": 15,
                           "滑轨螺栓尺寸": "M4X8", "基本动额定负载": "3.92",
                           "基本静额定负载": "5.59",
                           "容许静力矩": "", "MR": "70.34", "MP": "27.8", "MY": "27.8"}  #

        self.MGW12H_dict = {"组件尺寸(mm)": " ", "H": 14, "H1": 3.4, "N": 8,
                            "滑块尺寸(mm)": " ", "W": 40, "B": 28, "B1": 6, "C": "28", "L1": 45.6, "L": 60.4, "G": "-",
                            "Gn": "Φ1.2", "MXl": "M3X3.6",
                            "H2": 2.8,
                            "滑轨(mm)": " ", "WR": 24, "WB": "-", "HR": 8.5, "D": "8", "h": 4.5, "d": 4.5, "P": 40,
                            "E": 15,
                            "滑轨螺栓尺寸": "M4X8", "基本动额定负载": "5.10",
                            "基本静额定负载": "8.24",
                            "容许静力矩": "", "MR": "102.7", "MP": "57.37", "MY": "57.37"}  #

        self.MGW15C_dict = {"组件尺寸(mm)": " ", "H": 16, "H1": 3.4, "N": 9,
                            "滑块尺寸(mm)": " ", "W": 60, "B": 45, "B1": 7.5, "C": "20", "L1": 38, "L": 54.8, "G": "5.2",
                            "Gn": "M3", "MXl": "M4X4.2",
                            "H2": 3.2,
                            "滑轨(mm)": " ", "WR": 42, "WB": "23", "HR": 9.5, "D": "8", "h": 4.5, "d": 4.5, "P": 40,
                            "E": 15,
                            "滑轨螺栓尺寸": "M4X10", "基本动额定负载": "6.77",
                            "基本静额定负载": "9.22",
                            "容许静力矩": "", "MR": "199.34", "MP": "56.66", "MY": "56.66"}  #

        self.MGW15H_dict = {"组件尺寸(mm)": " ", "H": 16, "H1": 3.4, "N": 9,
                            "滑块尺寸(mm)": " ", "W": 60, "B": 45, "B1": 7.5, "C": "35", "L1": 57, "L": 73.8, "G": "5.2",
                            "Gn": "M3", "MXl": "M4X4.2",
                            "H2": 3.2,
                            "滑轨(mm)": " ", "WR": 42, "WB": "23", "HR": 9.5, "D": "8", "h": 4.5, "d": 4.5, "P": 40,
                            "E": 15,
                            "滑轨螺栓尺寸": "M4X10", "基本动额定负载": "8.93",
                            "基本静额定负载": "13.38",
                            "容许静力矩": "", "MR": "299.01", "MP": "122.60", "MY": "122.60"}  #



        self.MGW_series_dict = {"MGW5C":self.MGW5C_dict,"MGW7C":self.MGW7C_dict,"MGW7H":self.MGW7H_dict,"MGW9C":self.MGW9C_dict,
                                "MGW9H":self.MGW9H_dict,"MGW12C":self.MGW12C_dict,"MGW12H":self.MGW12H_dict,"MGW15C":self.MGW15C_dict,
                                "MGW15H":self.MGW15H_dict
                                }
        self.series = self.MGW_series_dict

    def Create_shape(self, filename):
        pass
        try:
            filepath = "./3Ddata/STP/" + filename + ".stp"
            self.acompoud = read_step_file(filepath)
            return self.acompoud
            #print(filepath)

        except:
            filepath = "./3Ddata/STP/" + filename + ".step"
            self.acompoud = read_step_file(filepath)
            return self.acompoud

    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["", "5", "7", "9", "12", "15"]}  #
        all_combox_list.append(["滑轨", "微小型"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"负荷型式": ["  ", "C:标准型 ", "H:长型"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Liner_guide_EGH(object):
    def __init__(self):
        pass
        self.EGH15SA_dict = {"组件尺寸(mm)":" ","H":24,"H1":4.5,"N":9.5,
                           "滑块尺寸(mm)":" ","W":34,"B":26,"B1":4,"C":"-","L1":23.1,"L":40.1,"K1":14.8,"K2":3.5,"G":"5.7",
                            "MXl":"M4X6","T":6,"H2":5.5,"H3":6,
                           "滑轨(mm)":" ","WR":15,"HR":12.5,"D":"6","h":4.5,"d":3.5,"P":60,"E":20,
                           "滑轨螺栓尺寸":"M3X16","基本动额定负载":"5.35",
                           "基本静额定负载":"9.40",
                           "容许静力矩":"","MR":"0.08","MP":"0.04","MY":"0.04",
                            "重量":"","滑块（kg）":0.09,"滑轨":1.25}  #

        self.EGH15CA_dict = {"组件尺寸(mm)": " ", "H": 24, "H1": 4.5, "N": 9.5,
                             "滑块尺寸(mm)": " ", "W": 34, "B": 26, "B1": 4, "C": "26", "L1": 39.8, "L": 56.8, "K1": 10.15,
                             "K2": 3.5, "G": "5.7",
                             "MXl": "M4X6", "T": 6, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 15, "HR": 12.6, "D": "6", "h": 4.5, "d": 3.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M3X16", "基本动额定负载": "7.83",
                             "基本静额定负载": "16.19",
                             "容许静力矩": "", "MR": "0.13", "MP": "0.10", "MY": "0.10",
                             "重量": "", "滑块（kg）": 0.15, "滑轨": 1.25}  #

        self.EGH20SA_dict = {"组件尺寸(mm)": " ", "H": 28, "H1": 6, "N": 11,
                             "滑块尺寸(mm)": " ", "W": 42, "B": 32, "B1": 5, "C": "-", "L1": 29, "L": 50, "K1": 18.75,
                             "K2": 4.15, "G": "12",
                             "MXl": "M5X7", "T": 7.5, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR":15.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "7.23",
                             "基本静额定负载": "12.74",
                             "容许静力矩": "", "MR": "0.13", "MP": "0.06", "MY": "0.06",
                             "重量": "", "滑块（kg）": 0.15, "滑轨": 2.08}  #

        self.EGH20CA_dict = {"组件尺寸(mm)": " ", "H": 28, "H1": 6, "N": 11,
                             "滑块尺寸(mm)": " ", "W": 42, "B": 32, "B1": 5, "C": "32", "L1": 48.1, "L": 69.1, "K1": 12.3,
                             "K2": 4.15, "G": "12",
                             "MXl": "M5X7", "T": 7.5, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 15.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "10.31",
                             "基本静额定负载": "21.13",
                             "容许静力矩": "", "MR": "0.22", "MP": "0.16", "MY": "0.16",
                             "重量": "", "滑块（kg）": 0.24, "滑轨": 2.08}  #

        self.EGH25SA_dict = {"组件尺寸(mm)": " ", "H": 33, "H1": 7, "N": 12.5,
                             "滑块尺寸(mm)": " ", "W": 48, "B": 35, "B1": 6.5, "C": "-", "L1": 35.5, "L": 59.1, "K1": 21.9,
                            "K2": 4.55, "G": "12",
                             "MXl": "M6X9", "T": 8, "H2": 8, "H3": 8,
                             "滑轨(mm)": " ", "WR": 23, "HR": 18, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "11.40",
                             "基本静额定负载": "19.50",
                             "容许静力矩": "", "MR": "0.23", "MP": "0.12", "MY": "0.12",
                             "重量": "", "滑块（kg）": 0.25, "滑轨": 2.67}  #

        self.EGH25CA_dict = {"组件尺寸(mm)": " ", "H": 33, "H1": 7, "N": 12.5,
                             "滑块尺寸(mm)": " ", "W": 48, "B": 35, "B1": 6.5, "C": "35", "L1": 59, "L": 82.6, "K1": 16.15,
                             "K2": 4.55, "G": "12",
                             "MXl": "M6X9", "T": 8, "H2": 8, "H3": 8,
                             "滑轨(mm)": " ", "WR": 23, "HR": 18, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "16.27",
                             "基本静额定负载": "32.40",
                             "容许静力矩": "", "MR": "0.38", "MP": "0.32", "MY": "0.32",
                             "重量": "", "滑块（kg）": 0.41, "滑轨": 2.67}  #

        self.EGH30SA_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 10, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 60, "B": 40, "B1": 10, "C": "-", "L1": 41.5, "L": 69.5, "K1": 26.75,
                             "K2": 6, "G": "12",
                             "MXl": "M8X12", "T": 9, "H2": 8, "H3": 9,
                             "滑轨(mm)": " ", "WR": 28, "HR": 23, "D": "11", "h": 9, "d": 7, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M6X25", "基本动额定负载": "16.42",
                             "基本静额定负载": "28.10",
                             "容许静力矩": "", "MR": "0.40", "MP": "0.21", "MY": "0.21",
                             "重量": "", "滑块（kg）": 0.45, "滑轨": 4.35}  #

        self.EGH30CA_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 10, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 60, "B": 40, "B1": 10, "C": "40", "L1": 70.1, "L": 98.1, "K1": 21.05,
                             "K2": 6, "G": "12",
                             "MXl": "M8X12", "T": 9, "H2": 8, "H3": 9,
                             "滑轨(mm)": " ", "WR": 28, "HR": 23, "D": "11", "h": 9, "d": 7, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M6X25", "基本动额定负载": "23.70",
                             "基本静额定负载": "47.46",
                             "容许静力矩": "", "MR": "0.68", "MP": "0.55", "MY": "0.55",
                             "重量": "", "滑块（kg）": 0.76, "滑轨": 4.35}  #

        self.EGH35SA_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 11, "N": 18,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 50, "B1": 10, "C": "-", "L1": 45, "L": 75, "K1": 28.5,
                             "K2": 7, "G": "12",
                             "MXl": "M8X12", "T": 10, "H2": 8.5, "H3": 8.5,
                             "滑轨(mm)": " ", "WR": 34, "HR": 27.5, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "22.66",
                             "基本静额定负载": "37.38",
                             "容许静力矩": "", "MR": "0.56", "MP": "0.31", "MY": "0.31",
                             "重量": "", "滑块（kg）": 0.66, "滑轨": 6.14}  #

        self.EGH35CA_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 11, "N": 18,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 50, "B1": 10, "C": "50", "L1": 78, "L": 108, "K1": 20,
                             "K2": 7, "G": "12",
                             "MXl": "M8X12", "T": 10, "H2": 8.5, "H3": 8.5,
                             "滑轨(mm)": " ", "WR": 34, "HR": 27.5, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "33.35",
                             "基本静额定负载": "64.84",
                             "容许静力矩": "", "MR": "0.98", "MP": "0.69", "MY": "0.69",
                             "重量": "", "滑块（kg）": 1.13, "滑轨": 6.14}  #




        self.EGH_series_dict = {"EGH15SA":self.EGH15SA_dict,"EGH15CA_dict":self.EGH15CA_dict,"EGH20SA":self.EGH20SA_dict,
                                "EGH20CA":self.EGH20CA_dict,"EGH25SA":self.EGH25SA_dict,"EGH25CA":self.EGH25CA_dict,"EGH30SA":self.EGH30SA_dict,
                                "EGH30CA":self.EGH30CA_dict,"EGH35SA":self.EGH35SA_dict,"EGH35CA":self.EGH35CA_dict
                                }
        self.series = self.EGH_series_dict

    def Create_shape(self, filename):
        pass
        try:
            filepath = "./3Ddata/STP/" + filename + ".stp"
            self.acompoud = read_step_file(filepath)
            return self.acompoud
            #print(filepath)

        except:
            filepath = "./3Ddata/STP/" + filename + ".step"
            self.acompoud = read_step_file(filepath)
            return self.acompoud

    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["", "15", "20", "25", "30", "35"]}  #
        all_combox_list.append(["滑轨", "低组装"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["H:四方型"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷 ", "S:中负荷"]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "B:下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Liner_guide_EGW(Create_Liner_guide_EGH):
    pass
    def __init__(self):
        pass
        self.EGW15SA_dict = {"组件尺寸(mm)":" ","H":24,"H1":4.5,"N":18.5,
                           "滑块尺寸(mm)":" ","W":52,"B":41,"B1":5.5,"C":"-","L1":23.1,"L":40.1,"K1":14.8,"K2":3.5,"G":"5.7",
                            "M":"M5","T":5,"T1":7,"H2":5.5,"H3":6,
                           "滑轨(mm)":" ","WR":15,"HR":12.5,"D":"6","h":4.5,"d":3.5,"P":60,"E":20,
                           "滑轨螺栓尺寸":"M3X16","基本动额定负载":"5.35",
                           "基本静额定负载":"9.40",
                           "容许静力矩":"","MR":"0.08","MP":"0.04","MY":"0.04",
                            "重量":"","滑块（kg）":0.12,"滑轨":1.25}  #

        self.EGW15CA_dict = {"组件尺寸(mm)": " ", "H": 24, "H1": 4.5, "N": 18.5,
                             "滑块尺寸(mm)": " ", "W": 52, "B": 41, "B1": 5.5, "C": "26", "L1": 39.8, "L": 56.8, "K1": 10.15,
                             "K2": 3.5, "G": "5.7",
                             "M": "M5", "T": 5, "T1": 7, "H2": 5.5, "H3": 6,
                             "滑轨(mm)": " ", "WR": 15, "HR": 12.5, "D": "6", "h": 4.5, "d": 3.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M3X16", "基本动额定负载": "7.83",
                             "基本静额定负载": "16.19",
                             "容许静力矩": "", "MR": "0.13", "MP": "0.10", "MY": "0.10",
                             "重量": "", "滑块（kg）": 0.21, "滑轨": 1.25}  #

        self.EGW20SA_dict = {"组件尺寸(mm)": " ", "H": 28, "H1": 6, "N": 19.5,
                             "滑块尺寸(mm)": " ", "W": 59, "B": 49, "B1": 5, "C": "-", "L1": 29, "L": 50, "K1": 18.75,
                             "K2": 4.15, "G": "12",
                             "M": "M6", "T": 7,"T1": 9, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 15.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "7.23",
                             "基本静额定负载": "12.74",
                             "容许静力矩": "", "MR": "0.13", "MP": "0.06", "MY": "0.06",
                             "重量": "", "滑块（kg）": 0.19, "滑轨": 2.08}  #

        self.EGW20CA_dict = {"组件尺寸(mm)": " ", "H": 28, "H1": 6, "N": 19.5,
                             "滑块尺寸(mm)": " ", "W": 59, "B": 49, "B1": 5, "C": "32", "L1": 48.1, "L": 69.1, "K1": 12.3,
                             "K2": 4.15, "G": "12",
                             "M": "M6", "T": 7, "T1": 9, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 15.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "10.31",
                             "基本静额定负载": "21.13",
                             "容许静力矩": "", "MR": "0.22", "MP": "0.16", "MY": "0.16",
                             "重量": "", "滑块（kg）": 0.32, "滑轨": 2.08}  #

        self.EGW25SA_dict = {"组件尺寸(mm)": " ", "H": 33, "H1": 7, "N": 25,
                             "滑块尺寸(mm)": " ", "W": 73, "B": 60, "B1": 6.5, "C": "-", "L1": 35.5, "L": 59.1, "K1": 21.9,
                             "K2": 4.55, "G": "12",
                             "M": "M8", "T": 7.5,"T1": 10, "H2": 8, "H3": 8,
                             "滑轨(mm)": " ", "WR": 23, "HR": 18, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "11.40",
                             "基本静额定负载": "19.50",
                             "容许静力矩": "", "MR": "0.23", "MP": "0.12", "MY": "0.12",
                             "重量": "", "滑块（kg）": 0.35, "滑轨": 2.67}  #

        self.EGW25CA_dict = {"组件尺寸(mm)": " ", "H": 33, "H1": 7, "N": 25,
                             "滑块尺寸(mm)": " ", "W": 73, "B": 60, "B1": 6.5, "C": "35", "L1": 59, "L": 82.6, "K1": 16.15,
                             "K2": 4.55, "G": "12",
                             "M": "M8", "T": 7.5, "T1": 10, "H2": 8, "H3": 8,
                             "滑轨(mm)": " ", "WR": 23, "HR": 18, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "16.27",
                             "基本静额定负载": "32.40",
                             "容许静力矩": "", "MR": "0.38", "MP": "0.32", "MY": "0.32",
                             "重量": "", "滑块（kg）": 0.59, "滑轨": 2.67}  #

        self.EGW30SA_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 10, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "-", "L1": 41.5, "L": 69.5, "K1": 26.75,
                             "K2": 6, "G": "12",
                             "M": "M10", "T": 7,"T1": 10, "H2": 8, "H3": 9,
                             "滑轨(mm)": " ", "WR": 28, "HR": 23, "D": "11", "h": 9, "d": 7, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M6X25", "基本动额定负载": "16.42",
                             "基本静额定负载": "28.10",
                             "容许静力矩": "", "MR": "0.40", "MP": "0.21", "MY": "0.21",
                             "重量": "", "滑块（kg）": 0.62, "滑轨": 4.35}  #

        self.EGW30CA_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 10, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "40", "L1": 70.1, "L": 98.1, "K1": 21.05,
                             "K2": 6, "G": "12",
                             "M": "M10", "T": 7, "T1": 10, "H2": 8, "H3": 9,
                             "滑轨(mm)": " ", "WR": 28, "HR": 23, "D": "11", "h": 9, "d": 7, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M6X25", "基本动额定负载": "23.70",
                             "基本静额定负载": "47.46",
                             "容许静力矩": "", "MR": "0.68", "MP": "0.55", "MY": "0.55",
                             "重量": "", "滑块（kg）": 1.04, "滑轨": 4.35}  #

        self.EGW35SA_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 11, "N": 33,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 82, "B1": 9, "C": "-", "L1": 45, "L": 75, "K1": 28.5,
                             "K2": 7, "G": "12",
                             "M": "M10", "T": 10,"T1": 13, "H2": 8.5, "H3": 8.5,
                             "滑轨(mm)": " ", "WR": 34, "HR": 27.5, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "22.66",
                             "基本静额定负载": "37.38",
                             "容许静力矩": "", "MR": "0.56", "MP": "0.31", "MY": "0.31",
                             "重量": "", "滑块（kg）": 0.84, "滑轨": 6.14}  #

        self.EGW35CA_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 11, "N": 33,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 82, "B1": 9, "C": "50", "L1": 78, "L": 108, "K1": 20,
                             "K2": 7, "G": "12",
                             "M": "M10", "T": 10, "T1": 13, "H2": 8.5, "H3": 8.5,
                             "滑轨(mm)": " ", "WR": 34, "HR": 27.5, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "33.35",
                             "基本静额定负载": "64.84",
                             "容许静力矩": "", "MR": "0.98", "MP": "0.69", "MY": "0.69",
                             "重量": "", "滑块（kg）": 1.45, "滑轨": 6.14}  #


        self.EGW_series_dict = {"EGW15SA":self.EGW15SA_dict,"EGW15CA":self.EGW15CA_dict,"EGW20SA":self.EGW20SA_dict,
                                "EGW20CA":self.EGW20CA_dict,"EGW25SA":self.EGW25SA_dict,"EGW25CA":self.EGW25CA_dict,
                                "EGW30SA":self.EGW30SA_dict,"EGW30CA":self.EGW30CA_dict,"EGW35SA":self.EGW35SA_dict,
                                "EGW35CA":self.EGW35CA_dict
                                }
        self.series = self.EGW_series_dict
    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["", "15", "20", "25", "30", "35"]}  #
        all_combox_list.append(["滑轨", "低组装"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["W:法兰型"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷 ", "S:中负荷"]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "B:下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Liner_guide_HGH(Create_Liner_guide_EGH):
    pass
    def __init__(self):
        pass
        self.HGH15CA_dict = {"组件尺寸(mm)":" ","H":28,"H1":4.3,"N":9.5,
                           "滑块尺寸(mm)":" ","W":34,"B":26,"B1":4,"C":"26","L1":39.4,"L":61.4,"K1":10,"K2":4.85,"G":"5.3",
                            "MXL":"M4X5","T":6,"H2":7.95,"H3":7.7,
                           "滑轨(mm)":" ","WR":15,"HR":15,"D":"7.5","h":5.3,"d":4.5,"P":60,"E":20,
                           "滑轨螺栓尺寸":"M4X16","基本动额定负载":"11.38",
                           "基本静额定负载":"16.97",
                           "容许静力矩":"","MR":"0.12","MP":"0.10","MY":"0.10",
                            "重量":"","滑块（kg）":0.18,"滑轨":1.45}  #

        self.HGH20CA_dict = {"组件尺寸(mm)": " ", "H": 30, "H1": 4.6, "N": 12,
                             "滑块尺寸(mm)": " ", "W": 44, "B": 32, "B1": 6, "C": "36", "L1": 50.5, "L": 77.5, "K1": 12.25,
                             "K2": 6, "G": "12",
                             "MXL": "M5X6", "T": 8, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 17.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "17.75",
                             "基本静额定负载": "27.76",
                             "容许静力矩": "", "MR": "0.27", "MP": "0.20", "MY": "0.20",
                             "重量": "", "滑块（kg）": 0.30, "滑轨": 2.21}  #

        self.HGH20HA_dict = {"组件尺寸(mm)": " ", "H": 30, "H1": 4.6, "N": 12,
                             "滑块尺寸(mm)": " ", "W": 44, "B": 32, "B1": 6, "C": "50", "L1": 65.2, "L": 92.2, "K1": 12.6,
                             "K2": 6, "G": "12",
                             "MXL": "M5X6", "T": 8, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 17.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "21.18",
                             "基本静额定负载": "35.90",
                             "容许静力矩": "", "MR": "0.35", "MP": "0.35", "MY": "0.35",
                             "重量": "", "滑块（kg）": 0.39, "滑轨": 2.21}  #

        self.HGH25CA_dict = {"组件尺寸(mm)": " ", "H": 40, "H1": 5.5, "N": 12.5,
                             "滑块尺寸(mm)": " ", "W": 48, "B": 35, "B1": 6.5, "C": "35", "L1": 58, "L": 84, "K1": 16.8,
                             "K2": 6, "G": "12",
                             "MXL": "M6X8", "T": 8, "H2": 10, "H3": 9,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "26.78",
                             "基本静额定负载": "36.49",
                             "容许静力矩": "", "MR": "0.42", "MP": "0.33", "MY": "0.33",
                             "重量": "", "滑块（kg）": 0.51, "滑轨": 3.21}  #

        self.HGH25HA_dict = {"组件尺寸(mm)": " ", "H": 40, "H1": 5.5, "N": 12.5,
                             "滑块尺寸(mm)": " ", "W": 48, "B": 35, "B1": 6.5, "C": "50", "L1": 78.6, "L": 104.6, "K1": 19.6,
                             "K2": 6, "G": "12",
                             "MXL": "M6X8", "T": 8, "H2": 10, "H3": 9,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "32.75",
                             "基本静额定负载": "49.44",
                             "容许静力矩": "", "MR": "0.56", "MP": "0.57", "MY": "0.57",
                             "重量": "", "滑块（kg）": 0.69, "滑轨": 3.21}  #

        self.HGH30CA_dict = {"组件尺寸(mm)": " ", "H": 45, "H1": 6, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 60, "B": 40, "B1": 10, "C": "40", "L1": 70, "L": 97.4, "K1": 20.25,
                             "K2": 6, "G": "12",
                             "MXL": "M8X10", "T": 8.5, "H2": 9.5, "H3": 13.8,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "38.74",
                             "基本静额定负载": "52.19",
                             "容许静力矩": "", "MR": "0.66", "MP": "0.53", "MY": "0.53",
                             "重量": "", "滑块（kg）": 0.88, "滑轨": 4.47}  #

        self.HGH30HA_dict = {"组件尺寸(mm)": " ", "H": 45, "H1": 6, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 60, "B": 40, "B1": 10, "C": "60", "L1": 93, "L": 120.4, "K1": 21.75,
                             "K2": 6, "G": "12",
                             "MXL": "M8X10", "T": 8.5, "H2": 9.5, "H3": 13.8,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "47.27",
                             "基本静额定负载": "69.16",
                             "容许静力矩": "", "MR": "0.88", "MP": "0.92", "MY": "0.92",
                             "重量": "", "滑块（kg）": 1.16, "滑轨": 4.47}  #

        self.HGH35CA_dict = {"组件尺寸(mm)": " ", "H": 55, "H1": 7.5, "N": 18,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 50, "B1": 10, "C": "50", "L1": 80, "L": 112.4, "K1": 20.6,
                             "K2": 7, "G": "12",
                             "MXL": "M8X12", "T": 10.2, "H2": 16, "H3": 19.6,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "49.52",
                             "基本静额定负载": "69.16",
                             "容许静力矩": "", "MR": "1.16", "MP": "0.81", "MY": "0.81",
                             "重量": "", "滑块（kg）": 1.45, "滑轨": 6.3}  #

        self.HGH35HA_dict = {"组件尺寸(mm)": " ", "H": 55, "H1": 7.5, "N": 18,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 50, "B1": 10, "C": "72", "L1": 105.8, "L": 138.2, "K1": 22.5,
                             "K2": 7, "G": "12",
                             "MXL": "M8X12", "T": 10.2, "H2": 16, "H3": 19.6,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "60.21",
                             "基本静额定负载": "91.63",
                             "容许静力矩": "", "MR": "1.54", "MP": "1.4", "MY": "1.4",
                             "重量": "", "滑块（kg）": 1.92, "滑轨": 6.3}  #

        self.HGH45CA_dict = {"组件尺寸(mm)": " ", "H": 70, "H1": 9.5, "N": 20.5,
                             "滑块尺寸(mm)": " ", "W": 86, "B": 60, "B1": 13, "C": "60", "L1": 97, "L": 139.4, "K1": 23,
                             "K2": 10, "G": "12.9",
                             "MXL": "M10X17", "T": 16, "H2": 18.5, "H3": 30.5,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "77.57",
                             "基本静额定负载": "102.71",
                             "容许静力矩": "", "MR": "1.98", "MP": "1.55", "MY": "1.55",
                             "重量": "", "滑块（kg）": 2.73, "滑轨": 10.41}  #

        self.HGH45HA_dict = {"组件尺寸(mm)": " ", "H": 70, "H1": 9.5, "N": 20.5,
                             "滑块尺寸(mm)": " ", "W": 86, "B": 60, "B1": 13, "C": "80", "L1": 128.8, "L": 171.2, "K1": 28.9,
                             "K2": 10, "G": "12.9",
                             "MXL": "M10X17", "T": 16, "H2": 18.5, "H3": 30.5,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "94.54",
                             "基本静额定负载": "136.46",
                             "容许静力矩": "", "MR": "2.63", "MP": "2.68", "MY": "2.68",
                             "重量": "", "滑块（kg）": 3.61, "滑轨": 10.41}  #

        self.HGH55CA_dict = {"组件尺寸(mm)": " ", "H": 80, "H1": 13, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 75, "B1": 12.5, "C": "75", "L1": 117.7, "L": 166.7, "K1": 27.35,
                             "K2": 11, "G": "12.9",
                             "MXL": "M12X18", "T": 17.5, "H2": 22, "H3": 29,
                             "滑轨(mm)": " ", "WR": 53, "HR": 44, "D": "23", "h": 20, "d": 16, "P": 120, "E": 30,
                             "滑轨螺栓尺寸": "M14X45", "基本动额定负载": "114.44",
                             "基本静额定负载": "148.33",
                             "容许静力矩": "", "MR": "3.69", "MP": "2.64", "MY": "2.64",
                             "重量": "", "滑块（kg）": 4.17, "滑轨": 15.08}  #

        self.HGH55HA_dict = {"组件尺寸(mm)": " ", "H": 80, "H1": 13, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 75, "B1": 12.5, "C": "95", "L1": 155.8, "L": 204.8,
                             "K1": 36.4,
                             "K2": 11, "G": "12.9",
                             "MXL": "M12X18", "T": 17.5, "H2": 22, "H3": 29,
                             "滑轨(mm)": " ", "WR": 53, "HR": 44, "D": "23", "h": 20, "d": 16, "P": 120, "E": 30,
                             "滑轨螺栓尺寸": "M14X45", "基本动额定负载": "139.35",
                             "基本静额定负载": "196.20",
                             "容许静力矩": "", "MR": "4.88", "MP": "4.57", "MY": "4.57",
                             "重量": "", "滑块（kg）": 5.49, "滑轨": 15.08}  #

        self.HGH65CA_dict = {"组件尺寸(mm)": " ", "H": 90, "H1": 15, "N": 31.5,
                             "滑块尺寸(mm)": " ", "W": 126, "B": 76, "B1": 25, "C": "70", "L1": 144.2, "L": 200.2,
                             "K1": 43.1,
                             "K2": 14, "G": "12.9",
                             "MXL": "M16X20", "T": 25, "H2": 15, "H3": 15,
                             "滑轨(mm)": " ", "WR": 63, "HR": 53, "D": "26", "h": 22, "d": 18, "P": 150, "E": 35,
                             "滑轨螺栓尺寸": "M16X50", "基本动额定负载": "163.63",
                             "基本静额定负载": "215.33",
                             "容许静力矩": "", "MR": "6.65", "MP": "4.27", "MY": "4.27",
                             "重量": "", "滑块（kg）": 7.0, "滑轨": 21.18}  #

        self.HGH65HA_dict = {"组件尺寸(mm)": " ", "H": 90, "H1": 15, "N": 31.5,
                             "滑块尺寸(mm)": " ", "W": 126, "B": 76, "B1": 25, "C": "120", "L1": 203.6, "L": 259.6,
                             "K1": 47.8,
                             "K2": 14, "G": "12.9",
                             "MXL": "M16X20", "T": 25, "H2": 15, "H3": 15,
                             "滑轨(mm)": " ", "WR": 63, "HR": 53, "D": "26", "h": 22, "d": 18, "P": 150, "E": 35,
                             "滑轨螺栓尺寸": "M16X50", "基本动额定负载": "208.36",
                             "基本静额定负载": "303.13",
                             "容许静力矩": "", "MR": "9.38", "MP": "7.38", "MY": "7.38",
                             "重量": "", "滑块（kg）": 9.82, "滑轨": 21.18}  #

        

        self.HGH_series_dict = {"HGH15CA":self.HGH15CA_dict,"HGH20CA":self.HGH20CA_dict,"HGH20HA":self.HGH20HA_dict,
                                "HGH25CA":self.HGH25CA_dict,"HGH25HA":self.HGH25HA_dict,"HGH30CA":self.HGH30CA_dict,
                                "HGH30HA":self.HGH30HA_dict,"HGH35CA":self.HGH35CA_dict,"HGH35HA":self.HGH35HA_dict,
                                "HGH45CA":self.HGH45CA_dict,"HGH45HA":self.HGH45HA_dict,"HGH55CA":self.HGH55CA_dict,
                                "HGH55HA":self.HGH55HA_dict,"HGH65CA":self.HGH65CA_dict,"HGH65HA":self.HGH65HA_dict

                                }
        self.series = self.HGH_series_dict
    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["", "15", "20", "25", "30", "35","45","55","65"]}  #
        all_combox_list.append(["滑轨", "高组装"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["H:四方型"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷 ", "H:超重负荷"]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "B:下锁式", "C:上或下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list


class Create_Liner_guide_HGW(Create_Liner_guide_EGH):
    pass
    def __init__(self):
        pass
        self.HGW15CA_dict = {"组件尺寸(mm)": " ", "H": 24, "H1": 4.3, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 47, "B": 38, "B1": 4.5, "C": "30", "L1": 39.4, "L": 61.4, "K1": 8,
                             "K2": 4.85, "G": "5.3",
                             "M": "M5", "T": 6,"T1": 8.9, "H2": 3.95, "H3": 3.7,
                             "滑轨(mm)": " ", "WR": 15, "HR": 15, "D": "7.5", "h": 5.3, "d": 4.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M4X16", "基本动额定负载": "11.38",
                             "基本静额定负载": "16.97",
                             "容许静力矩": "", "MR": "0.12", "MP": "0.10", "MY": "0.10",
                             "重量": "", "滑块（kg）": 0.17, "滑轨": 1.45}  #

        self.HGW20CA_dict = {"组件尺寸(mm)": " ", "H": 30, "H1": 4.6, "N": 21.5,
                             "滑块尺寸(mm)": " ", "W": 63, "B": 53, "B1": 5, "C": "40", "L1": 50.5, "L": 77.5, "K1": 10.25,
                             "K2": 6, "G": "12",
                             "M": "M6", "T": 8,"T1": 10, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 17.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "17.75",
                             "基本静额定负载": "27.66",
                             "容许静力矩": "", "MR": "0.27", "MP": "0.20", "MY": "0.20",
                             "重量": "", "滑块（kg）": 0.40, "滑轨": 2.21}  #

        self.HGW20HA_dict = {"组件尺寸(mm)": " ", "H": 30, "H1": 4.6, "N": 21.5,
                             "滑块尺寸(mm)": " ", "W": 63, "B": 53, "B1": 5, "C": "40", "L1": 65.2, "L": 92.2, "K1": 17.6,
                             "K2": 6, "G": "12",
                             "M": "M6", "T": 8,"T1": 10, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 17.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "21.18",
                             "基本静额定负载": "35.9",
                             "容许静力矩": "", "MR": "0.35", "MP": "0.35", "MY": "0.35",
                             "重量": "", "滑块（kg）": 0.52, "滑轨": 2.21}  #

        self.HGW25CA_dict = {"组件尺寸(mm)": " ", "H": 36, "H1": 5.5, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 57, "B1": 6.5, "C": "45", "L1": 58, "L": 84, "K1": 11.8,
                             "K2": 6, "G": "12",
                             "M": "M8", "T": 8,"T1": 14, "H2": 6, "H3": 5,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "26.78",
                             "基本静额定负载": "36.49",
                             "容许静力矩": "", "MR": "0.42", "MP": "0.33", "MY": "0.33",
                             "重量": "", "滑块（kg）": 0.59, "滑轨": 3.21}  #

        self.HGW25HA_dict = {"组件尺寸(mm)": " ", "H": 36, "H1": 5.5, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 57, "B1": 6.5, "C": "45", "L1": 78.6, "L": 104.6, "K1": 22.1,
                             "K2": 6, "G": "12",
                             "M": "M8", "T": 8,"T1": 14, "H2": 6, "H3": 5,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "32.75",
                             "基本静额定负载": "49.44",
                             "容许静力矩": "", "MR": "0.56", "MP": "0.57", "MY": "0.57",
                             "重量": "", "滑块（kg）": 0.80, "滑轨": 3.21}  #

        self.HGW30CA_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 6, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "52", "L1": 70, "L": 97.4, "K1": 14.25,
                             "K2": 6, "G": "12",
                             "M": "M10", "T": 8.5,"T1": 16, "H2": 6.5, "H3": 10.8,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "38.74",
                             "基本静额定负载": "52.19",
                             "容许静力矩": "", "MR": "0.66", "MP": "0.53", "MY": "0.53",
                             "重量": "", "滑块（kg）": 1.09, "滑轨": 4.47}  #

        self.HGW30HA_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 6, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "52", "L1": 93, "L": 120.4, "K1": 25.75,
                             "K2": 6, "G": "12",
                             "M": "M10", "T": 8.5,"T1": 16, "H2": 6.5, "H3": 10.8,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "47.27",
                             "基本静额定负载": "69.16",
                             "容许静力矩": "", "MR": "0.88", "MP": "0.92", "MY": "0.92",
                             "重量": "", "滑块（kg）": 1.44, "滑轨": 4.47}  #

        self.HGW35CA_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 7.5, "N": 33,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 82, "B1": 9, "C": "62", "L1": 80, "L": 112.4, "K1": 14.6,
                             "K2": 7, "G": "12",
                             "M": "M8", "T": 10.1,"T1": 18, "H2": 9, "H3": 12.6,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "49.52",
                             "基本静额定负载": "69.16",
                             "容许静力矩": "", "MR": "1.16", "MP": "0.81", "MY": "0.81",
                             "重量": "", "滑块（kg）": 1.56, "滑轨": 6.3}  #

        self.HGW35HA_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 7.5, "N": 33,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 82, "B1": 9, "C": "62", "L1": 105.8, "L": 138.2, "K1": 27.5,
                             "K2": 7, "G": "12",
                             "M": "M8", "T": 10.1,"T1": 18, "H2": 9, "H3": 12.6,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "60.21",
                             "基本静额定负载": "91.63",
                             "容许静力矩": "", "MR": "1.54", "MP": "1.40", "MY": "1.40",
                             "重量": "", "滑块（kg）": 2.06, "滑轨": 6.3}  #

        self.HGW45CA_dict = {"组件尺寸(mm)": " ", "H": 60, "H1": 9.5, "N": 37.5,
                             "滑块尺寸(mm)": " ", "W": 120, "B": 100, "B1": 10, "C": "80", "L1": 97, "L": 139.4, "K1": 13,
                             "K2": 10, "G": "12.9",
                             "M": "M12", "T": 15.1,"T1": 22, "H2": 8.5, "H3": 20.5,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "77.57",
                             "基本静额定负载": "102.71",
                             "容许静力矩": "", "MR": "1.98", "MP": "1.55", "MY": "1.55",
                             "重量": "", "滑块（kg）": 2.73, "滑轨": 10.41}  #

        self.HGW45HA_dict = {"组件尺寸(mm)": " ", "H": 60, "H1": 9.5, "N": 37.5,
                             "滑块尺寸(mm)": " ", "W": 120, "B": 100, "B1": 10, "C": "80", "L1": 128.8, "L": 171.2, "K1": 28.9,
                             "K2": 10, "G": "12.9",
                             "M": "M12", "T": 15.1,"T1": 22, "H2": 8.5, "H3": 20.5,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "94.54",
                             "基本静额定负载": "136.46",
                             "容许静力矩": "", "MR": "2.63", "MP": "2.68", "MY": "2.68",
                             "重量": "", "滑块（kg）": 3.69, "滑轨": 10.41}  #

        self.HGW55CA_dict = {"组件尺寸(mm)": " ", "H": 70, "H1": 13, "N": 43.5,
                             "滑块尺寸(mm)": " ", "W": 140, "B": 116, "B1": 12, "C": "95", "L1": 117.7, "L": 166.7,
                             "K1": 17.35,
                             "K2": 11, "G": "12.9",
                             "M": "M14", "T": 17.5,"T1": 26.5, "H2": 12, "H3": 19,
                             "滑轨(mm)": " ", "WR": 53, "HR": 44, "D": "23", "h": 20, "d": 16, "P": 120, "E": 30,
                             "滑轨螺栓尺寸": "M14X45", "基本动额定负载": "114.44",
                             "基本静额定负载": "148.33",
                             "容许静力矩": "", "MR": "3.69", "MP": "2.64", "MY": "2.64",
                             "重量": "", "滑块（kg）": 4.52, "滑轨": 15.08}  #

        self.HGH55HA_dict = {"组件尺寸(mm)": " ", "H": 70, "H1": 13, "N": 43.5,
                             "滑块尺寸(mm)": " ", "W": 140, "B": 116, "B1": 12, "C": "95", "L1": 155.8, "L": 204.8,
                             "K1": 36.4,
                             "K2": 11, "G": "12.9",
                             "M": "M14", "T": 17.5,"T1": 26.5, "H2": 12, "H3": 19,
                             "滑轨(mm)": " ", "WR": 53, "HR": 44, "D": "23", "h": 20, "d": 16, "P": 120, "E": 30,
                             "滑轨螺栓尺寸": "M14X45", "基本动额定负载": "139.35",
                             "基本静额定负载": "196.20",
                             "容许静力矩": "", "MR": "4.88", "MP": "4.57", "MY": "4.57",
                             "重量": "", "滑块（kg）": 5.96, "滑轨": 15.08}  #

        self.HGW65CA_dict = {"组件尺寸(mm)": " ", "H": 90, "H1": 15, "N": 53.5,
                             "滑块尺寸(mm)": " ", "W": 170, "B": 142, "B1": 14, "C": "110", "L1": 144.2, "L": 200.2,
                             "K1": 23.1,
                             "K2": 14, "G": "12.9",
                             "M": "M16", "T": 25,"T": 37.5, "H2": 15, "H3": 15,
                             "滑轨(mm)": " ", "WR": 63, "HR": 53, "D": "26", "h": 22, "d": 18, "P": 150, "E": 35,
                             "滑轨螺栓尺寸": "M16X50", "基本动额定负载": "163.63",
                             "基本静额定负载": "215.33",
                             "容许静力矩": "", "MR": "6.65", "MP": "4.27", "MY": "4.27",
                             "重量": "", "滑块（kg）": 9.17, "滑轨": 21.18}  #

        self.HGW65HA_dict = {"组件尺寸(mm)": " ", "H": 90, "H1": 15, "N": 53.5,
                             "滑块尺寸(mm)": " ", "W": 170, "B": 142, "B1": 14, "C": "110", "L1": 203.6, "L": 259.6,
                             "K1": 52.8,
                             "K2": 14, "G": "12.9",
                             "M": "M16", "T": 25,"T": 37.5, "H2": 15, "H3": 15,
                             "滑轨(mm)": " ", "WR": 63, "HR": 53, "D": "26", "h": 22, "d": 18, "P": 150, "E": 35,
                             "滑轨螺栓尺寸": "M16X50", "基本动额定负载": "208.36",
                             "基本静额定负载": "303.13",
                             "容许静力矩": "", "MR": "9.38", "MP": "7.38", "MY": "7.38",
                             "重量": "", "滑块（kg）": 12.89, "滑轨": 21.18}  #

        self.HGW_series_dict = {"HGW15CA": self.HGW15CA_dict,"HGW20CA":self.HGW20CA_dict,"HGW20HA":self.HGW20HA_dict,
                                "HGW25CA":self.HGW25CA_dict,"HGW25HA":self.HGW25HA_dict,"HGW30CA":self.HGW30CA_dict,
                                "HGW30HA":self.HGW30HA_dict,"HGW35CA":self.HGW35CA_dict,"HGW35HA":self.HGW35HA_dict,
                                "HGW45CA":self.HGW45CA_dict,"HGW45HA":self.HGW45HA_dict,"HGW55CA":self.HGW55CA_dict,
                                "HGH55HA":self.HGH55HA_dict,"HGW65CA":self.HGW65CA_dict,"HGW65HA":self.HGW65HA_dict
                                }

        self.series = self.HGW_series_dict
    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["", "15", "20", "25", "30", "35", "45", "55", "65"]}  #
        all_combox_list.append(["滑轨", "高组装"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["W:法兰型"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷 ", "H:超重负荷"]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "B:下锁式", "C:上或下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Liner_guide_HGL(Create_Liner_guide_EGH):
    pass
    def __init__(self):
        pass
        self.HGL15CA_dict = {"组件尺寸(mm)": " ", "H": 24, "H1": 4.3, "N": 9.5,
                             "滑块尺寸(mm)": " ", "W": 34, "B": 26, "B1": 4, "C": "26", "L1": 39.4, "L": 61.4, "K1": 10,
                             "K2": 4.85, "G": "5.3",
                             "MXL": "M4X4", "T": 6,"H2": 3.95, "H3": 3.7,
                             "滑轨(mm)": " ", "WR": 15, "HR": 15, "D": "7.5", "h": 5.3, "d": 4.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M4X16", "基本动额定负载": "11.38",
                             "基本静额定负载": "16.97",
                             "容许静力矩": "", "MR": "0.12", "MP": "0.10", "MY": "0.10",
                             "重量": "", "滑块（kg）": 0.17, "滑轨": 1.45}  #


        self.HGL25CA_dict = {"组件尺寸(mm)": " ", "H": 36, "H1": 5.5, "N": 12.5,
                             "滑块尺寸(mm)": " ", "W": 48, "B": 35, "B1": 6.5, "C": "35", "L1": 58, "L": 84, "K1": 15.7,
                             "K2": 6, "G": "12",
                             "MXL": "M6X6", "T": 8,"H2": 5, "H3": 5,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "26.48",
                             "基本静额定负载": "36.49",
                             "容许静力矩": "", "MR": "0.42", "MP": "0.33", "MY": "0.33",
                             "重量": "", "滑块（kg）": 0.42, "滑轨": 3.21}  #

        self.HGL25HA_dict = {"组件尺寸(mm)": " ", "H": 36, "H1": 5.5, "N": 12.5,
                             "滑块尺寸(mm)": " ", "W": 48, "B": 35, "B1": 6.5, "C": "50", "L1": 78.6, "L": 104.6, "K1": 18.5,
                             "K2": 6, "G": "12",
                             "MXL": "M6X6", "T": 8,"H2": 5, "H3": 5,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "32.75",
                             "基本静额定负载": "49.44",
                             "容许静力矩": "", "MR": "0.56", "MP": "0.57", "MY": "0.57",
                             "重量": "", "滑块（kg）": 0.57, "滑轨": 3.21}  #

        self.HGL30CA_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 6, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 60, "B": 40, "B1": 10, "C": "40", "L1": 70, "L": 97.4, "K1": 20.25,
                             "K2": 6, "G": "12",
                             "MXL": "M8X10", "T": 8.5,"H2": 6.5, "H3": 10.8,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "38.74",
                             "基本静额定负载": "52.19",
                             "容许静力矩": "", "MR": "0.66", "MP": "0.53", "MY": "0.53",
                             "重量": "", "滑块（kg）": 0.78, "滑轨": 4.47}  #

        self.HGL30HA_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 6, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 60, "B": 40, "B1": 10, "C": "60", "L1": 93, "L": 120.4, "K1": 21.75,
                             "K2": 6, "G": "12",
                             "MXL": "M8X10", "T": 8.5,"H2": 6.5, "H3": 10.8,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "47.27",
                             "基本静额定负载": "69.14",
                             "容许静力矩": "", "MR": "0.88", "MP": "0.92", "MY": "0.92",
                             "重量": "", "滑块（kg）": 1.03, "滑轨": 4.47}  #

        self.HGL35CA_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 7.5, "N": 18,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 50, "B1": 10, "C": "50", "L1": 80, "L": 112.4, "K1": 20.6,
                             "K2": 7, "G": "12",
                             "MXL": "M8X12", "T": 10.2,"H2": 9, "H3": 12.6,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X12", "基本动额定负载": "49.52",
                             "基本静额定负载": "69.16",
                             "容许静力矩": "", "MR": "1.16", "MP": "0.81", "MY": "0.81",
                             "重量": "", "滑块（kg）": 1.14, "滑轨": 6.3}  #

        self.HGL35HA_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 7.5, "N": 18,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 50, "B1": 10, "C": "72", "L1": 105.8, "L": 138.2, "K1": 22.5,
                             "K2": 7, "G": "12",
                             "MXL": "M8X12", "T": 10.2,"H2": 9, "H3": 12.6,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "60.12",
                             "基本静额定负载": "91.63",
                             "容许静力矩": "", "MR": "1.54", "MP": "1.40", "MY": "1.40",
                             "重量": "", "滑块（kg）": 1.52, "滑轨": 6.3}  #

        self.HGL45CA_dict = {"组件尺寸(mm)": " ", "H": 60, "H1": 9.5, "N": 20.5,
                             "滑块尺寸(mm)": " ", "W": 86, "B": 60, "B1": 13, "C": "60", "L1": 97, "L": 139.4, "K1": 23,
                             "K2": 10, "G": "12.9",
                             "MXL": "M10X17", "T": 16,"H2": 8.5, "H3": 20.5,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "77.57",
                             "基本静额定负载": "102.71",
                             "容许静力矩": "", "MR": "1.98", "MP": "1.55", "MY": "1.55",
                             "重量": "", "滑块（kg）": 2.08, "滑轨": 10.41}  #

        self.HGL45HA_dict = {"组件尺寸(mm)": " ", "H": 60, "H1": 9.5, "N": 20.5,
                             "滑块尺寸(mm)": " ", "W": 86, "B": 60, "B1": 13, "C": "80", "L1": 128.8, "L": 171.2, "K1": 28.9,
                             "K2": 10, "G": "12.9",
                             "MXL": "M10X17", "T": 16,"H2": 8.5, "H3": 20.5,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "94.54",
                             "基本静额定负载": "136.46",
                             "容许静力矩": "", "MR": "2.63", "MP": "2.68", "MY": "2.68",
                             "重量": "", "滑块（kg）": 2.75, "滑轨": 10.41}  #

        self.HGL55CA_dict = {"组件尺寸(mm)": " ", "H": 70, "H1": 13, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 75, "B1": 12.5, "C": "75", "L1": 117.7, "L": 166.7,
                             "K1": 27.35,
                             "K2": 11, "G": "12.9",
                             "MXL": "M12X18", "T": 17.5,"H2": 12, "H3": 19,
                             "滑轨(mm)": " ", "WR": 53, "HR": 44, "D": "23", "h": 20, "d": 16, "P": 120, "E": 30,
                             "滑轨螺栓尺寸": "M14X45", "基本动额定负载": "114.44",
                             "基本静额定负载": "148.33",
                             "容许静力矩": "", "MR": "3.69", "MP": "2.64", "MY": "2.64",
                             "重量": "", "滑块（kg）": 3.25, "滑轨": 15.08}  #

        self.HGL55HA_dict = {"组件尺寸(mm)": " ", "H": 70, "H1": 13, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 75, "B1": 12.5, "C": "95", "L1": 155.8, "L": 204.8,
                             "K1": 36.4,
                             "K2": 11, "G": "12.9",
                             "MXL": "M12X18", "T": 17.5,"H2": 12, "H3": 19,
                             "滑轨(mm)": " ", "WR": 53, "HR": 44, "D": "23", "h": 20, "d": 16, "P": 120, "E": 30,
                             "滑轨螺栓尺寸": "M14X45", "基本动额定负载": "139.35",
                             "基本静额定负载": "190.20",
                             "容许静力矩": "", "MR": "4.88", "MP": "4.57", "MY": "4.57",
                             "重量": "", "滑块（kg）": 4.27, "滑轨": 15.08}  #
        self.HGL_series_dict = {"HGL25CA":self.HGL25CA_dict,"HGL25HA":self.HGL25HA_dict,"HGL30CA":self.HGL30CA_dict,
                                "HGL30HA":self.HGL30HA_dict,"HGL35CA":self.HGL35CA_dict,"HGL35HA":self.HGL35HA_dict,
                                "HGL45CA":self.HGL45CA_dict,"HGL45HA":self.HGL45HA_dict,"HGL55CA":self.HGL55CA_dict,
                                "HGL55HA":self.HGL55HA_dict
                                }
        self.series = self.HGL_series_dict

    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["", "15", "25", "30", "35", "45", "55", ]}  #
        all_combox_list.append(["滑轨", "高组装"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["L:四方型（低）"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷 ", "H:超重负荷"]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "B:下锁式", "C:上或下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Liner_guide_QHH(Create_Liner_guide_EGH):
    pass
    def __init__(self):
        pass
        self.QHH15CA_dict = {"组件尺寸(mm)": " ", "H": 28, "H1": 4, "N": 9.5,
                             "滑块尺寸(mm)": " ", "W": 34, "B": 26, "B1": 4, "C": "26", "L1": 39.4, "L": 61.4,
                             "G": "5.3",
                             "MXL": "M4X5", "T": 6,"H2": 7.95, "H3": 8.2,
                             "滑轨(mm)": " ", "WR": 15, "HR": 15, "D": "7.5", "h": 5.3, "d": 4.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M4X16", "基本动额定负载": "13.88",
                             "基本静额定负载": "14.36",
                             "容许静力矩": "", "MR": "0.10", "MP": "0.08", "MY": "0.08",
                             "重量": "", "滑块（kg）": 0.18, "滑轨": 1.45}  #

        self.QHH20CA_dict = {"组件尺寸(mm)": " ", "H": 30, "H1": 4.6, "N": 12,
                             "滑块尺寸(mm)": " ", "W": 44, "B": 32, "B1": 6, "C": "36", "L1": 50.5, "L": 76.7,
                             "G": "12",
                             "MXL": "M5X6", "T": 8, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 17.5, "D": "9.5", "h": 8.3, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "23.08",
                             "基本静额定负载": "25.63",
                             "容许静力矩": "", "MR": "0.26", "MP": "0.19", "MY": "0.19",
                             "重量": "", "滑块（kg）": 0.29, "滑轨": 2.21}  #

        self.QHH20HA_dict = {"组件尺寸(mm)": " ", "H": 30, "H1": 4.6, "N": 12,
                             "滑块尺寸(mm)": " ", "W": 44, "B": 32, "B1": 6, "C": "50", "L1": 65.2, "L": 91.4,
                             "G": "12",
                             "MXL": "M5X6", "T": 8, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 17.5, "D": "9.5", "h": 8.3, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "27.53",
                             "基本静额定负载": "31.67",
                             "容许静力矩": "", "MR": "0.31", "MP": "0.27", "MY": "0.27",
                             "重量": "", "滑块（kg）": 0.38, "滑轨": 2.21}  #

        self.QHH25CA_dict = {"组件尺寸(mm)": " ", "H": 40, "H1": 5.5, "N": 12.5,
                             "滑块尺寸(mm)": " ", "W": 48, "B": 35, "B1": 6.5, "C": "35", "L1": 58, "L": 83.4,
                             "G": "12",
                             "MXL": "M6X8", "T": 8, "H2": 10, "H3": 8.5,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "31.78",
                             "基本静额定负载": "33.68",
                             "容许静力矩": "", "MR": "0.39", "MP": "0.31", "MY": "0.31",
                             "重量": "", "滑块（kg）": 0.50, "滑轨": 3.21}  #

        self.QHH25HA_dict = {"组件尺寸(mm)": " ", "H": 40, "H1": 5.5, "N": 12.5,
                             "滑块尺寸(mm)": " ", "W": 48, "B": 35, "B1": 6.5, "C": "50", "L1": 78.6, "L": 104,
                             "G": "12",
                             "MXL": "M6X8", "T": 8, "H2": 10, "H3": 8.5,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "39.3",
                             "基本静额定负载": "43.62",
                             "容许静力矩": "", "MR": "0.50", "MP": "0.45", "MY": "0.45",
                             "重量": "", "滑块（kg）": 0.68, "滑轨": 3.21}  #

        self.QHH30CA_dict = {"组件尺寸(mm)": " ", "H": 45, "H1": 6, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 60, "B": 40, "B1": 10, "C": "40", "L1": 70, "L": 97.4,
                             "G": "12",
                             "MXL": "M8X10", "T": 8.5, "H2": 9.5, "H3": 9,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "46.49",
                             "基本静额定负载": "48.17",
                             "容许静力矩": "", "MR": "0.60", "MP": "0.5", "MY": "0.5",
                             "重量": "", "滑块（kg）": 0.87, "滑轨": 4.47}  #

        self.QHH30HA_dict = {"组件尺寸(mm)": " ", "H": 45, "H1": 6, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 60, "B": 40, "B1": 10, "C": "60", "L1": 93, "L": 120.4,
                             "G": "12",
                             "MXL": "M8X10", "T": 8.5, "H2": 9.5, "H3": 9,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "56.72",
                             "基本静额定负载": "65.09",
                             "容许静力矩": "", "MR": "0.83", "MP": "0.89", "MY": "0.89",
                             "重量": "", "滑块（kg）": 1.15, "滑轨": 4.47}  #

        self.QHH35CA_dict = {"组件尺寸(mm)": " ", "H": 55, "H1": 7.5, "N": 18,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 50, "B1": 10, "C": "50", "L1": 80, "L": 113.6,
                             "G": "12",
                             "MXL": "M8X12", "T": 10.2, "H2": 15.5, "H3": 13.5,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "60.52",
                             "基本静额定负载": "63.84",
                             "容许静力矩": "", "MR": "1.07", "MP": "0.76", "MY": "0.76",
                             "重量": "", "滑块（kg）": 1.44, "滑轨": 6.30}  #

        self.QHH35HA_dict = {"组件尺寸(mm)": " ", "H": 55, "H1": 7.5, "N": 18,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 50, "B1": 10, "C": "72", "L1": 105.8, "L": 139.4,
                             "G": "12",
                             "MXL": "M8X12", "T": 10.2, "H2": 15.5, "H3": 13.5,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "73.59",
                             "基本静额定负载": "86.24",
                             "容许静力矩": "", "MR": "1.45", "MP": "1.33", "MY": "1.33",
                             "重量": "", "滑块（kg）": 1.90, "滑轨": 6.30}  #

        self.QHH45CA_dict = {"组件尺寸(mm)": " ", "H": 70, "H1": 9.2, "N": 20.5,
                             "滑块尺寸(mm)": " ", "W": 86, "B": 60, "B1": 13, "C": "60", "L1": 97, "L": 139.4,
                             "G": "12.9",
                             "MXL": "M10X17", "T": 16, "H2": 18.5, "H3": 20,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "89.21",
                             "基本静额定负载": "94.81",
                             "容许静力矩": "", "MR": "1.83", "MP": "1.38", "MY": "1.38",
                             "重量": "", "滑块（kg）": 2.72, "滑轨": 10.41}  #

        self.QHH45HA_dict = {"组件尺寸(mm)": " ", "H": 70, "H1": 9.2, "N": 20.5,
                             "滑块尺寸(mm)": " ", "W": 86, "B": 60, "B1": 13, "C": "80", "L1": 128.8, "L": 171.2,
                             "G": "12.9",
                             "MXL": "M10X17", "T": 16, "H2": 18.5, "H3": 20,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "108.72",
                             "基本静额定负载": "128.43",
                             "容许静力矩": "", "MR": "2.47", "MP": "2.41", "MY": "2.41",
                             "重量": "", "滑块（kg）": 3.59, "滑轨": 10.41}  #

        self.QHH_series_dict = {"QHH15CA":self.QHH15CA_dict,"QHH20CA_dict":self.QHH20CA_dict,"QHH20HA":self.QHH20HA_dict,
                                "QHH25CA":self.QHH25CA_dict,"QHH25HA":self.QHH25HA_dict,"QHH30CA":self.QHH30CA_dict,
                                "QHH30HA":self.QHH30HA_dict,"QHH35CA":self.QHH35CA_dict,"QHH35HA":self.QHH35HA_dict,
                                "QHH45CA":self.QHH45CA_dict,"QHH45HA":self.QHH45HA_dict
                                }
        self.series = self.QHH_series_dict

    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["", "15","20", "25", "30", "35", "45" ]}  #
        all_combox_list.append(["滑轨", "静音式"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["H:四方型"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷 ", "H:超重负荷"]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "B:下锁式", "C:上或下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Liner_guide_QHW(Create_Liner_guide_QHH):
    pass
    def __init__(self):
        pass
        self.QHW15CA_dict = {"组件尺寸(mm)": " ", "H": 24, "H1": 4, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 47, "B": 38, "B1": 4.5, "C": "30", "L1": 39.4, "L": 61.4,
                             "G": "5.3",
                             "M": "M5", "T": 6,"T1": 8.9,"H2": 3.95, "H3": 4.2,
                             "滑轨(mm)": " ", "WR": 15, "HR": 15, "D": "7.5", "h": 5.3, "d": 4.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M4X16", "基本动额定负载": "13.88",
                             "基本静额定负载": "14.36",
                             "容许静力矩": "", "MR": "0.10", "MP": "0.08", "MY": "0.08",
                             "重量": "", "滑块（kg）": 0.17, "滑轨": 1.45}  #

        self.QHW20CA_dict = {"组件尺寸(mm)": " ", "H": 30, "H1": 4.6, "N": 21.5,
                             "滑块尺寸(mm)": " ", "W": 63, "B": 53, "B1": 5, "C": "40", "L1": 50.5, "L": 76.7,
                             "G": "12",
                             "M": "M6", "T": 8,"T1": 10, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 17.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "23.08",
                             "基本静额定负载": "25.63",
                             "容许静力矩": "", "MR": "0.26", "MP": "0.19", "MY": "0.19",
                             "重量": "", "滑块（kg）": 0.40, "滑轨": 2.21}  #

        self.QHW20HA_dict = {"组件尺寸(mm)": " ", "H": 30, "H1": 4.6, "N": 21.5,
                             "滑块尺寸(mm)": " ", "W": 63, "B": 53, "B1": 5, "C": "40", "L1": 65.2, "L": 91.4,
                             "G": "12",
                             "M": "M6", "T": 8,"T1": 10, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 17.5, "D": "9.5", "h": 8.3, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "27.53",
                             "基本静额定负载": "31.67",
                             "容许静力矩": "", "MR": "0.31", "MP": "0.27", "MY": "0.27",
                             "重量": "", "滑块（kg）": 0.52, "滑轨": 2.21}  #

        self.QHW25CA_dict = {"组件尺寸(mm)": " ", "H": 36, "H1": 5.5, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 57, "B1": 6.5, "C": "45", "L1": 58, "L": 83.4,
                             "G": "12",
                             "M": "M8", "T": 8, "T1": 14,"H2": 6, "H3": 4.5,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "31.78",
                             "基本静额定负载": "33.68",
                             "容许静力矩": "", "MR": "0.39", "MP": "0.31", "MY": "0.31",
                             "重量": "", "滑块（kg）": 0.59, "滑轨": 3.21}  #

        self.QHW25HA_dict = {"组件尺寸(mm)": " ", "H": 36, "H1": 5.5, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 57, "B1": 6.5, "C": "45", "L1": 78.6, "L": 104,
                             "G": "12",
                             "M": "M8", "T": 8, "T1": 14,"H2": 6, "H3": 4.5,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "39.30",
                             "基本静额定负载": "43.62",
                             "容许静力矩": "", "MR": "0.50", "MP": "0.45", "MY": "0.45",
                             "重量": "", "滑块（kg）": 0.80, "滑轨": 3.21}  #

        self.QHW30CA_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 6, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "52", "L1": 70, "L": 97.4,
                             "G": "12",
                             "M": "M10", "T": 8.5,"T1": 16, "H2": 6.5, "H3": 6,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "46.49",
                             "基本静额定负载": "48.17",
                             "容许静力矩": "", "MR": "0.60", "MP": "0.5", "MY": "0.5",
                             "重量": "", "滑块（kg）": 1.09, "滑轨": 4.47}  #

        self.QHW30HA_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 6, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "52", "L1": 93, "L": 120.4,
                             "G": "12",
                             "M": "M10", "T": 8.5,"T1": 16, "H2": 6.5, "H3": 6,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "56.72",
                             "基本静额定负载": "65.09",
                             "容许静力矩": "", "MR": "0.83", "MP": "0.89", "MY": "0.89",
                             "重量": "", "滑块（kg）": 1.44, "滑轨": 4.47}  #

        self.QHH35CA_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 7.5, "N": 33,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 82, "B1": 9, "C": "62", "L1": 80, "L": 113.6,
                             "G": "12",
                             "M": "M10", "T": 10.1, "T1": 18 , "H2": 8.5, "H3": 6.5,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "60.52",
                             "基本静额定负载": "63.84",
                             "容许静力矩": "", "MR": "1.07", "MP": "0.76", "MY": "0.76",
                             "重量": "", "滑块（kg）": 1.56, "滑轨": 6.30}  #

        self.QHW35HA_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 7.5, "N": 33,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 82, "B1": 9, "C": "62", "L1": 105.8, "L": 139.4,
                             "G": "12",
                             "M": "M10", "T": 10.1, "T1": 18 , "H2": 8.5, "H3": 6.5,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "73.59",
                             "基本静额定负载": "86.24",
                             "容许静力矩": "", "MR": "1.45", "MP": "1.33", "MY": "1.33",
                             "重量": "", "滑块（kg）": 2.06, "滑轨": 6.30}  #

        self.QHW45CA_dict = {"组件尺寸(mm)": " ", "H": 63, "H1": 9.2, "N": 37.5,
                             "滑块尺寸(mm)": " ", "W": 120, "B": 100, "B1": 10, "C": "80", "L1": 97, "L": 139.4,
                             "G": "12.9",
                             "M": "M12", "T": 15.1,"T1": 22, "H2": 8.5, "H3": 10,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "89.21",
                             "基本静额定负载": "94.81",
                             "容许静力矩": "", "MR": "1.83", "MP": "1.38", "MY": "1.38",
                             "重量": "", "滑块（kg）": 2.79, "滑轨": 10.41}  #

        self.QHW45HA_dict = {"组件尺寸(mm)": " ", "H": 63, "H1": 9.2, "N": 37.5,
                             "滑块尺寸(mm)": " ", "W": 120, "B": 100, "B1": 10, "C": "80", "L1": 128.8, "L": 171.2,
                             "G": "12.9",
                             "M": "M12", "T": 15.1,"T1": 22, "H2": 8.5, "H3": 10,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "108.72",
                             "基本静额定负载": "128.43",
                             "容许静力矩": "", "MR": "2.47", "MP": "2.41", "MY": "2.41",
                             "重量": "", "滑块（kg）": 3.69, "滑轨": 10.41}  #

        #CC HC系列--------------------------------------------------------------
        self.QHW15CC_dict = {"组件尺寸(mm)": " ", "H": 24, "H1": 4, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 47, "B": 38, "B1": 4.5, "C": "30", "L1": 39.4, "L": 61.4,
                             "G": "5.3",
                             "M": "M5", "T": 6, "T1": 8.9, "H2": 3.95, "H3": 4.2,
                             "滑轨(mm)": " ", "WR": 15, "HR": 15, "D": "7.5", "h": 5.3, "d": 4.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M4X16", "基本动额定负载": "13.88",
                             "基本静额定负载": "14.36",
                             "容许静力矩": "", "MR": "0.10", "MP": "0.08", "MY": "0.08",
                             "重量": "", "滑块（kg）": 0.17, "滑轨": 1.45}  #

        self.QHW20CC_dict = {"组件尺寸(mm)": " ", "H": 30, "H1": 4.6, "N": 21.5,
                             "滑块尺寸(mm)": " ", "W": 63, "B": 53, "B1": 5, "C": "40", "L1": 50.5, "L": 76.7,
                             "G": "12",
                             "M": "M6", "T": 8, "T1": 10, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 17.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "23.08",
                             "基本静额定负载": "25.63",
                             "容许静力矩": "", "MR": "0.26", "MP": "0.19", "MY": "0.19",
                             "重量": "", "滑块（kg）": 0.40, "滑轨": 2.21}  #

        self.QHW20HC_dict = {"组件尺寸(mm)": " ", "H": 30, "H1": 4.6, "N": 21.5,
                             "滑块尺寸(mm)": " ", "W": 63, "B": 53, "B1": 5, "C": "40", "L1": 65.2, "L": 91.4,
                             "G": "12",
                             "M": "M6", "T": 8, "T1": 10, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 17.5, "D": "9.5", "h": 8.3, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "27.53",
                             "基本静额定负载": "31.67",
                             "容许静力矩": "", "MR": "0.31", "MP": "0.27", "MY": "0.27",
                             "重量": "", "滑块（kg）": 0.52, "滑轨": 2.21}  #

        self.QHW25CC_dict = {"组件尺寸(mm)": " ", "H": 36, "H1": 5.5, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 57, "B1": 6.5, "C": "45", "L1": 58, "L": 83.4,
                             "G": "12",
                             "M": "M8", "T": 8, "T1": 14, "H2": 6, "H3": 4.5,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "31.78",
                             "基本静额定负载": "33.68",
                             "容许静力矩": "", "MR": "0.39", "MP": "0.31", "MY": "0.31",
                             "重量": "", "滑块（kg）": 0.59, "滑轨": 3.21}  #

        self.QHW25HC_dict = {"组件尺寸(mm)": " ", "H": 36, "H1": 5.5, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 57, "B1": 6.5, "C": "45", "L1": 78.6, "L": 104,
                             "G": "12",
                             "M": "M8", "T": 8, "T1": 14, "H2": 6, "H3": 4.5,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "39.30",
                             "基本静额定负载": "43.62",
                             "容许静力矩": "", "MR": "0.50", "MP": "0.45", "MY": "0.45",
                             "重量": "", "滑块（kg）": 0.80, "滑轨": 3.21}  #

        self.QHW30CC_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 6, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "52", "L1": 70, "L": 97.4,
                             "G": "12",
                             "M": "M10", "T": 8.5, "T1": 16, "H2": 6.5, "H3": 6,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "46.49",
                             "基本静额定负载": "48.17",
                             "容许静力矩": "", "MR": "0.60", "MP": "0.5", "MY": "0.5",
                             "重量": "", "滑块（kg）": 1.09, "滑轨": 4.47}  #

        self.QHW30HC_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 6, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "52", "L1": 93, "L": 120.4,
                             "G": "12",
                             "M": "M10", "T": 8.5, "T1": 16, "H2": 6.5, "H3": 6,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "56.72",
                             "基本静额定负载": "65.09",
                             "容许静力矩": "", "MR": "0.83", "MP": "0.89", "MY": "0.89",
                             "重量": "", "滑块（kg）": 1.44, "滑轨": 4.47}  #

        self.QHH35CC_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 7.5, "N": 33,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 82, "B1": 9, "C": "62", "L1": 80, "L": 113.6,
                             "G": "12",
                             "M": "M10", "T": 10.1, "T1": 18, "H2": 8.5, "H3": 6.5,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "60.52",
                             "基本静额定负载": "63.84",
                             "容许静力矩": "", "MR": "1.07", "MP": "0.76", "MY": "0.76",
                             "重量": "", "滑块（kg）": 1.56, "滑轨": 6.30}  #

        self.QHW35HC_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 7.5, "N": 33,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 82, "B1": 9, "C": "62", "L1": 105.8, "L": 139.4,
                             "G": "12",
                             "M": "M10", "T": 10.1, "T1": 18, "H2": 8.5, "H3": 6.5,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "73.59",
                             "基本静额定负载": "86.24",
                             "容许静力矩": "", "MR": "1.45", "MP": "1.33", "MY": "1.33",
                             "重量": "", "滑块（kg）": 2.06, "滑轨": 6.30}  #

        self.QHW45CC_dict = {"组件尺寸(mm)": " ", "H": 63, "H1": 9.2, "N": 37.5,
                             "滑块尺寸(mm)": " ", "W": 120, "B": 100, "B1": 10, "C": "80", "L1": 97, "L": 139.4,
                             "G": "12.9",
                             "M": "M12", "T": 15.1, "T1": 22, "H2": 8.5, "H3": 10,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "89.21",
                             "基本静额定负载": "94.81",
                             "容许静力矩": "", "MR": "1.83", "MP": "1.38", "MY": "1.38",
                             "重量": "", "滑块（kg）": 2.79, "滑轨": 10.41}  #

        self.QHW45HC_dict = {"组件尺寸(mm)": " ", "H": 63, "H1": 9.2, "N": 37.5,
                             "滑块尺寸(mm)": " ", "W": 120, "B": 100, "B1": 10, "C": "80", "L1": 128.8, "L": 171.2,
                             "G": "12.9",
                             "M": "M12", "T": 15.1, "T1": 22, "H2": 8.5, "H3": 10,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "108.72",
                             "基本静额定负载": "128.43",
                             "容许静力矩": "", "MR": "2.47", "MP": "2.41", "MY": "2.41",
                             "重量": "", "滑块（kg）": 3.69, "滑轨": 10.41}  #

        #CB HB系列----------------------------------------------------------------------------------
        self.QHW15CB_dict = {"组件尺寸(mm)": " ", "H": 24, "H1": 4, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 47, "B": 38, "B1": 4.5, "C": "30", "L1": 39.4, "L": 61.4,
                             "G": "5.3",
                             "M": "Φ4.5", "T": 6, "T1": 8.9, "H2": 3.95, "H3": 4.2,
                             "滑轨(mm)": " ", "WR": 15, "HR": 15, "D": "7.5", "h": 5.3, "d": 4.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M4X16", "基本动额定负载": "13.88",
                             "基本静额定负载": "14.36",
                             "容许静力矩": "", "MR": "0.10", "MP": "0.08", "MY": "0.08",
                             "重量": "", "滑块（kg）": 0.17, "滑轨": 1.45}  #

        self.QHW20CB_dict = {"组件尺寸(mm)": " ", "H": 30, "H1": 4.6, "N": 21.5,
                             "滑块尺寸(mm)": " ", "W": 63, "B": 53, "B1": 5, "C": "40", "L1": 50.5, "L": 76.7,
                             "G": "12",
                             "M": "Φ6", "T": 8, "T1": 10, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 17.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "23.08",
                             "基本静额定负载": "25.63",
                             "容许静力矩": "", "MR": "0.26", "MP": "0.19", "MY": "0.19",
                             "重量": "", "滑块（kg）": 0.40, "滑轨": 2.21}  #

        self.QHW20HB_dict = {"组件尺寸(mm)": " ", "H": 30, "H1": 4.6, "N": 21.5,
                             "滑块尺寸(mm)": " ", "W": 63, "B": 53, "B1": 5, "C": "40", "L1": 65.2, "L": 91.4,
                             "G": "12",
                             "M": "Φ6", "T": 8, "T1": 10, "H2": 6, "H3": 6,
                             "滑轨(mm)": " ", "WR": 20, "HR": 17.5, "D": "9.5", "h": 8.3, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "27.53",
                             "基本静额定负载": "31.67",
                             "容许静力矩": "", "MR": "0.31", "MP": "0.27", "MY": "0.27",
                             "重量": "", "滑块（kg）": 0.52, "滑轨": 2.21}  #

        self.QHW25CB_dict = {"组件尺寸(mm)": " ", "H": 36, "H1": 5.5, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 57, "B1": 6.5, "C": "45", "L1": 58, "L": 83.4,
                             "G": "12",
                             "M": "Φ7", "T": 8, "T1": 14, "H2": 6, "H3": 4.5,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "31.78",
                             "基本静额定负载": "33.68",
                             "容许静力矩": "", "MR": "0.39", "MP": "0.31", "MY": "0.31",
                             "重量": "", "滑块（kg）": 0.59, "滑轨": 3.21}  #

        self.QHW25HB_dict = {"组件尺寸(mm)": " ", "H": 36, "H1": 5.5, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 57, "B1": 6.5, "C": "45", "L1": 78.6, "L": 104,
                             "G": "12",
                             "M": "Φ7", "T": 8, "T1": 14, "H2": 6, "H3": 4.5,
                             "滑轨(mm)": " ", "WR": 23, "HR": 22, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "39.30",
                             "基本静额定负载": "43.62",
                             "容许静力矩": "", "MR": "0.50", "MP": "0.45", "MY": "0.45",
                             "重量": "", "滑块（kg）": 0.80, "滑轨": 3.21}  #

        self.QHW30CB_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 6, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "52", "L1": 70, "L": 97.4,
                             "G": "12",
                             "M": "Φ9", "T": 8.5, "T1": 16, "H2": 6.5, "H3": 6,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "46.49",
                             "基本静额定负载": "48.17",
                             "容许静力矩": "", "MR": "0.60", "MP": "0.5", "MY": "0.5",
                             "重量": "", "滑块（kg）": 1.09, "滑轨": 4.47}  #

        self.QHW30HB_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 6, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "52", "L1": 93, "L": 120.4,
                             "G": "12",
                             "M": "Φ9", "T": 8.5, "T1": 16, "H2": 6.5, "H3": 6,
                             "滑轨(mm)": " ", "WR": 28, "HR": 26, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "56.72",
                             "基本静额定负载": "65.09",
                             "容许静力矩": "", "MR": "0.83", "MP": "0.89", "MY": "0.89",
                             "重量": "", "滑块（kg）": 1.44, "滑轨": 4.47}  #

        self.QHH35CB_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 7.5, "N": 33,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 82, "B1": 9, "C": "62", "L1": 80, "L": 113.6,
                             "G": "12",
                             "M": "Φ9", "T": 10.1, "T1": 18, "H2": 8.5, "H3": 6.5,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "60.52",
                             "基本静额定负载": "63.84",
                             "容许静力矩": "", "MR": "1.07", "MP": "0.76", "MY": "0.76",
                             "重量": "", "滑块（kg）": 1.56, "滑轨": 6.30}  #

        self.QHW35HB_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 7.5, "N": 33,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 82, "B1": 9, "C": "62", "L1": 105.8, "L": 139.4,
                             "G": "12",
                             "M": "Φ9", "T": 10.1, "T1": 18, "H2": 8.5, "H3": 6.5,
                             "滑轨(mm)": " ", "WR": 34, "HR": 29, "D": "14", "h": 12, "d": 9, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "73.59",
                             "基本静额定负载": "86.24",
                             "容许静力矩": "", "MR": "1.45", "MP": "1.33", "MY": "1.33",
                             "重量": "", "滑块（kg）": 2.06, "滑轨": 6.30}  #

        self.QHW45CB_dict = {"组件尺寸(mm)": " ", "H": 63, "H1": 9.2, "N": 37.5,
                             "滑块尺寸(mm)": " ", "W": 120, "B": 100, "B1": 10, "C": "80", "L1": 97, "L": 139.4,
                             "G": "12.9",
                             "M": "Φ11", "T": 15.1, "T1": 22, "H2": 8.5, "H3": 10,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "89.21",
                             "基本静额定负载": "94.81",
                             "容许静力矩": "", "MR": "1.83", "MP": "1.38", "MY": "1.38",
                             "重量": "", "滑块（kg）": 2.79, "滑轨": 10.41}  #

        self.QHW45HB_dict = {"组件尺寸(mm)": " ", "H": 63, "H1": 9.2, "N": 37.5,
                             "滑块尺寸(mm)": " ", "W": 120, "B": 100, "B1": 10, "C": "80", "L1": 128.8, "L": 171.2,
                             "G": "12.9",
                             "M": "Φ11", "T": 15.1, "T1": 22, "H2": 8.5, "H3": 10,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 105, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "108.72",
                             "基本静额定负载": "128.43",
                             "容许静力矩": "", "MR": "2.47", "MP": "2.41", "MY": "2.41",
                             "重量": "", "滑块（kg）": 3.69, "滑轨": 10.41}  #

        self.QHW_series_dict = {"QHW15CA":self.QHW15CA_dict,"QHW20CA":self.QHW20CA_dict,"QHW20HA":self.QHW20HA_dict,
                                "QHW25CA":self.QHW25CA_dict,"QHW25HA":self.QHW25HA_dict,"QHW30CA":self.QHW30CA_dict,
                                "QHW30HA":self.QHW30HA_dict,"QHH35CA_dict":self.QHH35CA_dict,"QHW35HA":self.QHW35HA_dict,
                                "QHW45CA":self.QHW45CA_dict,"QHW45HA":self.QHW45HA_dict,

                                "QHW15CC": self.QHW15CC_dict, "QHW20CC": self.QHW20CC_dict,
                                "QHW20HC": self.QHW20HC_dict,
                                "QHW25CC": self.QHW25CC_dict, "QHW25HC": self.QHW25HC_dict,
                                "QHW30CC": self.QHW30CC_dict,
                                "QHW30HC": self.QHW30HC_dict, "QHH35CC_dict": self.QHH35CC_dict,
                                "QHW35HC": self.QHW35HC_dict,
                                "QHW45CC": self.QHW45CC_dict, "QHW45HC": self.QHW45HC_dict,

                                "QHW15CB": self.QHW15CB_dict, "QHW20CB": self.QHW20CB_dict,
                                "QHW20HB": self.QHW20HB_dict,
                                "QHW25CB": self.QHW25CB_dict, "QHW25HB": self.QHW25HB_dict,
                                "QHW30CB": self.QHW30CB_dict,
                                "QHW30HB": self.QHW30HB_dict, "QHH35CB_dict": self.QHH35CB_dict,
                                "QHW35HB": self.QHW35HB_dict,
                                "QHW45CB": self.QHW45CB_dict, "QHW45HB": self.QHW45HB_dict,

                                }
        self.series = self.QHW_series_dict
    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["", "15","20", "25", "30", "35", "45" ]}  #
        all_combox_list.append(["滑轨", "静音式"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["W:法兰型"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷 ", "H:超重负荷"]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "B:下锁式", "C:上或下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list


class Create_Liner_guide_WEH(Create_Liner_guide_EGH):
    pass
    def __init__(self):
        pass
        self.WEH27CA_dict = {"组件尺寸(mm)": " ", "H": 27, "H1": 4, "N": 10,
                             "滑块尺寸(mm)": " ", "W": 62, "B": 46, "B1": 8, "C": "32", "L1": 51.8, "L": 72.8,"K1":14.15,
                             "K2": 3.5,
                             "G": "12",
                             "MXL": "M6X6", "T": 10,"H2": 6, "H3": 5,
                             "滑轨(mm)": " ", "WR": 42, "HR": 24,"HR":15, "D": "7.5", "h": 5.3, "d": 4.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M4X16", "基本动额定负载": "12.4",
                             "基本静额定负载": "21.6",
                             "容许静力矩": "", "MR": "0.47", "MP": "0.17", "MY": "0.17",
                             "重量": "", "滑块（kg）": 0.35, "滑轨": 4.8}  #

        self.WEH35CA_dict = {"组件尺寸(mm)": " ", "H": 35, "H1": 6, "N": 15.5,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 76, "B1": 12, "C": "50", "L1": 77.6, "L": 102.6,"K1":18.1,
                             "K2":5.25,
                             "G": "12",
                             "MXL": "M8X8", "T": 13, "H2": 8, "H3": 6.5,
                             "滑轨(mm)": " ", "WR": 69,"WB": 40, "HR": 19, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "29.8",
                             "基本静额定负载": "49.4",
                             "容许静力矩": "", "MR": "1.6", "MP": "0.67", "MY": "0.67",
                             "重量": "", "滑块（kg）": 1.1, "滑轨": 9.9}  #



        self.WEH_series_dict = {"WEH27CA":self.WEH27CA_dict,"WEH35CA":self.WEH35CA_dict }

        self.series = self.WEH_series_dict



    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["", "17","35"]}  #
        all_combox_list.append(["滑轨", "低组装"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["H:四方型"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷 "]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "C:上或下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Liner_guide_WEW(Create_Liner_guide_EGH):
    pass
    def __init__(self):
        pass
        self.WEW27CC_dict = {"组件尺寸(mm)": " ", "H": 27, "H1": 4, "N": 19,
                             "滑块尺寸(mm)": " ", "W": 80, "B": 70, "B1": 5, "C": "40", "L1": 51.8, "L": 72.8,"K1":10.15,
                             "K2": 3.5,
                             "G": "12",
                             "M": "M6", "T": 8,"T1": 10,"H2": 6, "H3": 5,
                             "滑轨(mm)": " ", "WR": 42, "HR": 24,"HR":15, "D": "7.5", "h": 5.3, "d": 4.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M4X16", "基本动额定负载": "12.4",
                             "基本静额定负载": "21.6",
                             "容许静力矩": "", "MR": "0.47", "MP": "0.17", "MY": "0.17",
                             "重量": "", "滑块（kg）": 0.43, "滑轨": 4.8}  #

        self.WEW35CC_dict = {"组件尺寸(mm)": " ", "H": 35, "H1": 4, "N": 25.5,
                             "滑块尺寸(mm)": " ", "W": 120, "B": 107, "B1": 6.5, "C": "60", "L1": 77.6, "L": 102.6,"K1":13.35,
                             "K2":5.25,
                             "G": "12",
                             "MXL": "M8X8", "T": 11.2,"T1": 14, "H2": 8, "H3": 6.5,
                             "滑轨(mm)": " ", "WR": 69,"WB": 40, "HR": 19, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "29.8",
                             "基本静额定负载": "49.4",
                             "容许静力矩": "", "MR": "1.6", "MP": "0.67", "MY": "0.67",
                             "重量": "", "滑块（kg）": 1.26, "滑轨": 9.9}  #



        self.WEW_series_dict = {"WEW27CC":self.WEW27CC_dict,"WEW35CC":self.WEW35CC_dict }

        self.series = self.WEW_series_dict



    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["", "17","35"]}  #
        all_combox_list.append(["滑轨", "低组装"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["W:法兰型"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷 "]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "C:上或下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Liner_guide_RGH(Create_Liner_guide_EGH):
    pass
    def __init__(self):
        pass
        self.RGH25CA_dict = {"组件尺寸(mm)": " ", "H": 40, "H1": 5.5, "N": 12.5,
                             "滑块尺寸(mm)": " ", "W": 48, "B": 35, "B1": 6.5, "C": "35", "L1": 64.5, "L": 97.9,"K1":20.75,
                             "K2": 7.25,
                             "G": "12",
                             "MXL": "M6X8", "T": 9.5,"H2": 10.2, "H3": 10,
                             "滑轨(mm)": " ", "WR": 23, "HR": 23.6,"D": "11", "h": 9, "d": 7, "P": 30, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "27.7",
                             "基本静额定负载": "57.1",
                             "容许静力矩": "", "MR": "0.758", "MP": "0.605", "MY": "0.605",
                             "重量": "", "滑块（kg）": 0.55, "滑轨": 3.08}  #

        self.RGH25HA_dict = {"组件尺寸(mm)": " ", "H": 40, "H1": 5.5, "N": 12.5,
                             "滑块尺寸(mm)": " ", "W": 48, "B": 35, "B1": 6.5, "C": "50", "L1": 81, "L": 114.4,"K1":21.5,
                             "K2": 7.25,
                             "G": "12",
                             "MXL": "M6X8", "T": 9.5,"H2": 10.2, "H3": 10,
                             "滑轨(mm)": " ", "WR": 23, "HR": 23.6,"D": "11", "h": 9, "d": 7, "P": 30, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "33.9",
                             "基本静额定负载": "73.4",
                             "容许静力矩": "", "MR": "0.975", "MP": "0.991", "MY": "0.991",
                             "重量": "", "滑块（kg）": 0.70, "滑轨": 3.08}  #

        self.RGH30CA_dict = {"组件尺寸(mm)": " ", "H": 45, "H1": 6, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 60, "B": 40, "B1": 10, "C": "40", "L1": 71, "L": 109.8,
                             "K1": 23.5,
                             "K2": 8,
                             "G": "12",
                             "MXL": "M8X10", "T": 9.5, "H2": 9.5, "H3": 10.3,
                             "滑轨(mm)": " ", "WR": 28, "HR": 28,  "D": "14", "h": 12, "d":9, "P": 40, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "39.1",
                             "基本静额定负载": "82.1",
                             "容许静力矩": "", "MR": "1.445", "MP": "1.06", "MY": "1.06",
                             "重量": "", "滑块（kg）": 0.82, "滑轨": 4.41}  #.

        self.RGH30HA_dict = {"组件尺寸(mm)": " ", "H": 45, "H1": 6, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 60, "B": 40, "B1": 10, "C": "60", "L1": 93, "L": 131.8,
                             "K1": 24.5,
                             "K2": 8,
                             "G": "12",
                             "MXL": "M8X10", "T": 9.5, "H2": 9.5, "H3": 10.3,
                             "滑轨(mm)": " ", "WR": 28, "HR": 28, "D": "14", "h": 12, "d": 9, "P": 40, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "48.1",
                             "基本静额定负载": "105",
                             "容许静力矩": "", "MR": "1.846", "MP": "1.712", "MY": "1.712",
                             "重量": "", "滑块（kg）": 1.07, "滑轨": 4.41}  #

        self.RGH35CA_dict = {"组件尺寸(mm)": " ", "H": 55, "H1": 6.5, "N": 18,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 50, "B1": 10, "C": "50", "L1": 79, "L": 124,
                             "K1": 22.5,
                             "K2": 10,
                             "G": "12",
                             "MXL": "M8X12", "T": 12, "H2": 16, "H3": 19.6,
                             "滑轨(mm)": " ", "WR": 34, "HR": 30.2, "D": "14", "h": 12, "d": 9, "P": 40, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "57.9",
                             "基本静额定负载": "105.2",
                             "容许静力矩": "", "MR": "2.17", "MP": "2.17", "MY": "1.44",
                             "重量": "", "滑块（kg）": 1.43, "滑轨": 6.06}  # .

        self.RGH35HA_dict = {"组件尺寸(mm)": " ", "H": 55, "H1": 6.5, "N": 18,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 50, "B1": 10, "C": "72", "L1": 106.5, "L": 151.5,
                             "K1": 25.25,
                             "K2": 10,
                             "G": "12",
                             "MXL": "M8X12", "T": 12, "H2": 16, "H3": 19.6,
                             "滑轨(mm)": " ", "WR": 34, "HR": 30.2, "D": "14", "h": 12, "d": 9, "P": 40, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "73.1",
                             "基本静额定负载": "142",
                             "容许静力矩": "", "MR": "2.93", "MP": "2.6", "MY": "2.6",
                             "重量": "", "滑块（kg）": 1.86, "滑轨": 6.06}  # .

        self.RGH45CA_dict = {"组件尺寸(mm)": " ", "H": 70, "H1": 8, "N": 20.5,
                             "滑块尺寸(mm)": " ", "W": 86, "B": 60, "B1": 13, "C": "60", "L1": 106, "L": 153.2,
                             "K1": 31,
                             "K2": 10,
                             "G": "12",
                             "MXL": "M10X17", "T": 16, "H2": 20, "H3": 24,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 52.5, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "92.6",
                             "基本静额定负载": "178.8",
                             "容许静力矩": "", "MR": "4.52", "MP": "3.05", "MY": "3.05",
                             "重量": "", "滑块（kg）": 2.97, "滑轨": 9.97}  # .

        self.RGH45HA_dict = {"组件尺寸(mm)": " ", "H": 70, "H1": 8, "N": 20.5,
                             "滑块尺寸(mm)": " ", "W": 86, "B": 60, "B1": 13, "C": "80", "L1": 139.8, "L": 187,
                             "K1": 37.9,
                             "K2": 10,
                             "G": "12",
                             "MXL": "M10X17", "T": 16, "H2": 20, "H3": 24,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 52.5, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "116",
                             "基本静额定负载": "230.9",
                             "容许静力矩": "", "MR": "6.33", "MP": "5.47", "MY": "5.47",
                             "重量": "", "滑块（kg）": 3.97, "滑轨": 9.97}  # .

        self.RGH55CA_dict = {"组件尺寸(mm)": " ", "H": 80, "H1": 10, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 75, "B1": 12.5, "C": "75", "L1": 125.5, "L": 183.7,
                             "K1": 37.75,
                             "K2": 12.5,
                             "G": "12.9",
                             "MXL": "M12X18", "T": 17.5, "H2": 22, "H3": 27.5,
                             "滑轨(mm)": " ", "WR": 53, "HR": 44, "D": "23", "h": 20, "d": 14, "P": 60, "E":30,
                             "滑轨螺栓尺寸": "M14X45", "基本动额定负载": "130.5",
                             "基本静额定负载": "252",
                             "容许静力矩": "", "MR": "8.01", "MP": "5.4", "MY": "5.4",
                             "重量": "", "滑块（kg）": 4.62, "滑轨": 13.98}  # .

        self.RGH55HA_dict = {"组件尺寸(mm)": " ", "H": 80, "H1": 10, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 75, "B1": 12.5, "C": "95", "L1": 173.8, "L": 232,
                             "K1": 51.9,
                             "K2": 12.5,
                             "G": "12.9",
                             "MXL": "M12X18", "T": 17.5, "H2": 22, "H3": 27.5,
                             "滑轨(mm)": " ", "WR": 53, "HR": 44, "D": "23", "h": 20, "d": 14, "P": 60, "E": 30,
                             "滑轨螺栓尺寸": "M14X45", "基本动额定负载": "167.8",
                             "基本静额定负载": "348",
                             "容许静力矩": "", "MR": "11.15", "MP": "10.25", "MY": "10.25",
                             "重量": "", "滑块（kg）": 6.4, "滑轨": 13.98}  # .

        self.RGH65CA_dict = {"组件尺寸(mm)": " ", "H": 90, "H1": 12, "N": 31.5,
                             "滑块尺寸(mm)": " ", "W": 126, "B": 76, "B1": 25, "C": "70", "L1": 160, "L": 232,
                             "K1": 60.8,
                             "K2": 15.8,
                             "G": "12.9",
                             "MXL": "M16X20", "T": 25, "H2": 15, "H3": 15,
                             "滑轨(mm)": " ", "WR": 63, "HR": 53, "D": "26", "h": 22, "d": 18, "P": 75, "E": 35,
                             "滑轨螺栓尺寸": "M16X50", "基本动额定负载": "213",
                             "基本静额定负载": "411.6",
                             "容许静力矩": "", "MR": "16.20", "MP": "11.59", "MY": "11.59",
                             "重量": "", "滑块（kg）": 8.33, "滑轨": 20.22}  # .

        self.RGH65HA_dict = {"组件尺寸(mm)": " ", "H": 90, "H1": 12, "N": 31.5,
                             "滑块尺寸(mm)": " ", "W": 126, "B": 76, "B1": 25, "C": "120", "L1": 223, "L": 295,
                             "K1":67.3,
                             "K2": 15.8,
                             "G": "12.9",
                             "MXL": "M16X20", "T": 25, "H2": 15, "H3": 15,
                             "滑轨(mm)": " ", "WR": 63, "HR": 53, "D": "26", "h": 22, "d": 18, "P": 75, "E": 35,
                             "滑轨螺栓尺寸": "M16X50", "基本动额定负载": "275.3",
                             "基本静额定负载": "572.7",
                             "容许静力矩": "", "MR": "22.55", "MP": "22.17", "MY": "22.17",
                             "重量": "", "滑块（kg）": 11.62, "滑轨": 20.22}  # .



        self.RGH_series_dict = {"RGH25CA":self.RGH25CA_dict,"RGH25HA":self.RGH25HA_dict,"RGH30CA":self.RGH30CA_dict,
                                "RGH30HA":self.RGH30HA_dict,"RGH35CA":self.RGH35CA_dict,"RGH35HA":self.RGH35HA_dict,
                                "RGH45CA":self.RGH45CA_dict,"RGH45HA":self.RGH45HA_dict,"RGH55CA":self.RGH55CA_dict,
                                "RGH55HA":self.RGH55HA_dict,"RGH65CA":self.RGH65CA_dict,"RGH65HA":self.RGH65HA_dict}

        self.series = self.RGH_series_dict



    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["","25" ,"30","35","45","55","65"]}  #
        all_combox_list.append(["滑轨", "滚柱式"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["H:四方型"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷","H:超重负荷 "]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "C:上或下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Liner_guide_RGW(Create_Liner_guide_EGH):
    pass
    def __init__(self):
        pass
        self.RGW25CC_dict = {"组件尺寸(mm)": " ", "H": 36, "H1": 5.5, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 57, "B1": 6.5, "C": "45","C1":40, "L1": 64.5, "L": 97.9,"K1":15.57,
                             "K2": 7.25,
                             "G": "12",
                             "M": "M8", "T": 9.5,"T1": 10,"H2": 6.2, "H3": 6,
                             "滑轨(mm)": " ", "WR": 23, "HR": 23.6,"D": "11", "h": 9, "d": 7, "P": 30, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "27.7",
                             "基本静额定负载": "57.1",
                             "容许静力矩": "", "MR": "0.758", "MP": "0.605", "MY": "0.605",
                             "重量": "", "滑块（kg）": 0.67, "滑轨": 3.08}  #

        self.RGW25HC_dict = {"组件尺寸(mm)": " ", "H": 36, "H1": 5.5, "N": 23.5,
                             "滑块尺寸(mm)": " ", "W": 70, "B": 57, "B1": 6.5, "C": "45","C1":40, "L1": 81, "L": 144.4,"K1":24,
                             "K2": 7.25,
                             "G": "12",
                             "M": "M8", "T": 9.5,"T1": 10,"H2": 6.2, "H3": 6,
                             "滑轨(mm)": " ", "WR": 23, "HR": 23.6,"D": "11", "h": 9, "d": 7, "P": 30, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "33.9",
                             "基本静额定负载": "73.4",
                             "容许静力矩": "", "MR": "0.975", "MP": "0.991", "MY": "0.991",
                             "重量": "", "滑块（kg）": 0.86, "滑轨": 3.08}  #

        self.RGW30CC_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 6, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "52","C1":44, "L1": 71, "L": 109.8,
                             "K1": 17.5,
                             "K2": 8,
                             "G": "12",
                             "M": "M10", "T": 9.5, "T1": 10,"H2": 6.5, "H3": 7.3,
                             "滑轨(mm)": " ", "WR": 28, "HR": 28,  "D": "14", "h": 12, "d":9, "P": 40, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "39.1",
                             "基本静额定负载": "82.1",
                             "容许静力矩": "", "MR": "1.445", "MP": "1.06", "MY": "1.06",
                             "重量": "", "滑块（kg）": 1.06, "滑轨": 4.41}  #.

        self.RGW30HC_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 6, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "52","C1":44, "L1": 93, "L": 131.8,
                             "K1": 28.5,
                             "K2": 8,
                             "G": "12",
                             "M": "M10", "T": 9.5, "T1": 10,"H2": 6.5, "H3": 7.3,
                             "滑轨(mm)": " ", "WR": 28, "HR": 28,  "D": "14", "h": 12, "d":9, "P": 40, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "48.1",
                             "基本静额定负载": "105",
                             "容许静力矩": "", "MR": "1.846", "MP": "1.712", "MY": "1.42",
                             "重量": "", "滑块（kg）": 1.42, "滑轨": 4.41}  #.

        self.RGW35CC_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 6.5, "N": 33,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 82, "B1": 9, "C": "62","C1": "52", "L1": 79, "L": 124,
                             "K1": 16.5,
                             "K2": 10,
                             "G": "12",
                             "M": "M10", "T": 12, "T1": 13, "H2": 9, "H3": 12.6,
                             "滑轨(mm)": " ", "WR": 34, "HR": 30.2, "D": "14", "h": 12, "d": 9, "P": 40, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "57.9",
                             "基本静额定负载": "105.2",
                             "容许静力矩": "", "MR": "2.17", "MP": "1.44", "MY": "1.44",
                             "重量": "", "滑块（kg）": 1.61, "滑轨": 6.06}  # .

        self.RGW35HC_dict = {"组件尺寸(mm)": " ", "H": 48, "H1": 6.5, "N": 33,
                             "滑块尺寸(mm)": " ", "W": 100, "B": 82, "B1": 9, "C": "62","C1": "52", "L1": 106.5, "L": 151.5,
                             "K1": 30.25,
                             "K2": 10,
                             "G": "12",
                             "M": "M10", "T": 12, "T1": 13, "H2": 9, "H3": 12.6,
                             "滑轨(mm)": " ", "WR": 34, "HR": 30.2, "D": "14", "h": 12, "d": 9, "P": 40, "E": 20,
                             "滑轨螺栓尺寸": "M8X25", "基本动额定负载": "73.1",
                             "基本静额定负载": "142",
                             "容许静力矩": "", "MR": "2.93", "MP": "2.6", "MY": "2.6",
                             "重量": "", "滑块（kg）": 2.21, "滑轨": 6.06}  # .

        self.RGW45CC_dict = {"组件尺寸(mm)": " ", "H": 60, "H1": 8, "N": 37.5,
                             "滑块尺寸(mm)": " ", "W": 120, "B": 100, "B1": 10, "C": "80","C1": "60", "L1": 106, "L": 153.2,
                             "K1": 21,
                             "K2": 10,
                             "G": "12",
                             "M": "M12", "T": 14, "T1": 15,"H2": 10, "H3": 14,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 52.5, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "92.6",
                             "基本静额定负载": "178.8",
                             "容许静力矩": "", "MR": "4.52", "MP": "3.05", "MY": "3.05",
                             "重量": "", "滑块（kg）": 3.22, "滑轨": 9.97}  # .

        self.RGW45HC_dict = {"组件尺寸(mm)": " ", "H": 60, "H1": 8, "N": 37.5,
                             "滑块尺寸(mm)": " ", "W": 120, "B": 100, "B1": 10, "C": "80","C1": "60", "L1": 139.8, "L": 187,
                             "K1": 37.9,
                             "K2": 10,
                             "G": "12",
                             "M": "M12", "T": 14, "T1": 15,"H2": 10, "H3": 14,
                             "滑轨(mm)": " ", "WR": 45, "HR": 38, "D": "20", "h": 17, "d": 14, "P": 52.5, "E": 22.5,
                             "滑轨螺栓尺寸": "M12X35", "基本动额定负载": "116",
                             "基本静额定负载": "230.9",
                             "容许静力矩": "", "MR": "6.33", "MP": "5.47", "MY": "5.47",
                             "重量": "", "滑块（kg）": 4.41, "滑轨": 9.97}  # .

        self.RGW55CC_dict = {"组件尺寸(mm)": " ", "H": 70, "H1": 10, "N": 43.5,
                             "滑块尺寸(mm)": " ", "W": 140, "B": 116, "B1": 12, "C": "95","C1": "70", "L1": 125.5, "L": 183.7,
                             "K1": 27.75,
                             "K2": 12.5,
                             "G": "12.9",
                             "M": "M14", "T": 16,"T1": 17, "H2": 12, "H3": 17.5,
                             "滑轨(mm)": " ", "WR": 53, "HR": 44, "D": "23", "h": 20, "d": 14, "P": 60, "E":30,
                             "滑轨螺栓尺寸": "M14X45", "基本动额定负载": "130.5",
                             "基本静额定负载": "252",
                             "容许静力矩": "", "MR": "8.01", "MP": "5.4", "MY": "5.4",
                             "重量": "", "滑块（kg）": 5.18, "滑轨": 13.98}  # .

        self.RGW55HC_dict = {"组件尺寸(mm)": " ", "H": 70, "H1": 10, "N": 43.5,
                             "滑块尺寸(mm)": " ", "W": 140, "B": 116, "B1": 12, "C": "95","C1": "70", "L1": 173.8, "L": 232,
                             "K1": 27.75,
                             "K2": 12.5,
                             "G": "12.9",
                             "M": "M14", "T": 16,"T1": 17, "H2": 12, "H3": 17.5,
                             "滑轨(mm)": " ", "WR": 53, "HR": 44, "D": "23", "h": 20, "d": 14, "P": 60, "E":30,
                             "滑轨螺栓尺寸": "M14X45", "基本动额定负载": "167.8",
                             "基本静额定负载": "348",
                             "容许静力矩": "", "MR": "11.15", "MP": "10.25", "MY": "10.25",
                             "重量": "", "滑块（kg）": 7.34, "滑轨": 13.98}  # .

        self.RGW65CC_dict = {"组件尺寸(mm)": " ", "H": 90, "H1": 12, "N": 53.5,
                             "滑块尺寸(mm)": " ", "W": 170, "B": 142, "B1": 14, "C": "110","C1": "82", "L1": 160, "L": 232,
                             "K1": 40.8,
                             "K2": 15.8,
                             "G": "12.9",
                             "M": "M16", "T": 22,"T1": 23, "H2": 15, "H3": 15,
                             "滑轨(mm)": " ", "WR": 63, "HR": 53, "D": "26", "h": 22, "d": 18, "P": 75, "E": 35,
                             "滑轨螺栓尺寸": "M16X50", "基本动额定负载": "213",
                             "基本静额定负载": "411.6",
                             "容许静力矩": "", "MR": "16.20", "MP": "11.59", "MY": "11.59",
                             "重量": "", "滑块（kg）": 11.04, "滑轨": 20.22}  # .

        self.RGW65HC_dict = {"组件尺寸(mm)": " ", "H": 90, "H1": 12, "N": 53.5,
                             "滑块尺寸(mm)": " ", "W": 170, "B": 142, "B1": 14, "C": "110","C1": "82", "L1": 223, "L": 295,
                             "K1": 72.3,
                             "K2": 15.8,
                             "G": "12.9",
                             "M": "M16", "T": 22,"T1": 23, "H2": 15, "H3": 15,
                             "滑轨(mm)": " ", "WR": 63, "HR": 53, "D": "26", "h": 22, "d": 18, "P": 75, "E": 35,
                             "滑轨螺栓尺寸": "M16X50", "基本动额定负载": "275.3",
                             "基本静额定负载": "572.7",
                             "容许静力矩": "", "MR": "22.55", "MP": "22.17", "MY": "22.17",
                             "重量": "", "滑块（kg）": 15.75, "滑轨": 20.22}  # .



        self.RGW_series_dict = {"RGW25CC":self.RGW25CC_dict,"RGW25HC":self.RGW25HC_dict,"RGW30CC":self.RGW30CC_dict,
                                "RGW30HC":self.RGW30HC_dict,"RGW35CC":self.RGW35CC_dict,"RGW35HC":self.RGW35HC_dict,
                                "RGW45CC":self.RGW45CC_dict,"RGW45HC":self.RGW45HC_dict,"RGW55CC":self.RGW55CC_dict,
                                "RGW55HC":self.RGW55HC_dict,"RGW65CC":self.RGW65CC_dict,"RGW65HC":self.RGW65HC_dict}

        self.series = self.RGW_series_dict



    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["","25" ,"30","35","45","55","65"]}  #
        all_combox_list.append(["滑轨", "滚柱式"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["W:法兰型"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷","H:超重负荷 "]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "C:上或下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Liner_guide_QEH(Create_Liner_guide_EGH):
    pass
    def __init__(self):
        pass
        self.QEH15SA_dict = {"组件尺寸(mm)": " ", "H": 24, "H1": 4, "N": 9.5,
                             "滑块尺寸(mm)": " ", "W": 34, "B": 26, "B1": 4, "C": "-", "L1": 23.1, "L": 40.1,"K1":14.8,
                             "G": "5.7",
                             "MXL": "M4X6", "T": 6,"H2": 5.5, "H3": 6,
                             "滑轨(mm)": " ", "WR": 15, "HR": 12.5,"D": "6", "h": 4.5, "d": 3.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M3X16", "基本动额定负载": "8.56",
                             "基本静额定负载": "8.79",
                             "容许静力矩": "", "MR": "0.07", "MP": "0.03", "MY": "0.03",
                             "重量": "", "滑块（kg）": 0.09, "滑轨": 1.25}  #

        self.QEH15CA_dict = {"组件尺寸(mm)": " ", "H": 24, "H1": 4, "N": 9.5,
                             "滑块尺寸(mm)": " ", "W": 34, "B": 26, "B1": 4, "C": "26", "L1": 39.8, "L": 56.8, "K1": 10.15,
                             "G": "5.7",
                             "MXL": "M4X6", "T": 6, "H2": 5.5, "H3": 6,
                             "滑轨(mm)": " ", "WR": 15, "HR": 12.5, "D": "6", "h": 4.5, "d": 3.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M3X16", "基本动额定负载": "12.53",
                             "基本静额定负载": "15.28",
                             "容许静力矩": "", "MR": "0.12", "MP": "0.09", "MY": "0.09",
                             "重量": "", "滑块（kg）": 0.15, "滑轨": 1.25}  #

        self.QEH20SA_dict = {"组件尺寸(mm)": " ", "H": 28, "H1": 6, "N": 11,
                             "滑块尺寸(mm)": " ", "W": 42, "B": 32, "B1": 5, "C": "-", "L1": 29, "L": 50, "K1": 18.75,
                             "G": "12",
                             "MXL": "M5X7", "T": 7.5, "H2": 6, "H3": 6.5,
                             "滑轨(mm)": " ", "WR": 20, "HR": 15.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "11.57",
                             "基本静额定负载": "12.18",
                             "容许静力矩": "", "MR": "0.13", "MP": "0.05", "MY": "0.05",
                             "重量": "", "滑块（kg）": 0.15, "滑轨": 0.28}  #

        self.QEH20CA_dict = {"组件尺寸(mm)": " ", "H": 28, "H1": 6, "N": 11,
                             "滑块尺寸(mm)": " ", "W": 42, "B": 32, "B1": 5, "C": "32", "L1": 48.1, "L": 69.1, "K1": 12.3,
                             "G": "12",
                             "MXL": "M5X7", "T": 7.5, "H2": 6, "H3": 6.5,
                             "滑轨(mm)": " ", "WR": 20, "HR": 15.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "16.50",
                             "基本静额定负载": "20.21",
                             "容许静力矩": "", "MR": "0.21", "MP": "0.15", "MY": "0.15",
                             "重量": "", "滑块（kg）": 0.23, "滑轨": 0.28}  #

        self.QEH25SA_dict = {"组件尺寸(mm)": " ", "H": 33, "H1": 6.2, "N": 12.5,
                             "滑块尺寸(mm)": " ", "W": 48, "B": 35, "B1": 6.5, "C": "-", "L1": 36.5, "L": 60.1, "K1": 21.9,
                             "G": "12",
                             "MXL": "M6X9", "T": 8, "H2": 8, "H3": 8,
                             "滑轨(mm)": " ", "WR": 23, "HR": 18, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "18.24",
                             "基本静额定负载": "18.90",
                             "容许静力矩": "", "MR": "0.22", "MP": "0.10", "MY": "0.10",
                             "重量": "", "滑块（kg）": 0.24, "滑轨": 2.67}  #

        self.QEH25CA_dict = {"组件尺寸(mm)": " ", "H": 33, "H1": 6.2, "N": 12.5,
                             "滑块尺寸(mm)": " ", "W": 48, "B": 35, "B1": 6.5, "C": "35", "L1": 59, "L": 83.6, "K1": 16.15,
                             "G": "12",
                             "MXL": "M6X9", "T": 8, "H2": 8, "H3": 8,
                             "滑轨(mm)": " ", "WR": 23, "HR": 18, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "26.03",
                             "基本静额定负载": "31.49",
                             "容许静力矩": "", "MR": "0.37", "MP": "0.29", "MY": "0.29",
                             "重量": "", "滑块（kg）": 0.40, "滑轨": 2.67}  #

        self.QEH30SA_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 10, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 60, "B": 40, "B1": 10, "C": "-", "L1": 41.5, "L": 67.5, "K1": 25.75,
                             "G": "12",
                             "MXL": "M8X12", "T": 9, "H2": 8, "H3": 9,
                             "滑轨(mm)": " ", "WR": 28, "HR": 23, "D": "11", "h": 9, "d": 7, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "26.27",
                             "基本静额定负载": "27.82",
                             "容许静力矩": "", "MR": "0.40", "MP": "0.18", "MY": "0.18",
                             "重量": "", "滑块（kg）": 0.44, "滑轨": 4.35}  #

        self.QEH30CA_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 10, "N": 16,
                             "滑块尺寸(mm)": " ", "W": 60, "B": 40, "B1": 10, "C": "40", "L1": 70.1, "L": 96.1, "K1": 20.05,
                             "G": "12",
                             "MXL": "M8X12", "T": 9, "H2": 8, "H3": 9,
                             "滑轨(mm)": " ", "WR": 28, "HR": 23, "D": "11", "h": 9, "d": 7, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "37.92",
                             "基本静额定负载": "46.63",
                             "容许静力矩": "", "MR": "0.67", "MP": "0.51", "MY": "0.51",
                             "重量": "", "滑块（kg）": 0.75, "滑轨": 4.35}  #




        self.QEH_series_dict = {"QEH15SA":self.QEH15SA_dict,"QEH15CA":self.QEH15CA_dict,"QEH20SA":self.QEH20SA_dict,
                                "QEH20CA":self.QEH20CA_dict,"QEH25SA":self.QEH25SA_dict,"QEH25CA":self.QEH25CA_dict,
                                "QEH30SA":self.QEH30SA_dict,"QEH30CA":self.QEH30CA_dict}

        self.series = self.QEH_series_dict



    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["","15" ,"20","25","30"]}  #
        all_combox_list.append(["滑轨", "静音式"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["H:四方型"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷","S:中负荷 "]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "B:下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list

class Create_Liner_guide_QEW(Create_Liner_guide_EGH):
    pass
    def __init__(self):
        pass
        self.QEW15SB_dict = {"组件尺寸(mm)": " ", "H": 24, "H1": 4, "N": 18.5,
                             "滑块尺寸(mm)": " ", "W": 52, "B": 41, "B1": 5.5, "C": "-", "L1": 23.1, "L": 40.1,
                             "G": "14.8",
                             "M": "5.7", "T": "Φ4.5","T1": "5","T2": "7","H2": 5.5, "H3": 6,
                             "滑轨(mm)": " ", "WR": 15, "HR": 12.5,"D": "6", "h": 4.5, "d": 3.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M3X16", "基本动额定负载": "8.56",
                             "基本静额定负载": "8.79",
                             "容许静力矩": "", "MR": "0.07", "MP": "0.03", "MY": "0.03",
                             "重量": "", "滑块（kg）": 0.12, "滑轨": 1.25}  #

        self.QEW15CB_dict = {"组件尺寸(mm)": " ", "H": 24, "H1": 4, "N": 18.5,
                             "滑块尺寸(mm)": " ", "W": 52, "B": 41, "B1": 5.5, "C": "26", "L1": 39.8, "L": 56.8,
                             "G": "10.15",
                             "M": "5.7", "T": "Φ4.5","T1": "5","T2": "7","H2": 5.5, "H3": 6,
                             "滑轨(mm)": " ", "WR": 15, "HR": 12.5,"D": "6", "h": 4.5, "d": 3.5, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M3X16", "基本动额定负载": "12.53",
                             "基本静额定负载": "15.28",
                             "容许静力矩": "", "MR": "0.12", "MP": "0.09", "MY": "0.09",
                             "重量": "", "滑块（kg）": 0.21, "滑轨": 1.25}  #

        self.QEW20SB_dict = {"组件尺寸(mm)": " ", "H": 28, "H1": 6, "N": 19.5,
                             "滑块尺寸(mm)": " ", "W": 59, "B": 49, "B1": 5, "C": "-", "L1": 29, "L": 50, "G": 18.75,
                             "M": "12", "T": "Φ5.5", "T1": "7","T2": "9","H2": 6, "H3": 6.5,
                             "滑轨(mm)": " ", "WR": 20, "HR": 15.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "11.57",
                             "基本静额定负载": "12.18",
                             "容许静力矩": "", "MR": "0.13", "MP": "0.05", "MY": "0.05",
                             "重量": "", "滑块（kg）": 0.19, "滑轨": 0.28}  #

        self.QEW20CB_dict = {"组件尺寸(mm)": " ", "H": 28, "H1": 6, "N": 19.5,
                             "滑块尺寸(mm)": " ", "W": 59, "B": 49, "B1": 5, "C": "32", "L1": 48.1, "L": 69.1, "G": 12.3,
                             "M": "12", "T": "Φ5.5", "T1": "7","T2": "9","H2": 6, "H3": 6.5,
                             "滑轨(mm)": " ", "WR": 20, "HR": 15.5, "D": "9.5", "h": 8.5, "d": 6, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "16.50",
                             "基本静额定负载": "20.21",
                             "容许静力矩": "", "MR": "0.21", "MP": "0.15", "MY": "0.15",
                             "重量": "", "滑块（kg）": 0.31, "滑轨": 0.28}  #

        self.QEW25SB_dict = {"组件尺寸(mm)": " ", "H": 33, "H1": 6.2, "N": 25,
                             "滑块尺寸(mm)": " ", "W": 73, "B": 60, "B1": 6.5, "C": "-", "L1": 36.5, "L": 60.1,
                             "G": "21.9",
                             "M": "12", "T": "Φ7","T1": "7.5","T2": "10", "H2": 8, "H3": 8,
                             "滑轨(mm)": " ", "WR": 23, "HR": 18, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "18.24",
                             "基本静额定负载": "18.90",
                             "容许静力矩": "", "MR": "0.22", "MP": "0.10", "MY": "0.10",
                             "重量": "", "滑块（kg）": 0.34, "滑轨": 2.67}  #

        self.QEW25CB_dict = {"组件尺寸(mm)": " ", "H": 33, "H1": 6.2, "N": 25,
                             "滑块尺寸(mm)": " ", "W": 73, "B": 60, "B1": 6.5, "C": "35", "L1": 59, "L": 83.6,
                             "G": "16.15",
                             "M": "12", "T": "Φ7","T1": "7.5","T2": "10", "H2": 8, "H3": 8,
                             "滑轨(mm)": " ", "WR": 23, "HR": 18, "D": "11", "h": 9, "d": 7, "P": 60, "E": 20,
                             "滑轨螺栓尺寸": "M6X20", "基本动额定负载": "20.63",
                             "基本静额定负载": "31.49",
                             "容许静力矩": "", "MR": "037", "MP": "0.29", "MY": "0.29",
                             "重量": "", "滑块（kg）": 0.58, "滑轨": 2.67}  #

        self.QEW30SB_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 10, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "-", "L1": 41.5, "L": 67.5,
                             "G": "25.75",
                             "M": "12", "T":"Φ9", "T1":"7","T2":"10","H2": 8, "H3": 9,
                             "滑轨(mm)": " ", "WR": 28, "HR": 23, "D": "11", "h": 9, "d": 7, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "26.27",
                             "基本静额定负载": "27.82",
                             "容许静力矩": "", "MR": "0.40", "MP": "0.18", "MY": "0.18",
                             "重量": "", "滑块（kg）": 0.61, "滑轨": 4.35}  #

        self.QEW30CB_dict = {"组件尺寸(mm)": " ", "H": 42, "H1": 10, "N": 31,
                             "滑块尺寸(mm)": " ", "W": 90, "B": 72, "B1": 9, "C": "40", "L1": 70.1, "L": 96.1,
                             "G": "20.05",
                             "M": "12", "T":"Φ9", "T1":"7","T2":"10","H2": 8, "H3": 9,
                             "滑轨(mm)": " ", "WR": 28, "HR": 23, "D": "11", "h": 9, "d": 7, "P": 80, "E": 20,
                             "滑轨螺栓尺寸": "M5X16", "基本动额定负载": "37.92",
                             "基本静额定负载": "46.63",
                             "容许静力矩": "", "MR": "0.67", "MP": "0.51", "MY": "0.51",
                             "重量": "", "滑块（kg）": 1.03, "滑轨": 4.35}  #





        self.QEW_series_dict = {"QEW15SB":self.QEW15SB_dict,"QEW15CB":self.QEW15CB_dict,"QEW20SB":self.QEW20SB_dict,
                                "QEW20CB":self.QEW20CB_dict,"QEW25SB":self.QEW25SB_dict,"QEW25CB":self.QEW25CB_dict,
                                "QEW30SB":self.QEW30SB_dict,"QEW30CB":self.QEW30CB_dict
                                }

        self.series = self.QEW_series_dict



    def Create_combox_list(self):
        combox_list = []  # 单个选型的列,
        all_combox_list = []  # 所有不同选项的列表
        for i in self.series.keys():
            combox_list.append(i)
        combox_list.insert(0, "  ")  # 导轨高度列表
        dict_combox = {"滑块型号": ["","15" ,"20","25","30"]}  #
        all_combox_list.append(["滑轨", "静音式"])
        all_combox_list.append(["组装高度", "-"])
        all_combox_list.append(["硬度", "58～62HRC"])
        all_combox_list.append(["滑轨材料", "S55C"])
        all_combox_list.append(["滑块材料", "SCM420"])
        all_combox_list.append(["精度等级", "普通"])
        all_combox_list.append(dict_combox)  # 导轨高度列表
        all_combox_list.append({"滑块型式": ["W:法兰型"]})
        all_combox_list.append({"负荷型式": ["  ", "C:重负荷","S:中负荷 "]})
        all_combox_list.append({"滑块固定方式": ["  ", "A:上锁式 ", "B:下锁式"]})
        all_combox_list.append(["滑轨长度L(mm)", "-"])
        all_combox_list.append(["订货代码", ""])
        return all_combox_list
