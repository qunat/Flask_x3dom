import logging
#import requests
import time
from OCC.Extend.DataExchange import read_step_file, write_step_file
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Builder, TopoDS_Compound, topods_CompSolid, TopoDS_Edge
from OCC.Extend.DataExchange import read_iges_file, read_step_file, read_stl_file, write_step_file, write_stl_file, \
    write_iges_file
from CreateParameter import *
import re
import random


class CADcreatorClass():
    def __init__(self):
        self.new_Create_boll_SCcrew_sfu = Create_boll_SCcrew_sfu()
    def Translation_Assemble(self):  # 转换为装配体
        try:
            self.new_build = TopoDS_Builder()  # 建立一个TopoDS_Builder()
            self.New_Compound = TopoDS_Compound()  # 定义一个复合体
            self.new_build.MakeCompound(self.New_Compound)  # 生成一个复合体DopoDS_shape
            for shape in self.aCompound:
                self.new_build.Add(self.New_Compound, shape)
            self.aCompound = self.New_Compound
        except Exception as e:
            pass
            print(e)
            
            
            
    def Output_stp_data(self,filename,series,fixted_side,support_side,trip_distance):  # 将数据转换成stp并导出
        try:
            self.aCompound = TopoDS_Compound()
            self.series=series
            if "BF" in support_side:
                    D=int(12)#获取螺杆公称直径
                    BF_series={12:"BF10",14:["BF10","BF12"],15:["BF10","BF12"],16:"BF12",18:"BF15",
                               20:["BF15","BF17"],25:["BF17","BF20"],28:"BF20",32:"BF25",36:["BF25","BF30"],
                               40:["BF30","BF35"],45:"BF35",50:["BF35","BF40"],55:"BF40"}
                    if  isinstance(BF_series[D],list):
                        F_type=random.choice(BF_series[D])
                    else:
                        F_type=BF_series[D]

            elif "EF" in support_side:
                    D = int(series[3:6])  # 获取螺杆公称直径
                    EF_series = {6: "EF6", 8:"EF6", 10:"EF8", 12: ["EF8","EF10"],14:["EF10","EF12"],15:["EF10","EF12"],
                                 16:"EF12",18:"EF15",20:"EF15",25:"EF20",28:"EF20",32:"EF25",36:"EF25"}
                    if isinstance(EF_series[D], list):
                        F_type = random.choice(EF_series[D])
                    else:
                        F_type = EF_series[D]

            elif "FF" in support_side:
                    D = int(series[3:6])  # 获取螺杆公称直径
                    FF_series = {10: "FF6", 12: ["FF6","FF10"],14:["FF10","FF12"],15:["FF10","FF12"],16:"FF12",18:"FF15",
                                 20:"FF15",25:"FF20",28:"FF20",32:"FF25",36:"FF25",40:"FF30",50:"FF50"}
                    if isinstance(FF_series[D], list):
                        F_type = random.choice(FF_series[D])
                    else:
                        F_type = FF_series[D]
            
            if "BK" in fixted_side:
                    print('进入了BK',filename,trip_distance,F_type)
                    self.aCompound = self.new_Create_boll_SCcrew_sfu.Create_Bk(filename=series, L=trip_distance,suppor_side_type=F_type)
            elif "EK" in fixted_side:
                    print('进入了EK',filename,trip_distance,F_type)
                    self.aCompound = self.new_Create_boll_SCcrew_sfu.Create_Ek(filename=series, L=trip_distance,suppor_side_type=F_type)
            elif "FK" in fixted_side:
                    print('进入了FK',filename,trip_distance,F_type)
                    self.aCompound = self.new_Create_boll_SCcrew_sfu.Create_Fk(filename=series, L=trip_distance,suppor_side_type=F_type)
            
            
            
            #print(55555,self.aCompound)
            self.Translation_Assemble()
            newfilename = series
            #print('filename',series)
            #print('aCompound',self.aCompound)
            #path = "./" + self.filename
            #fileName, ok = QFileDialog.getSaveFileName(self, "文件保存", path, "All Files (*) (*.step)")
            write_step_file(self.aCompound, newfilename + '.step')
            CADcreatorClass().step_rename(newfilename + '.step')
       
            return newfilename

        except:
            pass
            #self.statusbar.showMessage("错误：没用模型可以导出")

    def step_rename(self,filename):
        try:
            Part_NO = 0
            with open(filename, "r") as f:
                words = f.read()
                f.close()
            p = re.compile(r"Open CASCADE STEP translator 7.5 \d{1,2}") # h获取子装配体名称
            assemble_part_name_list = p.findall(words)
            for i in range(0, (len(assemble_part_name_list)), 2):
                pass
                new_name = "my test-" + str(Part_NO)
                words = words.replace(assemble_part_name_list[i], new_name)
                Part_NO += 1
            with open(filename, "w+") as f:  # 重新写入stp
                f.write(words)
                f.close()
                # print("succeed")
        except:
            pass
    

    def return_json(self):
        pass
        return self.new_Create_boll_SCcrew_sfu.series[self.series]