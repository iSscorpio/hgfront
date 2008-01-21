from django.http import Http404
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.shortcuts import _get_queryset
def get_object_related_or_404(klass, *args, **kwargs):
    """
    Works just like get_object_or_404, only it does the query with select_related
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.select_related().get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)
