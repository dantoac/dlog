# -*- coding: utf-8 -*-

from gluon import *

if request.is_local:
    from gluon.custom_import import track_changes
    track_changes()


# documentos
data = db((db.post.id == db.content_position.post) & (db.content_position.place == db.place.id) & (db.post.is_active == True) & (db.place.name == 'documento')).select(db.post.id, db.post.title, db.content_position.priority, orderby = db.content_position.priority)
meta_menudocumentos = []

for d in data:
    meta = (d.post.title, None, URL(c = 'content', f = 'read.html', args = [d.post.title, d.post.id]))
    meta_menudocumentos.append(meta)

menudocumentos = [(T('Documentos'), False, None, meta_menudocumentos)]
response.menu += menudocumentos
