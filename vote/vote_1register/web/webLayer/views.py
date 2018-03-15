from django.shortcuts import render, render_to_response
from django.http import JsonResponse
from django.template import loader


def index(request):
	return _success_response(request)

def goober(request):
	return _success_response(request, resp = "I'm a goofy goober!")


def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})

def login(request):
    return render_to_response('webLayer/login.html')
