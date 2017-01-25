from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Email


class EmailAnalysisHome(generic.ListView):
    template_name = "emailanalysis/index.html"
    context_object_name = 'recent_emails'

    def get_queryset(self):
        """
        Return the five, most recently updated, emails.
        """
        # todo: implement this more thoroughly
        return Email.objects.all()[:5]


def upload(request):
    return render(request, 'emailanalysis/upload.html')

class EmailDetailView(generic.DetailView):
    model = Email
    template_name = "emailanalysis/email-details.html"
