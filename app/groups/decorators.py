from functools import wraps
from django.utils.decorators import available_attrs
from django.http import Http404


def group_members_only(group):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            group_id = kwargs.get('id', 0)

            try:
                exists = request.user.groupmembership_set.get(group__id=group_id, status=1)
                print exists
                return func(request, *args, **kwargs)
            except:
                raise Http404
        return inner
    return decorator
