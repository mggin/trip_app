from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login_register$', views.login_register),
    url(r'^users/create$', views.create_user),
    url(r'^login$', views.login),
    url(r'^trips$', views.view_trips),
    url(r'^trips/form$', views.view_trip_form),
    url(r'^trips/create$', views.create_trip),
    url(r'^trips/(?P<trip_id>[0-9]+)/show$', views.show_trip),
    url(r'^trips/(?P<trip_id>[0-9]+)/edit$', views.edit_trip),
    url(r'^trips/(?P<trip_id>[0-9]+)/update$', views.update_trip),
    url(r'^trips/(?P<trip_id>[0-9]+)/destroy$', views.delete_trip),
    url(r'^log_off$', views.log_off),
    url(r'^trips/(?P<trip_id>[0-9]+)/join$', views.join_trip),
    url(r'^trips/(?P<trip_id>[0-9]+)/cancel$', views.cancel_trip),


    

]