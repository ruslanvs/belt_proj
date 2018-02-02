print '*'*25, 'APPS URLS.PY', '*'*25
from django.conf.urls import url
from . import views

urlpatterns = [
    url( r'^$', views.index ),
    url( r'^sign_in$', views.sign_in ),
    url( r'^sign_out$', views.sign_out ),
    url( r'^sign_up$', views.sign_up ),
    url( r'^travels$', views.travels ),
    url( r'^travels/(?P<id>\d+)/show$', views.travel_show ),
    url( r'^travels/(?P<id>\d+)/join$', views.travel_join ),
    url( r'^travels/(?P<id>\d+)/leave$', views.travel_leave ),
    url( r'^travels/new$', views.travel_new ),
    url( r'^travels/create$', views.travel_create ),

    # url( r'^route2$', views.route2 ),
    # url( r'^route3$', views.route3 ),
]