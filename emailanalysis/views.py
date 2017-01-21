from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
# from django.views import generic

from .models import Email


def index(request):
    return HttpResponse("You're on the email analysis page!")


def upload(request):
    return HttpResponse("You're on the email upload page!")


def details(request, email_id):
    email = get_object_or_404(Email, pk=email_id)
    return render(request, 'emailanalysis/specific-email.html', {'email': email})