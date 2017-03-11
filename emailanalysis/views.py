import email

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
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


class EmailDetailView(generic.DetailView):
    model = Email
    template_name = "emailanalysis/email-details.html"


def import_(request):
    return render(request, 'emailanalysis/import.html')

# TODO: this is a temporary hack to get data from the parse view to the review view. In the future, parse out all of the details from the email as done below, render an html page which then submits a get request to the review view with all of the pertinent information

temp_email_data = {
    'subject': None,
    'recipient_email': None,
    'sender_email': None,
    'sender_ip': None
}


def parse(request):
    try:
        if request.POST.get('full-text'):
            full_email_text = request.POST['full-text']

        elif request.FILES.get('email-file'):
            email_file = request.FILES['email-file']

        # full_email_text = request.POST['full-text']
        # email_subject = request.POST['subject']
        # recipient_email = request.POST['recipient-email']
        # sender_email = request.POST['sender-email']
        # sender_ip_address = request.POST['sender-ip']
        parsed_email = email.message_from_string(full_email_text)
        temp_email_data['subject'] = parsed_email.get('subject')
        temp_email_data['recipient_email'] =  parsed_email.get('to')
        temp_email_data['sender_email'] = parsed_email.get('from')
        temp_email_data['sender_ip'] = parsed_email.get('x-originating-ip')
    except KeyError as e:
        # Redisplay the question voting form.
        # todo: implement an error message
        # return render(request, 'polls/detail.html', {
        #     'question': question,
        #     'error_message': "You didn't select a choice.",
        # })
        print("Error: {}".format(e))
    else:
        # email_file = request.FILES.get('file')
        # print(email_file)
        # new_email = Email(full_text=full_email_text, subject=email_subject, recipient_email=recipient_email, sender_email=sender_email, sender_ip=sender_ip_address, submitter="12345678")
        # new_email.save()
        # return HttpResponseRedirect(reverse('emailanalysis:details', args=(new_email.id,)))
        return HttpResponseRedirect(reverse('emailanalysis:review'))

def review(request):
    """."""
    print("here: {}".format(request))
    return render(request, 'emailanalysis/review.html', temp_email_data)
