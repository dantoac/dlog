# -*- coding: utf-8 -*-

from menucontext import MenuContext
response.files.append(URL('static', 'css/last.css'))
menuadds = MenuContext(db)

response.menu += menuadds.menudocs()
response.menu += menuadds.menupags()


def read():

    slug = request.args(1)
    pid = int(request.args(0))
    post_data = db(db.post.id == pid).select(
        db.post.title,
        db.post.body,
        db.post.created_on,
        db.post.is_active,
        db.post.markup,
        db.post.xurl,
        )


    markmin_extra = {'code_cpp':lambda text: CODE(text, language = 'cpp').xml(),
           'code_java':lambda text: CODE(text, language = 'java').xml(),
           'code_python':lambda text: CODE(text, language = 'python').xml(),
           'code_html':lambda text: CODE(text, language = 'html').xml()}


    if len(post_data) > 0:
        for p in post_data:
            date = p.created_on
            response.title = p.title
            response.subtitle = date
            title = H1(A(p.title, _href = URL(c = 'post', f = 'read.html', args = [pid,slug])), _class = 'title ui-corner-all')


            if p.is_active == False:
                response.flash = 'Este post está actualmente desactivado.'

            # generando el texto para postear a identi.ca
            #dentmsg = str(p.title+' '+p.xurl)[:140]

            post_meta = DIV(
                UL(
                    #LI(A('permalink ',_href=URL(f='read',args=[slug,pid],extension='html'),_class='meta_link')),
                    LI(A('permalink ', _href = p.xurl, extension = 'html', _class = 'meta_link')),
                    LI(A('editar', _href= URL(c = 'gestor', f = 'index.html', args = ['post','edit','post',pid], user_signature=True), _class = 'meta_link')),
                       #A('editar ', _href = URL(c='',f = 'post', args = ['edit', pid], extension = 'html'), _class = 'meta_link')),
                    #LI(A('dent ',_href='http://identi.ca/index.php?action=newnotice&status_textarea=%s' % dentmsg,_class='meta_link',_taget='_new'),_class='dent'),
                    _class = 'sf-menu der'),
                #SPAN(date, _class = 'izq'),
                _class = 'post_meta')

            #revisa el tipo de marcado del post
            #y setea la forma correcta de rendirlo

            if p.markup.name == 'markmin':
                post_content = DIV(
                    MARKMIN(p.body, extra = markmin_extra),
                    _class = 'post_body'
                    )

            elif p.markup.name == 'html':
                post_content = DIV(
                    XML(p.body),
                    _class = 'post_body'
                    )
            elif p.markup.name == 'template':
                import gluon.template
                try:
                    post_content = XML((gluon.template.render(p.body,context=globals())))
                except:
                    post_content = 'asdf'




        return dict(meta = post_meta, body = post_content, title = title, created_on = date, active = p.is_active)
    else:
        raise HTTP(404, 'No existe la publicación.<a href="%s">Ir a la Portada</a>' % URL(c = 'd2efault', f = 'index.html'))




@auth.requires_login()
def add():
    if request.args(0) == 'edit' or 'post' and request.args(1):
        pid = int(request.args(1))
        response.title = 'Editando post'
    else:
        pid = ''
        response.title = 'Nuevo post'

    form = SQLFORM(db.post, pid, deletable = True, formstyle='divs')

    #response.files.append(URL('static','js/fileuploader.js'))
    #form.append(LOAD(c='widget',f='uploader.load'))

    if form.process().accepted:

        # genera url corta
        #db.post[int(form.vars.id)]=dict(xurl=xurl(XML(FULL_URL+str(URL(f='read',args=[form.vars.id,IS_SLUG.urlify(form.vars.title)])))))

        #redirect(URL(f = 'read', args = [IS_SLUG.urlify(form.vars.title), form.vars.id]))

        session.flash = 'Señale ahora el bloque donde quiere presentar el post recién creado.'
        redirect(URL(r = request, c = 'gestor', f = 'index', args = ['post', 'context.post', form.vars.id, 'new','context'], user_signature=True))
    elif form.errors:
        response.flash = 'err'

    return dict(form = form)
