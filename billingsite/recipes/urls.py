from django.conf.urls import url
from . import views
from . import viewsroommates

app_name = "recipes"

urlpatterns = [

# =======================================================
# ======                 Bills                     ======
# =======================================================

# ~~~~~~~~~~~ Display ~~~~~~~~~~~~

    #<WebSite.com>/bills/
    url(r'^$', views.index, name="index"),
    #<WebSite.com>/bills/
    url(r'^bymonth/$', views.indexbymonth, name="indexbymonth"),
    #<WebSite.com>/bills/<recipe_id>/
    url(r'^(?P<bill_id>[0-9]+)/$', views.viewBill, name="viewBill"),

# ~~~~~~~~~~~~~ Edit/Submit/Delete ~~~~~~~~~~~~~~~~
    #<WebSite.com>/bills/<recipe_id>/edit
    url(r'^(?P<bill_id>[0-9]+)/edit$', views.editBill, name="editBill"),

    #<WebSite.com>/bills/submit/
    url(r'^submit/$', views.submitBill, name="submitBill"),

    #<WebSite.com>/bills/<bill_id>/delete
    url(r'^(?P<bill_id>[0-9]+)/deletebill$', views.deletebill, name="deletebill"),

# =======================================================
# ======               Roommates                   ======
# =======================================================


    #<WebSite.com>/bills/
    url(r'^allroommates/$', viewsroommates.allroommates, name="allroommates"),

    #<WebSite.com>/bills/<roommate_id>/edit
    url(r'^roommate/(?P<roommate_id>[0-9]+)/edit/$', viewsroommates.editroommate, name="editroommate"),


    #<WebSite.com>/bills/roommate/<roommate_id>/
    url(r'^roommate/(?P<roommate_id>[0-9]+)/$', viewsroommates.userpayments, name="userpayments"),
    #<WebSite.com>/bills/roommate/<roommate_id>/editpayment/<payment_id>/
    url(r'^roommate/(?P<roommate_id>[0-9]+)/editpayment/(?P<payment_id>[0-9]+)/$', viewsroommates.edituserpayments, name="edituserpayments"),

    # ======================
    # ====== Payments ======
    # ======================

    # ~~~~~~~~~~~ Display ~~~~~~~~~~~~
    #<WebSite.com>/bills/
    url(r'^payments/(?P<payment_id>[0-9]+)/$', viewsroommates.paymentdetails, name="paymentdetails"),

    # ~~~~~~~~~~~~~ Edit/Submit/Delete ~~~~~~~~~~~~~~~~
    #<WebSite.com>/bills/submitpayment/
    url(r'^submitpayment/$', viewsroommates.submitPayment, name="submitPayment"),
    #<WebSite.com>/bills/submitPaymentFor/
    url(r'^submitpaymentfor/(?P<roommate_id>[0-9]+)$', viewsroommates.submitPaymentFor, name="submitPaymentFor"),

    #<WebSite.com>/bills/<bill_id>/delete
    url(r'^(?P<payment_id>[0-9]+)/deletepayment$', viewsroommates.deletepayment, name="deletepayment"),

]
