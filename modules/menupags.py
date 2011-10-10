# -*- coding: utf-8 -*-

from gluon import *

if request.is_local:
    from gluon.custom_import import track_changes
    track_changes()


#páginas
data = db((db.post.id == db.content_position.post) & (db.content_position.place == db.place.id) & (db.post.is_active == True) & (db.place.name == 'página')).select(db.post.id, db.post.title, db.content_position.priority, orderby = db.content_position.priority)
meta_menudocumentos = []

for d in data:
    menupaginas = [(d.post.title, None, URL(c = 'content', f = 'read.html', args = [d.post.title, d.post.id]))]
    #menupaginas.sort()
    response.menu += menupaginas
