# coding: utf8
# try something like
response.files.append(URL('static', 'css/last.css'))

from menucontext import MenuContext


def index():
    return redirect(URL(r = request, c = 'default', f = 'index'), '301')


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
        xurl = urllib2.urlopen("%(api)s=%(longurl)s" % dict(api = xurl_api, longurl = url)).read()
    except:
        pass
    return str(xurl)

