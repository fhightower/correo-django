import email

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Email, Host, IPAddress, Url

from .utility import indicator_parser


CONFIG = {
    "index_max_emails_listed": 7
}

class EmailAnalysisHome(generic.ListView):
    template_name = "emailanalysis/index.html"
    context_object_name = 'recent_emails'

    def get_queryset(self):
        """
        Return the five, most recently updated, emails.
        """
        if len(Email.objects.all()) >= CONFIG['index_max_emails_listed']:
            return Email.objects.all()[ len(Email.objects.all()) - CONFIG['index_max_emails_listed']:]
        else:
            return Email.objects.all()


class EmailDetailView(generic.DetailView):
    model = Email
    template_name = "emailanalysis/email-details.html"


def import_(request):
    return render(request, 'emailanalysis/import.html')

# TODO: this is a temporary hack to get data from the parse view to the review view. In the future, parse out all of the details from the email as done below, render an html page which then submits a get request to the review view with all of the pertinent information

temp_email_data = {
    'parsed_hosts': list(),
    'parsed_ip_addresses': list(),
    'parsed_urls': list(),
    'subject': None,
    'recipient_email': None,
    'sender_email': None,
    'sender_ip': None
}


def parse(request):
    try:
        full_email_text = None

        if request.POST.get('full-text'):
            full_email_text = request.POST['full-text']
        elif request.FILES.get('email-file'):
            raw_email = request.FILES['email-file'].read()
            full_email_text = raw_email.decode()

        if full_email_text is not None:
            parsed_email = email.message_from_string(full_email_text)
            temp_email_data['subject'] = parsed_email.get('subject')
            temp_email_data['recipient_email'] =  parsed_email.get('to')
            temp_email_data['reply_to'] = parsed_email.get('reply-to')
            temp_email_data['sender_email'] = parsed_email.get('from')
            temp_email_data['sender_ip'] = parsed_email.get('x-originating-ip')

            # TODO: validate that it is a good assumption that the first section of the payload will be the main body
            parser = indicator_parser.IndicatorParser(str(parsed_email.get_payload()[0]))
            results = parser.parse_indicators()
            temp_email_data['parsed_hosts'] = results['hosts']
            temp_email_data['parsed_ip_addresses'] = results['ip_addresses']
            temp_email_data['parsed_urls'] = results['urls']
        else:
            # TODO: log error here
            pass
    except KeyError as e:
        # Redisplay the question voting form.
        # TODO: implement an error message
        # return render(request, 'polls/detail.html', {
        #     'question': question,
        #     'error_message': "You didn't select a choice.",
        # })
        print("Error: {}".format(e))
    else:
        return HttpResponseRedirect(reverse('emailanalysis:review'))


def review(request):
    """Review view letting users redact information from an email."""
    return render(request, 'emailanalysis/review.html', temp_email_data)


def save(request):
    """Save an email."""
    try:
        # TODO: When I start storing the emails as files, replace the full_text variable below
        full_email_text = "This is just a placeholder text"
        email_subject = request.POST.get('email_subject')
        recipient_email = request.POST.get('recipient_email')
        sender_email = request.POST.get('sender_email')
        sender_ip = request.POST.get('sender_ip')
    except KeyError as e:
        # Redisplay the question voting form.
        # TODO: implement an error message
        # return render(request, 'polls/detail.html', {
        #     'question': question,
        #     'error_message': "You didn't select a choice.",
        # })
        print("Error: {}".format(e))
    else:
        new_email = Email(full_text=full_email_text, subject=email_subject, recipient_email=recipient_email, sender_email=sender_email, sender_ip=sender_ip, submitter="12345678")
        new_email.save()
        return HttpResponseRedirect(reverse('emailanalysis:details', args=(new_email.id,)))
