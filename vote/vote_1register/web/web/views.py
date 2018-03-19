from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from django.template import loader




def index(request):
	return _success_response(request)

def goober(request):
	return _success_response(request, resp = "I'm a goofy goober!")

def registrationcheck(request):
    return render(request, 'web/registrationcheck.html')
    

def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})