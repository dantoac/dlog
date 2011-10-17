# -*- coding: utf-8 -*-

@cache(request.env.path_info, time_expire = 200, cache_model = cache.ram)
def identica():

    from floscial import Floscial
    user = 'dantoac'
    identica_contactos = Floscial(user,'friends',3).identica()
    identica_personal = Floscial(user,'user',3).identica()

    d =  dict(friends = identica_contactos, personal = identica_personal)
    return response.render(d)


#@cache(request.env.path_info, time_expire=3600, cache_model=cache.ram)
def postlist():
    #chk que sea una llamada ajax
    if request.cid: #

        if request.vars.pag:
            page = int(request.vars.pag)
        else:
            page = 0


        items_per_page = 3
        limitby = (page * items_per_page, (page + 1) * items_per_page + 1)

        data = db(
            (db.context.place == db.place.id) &
            (db.context.post == db.post.id) &
            (db.post.is_active == True) &
            (db.place.name == 'blogpost') &
            (db.context.priority > 0)
            ).select(
            db.post.title,
            db.post.slug,
            db.post.id,
            db.post.created_on,
            db.post.modified_on,
            orderby =~ db.post.created_on,
            limitby = limitby
            )

        posts_list = UL()

        #paginador
        paginar = DIV(_id = 'paginar')

        if page:
            paginar.append(A('← recientes', _href = URL(r = request, vars = {'pag':page - 1}), cid = request.cid))
            paginar.append(' | ')

        if len(data) > items_per_page:
            paginar.append(A('antiguos →', _href = URL(r = request, vars = {'pag':page + 1}), cid = request.cid))
        #/paginador


        #
        for n, p in enumerate(data):
            if n == items_per_page: break
            posts_list.append(LI(SPAN(p.created_on.date(), _class = 'created_on'), A(' ' + p.title, _href = URL(c = 'post', f = 'read.load', args = [p.id, p.slug]), cid = 'post')))

            # agregamos un botón de 'edición rápida' si es que el usuario está autentificado
            if auth.is_logged_in():
                posts_list[-1].append(SPAN(A('editar', _href= URL(c = 'gestor', f = 'index.html', args = ['post','edit','post',p.id], user_signature=True), _class = 'ui-button ui-icon ui-icon-pencil')))

            if p.modified_on != p.created_on:
                posts_list[-1].append(SPAN(EM(' actualizado: %s' % p.modified_on.date()),_class='updated green_light_bg'))

        posts_list.insert(0,DIV(TAG.STRONG('Publicaciones'),_class='title'))
               
        return dict(posts_list = posts_list, paginar = paginar)




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
                """ % dict(extensiones_permitidas = EXTENSIONES_PERMITIDAS.split('|'), uploader_url = URL(c = 'widget', f = 'upload'))
    return dict(uploader = XML(uploader))


def upload():
    if request.vars:
        afile = request.vars.qqfile

        db.attach.insert(file = db.attachment.file.store(request.body, afile), name = afile)
        return response.json({'success':'true'})
    else:
        return redirect(URL('default', 'index'))

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


def admin():
    try:
        form = SQLFORM.smartgrid(db[request.args(0) or 'post'])
    except:
        form = ''
    return dict(form = form)


def posts():
    query = (db.post.id > 0) #& (db.post.is_active==True) & (db.post.static==True)
    form = SQLFORM.grid(query, headers = {'post.id':'pid', 'post.title':'Título', 'post.is_active':'Activo', 'post.static':'Pág. Estática'}, columns = ['post.id', 'post.title', 'post.static', 'post.is_active'])
    return dict(form = form)
