def check_project_permissions(*args):
    """ 
    This function returns a decorator that checks if the user has all the permissions in *args.
    It is to be used to decorate views so that they require certain permissions to be accessed.
    Example usage:

        @check_permission('view_issues')
        def issue_detail(request, slug ...

    Also, it can be given multiple permissions to check.
        
        @check_permission('view_project','view_issues')
        def ...

    Note that the use of this decorator mandates that the view receives the slug of the project
    as a keyword argument, not just a normal argument. That means that the urlconf must call it as
    ?P<slug>
    """
    required_permissions = args
    def the_decorator(func):
        from hgfront.project.models import Project
        from django.contrib.auth.models import User
        from django.shortcuts import get_object_or_404
        from django.http import HttpResponseForbidden
        def inner(*args, **kwargs):
            request = args[0]
            project_permissions = get_object_or_404(Project, name_short=kwargs['slug']).get_permissions(request.user)
            for permission in required_permissions:
                if not getattr(project_permissions, permission):
                    return HttpResponseForbidden('Forbidden')
            return func(*args, **kwargs)
        return inner
    return the_decorator


