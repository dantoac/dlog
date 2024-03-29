# -*- coding: utf-8 -*-

from gluon import *


#@cache(request.env.path_info, time_expire = 300, cache_model = cache.ram)
class Floscial():

    request = current.request
    cache = current.cache
       
    def __init__(self,user,tl,limit):
        self.user = user
        self.timeline = tl
        self.limit = limit
        
    
    def identica(self):
        import gluon.contrib.feedparser as feedparser

        identica_user = self.user

        limite = 0

        
        if self.timeline == 'friends':
            identica_feed = 'friends_timeline'
            link2src = A('Timeline Contactos', _href = 'http://identi.ca/%s/all' % identica_user, _class = 'title', _title = 'Timeline público de mi red de contactos')
        elif self.timeline == 'user':
            identica_feed = 'user_timeline'
            link2src = A('@' + identica_user, _href = 'http://identi.ca/' + identica_user, _class = 'title', _title = 'Mi microblog en identi.ca')
            
        urlfeed = 'http://identi.ca/api/statuses/%(tl)s/%(user)s.rss' % dict(user = identica_user, tl = identica_feed)
            
        feed = feedparser.parse(urlfeed)
        identica = DIV(link2src, _class = 'microblog')
            
        dents = UL(_class = 'dents')
            
        for dent in feed.entries:
            if limite == self.limit:
                break
            else:
                limite = limite + 1
            if self.timeline:
                try:
                #autor = XML(B(str(dent.title).split(':')[0]))
                    autor = dent.title.split(':')[0] + ': '
                    dents.append(LI(B(autor), XML(dent.description)))
                except:
                    self.timeline = None

                #redirect(URL(f='microblog'))
            else:
                dents.append(LI(XML(dent.description)))

        identica.insert(len(identica), dents)
        '''
        import urllib2
        #import re
        
        u = urllib2.urlopen(atom).read()
        
        meta = TAG(u)
        
        dents = UL()
        
        for dent in meta.elements('content',_type='html'):
        dents.append(LI(XML(str(dent).replace('&lt;','<').replace('&gt;','>'))))
        '''
        return XML(identica)

