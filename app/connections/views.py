from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext

from friendship.models import Friend


@login_required
def search(request, template='connections/search.html'):
    query = request.GET.get('q', '')
    users = User.objects.filter(is_active=True)

    if query:
        users = users.filter(username__icontains=query)

    variables = RequestContext(request, {
        'users': users,
        'query': query
    })
    return render(request, template, variables)


@login_required
def add(request, username):
    request_user = request.user
    added_user = get_object_or_404(User, username=username, is_active=True)

    friends = Friend.objects.are_friends(request_user, added_user)

    if friends:
        Friend.objects.remove_friend(request_user, added_user)
    else:
        Friend.objects.add_friend(request_user, added_user)

    previous_url = request.META.get('HTTP_REFERER', reverse('connections:search'))
    return HttpResponseRedirect(previous_url)
