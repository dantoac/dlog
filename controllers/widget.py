# -*- coding: utf-8 -*-

@cache(request.env.path_info, time_expire = 300, cache_model = cache.ram)
def identica():
    from floscial import Floscial
    identica_contactos = Floscial('dantoac','friends',3).identica()
    identica_personal = Floscial('dantoac','user',3).identica()

    d =  dict(friends = identica_contactos, personal = identica_personal)
    return response.render(d)


def postlist():
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
        (db.place.name == 'blog') &
        (db.context.priority > 0)
        ).select(
            db.post.title,
            db.post.slug,
            db.post.id,
            db.post.created_on,
            db.post.modified_on,
            orderby =~ db.post.created_on,
            limitby = limitby,
            )

    posts_list = UL()

    total_posts = db((db.post.id == db.context.post) &
                     (db.post.is_active == True) &
                     (db.context.place == db.place.id) &
                     (db.place.name == 'blog')
                     ).select(db.post.id.count())[0][db.post.id.count()]-1

    if not total_posts > 0:
        total_posts = 0
    
    #paginador
    paginar = DIV(_id = 'paginar')

    if page:
        paginar.append(A('← Recientes', _href = URL(r = request, vars = {'pag':page - 1}), cid = request.cid, _class=''))
        paginar.append(' | ')

    if len(data) > items_per_page:
        paginar.append(A('Antiguos →', _href = URL(r = request, vars = {'pag':page + 1}), cid = request.cid, _class=''))
    #/paginador


    #
    for n, p in enumerate(data):
        if n == items_per_page: break
        # agregamos un botón de 'edición rápida' si es que el usuario está autentificado
        if auth.is_logged_in():
            edit_button = SPAN(A('editar', _href= URL(c = 'gestor', f = 'index.html', 
                                                      args = ['post','edit','post',p.id], 
                                                      user_signature=True), 
                                                      _class = 'ui-button ui-icon ui-icon-pencil'))
        else: edit_button = ''

        if p.id == db(db.post).select(db.post.id).last()['id']: continue

        # crea el link para cargar el post usando ajax
        posts_list.append(LI(
        SPAN(p.created_on.date(), _class = 'created_on'), 
        #A(' ' + p.title, _href = URL(c = 'post', f = 'read.load', args = [p.id, p.slug]), cid = 'post'), 
        A(' '+p.title, _href="#post",
          _onmouseup = 'web2py_component("%s","post");return false;' % URL('post','read.load', args=p.id)),
          edit_button))
      
    posts_list = CAT(DIV(TAG.STRONG('Publicaciones anteriores: ',EM(total_posts)),_class='title'),posts_list)

    return dict(posts_list = posts_list, paginar = paginar)


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
