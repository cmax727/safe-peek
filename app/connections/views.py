from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext

from friendship.models import Friend, FriendshipRequest


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
def friends(request):
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)
    variables = RequestContext(request, {
        'requests': friendship_requests
    })
    return render(request, 'friendship/friend/requests_list.html', variables)


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


@login_required
def accept(request, req_id):
    f_request = get_object_or_404(FriendshipRequest, id=req_id)
    f_request.accept()
    #return redirect('friendship_view_friends', username=request.user.username)

    previous_url = request.META.get('HTTP_REFERER', reverse('connections:requests'))
    return HttpResponseRedirect(previous_url)


@login_required
def reject(request, req_id):
    f_request = get_object_or_404(FriendshipRequest, id=req_id)
    f_request.reject()
    #return redirect('friendship_view_friends', username=request.user.username)

    previous_url = request.META.get('HTTP_REFERER', reverse('connections:requests'))
    return HttpResponseRedirect(previous_url)
