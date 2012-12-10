from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from .models import Event


def main(request):
    variables = RequestContext(request)
    return render_to_response('timelines/main.html', variables)


def detail(request, id, template='timelines/detail.html'):
    obj = get_object_or_404(Event, id=id)

    variables = RequestContext(request, {
        'timeline': obj
    })
    return render(request, template, variables)


def text(request, template='   timelines/text.html'):
    if request.method == 'POST':
        form = TextTimelineForm(request.POST or None, request.FILES)
        if form.is_valid():
            #print 'test'
            new_status = form.save(commit=False)
            new_status.created_by = request.user
            new_status.save()
            previous_url = request.META.get('HTTP_REFERER', reverse('timelines:text', args=(request.user,)))
            return HttpResponseRedirect(previous_url)
    else:
        form = TextTimelineForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('timelines/text.html', variables)
