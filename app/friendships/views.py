from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from friendship.models import Friend
#from django.core.paginator import PageNotAnInteger


def search(request):
    all_friends = Friend.objects.friends(request.user)
    if request.method == 'POST':
        search = request.POST.get('searchbox', '')
        looks = User.objects.filter(username__contains=request.POST.get('searchbox', ''))
    else:
        search = ""
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
        'looks': looks,
        'search': search,
        'all_friends': all_friends
        })
    return render_to_response('search.html', variables)


def profile(request):
    variables = RequestContext(request)
    return render_to_response('profile.html', variables)

