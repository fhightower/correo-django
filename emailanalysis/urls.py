from django.conf.urls import url

from . import views

app_name = 'emailanalysis'
urlpatterns = [
    url(r'^$', views.EmailAnalysisHome.as_view(), name='index'),
    url(r'^import/$', views.import_, name='import'),
<<<<<<< HEAD
    url(r'^import/submit$', views.submit, name='submit'),
    url(r'^import/submitFile$', views.submit_file, name='submit_file'),
=======
    url(r'^import/parse$', views.parse, name='parse'),
    url(r'^import/review$', views.review, name='review'),
    url(r'^import/save$', views.save, name='save'),
>>>>>>> simple_email_upload
    url(r'^(?P<pk>[0-9]+)/$', views.EmailDetailView.as_view(), name='details'),
]
