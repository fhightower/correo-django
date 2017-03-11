import datetime
import email
import json

# todo: do we need this import?
from django.http import Http404, HttpResponse

from django.core.files import File
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


from .forms import ExampleForm
from .models import Email


class EmailAnalysisHome(generic.ListView):
    template_name = "emailanalysis/index.html"
    context_object_name = 'recent_emails'

    def get_queryset(self):
        """Return the five, most recently updated, emails."""
        # todo: implement this more thoroughly
        return Email.objects.all()[:5]


class EmailDetailView(generic.DetailView):
    model = Email
    template_name = "emailanalysis/email-details.html"


# def import_(request):
#     return render(request, 'emailanalysis/import.html')


class ExampleFormView(generic.FormView):
    template_name = 'emailanalysis/import.html'
    form_class = ExampleForm

    # def get_initial(self):
    #     return {
    #         "images": "http://localhost:8001/media/user_uploads/2016-01-06 13:30:12.432073-"
    #                   "Dressage-Mastery-Academy-Dressage-Explained-Part-2-Losgelassenheit-Mindset.pdf,"
    #                   "http://localhost:8001/media/user_uploads/2016-01-06 08:02:00.185925-IMG_20160104_215821.jpg"
    #     }

    def get(self, *args, **kwargs):
        return super(ExampleFormView, self).get(*args, **kwargs)


def submit(request):
    """Handle email import (using individual form elements)."""
    try:
        full_email_text = request.POST['full-text']
        email_subject = request.POST['subject']
        recipient_email = request.POST['recipient-email']
        sender_email = request.POST['sender-email']
        sender_ip_address = request.POST['sender-ip']
    except (KeyError):
        # Redisplay the question voting form.
        # todo: implement an error message
        # return render(request, 'polls/detail.html', {
        #     'question': question,
        #     'error_message': "You didn't select a choice.",
        # })
        pass
    else:
        new_email = Email(full_text=full_email_text, subject=email_subject, recipient_email=recipient_email, sender_email=sender_email, sender_ip=sender_ip_address, submitter="12345678")
        new_email.save()
        return HttpResponseRedirect(reverse('emailanalysis:details', args=(new_email.id,)))


# def submit_file(request):
#     """Handle an email that is uploaded as a file."""
#     redirect_id = 1
#     # todo: figure out why there are two post requests coming in here when uploading a file (I am almost positive it has to do with drop-zone)
#     if request.FILES.get('file'):
#         try:
#             # read the file sent in the POST
#             my_file = File(request.FILES['file'])
#             raw_email = my_file.read()
#         except Exception as e:
#             # handle any errors retrieving the file from the POST
#             # todo: add error message here
#             print(e)
#             # return HttpResponseRedirect(reverse('emailanalysis:details', args=(redirect_id,)))
#         else:
#             # parse and create a new email object
#             try:
#                 parsed_email = email.message_from_string(raw_email.decode())
#             except Exception as e:
#                 # todo: add error handling here
#                 raise e
#             else:
#                 subject = parsed_email.get('subject')
#                 recipient_email = parsed_email.get('to')
#                 sender_email = parsed_email.get('from')
#                 sender_ip = parsed_email.get('x-originating-ip')

#                 # todo: implement submitter id creation
#                 new_email = Email(full_text=raw_email, subject=subject, recipient_email=recipient_email, sender_email=sender_email, sender_ip=sender_ip, submitter="12345678")
#                 new_email.save()
#                 redirect_id = new_email.id

#             print(redirect_id)
#             return HttpResponseRedirect(reverse('emailanalysis:details', args=(redirect_id,)))
#     else:
#         return HttpResponse()


# def upload_file(self, request, *args, **kwargs):
#     try:
#         album = Album.objects.get(pk=kwargs.get('pk'))
#     except Album.DoesNotExist:
#         error_dict = {'message': 'Album not found.'}
#         return self.render_json_response(error_dict, status=404)

#     uploaded_file = request.FILES['file']
#     Photo.objects.create(album=album, file=uploaded_file)

#     response_dict = {
#         'message': 'File uploaded successfully!',
#     }

#     return self.render_json_response(response_dict, status=200)


class ParseView(generic.View):
    def post(self, request):
        assert len(self.request.FILES) == 1
        redirect_id = 1

        if request.FILES.get('file'):
            try:
                # read the file sent in the POST
                my_file = File(request.FILES['file'])
                raw_email = my_file.read()
            except Exception as e:
                # handle any errors retrieving the file from the POST
                # todo: add error message here
                print("Error: {}".format(e))
                # return HttpResponseRedirect(reverse('emailanalysis:details', args=(redirect_id,)))
            else:
                # parse and create a new email object
                try:
                    parsed_email = email.message_from_string(raw_email.decode())
                except Exception as e:
                    # todo: add error handling here
                    raise e
                else:
                    subject = parsed_email.get('subject')
                    recipient_email = parsed_email.get('to')
                    sender_email = parsed_email.get('from')
                    sender_ip = parsed_email.get('x-originating-ip')

                    # todo: implement submitter id creation
                    new_email = Email(full_text=raw_email, subject=subject, recipient_email=recipient_email, sender_email=sender_email, sender_ip=sender_ip, submitter="12345678")

                    # new_email.save()
                    # redirect_id = new_email.id

                return HttpResponseRedirect(reverse('emailanalysis:review', args=({'recipient_email': recipient_email, 'sender_email': sender_email, 'sender_ip': sender_ip})))

            # except Exception as e:
            #     print("Error: {}".format(e))

def review(subject, recipient_email, sender_email, sender_ip):
    """."""
    print(sender_ip)
    context = {
        'subject': subject,
        'recipient_email': recipient_email,
        'sender_email': sender_email,
        'sender_ip': sender_ip,
    }

    return render(request, 'emailanalysis/review.html', context)


class UploadView(generic.View):
    def post(self, request):
        assert len(self.request.FILES) == 1
        redirect_id = 1

        if request.FILES.get('file'):
            try:
                # read the file sent in the POST
                my_file = File(request.FILES['file'])
                raw_email = my_file.read()
            except Exception as e:
                # handle any errors retrieving the file from the POST
                # todo: add error message here
                print("Error: {}".format(e))
                # return HttpResponseRedirect(reverse('emailanalysis:details', args=(redirect_id,)))
            else:
                # parse and create a new email object
                try:
                    parsed_email = email.message_from_string(raw_email.decode())
                except Exception as e:
                    # todo: add error handling here
                    raise e
                else:
                    subject = parsed_email.get('subject')
                    recipient_email = parsed_email.get('to')
                    sender_email = parsed_email.get('from')
                    sender_ip = parsed_email.get('x-originating-ip')

                    # todo: implement submitter id creation
                    new_email = Email(full_text=raw_email, subject=subject, recipient_email=recipient_email, sender_email=sender_email, sender_ip=sender_ip, submitter="12345678")
                    # new_email.save()
                    # redirect_id = new_email.id

                return HttpResponseRedirect(reverse('emailanalysis:details', args=(redirect_id,)))
            # except Exception as e:
            #     print("Error: {}".format(e))


# class UploadView(generic.View):
#     def post(self, request):
#         assert len(self.request.FILES) == 1

#         if request.FILES.get('file'):
#             try:
#                 # read the file sent in the POST
#                 tmp_file = File(request.FILES['file'])
#                 # raw_email = my_file.read()
#                 # print(raw_email)
#                 # print(my_file.name)

#                 with default_storage.open("raw_emails/" + str(datetime.datetime.now()).split(" ")[0] + "-" + tmp_file.name, "wb+") as f:
#                     for chunk in tmp_file.chunks():
#                         f.write(chunk)

#                     file_url = default_storage.url(f.name)
#                     print(file_url)

#                 return HttpResponse(json.dumps({"file_url": file_url}))
#             except Exception as e:
#                 print("Error: {}".format(e))

        # print(self.request.FILES)
        # field_name = my_file.name
        # , tmp_file = self.request.FILES.items()
        # # TODO: Use "T" as date and time separator instead of space.
        # with default_storage.open("user_uploads/" + str(datetime.datetime.now()) + "-" + tmp_file.name, "wb+") as f:
        #     for chunk in tmp_file.chunks():
        #         f.write(chunk)

        #     file_url = default_storage.url(f.name)

        # return HttpResponse(json.dumps({"file_url": file_url}))
