# -*- coding: utf-8 -*-

@cache(request.env.path_info, time_expire=300, cache_model=cache.ram)
def microblog():
    import gluon.contrib.feedparser as feedparser
    response.files.append(URL('static','css/simplicity20.css'))

    identica_user = 'danto'

    limite=0
    who = request.args(0)
    if who == 'amigostl':
        identica_feed = 'friends_timeline'
        link2src = A('Timeline Contactos',_href='http://identi.ca/danto/all',_class='title',_title='Timeline público de mi red de contactos')
    else:
        identica_feed = 'user_timeline'
        link2src = A('@'+identica_user,_href='http://identi.ca/'+identica_user,_class='title',_title='Mi microblog en identi.ca')
       
    urlfeed = 'http://identi.ca/api/statuses/%(who)s/%(user)s.rss' % dict(user=identica_user,who=identica_feed)

    feed = feedparser.parse(urlfeed)
    identica = DIV(link2src,_class='microblog')

    dents = UL(_id='dents')

    for dent in feed.entries:
        if limite==5:
            break
        else:
            limite=limite+1
        if who:
            try:
                #autor = XML(B(str(dent.title).split(':')[0]))
                autor = dent.title.split(':')[0]+': '
                dents.append(LI(B(autor),XML(dent.description)))
            except:
                who = None
                
                #redirect(URL(f='microblog'))
        else:
            dents.append(LI(XML(dent.description)))
        
    identica.insert(len(identica),dents)
    '''
    import urllib2
    #import re

    u = urllib2.urlopen(atom).read()

    meta = TAG(u)

    dents = UL()

    for dent in meta.elements('content',_type='html'):
        dents.append(LI(XML(str(dent).replace('&lt;','<').replace('&gt;','>'))))
    '''
    return dict(microblog=identica)

#@cache(request.env.path_info, time_expire=3600, cache_model=cache.disk)
@auth.requires(request.cid)
def postlist():  

    #if request.args(0) == 'pag':
    if request.vars.pag:
        #page = int(request.args(1))
        page = int(request.vars.pag)

    else:
        page = 0
         
    
    # chequea si es que el widget es llamado desde el controlador 'gestor'
    if request.cid == 'gestor':
        items_per_page = 50
        limitby = (page*items_per_page,(page+1)*items_per_page+1)
        data = db(
            (db.post.id>0)
            ).select(
            db.post.title,
            db.post.slug,
            db.post.id,
            db.post.created_on,
            db.post.static,
            db.post.is_active,
            orderby=~db.post.created_on,
            limitby=limitby
            )
    else:
        items_per_page = 3
        limitby = (page*items_per_page,(page+1)*items_per_page+1)
        data = db(
            (db.post.id>0) & 
            (db.post.is_active==True) &
            (db.post.static == False)
            ).select(
            db.post.title,
            db.post.slug,
            db.post.id,
            db.post.created_on,
            orderby=~db.post.created_on,
            limitby=limitby
            )
    
    posts_list = UL()

    #paginador
    paginar = DIV(_id='paginar') 

    if page:
        paginar.append(A('<< recientes',_href=URL(r=request,vars={'pag':page-1}),cid=request.cid))
        paginar.append(' | ')

    if len(data)>items_per_page:
        paginar.append(A('antiguos >>',_href=URL(r=request,vars={'pag':page+1}),cid=request.cid))
    #/paginador

    for n,p in enumerate(data):
        if n == items_per_page: break
        posts_list.append(LI(SPAN(p.created_on.date(),_class='created_on'),A(' '+p.title,_href=URL(c='content',f='read.load',args=[p.slug,p.id]),cid='post')))           


        # agregamos un botón de 'edición rápida' si es que el usuario está autentificado
        if auth.is_logged_in():
            posts_list[-1].append(SPAN(A('editar',_href=URL(c='content',f='post',args=['edit',p.id,p.slug]),cid='post',_class='ui-button ui-icon ui-icon-pencil')))

            # si llamamos al widget desde el controlador 'gestor', agrega links con más opciones:
            if request.cid == 'gestor':
                #posts_list[-1].append(SPAN(A('editar',_href=URL(c='content',f='post',args=['edit',p.id,p.slug]),cid='post',_class='ui-button ui-icon ui-icon-pencil')))
                if p.static:
                    posts_list[-1].append(SPAN(EM(',static')))
                if not p.is_active:
                    posts_list[-1].append(SPAN(EM(',Inactivo')))

    return dict(posts_list=posts_list,paginar=paginar)


### UPLOADER
def uploader():
    uploader = """

                <div id='uploader'></div>

                <script>
                $(document).ready(function(){
                        var uploader = new qq.FileUploader({
                        element: document.getElementById('uploader'),
                        action: '%(uploader_url)s',
                        multiple: false,
                        debug: false,
                        allowedExtensions: %(extensiones_permitidas)s,
                        template: '<div class=\"qq-uploader\">' +
                                '<div class=\"qq-upload-drop-area\"><span>Arrastra los videos aquí para cargarlos</span></div>' +
                                '<a class=\"qq-upload-button big positive primary button \"><span class=\"icon uparrow\"></span>Cargar un Fichero</a>' +
                                '<ul class=\"qq-upload-list\"></ul>' +
                             '</div>',
                        fileTemplate: '<li>' +
                                    '<span class=\"qq-upload-file\"></span>' +
                                    '<span class=\"qq-upload-spinner\"></span>' +
                                    '<span class=\"qq-upload-size\"></span>' +
                                    '<a class=\"qq-upload-cancel\ negative button\" href=\"#\">ANULAR</a>' +
                                    '<div class=\"qq-upload-failed-text error \">ha fallado.</div>' +
                                    '</li>',
                            messages:{
                            typeError: '{file} es un archivo inválido. Sólo se permiten los archivos {extensions}',
                            onLeave: 'Hay videos cargándose. Si te vas ahora se anulará la carga, aunque podrás repetirla.'
                            },
                        //onComplete: function(){window.location.reload()},
                        onComplete: function(){jQuery(\".flash\").html(\"Ha finalizado la carga de un video.\").slideDown()}

                        });

                    });

                </script>
                """ % dict(extensiones_permitidas=EXTENSIONES_PERMITIDAS.split('|'),uploader_url=URL(c='widget',f='upload'))
    return dict(uploader=XML(uploader))


def upload():
    if request.vars:
        afile=request.vars.qqfile

        db.attach.insert(file=db.attachment.file.store(request.body,afile),name=afile)
        return response.json({'success':'true'})
    else:
        return redirect(URL('default','index'))

    #"""
    """
    form = SQLFORM(db.attach,upload=URL(c='default',f='download'))

    if form.accepts(request.vars,session):
        response.flash = 'form ok'
        afile=request.vars.qqfile

        db.attach.insert(file=db.attachment.file.store(request.body,afile),name=afile)
        return response.json({'success':'true'})
    elif form.errors:
        response.flash = 'hubo errores'
        
    return dict(upload=form)
    """
