from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.paginator import PageNotAnInteger


def search(request):
    looks = User.objects.all()
    # paginator = Paginator(look, 2)

    # page = request.GET.get('page')
    # try:
    #     look_for = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     look_for = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     look_for = paginator.page(paginator.num_pages)
    variables = RequestContext(request, {
        'looks': looks
        })
    return render_to_response('search.html', variables)


def profile(request):
    variables = RequestContext(request)
    return render_to_response('profile.html', variables)

