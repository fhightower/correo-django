import datetime
import json

from django.core.files import File
from django.core.files.storage import default_storage
from django.http import Http404, HttpResponse
from django.views.generic import View


class UploadView(View):
    def post(self, request):
        assert len(self.request.FILES) == 1

        if request.FILES.get('file'):
            try:
                # read the file sent in the POST
                tmp_file = File(request.FILES['file'])
                # raw_email = my_file.read()
                # print(raw_email)
                # print(my_file.name)

                with default_storage.open("user_uploads/" + str(datetime.datetime.now()).split(" ")[0] + "-" + tmp_file.name, "wb+") as f:
                    for chunk in tmp_file.chunks():
                        f.write(chunk)

                    file_url = default_storage.url(f.name)
                    print(file_url)

                return HttpResponse(json.dumps({"file_url": file_url}))
            except Exception as e:
                print("Error: {}".format(e))

        # print(self.request.FILES)
        # field_name = my_file.name
        # , tmp_file = self.request.FILES.items()
        # # TODO: Use "T" as date and time separator instead of space.
        # with default_storage.open("user_uploads/" + str(datetime.datetime.now()) + "-" + tmp_file.name, "wb+") as f:
        #     for chunk in tmp_file.chunks():
        #         f.write(chunk)

        #     file_url = default_storage.url(f.name)

        # return HttpResponse(json.dumps({"file_url": file_url}))
