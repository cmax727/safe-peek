from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import ProfileForm, NameForm
from models import Profile

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


@login_required
def profile(request, template='userprofiles/edit.html'):
    record1 = User.objects.get(username=request.user)
    #record2 = get_object_or_404(Profile, user=request.user)
    form1 = NameForm()
    form2 = ProfileForm()
    #user = get_object_or_404(User, username=request.user, is_active=True)
    variables = RequestContext(request, {
        'form1': form1,
        'form2': form2,
    })
    return render(request, template, variables)
