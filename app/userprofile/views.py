from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import StatusForm, EditProfileForm
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


def main(request, template='userprofile/index.html'):
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


def profile_detail(request, username, template='userprofile/detail.html'):
    user = get_object_or_404(User, username=username, is_active=True)
    variables = RequestContext(request, {
        'user_profile': user
    })
    return render(request, template, variables)


@login_required
def edit(request, username, template='userprofile/edit.html'):
    user = get_object_or_404(User, is_active=True, username=username)
    user_profile, created = Profile.objects.get_or_create(user=user)

    if request.user != user:
        raise Http404('You are not allowed to edit this page')

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            # use existing profile instead of creating one
            profile = form.save()

            profile.user.username = cleaned_data.get('username')
            profile.user.first_name = cleaned_data.get('first_name')
            profile.user.last_name = cleaned_data.get('last_name')
            profile.user.save()
            return HttpResponseRedirect(reverse('userprofile:detail', args=[profile.user.username]))

    else:
        initial_data = {
            'user': user,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
        }
        form = EditProfileForm(initial=initial_data, instance=user_profile)

    variables = RequestContext(request, {
        'form': form,
    })
    return render(request, template, variables)
