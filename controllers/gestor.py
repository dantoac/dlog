# -*- coding: utf-8 -*-
response.files.append(URL('static','css/last.css'))

def index():
    #data = db(db.post.id>0).select(db.post.id,db.post.title,db.post.is_active,db.post.static)
    #table = SQLTABLE(data,linkto=URL(c='content',f='post.html'))
    table = LOAD(r=request,c='widget',f='postlist.load',ajax=False,target='gestor',_class='ui-widget-content ui-corner-all')
    return dict(table=table)


def post():
    data = db(db.post.id>0).select(db.post.id,db.post.title,db.post.is_active,db.post.static)

    
    lista = UL()
    for d in data:
        lista.append(LI(A(d.title, _href=URL(c='content',f='post.html',args=['edit',d.id])),d.static))
    

    
    return dict(lista=lista)
