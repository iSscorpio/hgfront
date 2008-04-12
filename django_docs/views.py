from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from django.http import Http404

from docreader import get_doc

def index(request):
    return direct_to_template(request, 'admin_doc/django/index.html')

def doc_reader(request, docname):
    try:
        doc = get_doc(docname)
    except Exception, e:
        # Always use the debug response, even if we aren't in DEBUG mode.
        import sys
        from django.views import debug
        return debug.technical_500_response(request, *sys.exc_info())
    if not doc:
        raise Http404
    title = docname.replace('_', ' ')
    return direct_to_template(request, 'admin_doc/django/doc.html',
                              dict(doc=doc, doctitle=title))