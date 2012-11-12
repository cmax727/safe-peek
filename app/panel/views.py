from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from friendship.models import Friend
from django.contrib.auth.models import User
from forms import RegistrationForm
from allauth.account.utils import get_default_redirect, complete_signup
#from models import UserAvatar


def main(request):
    variables = RequestContext(request)
    return render_to_response('index.html', variables)


def remove_friend(request, uname):
    if request.method == 'POST':
        other_user = User.objects.get(username=request.POST.get('to_username', ''))
        print other_user
        print request.user
        Friend.objects.remove_friend(other_user, request.user)

        return HttpResponseRedirect(reverse('connections:friends'))
    else:
        variables = RequestContext(request, {
            'to_username': uname
        })
        return render_to_response('friendship/friend/remove.html', variables)


def signup(request):
    # success_url = kwargs.pop("success_url", None)
    # if request.method == 'POST':
    #     form = RegistrationForm(request.POST or None, request.FILES)
    #     if form.is_valid():
    #         username = request.POST['username']
    #         email = request.POST['email']
    #         passwd = request.POST['password1']
    #         user = User.objects.create_user(username, email, passwd)
    #         user.is_staff = True
    #         user.first_name = request.POST['first_name']
    #         user.last_name = request.POST['last_name']
    #         user.save()

    #         #user = form.save(request=request)
    #         return complete_signup(request, user, success_url)

    #         #avatar = UserAvatar(User=user, avatar=request.FILES['avatar'])
    #         #avatar.save()

    #         #return HttpResponseRedirect(reverse('account_login'))
    # else:
    #     form = RegistrationForm()

    form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('usersignup.html', variables)
