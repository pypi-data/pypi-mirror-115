from django.http import HttpResponse


def test(*args, **kwargs):
    return HttpResponse('ok', status=200)
