from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.db.models import Q
from friendship.models import Friend, FriendshipRequest
from django.utils import simplejson
from app.academy.models import Course, CourseMembership


@login_required
def finduser(request):
    users = User.objects.filter(is_active=True)
    if request.is_ajax():
        q = request.GET.get('term', '')
        list_users = users.filter(username__icontains=q)
        results = []
        for user in list_users:
            user_dict = user.username
            results.append(user_dict)
        output = simplejson.dumps(results)
    else:
        output = 'fail'
    return HttpResponse(output, mimetype='application/json')


@login_required
def findlocation(request):
    users = User.objects.filter(is_active=True)
    if request.is_ajax():
        q = request.GET.get('term', '')
        list_users = users.filter(profile__location__icontains=q)
        results = []
        for user in list_users:
            loc_dict = user.profile.location
            results.append(loc_dict)
        output = simplejson.dumps(results)
    else:
        output = 'fail'
    return HttpResponse(output, mimetype='application/json')


@login_required
def findcourse(request):
    courses = Course.objects.filter(name__in=request.user.active_courses())
    if request.is_ajax():
        q = request.GET.get('term', '')
        list_course = courses.filter(name__icontains=q)
        results = []
        for course in list_course:
            loc_dict = course.name
            results.append(loc_dict)
        output = simplejson.dumps(results)
    else:
        output = 'fail'
    return HttpResponse(output, mimetype='application/json')


@login_required
def search(request, template='connections/search.html'):
    query = request.GET.get('q', '')
    qlocation = request.GET.get('l', '')
    qphoto = request.GET.get('p', '')
    qschool = request.GET.get('s', '')
    qcourse = request.GET.get('c', '')
    photocheck = ''
    schoolcheck = ''
    users = User.objects.filter(is_active=True)
    all_friends = Friend.objects.friends(request.user)
    filters = Q(is_active=True)
    if qphoto:
        filters = ~Q(profile__picture='')
        photocheck = ' checked'

    if query or qlocation:
        users = users.filter(username__icontains=query, profile__location__icontains=qlocation, profile__picture__isnull=True)

    users = users.filter(filters)

    if qcourse:
        course = Course.objects.get(name=qcourse)
        users = course.members.all()

    if qschool:
        filters = Q(university=request.user.university_set.get())
        users = users.filter(filters)
        schoolcheck = ' checked'

    variables = RequestContext(request, {
        'users': users,
        'query': query,
        'qlocation': qlocation,
        'qcourse': qcourse,
        'photocheck': photocheck,
        'schoolcheck': schoolcheck,
        'friends': all_friends
    })
    return render(request, template, variables)


@login_required
def friends(request):
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)
    variables = RequestContext(request, {
        'user_profile': request.user,
        'requests': friendship_requests,
    })
    return render(request, 'friendship/friend/requests_list.html', variables)


@login_required
def add(request, username):
    request_user = request.user
    added_user = get_object_or_404(User, username=username, is_active=True)

    friends = Friend.objects.are_friends(request_user, added_user)

    if friends:
        Friend.objects.remove_friend(request_user, added_user)

    else:
        try:
            Friend.objects.add_friend(request_user, added_user)
        except:
            pass

    previous_url = request.META.get('HTTP_REFERER', reverse('connections:search'))
    return HttpResponseRedirect(previous_url)


@login_required
def accept(request, req_id):
    f_request = get_object_or_404(FriendshipRequest, id=req_id)
    f_request.accept()
    #return redirect('friendship_view_friends', username=request.user.username)

    previous_url = request.META.get('HTTP_REFERER', reverse('connections:friends'))
    return HttpResponseRedirect(previous_url)


@login_required
def reject(request, req_id):
    f_request = get_object_or_404(FriendshipRequest, id=req_id)
    f_request.reject()
    #return redirect('friendship_view_friends', username=request.user.username)

    previous_url = request.META.get('HTTP_REFERER', reverse('connections:friends'))
    return HttpResponseRedirect(previous_url)
