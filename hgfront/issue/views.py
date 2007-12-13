from django.http import HttpResponse

def issue_list(request, slug):
    """Returns a list of isses that belong to the project identified by `slug`"""
    return HttpResponse("%s issues" % slug)
    #TODO: Implement this

def issue_detail(request, issue_id, slug=None):
    """Returns the details of the issue identified by `issue_id`
    The project slug is default to None because you just need an issue_id
    to get the details of an issue, so if the view doesn't get the project
    slug as an argument (for instance if it's called from {% url %}), it's
    still all cool."""
    return HttpResponse("issue_id %s in %s" % (issue_id, slug))
    #TODO: Implement this

def issue_list_by(request, slug, listed_by, group_by_value):
    """This view gives a list of issues that belong to the project identified
    by `slug`. `group_by_value` can either be a severity, type or status identifier.
    This view receives an extra variable named `listed_by`, so that it knows whether
    the `group_by_value` indicates severity, type or status. For instance, if
    the following url is called:

    /projects/<slug>/issues/severity/really_important

    Then `group_by_value` will have the value of 'really_important' and `listed_by`
    will be severity
    """
    return HttpResponse("the project slug is %s, this will give issues of that project that have a %s of %s" % (slug, listed_by, group_by_value))
    #TODO: Implement this
