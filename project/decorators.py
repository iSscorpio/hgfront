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

    If the user doesn't have all the permissions listed in *args, a 403 error is returned and
    403.html is loaded as the template.
    Note that the use of this decorator mandates that the view receives the slug of the project
    as a keyword argument, not just a normal argument. That means that the urlconf must call it as
    ?P<slug>
    """
    required_permissions = args
    def the_decorator(func):
        from project.models import Project
        from django.shortcuts import get_object_or_404
        from django.http import HttpResponseForbidden
        from django.template.loader import Context, render_to_string
        def inner(*args, **kwargs):
            request = args[0]
            # FIXME: Weird hack, had to add the print statement to stop the ORM failing on line 31
            #print request
            #import pdb; pdb.set_trace()
            project = get_object_or_404(Project, project_id__exact=str(kwargs['slug']))
            project_permissions = project.get_permissions(request.user)
            for permission in required_permissions:
                if not getattr(project_permissions, permission):
                    return HttpResponseForbidden(render_to_string('403.html'))
            return func(*args, **kwargs)
        return inner
    return the_decorator