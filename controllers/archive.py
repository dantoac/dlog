# -*- coding: utf-8 -*-

def index():
    data = db(db.post.id>0).select(
        #db.post.title,
        #1db.post.id,
        db.post.created_on,
        orderby =~ db.post.created_on,
        )

    listado = UL()

    for p in data:
        archived = []

        
        listado.append(LI(p.created_on.date(),_title='Función de Archivador: Incompleto'))
        
    return dict(listado = listado)


class archive:
    """archivador de post"""
    
