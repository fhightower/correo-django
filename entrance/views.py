from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Your on the home page!")


def about(request):
    return HttpResponse("Your on the about page!")


def buy(request):
    return HttpResponse("Your on the buy page!")
