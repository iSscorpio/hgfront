import re

class RemoveSelfLinks:
    def process_response(self, request, response):
        if response.status_code == 200:
            link = request.META['PATH_INFO']
            response.content = \
                re.sub( \
                    r'<a([^>]+)href="%s"([^>]*)>([^<]+)</a>' % link, \
                    r'<span \1 \2>\3</span>', \
                    response.content)
        return response