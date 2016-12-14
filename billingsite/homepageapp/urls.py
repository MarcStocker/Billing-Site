from django.conf.urls import url
from . import views

app_name = 'homepageapp'

urlpatterns = [
    #<WebSite.com>/
    url(r'^$', views.home, name="home"),
    #<WebSite.com>/home/
    url(r'^home/$', views.home, name="home"),
    #<WebSite.com>/home/edit
    url(r'^home/edit/$', views.editwebsite, name="editwebsite"),
]
