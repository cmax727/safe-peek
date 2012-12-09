from functools import wraps
from django.utils.decorators import available_attrs
from django.http import Http404


def school_members_only(school):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            u_slug = kwargs.get('slug', '')
            exists = request.user.academy_roles.filter(university__slug=u_slug).exists()

            if exists:
                return func(request, *args, **kwargs)
            else:
                raise Http404
        return inner
    return decorator
