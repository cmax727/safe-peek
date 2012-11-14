from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from forms import ProfileForm, NameForm, StatusForm
from .models import Profile, Status
from postman.models import Message
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# from forms import RegistrationForm
# from models import UserAvatar

def write_status(request):
    if request.method == 'POST':
        form = StatusForm(request.POST or None)
        if form.is_valid():
            #print 'test'
            title = form.cleaned_data.get('title')
            image = form.cleaned_data.get('image')
            ins = Status(title=title, image=image)
            ins.save()
            previous_url = request.META.get('HTTP_REFERER', reverse('userprofile:write_status'))
            return HttpResponseRedirect(previous_url)
    else:
        form = StatusForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('write_status.html', variables)


def statuses(request):
    statuses = Status.objects.all()
    # paginator = Paginator(statuses_list, 2)

    # page = request.GET.get('page')
    # try:
    #     status = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     status = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     status = paginator.page(paginator.num_pages)
    variables = RequestContext(request, {
        'status': statuses
        })
    return render_to_response('statuses.html', variables)


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
    if request.method == 'POST':
        form1 = NameForm(request.POST or None)
        form2 = ProfileForm(request.POST or None, request.FILES or None)
        if form1.is_valid() and form2.is_valid():
            User.objects.filter(username=request.user).update(first_name=request.POST.get('first_name', ''), last_name=request.POST.get('last_name', ''))
            Profile.objects.filter(user=request.user).update(picture=request.FILES['picture'], gender=request.POST.get('gender', ''))
            variables = RequestContext(request, {
                'form1': form1,
                'form2': form2,
            })
            previous_url = request.META.get('HTTP_REFERER', reverse('userprofile:main_page'))
            return HttpResponseRedirect(previous_url)
    else:
        record1 = User.objects.get(username=request.user)
        record2 = get_object_or_404(Profile, user=request.user)
        form1 = NameForm(instance=record1)
        form2 = ProfileForm(instance=record2)
    #user = get_object_or_404(User, username=request.user, is_active=True)
    variables = RequestContext(request, {
        'form1': form1,
        'form2': form2,
    })
    return render(request, template, variables)
