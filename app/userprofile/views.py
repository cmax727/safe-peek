from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from forms import ProfileForm, NameForm
from models import Profile
from postman.models import Message
from datetime import datetime

# from forms import RegistrationForm
# from models import UserAvatar


def main(request, template='userprofiles/index.html'):
    variables = RequestContext(request, {
    })
    return render(request, template, variables)


def setread(request, template='postman/base_folder.html'):
    pks = request.POST.getlist('pks', '')
    tpks = request.POST.getlist('tpks', '')
    filter = Q(pk__in=pks) | Q(pk__in=tpks)
    #idm = request.POST.getlist('tpks', '')
    #msg = Message.objects.get(id=idm)
    Message.objects.filter(filter).update(read_at=datetime.now())

    previous_url = request.META.get('HTTP_REFERER', reverse('postman_inbox'))
    return HttpResponseRedirect(previous_url)


def setunread(request, template='postman/base_folder.html'):
    pks = request.POST.getlist('pks', '')
    tpks = request.POST.getlist('tpks', '')
    filter = Q(pk__in=pks) | Q(pk__in=tpks)
    #idm = request.POST.getlist('tpks', '')
    #msg = Message.objects.get(id=idm)
    Message.objects.filter(filter).update(read_at=None)
    #update.save()
    #print idm
    #print msg.id
    previous_url = request.META.get('HTTP_REFERER', reverse('postman_inbox'))
    return HttpResponseRedirect(previous_url)


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
