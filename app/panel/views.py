from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from friendship.models import Friend
from django.contrib.auth.models import User


def main(request):
    variables = RequestContext(request)
    return render_to_response('panel/index.html', variables)


def remove_friend(request, uname):
    if request.method == 'POST':
        other_user = User.objects.get(username=request.POST.get('to_username', ''))
        #print other_user
        #print request.user
        Friend.objects.remove_friend(other_user, request.user)

        return HttpResponseRedirect(reverse('friendship_view_users'))
    else:
        variables = RequestContext(request, {
            'to_username': uname
        })
        return render_to_response('friendship/friend/remove.html', variables)
