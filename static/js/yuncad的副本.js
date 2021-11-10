/*!
 * yuncad v1.0
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under the MIT license
 */
function Create_dateil(){
    var ls_col_md_4=document.createElement("div");
    document.getElementById("id1").appendChild(ls_col_md_4);//增加加点ls_col_md_4
    ls_col_md_4.setAttribute("class","col-md-4");

    var ls_thumbnail=document.createElement("div");
    ls_col_md_4.appendChild(ls_thumbnail);//增加加点ls_thumbnail
    ls_thumbnail.setAttribute("class","thumbnail");//增加属性
    ls_thumbnail.style.borderColor="red";

    var ls_img=document.createElement("img");
    ls_thumbnail.appendChild(ls_img);
    ls_img.setAttribute("alt","300x200");
    ls_img.setAttribute("src","../static/img/3D.jpg");

    var ls_caption=document.createElement("div");
    ls_thumbnail.appendChild(ls_caption)
    ls_caption.setAttribute("class","caption")

    ls_h3=document.createElement("h3");
    ls_text=document.createTextNode("激光打标机")
    ls_h3.appendChild(ls_text)
    ls_caption.appendChild(ls_h3)

    var ls_p1=document.createElement("p");
    ls_text=document.createTextNode("Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.");
    ls_p1.appendChild(ls_text);
    ls_caption.appendChild(ls_p1)

    var ls_p2=document.createElement("p");
    ls_caption.appendChild(ls_p2);
    ls_a=document.createElement("a");
    ls_p2.appendChild(ls_a)
    ls_a.setAttribute("class","btn btn-primary")
    ls_a.setAttribute("href","http://www.aliyuncad.com:9090/index1.html")
    ls_text=document.createTextNode("浏览")
    ls_a.appendChild(ls_text)

    ls_a=document.createElement("a");
    ls_p2.appendChild(ls_a)
    ls_a.setAttribute("class","btn  ")
    ls_a.setAttribute("href","#")
    ls_text=document.createTextNode("下载")
    ls_a.appendChild(ls_text)
    }
    
    Create_dateil()