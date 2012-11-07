from django.shortcuts import render_to_response
#from django.http import HttpResponse
from django.template import RequestContext
# Create your views here.


def inbox(request):
    variables = RequestContext(request)
    return render_to_response('inbox.html', variables)


# def write(request):
#     variables = RequestContext(request)
#     return render_to_response('write.html', variables)


def sent(request):
    variables = RequestContext(request)
    return render_to_response('sent.html', variables)


def reply(request):
    variables = RequestContext(request)
    return render_to_response('reply.html', variables)
