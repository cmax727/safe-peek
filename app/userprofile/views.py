from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext

# from forms import RegistrationForm
# from models import UserAvatar


def main(request, template='userprofiles/index.html'):
    variables = RequestContext(request, {
    })
    return render(request, template, variables)


def profile_detail(request, username, template='userprofiles/detail.html'):
    user = get_object_or_404(User, username=username, is_active=True)
    variables = RequestContext(request, {
        'user_profile': user
    })
    return render(request, template, variables)
