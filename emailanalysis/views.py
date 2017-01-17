from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic


def index(request):
    return HttpResponse("You're on the email analysis page!")


def upload(request):
    return HttpResponse("You're on the email upload page!")


class SpecificEmailView(generic.DetailView):
    """"""
    template_name = 'emailanalysis/specific_email.html'


