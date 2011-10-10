# -*- coding: utf-8 -*-

from gluon import *

class MenuContext(object):
    """
    Agrega nuevos ítems de menú según la contextualización
    del post.

    Se define:
    - menupags = lista de post de contexto "páginas"
    - menudocs = lista de post de context "documentos"

    Para usarlo desde un controlador basta importar la clase y
    pasarle como parámetro el objeto de la base de datos:

        from menucontext import MenuContext
        var = MenuContext(db)

    y luego agregar al menu como es usual:
        
        response.menu += var.menupags()
        response.menu += var.menudocs()
    """
    def __init__(self,db):
        self.db = db


    def menudocs(self):
        """
        Forma una lista de post de contexto "documento" en formato listo para usar con el objeto helper MENU() de web2py.
        Creará en el menú un ítem "Documentos" y en ella anidará los post que le correspondan al contexto.
        """
        db = self.db

        data = db((db.post.id == db.context.post) & (db.context.place == db.place.id) & (db.post.is_active == True) & (db.place.name == 'documento')).select(db.post.id, db.post.title, db.context.priority, orderby = db.context.priority)
        meta_menudocumentos = []

        for d in data:
            meta = (d.post.title, None, URL(c = 'post', f = 'read.html', args = [d.post.id,d.post.title]))
            meta_menudocumentos.append(meta)

        menudocumentos = [('Documentos', False, None, meta_menudocumentos)]

        #return dict(menudocumentos=menudocumentos)
        #response.menu += menudocumentos

        return menudocumentos


    def menupags(self):
        """
        Forma una lista de post de contexto "página" en formato listo para usar con el objeto helper MENU() de web2py.
        Las páginas se agregarán una a una al menú como ítems separados e independientes.
        """
        db = self.db

        data = db((db.post.id == db.context.post) & (db.context.place == db.place.id) & (db.post.is_active == True) & (db.place.name == 'página')).select(db.post.id, db.post.title, db.context.priority, orderby = db.context.priority)

        menupaginas = []

        for d in data:
            menupaginas += [(d.post.title, None, URL(c = 'post', f = 'read.html', args = [d.post.id,d.post.title]))]

        #response.menu += [menupaginas]
        return menupaginas
        
