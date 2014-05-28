from django.http import HttpResponse


def sync(request):
    return HttpResponse('hey!')
