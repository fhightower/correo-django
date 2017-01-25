from django.conf.urls import url

from . import views

app_name = 'emailanalysis'
urlpatterns = [
    url(r'^$', views.EmailAnalysisHome.as_view(), name='index'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^upload/review$', views.review, name='review'),
    url(r'^(?P<pk>[0-9]+)/$', views.EmailDetailView.as_view(), name='details'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
