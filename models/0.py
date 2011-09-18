# coding: utf8

EXTENSIONES_PERMITIDAS = 'ogg|png|jpg|odt|pdf|txt|muse|planner|ods|odp|ogv|vp8|oga'

if request.env.wsgi_url_scheme != None: #necesario para cargar la app desde shell web2py
    FULL_URL = request.env.wsgi_url_scheme+'://'+request.env.http_host


