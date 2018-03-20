from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from django.template import loader




def registrationcheck(request):
    return render(request, 'registrationcheck.html')
    
