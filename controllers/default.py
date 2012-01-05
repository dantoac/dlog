# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

if 0:
    from gluon.dal import *
    from gluon.html import *
    from gluon.globals import *
    session = Session
    request = Request
    response = Response
    db = DAL

response.files.insert(len(response.files), URL('static', 'css/last.css'))

from menucontext import MenuContext
menuadds = MenuContext(db)
response.menu += menuadds.menudocs()
response.menu += menuadds.menupags()

response.title = 'dantoac'
response.subtitle = 'be-log'

def index():

    try:
        data = db((db.context.place == db.place.id)
                & (db.context.post == db.post.id)
                & (db.place.name == 'blogpost')
                & (db.post.is_active == True)
                ).select(
                db.post.id,
                db.post.slug,
                db.context.priority,
                cache=(cache.disk, 600)
                )


        for d in data:

            if d.context.priority==0:
                frontpage = LOAD(c='post',f='read.load',args=[d.post.id,d.post.slug],target='post')
                break

            else:
                frontpage = LOAD(c='post',f='read.load',args=[d.post.id,d.post.slug],target='post')


    except Exception,e:
        frontpage = 'frontpage error'

    return dict(frontpage=frontpage)

def user():

    """
    exposes:
      http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form = auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id[
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form = crud())

