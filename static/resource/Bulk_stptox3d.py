# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 08:29:23 2020

@author: Administrator
"""
from urllib import request

from OCC.Display.WebGl import x3dom_renderer
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Solid, TopoDS_Builder, TopoDS_Compound
from OCC.Core.BRepTools import breptools_Read
from OCC.Extend.DataExchange import read_step_file


from OCC.Display.SimpleGui import init_display
from OCC.Core.TopoDS import topods_Edge
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.OCCViewer import rgb_color
from OCC.Core.AIS import AIS_ColoredShape
from random import random
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.Quantity import Quantity_Color,Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
import os
import socket
import webbrowser
import errno
from flask import Flask, redirect, url_for, request,send_from_directory
from flask import Flask, render_template
import sys
import assemble

#display, start_display, add_menu, add_function_to_menu = init_display()
#context = display.Context


class Bulk_stptox3d(object):
    def __init__(self,path="."):
        path=os.getcwd()
        self.file_list=os.listdir(path)#返回指定目录下的所有文件和目录名
       
        
    def Exchange_stp_3xd(self,mode=0):
        try:
            if mode==0:
                for file in self.file_list:
                    if file.lower().endswith("stp") or file.lower().endswith("step") or file.lower().endswith("iges"):
                        try:
                            the_shape = read_step_file(file)
                            my_renderer = x3dom_renderer.X3DomRenderer("./")
                            name = file.split(".")
                            my_renderer.DisplayShape(the_shape, export_edges=True, color=(random(), random(), random()),
                                                     file_name=name[0])


                        except:
                            pass
            elif mode==1:
                for file in self.file_list:
                    if file.lower().endswith("stp") or file.lower().endswith("step") or file.lower().endswith("iges"):
                        try:
                            dir = file.split(".")[0]
                            os.mkdir(dir)
                            my_renderer = x3dom_renderer.X3DomRenderer(dir)
                            self.shape_property_dic = {}
                            shapes_labels_colors, assemble_relation_list = assemble.read_step_file_with_names_colors(
                                file)
                            num = 0

                            for shpt_lbl_color in shapes_labels_colors:
                                label, c, property = shapes_labels_colors[shpt_lbl_color]
                                color = (c.Red(), c.Green(), c.Blue())
                                if isinstance(shpt_lbl_color, TopoDS_Solid):
                                    self.shape_property = []
                                    self.shape_property.append(shpt_lbl_color)
                                    self.shape_property.append(color)
                                    name = property["name"]
                                    print(name)
                                    if name in self.shape_property_dic:
                                        name = name + "_" + str(num)
                                        num += 1
                                    print(name)
                                    self.shape_property_dic[name] = self.shape_property
                                    my_renderer.DisplayShape(shpt_lbl_color, color=color, export_edges=True,
                                                             file_name=name)

                        except Exception as e:
                            print(e)


        except Exception as e:
            pass
            print(e)
   
        
        
if __name__ == '__main__':
    pass
    
    new_Bulk_stptox3d=Bulk_stptox3d()
    new_Bulk_stptox3d.Exchange_stp_3xd()
    sys.exit()

   
