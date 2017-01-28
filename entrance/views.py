from django.shortcuts import get_object_or_404, render
from django.views import generic


def index(request):
    return render(request, 'entrance/index.html')


def about(request):
    return render(request, 'entrance/about.html')


def invest(request):
    return render(request, 'entrance/invest.html')
