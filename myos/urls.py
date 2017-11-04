from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.try_login, name='login'),
    url(r'^logout/$',views.try_logout,name='logout'),
    url(r'^system/$',views.system,name='system'),
    url(r'^now/$',views.now,name='now'),
    url(r'^kill/$',views.killprocesstree,name='kill'),
    url(r'^is_login/$',views.is_login,name='is_login')
]