from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from friendship.models import Friend
from django.contrib.auth.models import User
from forms import RegistrationForm
from models import UserAvatar


def main(request):
    variables = RequestContext(request)
    return render_to_response('panel/index.html', variables)


def remove_friend(request, uname):
    if request.method == 'POST' and request.method == 'FILES':
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


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None, request.FILES)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            passwd = request.POST['password1']
            user = User.objects.create_user(username, email, passwd)
            user.is_staff = True
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()

            avatar = UserAvatar(User=user, avatar=request.FILES['avatar'])
            avatar.save()

            return HttpResponseRedirect(reverse('account_login'))
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('usersignup.html', variables)
