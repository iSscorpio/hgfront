def get_option(*args):
"""
    This function gets the required option from the database
"""
    request_option_key = args
    def the_decorator(func):
        from hgfront.config.models import SiteOptions
        from django.template.loader import Context, render_to_string
        def inner(*args, **kwargs):
            request = args[0]
            SiteOptions.objects.get(option_key__exact = request_option_key)
            return func(*args, **kwargs)
        return inner
    return the_decorator
