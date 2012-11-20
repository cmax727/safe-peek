from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.timezone import utc

from .models import Timeline, TextTimeline, ImageTimeline, YoutubeTimeline, FileTimeline
from .forms import TimelineForm, TextTimelineForm, ImageTimelineForm, YoutubeTimelineForm, FileTimelineForm


def main(request):
    variables = RequestContext(request)
    return render_to_response('timelines/main.html', variables)


def detail(request, id, template='  timelines/detail.html'):
    obj = get_object_or_404(Timeline, id=id)

    variables = RequestContext(request, {
        'obj': obj
    })
    return render(request, template, variables)


def write(request, template='   timelines/write.html'):
    if request.method == 'POST':
        form = TimelineForm(request.POST or None, request.FILES)
        if form.is_valid():
            #print 'test'
            new_status = form.save(commit=False)
            new_status.created_by = request.user
            new_status.save()
            previous_url = request.META.get('HTTP_REFERER', reverse('timelines:write', args=(request.user,)))
            return HttpResponseRedirect(previous_url)
    else:
        form = TimelineForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('timelines/write.html', variables)


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


def picture(request, template='   timelines/picture.html'):
    if request.method == 'POST':
        form = ImageTimelineForm(request.POST or None, request.FILES)
        if form.is_valid():
            #print 'test'
            new_status = form.save(commit=False)
            new_status.created_by = request.user
            new_status.save()
            previous_url = request.META.get('HTTP_REFERER', reverse('timelines:picture', args=(request.user,)))
            return HttpResponseRedirect(previous_url)
    else:
        form = ImageTimelineForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('timelines/picture.html', variables)


def video(request, template='   timelines/video.html'):
    if request.method == 'POST':
        form = YoutubeTimelineForm(request.POST or None, request.FILES)
        if form.is_valid():
            #print 'test'
            new_status = form.save(commit=False)
            new_status.created_by = request.user
            new_status.save()
            previous_url = request.META.get('HTTP_REFERER', reverse('timelines:video', args=(request.user,)))
            return HttpResponseRedirect(previous_url)
    else:
        form = YoutubeTimelineForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('timelines/video.html', variables)


def attach(request, template='   timelines/attach.html'):
    if request.method == 'POST':
        form = FileTimelineForm(request.POST or None, request.FILES)
        if form.is_valid():
            #print 'test'
            new_status = form.save(commit=False)
            new_status.created_by = request.user
            new_status.save()
            previous_url = request.META.get('HTTP_REFERER', reverse('timelines:attach', args=(request.user,)))
            return HttpResponseRedirect(previous_url)
    else:
        form = FileTimelineForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('timelines/attach.html', variables)
