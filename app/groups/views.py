from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import RequestContext

from .forms import GroupForm
from .models import Group, GroupMembership


@login_required
def create(request, template='groups/create.html'):
    if request.method == 'POST':
        form = GroupForm(request.POST or None)
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.created_by = request.user
            new_group.group_members.add(request.user)
            new_group.save()
            new_group.save_m2m()

            previous_url = reverse('groups:index')
            return HttpResponseRedirect(previous_url)
    else:
        form = GroupForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render(request, template, variables)


@login_required
def index(request, template='groups/index.html'):
    groups = Group.objects.filter(created_by=request.user)

    variables = RequestContext(request, {
        'groups': groups
    })
    return render(request, template, variables)


@login_required
def detail(request, groupname, template='groups/detail.html'):
    group = get_object_or_404(Group, name=groupname)
    #print group.get_authorize(user=request.user)
    if request.method == 'POST':
        if request.POST.get('act', '') == 'accept':
            GroupMembership.objects.filter(user=request.user, group=group).update(status=2)
            print request.POST.get('act', '')
        else:
            GroupMembership.objects.filter(user=request.user, group=group).update(status=3)
            print request.POST.get('act', '')
            print "x"

    member = GroupMembership.objects.filter(user=request.user, group=group)
    variables = RequestContext(request, {
        'group': group,
        'member': member,
        'authorize': group.get_authorize(user=request.user)
    })
    return render(request, template, variables)
