# -*- coding: utf-8 -*-

def index():

    if len(request.extension) > 0:
        if request.extension != 'rss':
            request.view = 'rss'

    """
    Crea un dict() de los últimos post para rendirlos como RSS
    """
    response.view = 'generic.rss'
    data = db(
        (db.post.id > 0) &
        (db.post.is_active == True)
        ).select(
        db.post.title,
        db.post.slug,
        db.post.body,
        db.post.id,
        db.post.created_on,
        orderby = ~db.post.id,
        limitby = (0, 10)
        )


    feed_title = 'varpub.org'
    url_prefix = ''
    feed_url = 'http://varpub.org'
    feed_description = 'blog'
    e = []
    for pub in data:
        entradas = dict(title = unicode(str(pub.title), 'utf8'),
                        link = url_prefix + URL(c = 'default', f = 'blog', args = [pub.slug, pub.id], extension = False),
                        description = unicode(str(pub.body), 'utf8'),
                        created_on = pub.created_on,
                        pub_date = request.now
                        )

        e.append(entradas)

    return dict(title = feed_title,
                link = feed_url,
                description = feed_description,
                entries = e
                )
