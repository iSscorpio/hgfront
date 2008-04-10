from django.template import Library, Node, TemplateSyntaxError

register = Library()

def do_menubox(parser, token):
    nodelist = parser.parse(('endmenubox',))
    parser.delete_first_token()
    try:
        tag_name, title = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, "%r tag requires exactly two arguments" % \
              token.contents.split()[0]
    return MenuboxNode(nodelist, parser.compile_filter(title))

register.tag('menubox', do_menubox)

class MenuboxNode(Node):
    
    def __init__(self, nodelist, title):
        self.nodelist = nodelist
        self.title = title
        
    def render(self, context):
        title = self.title.resolve(context)
        output = self.nodelist.render(context)
        return '''<div class="box"><div class="box-outer"><div class="box-inner"><h2>%s</h2>%s</div></div></div>''' % (title, output)


def filetype(value):
    file_type = "default"
    if value.endswith('py'): file_type = "python"
    if value.endswith('html'): file_type = "html"
    if value.endswith('js'): file_type = "javascript"
    if value.endswith('png'): file_type = "png"
    if value.endswith('css'): file_type = "css"   
    return file_type
register.filter('filetype', filetype)

@register.filter
def megs(value):
    size = (value/(1024*1024.0))
    return size