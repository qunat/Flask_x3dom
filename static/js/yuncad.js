/*!
 * yuncad v1.0
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under the MIT license
 */
function Create_dateil(filename){
    var ls_col_md_4=document.createElement("Inline");
    document.getElementById("glbal_scene_rotation_Id").appendChild(ls_col_md_4);//增加加点ls_col_md_4
    ls_col_md_4.setAttribute("onload","fitCamera()");
    ls_col_md_4.setAttribute("mapDEFToID","true");
    ls_col_md_4.setAttribute("url",filename);
    }
    
    Create_dateil()