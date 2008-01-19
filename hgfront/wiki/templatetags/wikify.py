from django import template
import re
import cgi
import string

register = template.Library()

# register the templatetag
@register.filter("wikify") 
def wikify(content):
    out = ''
    for rt in string.split(content,"\n"):
        rt = rt.replace('&', '&amp;')
        rt = rt.replace('<', '&lt;')
        rt = rt.replace('>', '&gt;')
        rt = rt.replace('"', '&quot;')
        rt = rt.replace("'", '&#39;')
        # link  [[URL]] 
        try:
            rt = re.sub('\[\[([^\]|]*)\]\]','<a href="\\1">\\1</a>',rt)
        except:pass
        # link with title [[URL|TITLE]]
        try:
            rt = re.sub('\[\[([^\]|]*)\|([^\]]*)\]\]','<a href="\\1">\\2</a>',rt)
        except:pass
        # bold **TEXT**
        try: 
            rt = re.sub('\*\*([^\*]*)\*\*','<strong>\\1</strong>',rt)
        except:pass
        # italic //TEXT//
        try: 
            rt = re.sub('//([^\*]*)//','<strong>\\1</strong>',rt)
        except:pass
        # image {{IMG}}
        try: 
            rt = re.sub('\{\{([^\]|]*)\}\}','<img src="\\1" alt=""/>',rt)
        except:pass
        # h5 ==H5==
        try:
            rt = re.sub('^==([^=]*)==$','<h5>\\1</h5>',rt)
        except:pass
        # h4 ===H4===
        try:
            rt = re.sub('^===([^=]*)===$','<h4>\\1</h4>',rt)
        except:pass
        # h3  ====H3====
        try:
            rt = re.sub('^====([^=]*)====$','<h3>\\1</h3>',rt)
        except:pass
        # code [code]SOME CODE[/code]
        try:
            rt = re.sub('^\[code\]([^\]]*)\[/code\]$','<code>\\1</code>',rt)
        except:pass
        out += '<p>'+rt+'</p>'
    return out
