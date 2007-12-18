def check_project_permission(permission):
    """ 
    This function returns a decorator that checks if the user has the permission `permission`.
    It is to be used to decorate views so that they require certain permissions to be accessed.
    Example usage:

        @check_permission('view_issues')
        def issue_detail(request, slug ...

    Also, it can be used in succession to mandate several permissions
        
        @check_permission('view_issues')
        @check_permission('add_issues')
        def ...

    Note that the use of this decorator mandates that the view receives the slug of the project
    as a keyword argument, not just a normal argument. That means that the view definition must
    define the argument as `slug` and the urlconf must name it as ?P<slug>
    """
    def the_decorator(func):
        from hgfront.project.models import Project
        from django.contrib.auth.models import User
        from django.shortcuts import get_object_or_404
        from django.http import HttpResponseForbidden
        def inner(*args, **kwargs):
            request = args[0]
            project = get_object_or_404(Project, name_short=kwargs['slug'])
            if getattr(project.get_permissions(request.user), permission):
                return func(*args, **kwargs)
            else:
                return HttpResponseForbidden('Forbidden')
        return inner
    return the_decorator
    #TODO: Make the forbidden screen nicer
