from os import mkdir
from os.path import dirname, join, getmtime, isdir, realpath, exists

from django.conf import settings
from django.utils.safestring import mark_safe

from builder import build_document

try:
    DOCS_ROOT = settings.DOCS_ROOT
except AttributeError: 
    import django
    DOCS_ROOT = join(dirname(dirname(realpath(django.__file__))), 'docs')

def get_doc(docname):
    txt_path = join(DOCS_ROOT, '%s.txt' % docname)
    if not exists(txt_path):
        return None
    html_dir = join(settings.MEDIA_ROOT, 'django_docs')
    if not isdir(html_dir):
        mkdir(html_dir)
    html_path = join(html_dir, '%s.body' % docname)
    html_toc_path = join(html_dir, '%s.toc' % docname)
    # If the HTML exists already (and the text file isn't newer), return it.
    try:
        if getmtime(txt_path) <= getmtime(html_path):
            return {'toc': open(html_toc_path).read(),
                    'html_body': open(html_path).read()}
    except OSError:
        pass
    # Otherwise, convert the RST text file to html...
    txt = open(txt_path).read()
    doc = build_document(txt)
    # ... and write the TOC and html_body sections to disk
    f = open(html_toc_path, 'w')
    f.write(doc['toc'])
    f.close()
    f = open(html_path, 'w')
    f.write(doc['html_body'])
    f.close()
    return {'toc': mark_safe(doc['toc']),
            'html_body': mark_safe(doc['html_body'])}
