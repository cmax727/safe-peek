from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.timezone import utc

from .forms import GroupForm
from .models import Group, GroupMembership

import datetime


@login_required
def create(request, template='groups/create.html'):
    if request.method == 'POST':
        form = GroupForm(request.POST, user=request.user)
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.created_by = request.user
            new_group.save()

            # create a membership for group creator
            membership, new = GroupMembership.objects.get_or_create(
                    user=request.user, group=new_group)
            membership.status = 2
            membership.joined_at = new_group.created_at
            membership.save()

            # set pending status for all the members chosen within form
            added_users = form.cleaned_data.get('members')

            for user in added_users:
                membership, new = GroupMembership.objects.get_or_create(
                    user=user, group=new_group)
                membership.status = 1
                membership.save()

            previous_url = reverse('groups:index')
            return HttpResponseRedirect(previous_url)
    else:
        form = GroupForm(user=request.user)

    variables = RequestContext(request, {
        'form': form
    })
    return render(request, template, variables)


@login_required
def index(request, template='groups/index.html'):
    groups = Group.objects.all()

    variables = RequestContext(request, {
        'groups': groups
    })
    return render(request, template, variables)


@login_required
def detail(request, id, template='groups/detail.html'):
    group = get_object_or_404(Group, pk=id)
    members = group.groupmembership_set.all()

    variables = RequestContext(request, {
        'group': group,
        'members': members,
    })
    return render(request, template, variables)


@login_required
def join(request, id, template='groups/joined.html'):
    group = get_object_or_404(Group, pk=id)

    if request.user not in group.members.all():
        membership, new = GroupMembership.objects.get_or_create(user=request.user,
                group=group)

        # if a group's privacy is open then let the user becomes a member
        # automatically
        if group.privacy == 1:
            membership.status = 2
        else:
            membership.status = 1
            membership.joined_at = datetime.datetime.now().replace(tzinfo=utc)
        membership.save()

    variables = RequestContext(request, {
        'membership': membership
    })
    return render(request, template, variables)


@login_required
def manage(request, id, template='groups/manage.html'):
    group = get_object_or_404(Group, created_by=request.user, pk=id)
    memberships = group.groupmembership_set.prefetch_related('user').order_by('user')

    variables = RequestContext(request, {
        'group': group,
        'memberships': memberships,
    })
    return render(request, template, variables)


@login_required
def accept_membership(request, id, user_id):
    group = get_object_or_404(Group, created_by=request.user, pk=id)
    membership = get_object_or_404(GroupMembership, user_id=user_id, group=group, status=1)
    membership.status = 2
    membership.save()

    return HttpResponseRedirect(reverse('groups:manage', args=[group.pk]))