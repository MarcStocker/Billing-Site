from django.conf.urls import url
from . import views

app_name = "recipes"

urlpatterns = [
    #<WebSite.com>/bills/
    url(r'^$', views.index, name="index"),
    #<WebSite.com>/bills/
    url(r'^bymonth/$', views.indexbymonth, name="indexbymonth"),


    #<WebSite.com>/bills/
    url(r'^allroommates/$', views.allroommates, name="allroommates"),

    #<WebSite.com>/bills/<recipe_id>/edit
    url(r'^roommate/(?P<roommate_id>[0-9]+)/edit/$', views.editroommate, name="editroommate"),

    #<WebSite.com>/bills/
    url(r'^payments/(?P<payment_id>[0-9]+)/$', views.paymentdetails, name="paymentdetails"),

    #<WebSite.com>/bills/
    url(r'^roommate/(?P<roommate_id>[0-9]+)/$', views.userpayments, name="userpayments"),

    #<WebSite.com>/bills/search
    # url(r'^search$', views.searchRecipes, name="searchRecipes"),
    #<WebSite.com>/bills/<recipe_id>/
    url(r'^(?P<bill_id>[0-9]+)/$', views.viewBill, name="viewBill"),
    #<WebSite.com>/bills/<recipe_id>/edit
    url(r'^(?P<bill_id>[0-9]+)/edit$', views.editBill, name="editBill"),


    #<WebSite.com>/bills/submit/
    url(r'^submit/$', views.submitBill, name="submitBill"),
    #<WebSite.com>/bills/submit/
    url(r'^submitpayment/$', views.submitPayment, name="submitPayment"),

    #<WebSite.com>/bills/<bill_id>/delete
    url(r'^(?P<bill_id>[0-9]+)/deletebill$', views.deletebill, name="deletebill"),
    #<WebSite.com>/bills/<bill_id>/delete
    url(r'^(?P<payment_id>[0-9]+)/deletepayment$', views.deletepayment, name="deletepayment"),
]
