# -*- coding: utf-8 -*-

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

if 0:
    from gluon import *
    from gluon.tools import Auth
    session = current.session
    request = current.request
    response = current.response
    T = current.T
    auth = Auth
    db = DAL

table = db.define_table

table('place',
      Field('name'),
          #ejemplo: sidebar, header, etc
      format='%(name)s'
      )

table('markup',
      Field('name', 'string'), # ejemplo: markmin, xml, etc
      format = '%(name)s'
      )


#if db.markup[1] and db.markup[2] == None:
#    db.markup.bulk_insert([{'name':'markmin'}, {'name':'html'}, {'name':'python'}])
table('post',
      Field('title', 'string', length = 80, label = T('Título')),
      Field('body', 'text', length = 4000, label = T('Cuerpo')),
      auth.signature,
      Field('slug', 'string', compute = lambda r: IS_SLUG.urlify(r['title'])),
      Field('markup', db.markup),
      Field('xurl', 'string'),
      format = '%(title)s'
      )

db.post.xurl.writable = False
db.post.xurl.requires = IS_URL()
db.post.is_active.default = False
db.post.markup.default = 1

table('context',
      Field('post', 'reference post'),
      Field('place', 'reference place'),
      Field('priority', 'integer',default=1,comment = T('Un post tipo "blogpost" con prioridad 0 lo estableces como "frontpage"'))
      )

"""
table('block_content',
      Field('block','reference block'),
      Field('content','reference post'),
      Field('position','integer')
      )

query_block_content = db((db.post.id>0) & (db.post.is_active == True) & (db.post.block == True))
db.block_content.content.requires=IS_IN_DB(query_block_content,'post.id','%(title)s')
"""

#auth.add_permission(1, 'delete', 'post')
