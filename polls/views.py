from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

#가장 간단한 형태의 뷰.
