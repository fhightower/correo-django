from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    # todo: implement the landing pages, etc.
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^email/', include('email_analysis.urls')),
    url(r'^admin/', admin.site.urls),
]
