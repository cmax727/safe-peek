from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext

from .forms import GroupForm
from .models import Group


@login_required
def create(request, template='groups/create.html'):
    if request.method == 'POST':
        form = GroupForm(request.POST or None)
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.created_by = request.user
            new_group.save()

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
