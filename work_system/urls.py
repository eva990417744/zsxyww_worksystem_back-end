from django.conf.urls import url
from . import views

# all char !!!!!!!!!!(?P<start>\d+)char!!!!!!!!!!!change view
urlpatterns = [
    url(r'^change_announcement/$', views.change_announcement, name='change_announcement'),
    url(r'^try_logout/$', views.try_logout, name='logout'),
    url(r'^try_login/$', views.try_login, name='login'),
    url(r'^is_login/$', views.is_login, name='is_login'),
    url(r'^personal_change/$', views.personal_change, name='personal_change'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^check_in/$', views.check_in, name='check_in'),
    url(r'^check_out/$', views.check_out, name='check_out'),
    url(r'^extra_work_add/$', views.extra_work_add, name='extra_work_add'),
    url(r'^personal_extra_work_view/$', views.personal_extra_work_view, name='personal_extra_work_view'),
    url(r'^extra_work_view/$', views.extra_work_view, name='extra_work_view'),
    url(r'^extra_work_change/$', views.extra_work_change, name='extra_work_change'),
    url(r'^work_situation_add/$', views.work_situation_add, name='work_situation_add'),
    url(r'^work_situation_view/(?P<area>\S+)/$', views.work_situation_view, name='work_situation_view'),
    url(r'^work_situation_change/$', views.work_situation_change, name='work_situation_change'),
    url(r'^work_order_add/$', views.work_order_add, name='work_situation_add'),
    url(r'^work_order_view/(?P<area>\S+)/(?P<operator>\S+)/$', views.work_order_view, name='work_situation_view'),
    url(r'^work_order_change/', views.work_order_change, name='work_situation_change'),
    url(r'^get_upload_token/$', views.get_upload_token, name='get_upload_token'),
    url(r'^qiniu_callback/$', views.qiniu_callback, name='qiniu_callback'),
    url(r'^inquire/$', views.inquire, name='inquire'),
    url(r'^person_today/$', views.person_today, name='person_today'),
    url(r'^view_today/$', views.view_today, name='view_today'),
    url(r'^experience_view/$', views.experience_view, name='experience_view'),
    url(r'^experience_add/$', views.experience_add , name='experience_add'),
]
