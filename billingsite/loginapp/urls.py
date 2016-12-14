from django.conf.urls import url
from . import views

app_name = 'loginapp'

urlpatterns = [
    #<WebSite.com>/login/
    url(r'^$', views.index, name="index"),
    #<WebSite.com>/register/
    url(r'register$', views.register, name="register"),
]
