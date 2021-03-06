from django.conf.urls import url

from . import views

app_name = 'email_analysis'
urlpatterns = [
    url(r'^$', views.EmailAnalysisIndex.as_view(), name='index'),
    url(r'^import/$', views.ImportView.as_view(), name='import'),
    # url(r'^import/parse$', views.parse, name='parse'),
    url(r'^import/review$', views.review, name='review'),
    url(r'^import/save$', views.save, name='save'),
    url(r'^(?P<pk>[0-9a-z]{32})/$', views.EmailDetailView.as_view(), name='details'),
]
