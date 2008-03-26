from django.http import HttpResponseForbidden

def check_allowed_methods(methods=['GET']):
    '''Convenient decorator that verifies that a view is being called with 
an allowed set of request methods and no others.
Returns HttpResponseForbidden if view is called with a disallowed method.'''
    def _decorator(view_func):
        def _wrapper(request, *args, **kwargs):
            if request.method in methods:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        _wrapper.__doc__ = view_func.__doc__
        _wrapper.__dict__ = view_func.__dict__
        return _wrapper
    return _decorator