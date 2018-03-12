from django.http import JsonResponse


def index(request):
	return _success_response(request)

def goober(request):
	return _success_response(request, resp = "I'm a goofy goober!")


def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})