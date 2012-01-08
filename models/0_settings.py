# coding: utf8

EXTENSIONES_PERMITIDAS = 'ogg|png|jpg|odt|pdf|txt|muse|planner|ods|odp|ogv|vp8|oga'

#if request.env.wsgi_url_scheme != None: #necesario para cargar la app desde shell web2py
#    FULL_URL = request.env.wsgi_url_scheme+'://'+request.env.http_host
FULL_URL = URL(r = request, scheme = True, host = True)

copyleft = SPAN(' ↄ⃝ ', _style = 'font:normal 1em- monospace, sans-serif;')


if request.is_local:
    from gluon.custom_import import track_changes
    track_changes()

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
