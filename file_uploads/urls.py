from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        '^upload/$',
        views.UploadView.as_view(),
        name='upload',
    ),
]
