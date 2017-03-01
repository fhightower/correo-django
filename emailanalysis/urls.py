from django.conf.urls import url

from . import views

app_name = 'emailanalysis'
urlpatterns = [
    url(r'^$', views.EmailAnalysisHome.as_view(), name='index'),
    url(r'^import/$', views.ExampleFormView.as_view(), name='import'),
    url(r'^import/submit$', views.submit, name='submit'),
    url(r'^import/submitFile$', views.submit_file, name='submit_file'),
    url(r'^import/upload/$', views.UploadView.as_view(), name='upload'),
    url(r'^(?P<pk>[0-9]+)/$', views.EmailDetailView.as_view(), name='details'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
