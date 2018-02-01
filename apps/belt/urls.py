print '*'*25, 'APPS URLS.PY', '*'*25
from django.conf.urls import url
from . import views

urlpatterns = [
    url( r'^$', views.index ),
    url( r'^home$', views.home ),
    url( r'^sign_in$', views.sign_in ),
    url( r'^sign_out$', views.sign_out ),
    url( r'^sign_up$', views.sign_up ),
    # url( r'^route2$', views.route2 ),
    # url( r'^route3$', views.route3 ),
]