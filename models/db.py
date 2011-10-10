# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key = Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables()

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy

auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.login_after_registration = False


## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename = 'private/janrain.key')

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


table = db.define_table

import uuid

table('place',
      Field('name'), #sidebar
      format = '%(name)s'
      )

table('markup',
      Field('name', 'string'),
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

auth.add_permission(1, 'delete', 'post')

if db(db.markup).isempty():
    db.markup.bulk_insert([{'name':'markmin'},
                           {'name':'html'}
                           ])

if db(db.place).isempty():
    db.place.bulk_insert([{'name':'blogpost'},
                          {'name':'sidebar'},
                          {'name':'página'},
                          {'name':'documento'}
                          ])

if request.is_local:
    from gluon.custom_import import track_changes
    track_changes()
