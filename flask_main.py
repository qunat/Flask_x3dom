#-*-coding:UTF-8 -*-
from OCC.Display.WebGl import x3dom_renderer
from flask import Flask, redirect, url_for, request,send_from_directory,render_template
import os
from module import core_modeling_sprocket
app = Flask(__name__,static_folder="./static")

@app.route("/",methods = ['GET', 'POST'])
def index():
   return render_template("index.html")

@app.route("/order_name",methods = ['GET', 'POST'])

def receive_order():
   order_name=request.args["name"]
   order_name=order_name+".x3d"
   basedir = os.path.abspath(os.path.dirname(__file__))
   all_name_path=os.path.join("../static/resource",order_name,).replace("\\","/")
   #通过url访问 本地目录为html所在的目录
   print(all_name_path)
   return render_template("index.html",
                        order_name=all_name_path)

@app.route("/sprocket",methods = ['GET', 'POST'])
def exchange_to_show_web():
   shape=core_modeling_sprocket.build_sprocket()#生成链轮
   my_renderer = x3dom_renderer.X3DomRenderer("./static/resource")#指定存储该目录
   my_renderer.DisplayShape(shape,  export_edges=True, file_name="sprocket")#转换成想x3d,存储到该目录下
   all_name_path = os.path.join("../static/resource", "sprocket.x3d", ).replace("\\", "/")
   return render_template("index.html",
                          order_name=all_name_path)#生成htnl 显示3D



if __name__ == '__main__':
   app.run(host="172.18.5.130",port=9090,threaded=True)
