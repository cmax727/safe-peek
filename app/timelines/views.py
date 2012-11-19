from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.timezone import utc

from .models import Timeline


def detail(request, id, template='timelines/detail.html'):
    obj = get_object_or_404(Timeline, id=id)

    variables = RequestContext(request, {
        'obj': obj
    })
    return render(request, template, variables)
