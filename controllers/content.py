# coding: utf8
# try something like
response.files.append(URL('static','css/last.css'))

def index():
    return redirect(URL(r=request,c='default',f='index'),'301')

def read():
    slug = request.args(0)
    pid = int(request.args(1))
    post_data = db(db.post.id==pid).select(
        db.post.title,
        db.post.body,
        db.post.created_on,
        db.post.is_active,
        db.post.xurl,
        )
    

    markmin_extra={'code_cpp':lambda text: CODE(text,language='cpp').xml(),
           'code_java':lambda text: CODE(text,language='java').xml(),
           'code_python':lambda text: CODE(text,language='python').xml(),
           'code_html':lambda text: CODE(text,language='html').xml()}

    
    if len(post_data)>0:
        for p in post_data:
            response.title = p.title
            title = H1(A(p.title,_href=URL(c='content',f='read.html',args=[slug,pid])),_class='title ui-corner-all')
            date = p.created_on
    
            if p.is_active == False:
                response.flash = 'Este post está actualmente desactivado.'

            # generando el texto para postear a identi.ca
            #dentmsg = str(p.title+' '+p.xurl)[:140]

            post_meta = DIV(
                UL(                    
                    #LI(A('permalink ',_href=URL(f='read',args=[slug,pid],extension='html'),_class='meta_link')),
                    LI(A('permalink ',_href=p.xurl,extension='html',_class='meta_link')),
                    LI(A('editar ',_href=URL(f='post',args=['edit',pid],extension='html'),_class='meta_link')),
                    #LI(A('dent ',_href='http://identi.ca/index.php?action=newnotice&status_textarea=%s' % dentmsg,_class='meta_link',_taget='_new'),_class='dent'),
                    _class='sf-menu der'),
                SPAN(date,_class='izq'),
                _class='post_meta')
            
            post_content = DIV(
                MARKMIN(p.body,extra=markmin_extra),
                _class='post_body'
                )
                             
        return dict(meta=post_meta,body=post_content, title=title, created_on=date,active=p.is_active)
    else:
        raise HTTP(404,'No existe la publicación.<a href="%s">Ir a la Portada</a>' % URL(c='default',f='index.html'))

        


@auth.requires_login()
def post():
    if request.args(0) == 'edit' or 'post' and request.args(1):
        pid = int(request.args(1))
        response.flash = pid
        response.title = 'Editando post'
    else:
        pid = ''
        response.title = 'Nuevo post'

    form = SQLFORM(db.post,pid,deletable=True)

    #response.files.append(URL('static','js/fileuploader.js'))
    #form.append(LOAD(c='widget',f='uploader.load'))

    if form.accepts(request.vars,session):
        session.flash = 'ok'
        # genera url corta
        #db.post[int(form.vars.id)]=dict(xurl=xurl(XML(FULL_URL+str(URL(f='read',args=[form.vars.id,IS_SLUG.urlify(form.vars.title)])))))

        redirect(URL(f='read',args=[IS_SLUG.urlify(form.vars.title),form.vars.id]))
    elif form.errors:
        response.flash = 'err'

    return dict(form=form)


def feed():
    """
    Crea un dict() de los últimos post para rendirlos como RSS
    """    
    response.view = 'generic.rss'
    data = db(
        (db.post.id>0) & 
        (db.post.is_active==True)
        ).select(
        db.post.title,
        db.post.slug,
        db.post.body,
        db.post.id,
        db.post.created_on,
        orderby=~db.post.id,
        limitby=(0,10)
        )


    feed_title = 'varpub.org'
    url_prefix = ''
    feed_url = 'http://varpub.org'
    feed_description = 'blog'
    e = []
    for pub in data:
        entradas = dict(title=unicode(str(pub.title),'utf8'),
                        link = url_prefix+URL(c='default',f='blog',args=[pub.slug,pub.id], extension=False),
                        description = unicode(str(pub.body),'utf8'),
                        created_on = pub.created_on,
                        pub_date = request.now
                        )

        e.append(entradas)

    return dict(title= feed_title,
                link = feed_url,
                description = feed_description,
                entries = e
                )



def page():
    return dict()

def xurl(url):
    from random import choice
    import urllib2

    url = str(url)
    xurl_service = ['http://go.gnu.cl/api.php?url',
                    #'http://xurl.cl/api.php?url',
                    #'http://to.ly/api.php?longurl',
                    #'http://tinyurl.com/api-create.php?url',
                    'http://is.gd/create.php?format=simple&url']

    xurl_api = choice(xurl_service)      
    try:
        xurl = urllib2.urlopen("%(api)s=%(longurl)s" % dict(api=xurl_api,longurl=url)).read()
    except:
        pass
    return str(xurl)
    
