from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<work_number>\d\d\d\d)/$', views.details),
]
