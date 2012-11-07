from django.shortcuts import render_to_response
from django.template import RequestContext


def main(request):
    variables = RequestContext(request)
    return render_to_response('panel/index.html', variables)
