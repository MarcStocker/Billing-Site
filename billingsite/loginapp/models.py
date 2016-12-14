from django.db import models
from datetime import datetime

# Create your models here.

class edgar(models.Model):
    banner = models.CharField(max_length=50, default="")
    description = models.TextField(max_length=1000, null=True, blank=True)
    pge_image = models.ImageField(max_length=144, upload_to='companyImages/pge/', null=True, blank=True)
    calwater_image = models.ImageField(max_length=144, upload_to='companyImages/calwater/', null=True, blank=True)
    comcast_image = models.ImageField(max_length=144, upload_to='companyImages/comcast/', null=True, blank=True)

    def __str__(self):
        return "Website_Info"
class Roommates(models.Model):
    name = models.CharField(max_length=30, default="no name")
    totalpaid = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, default=0)
    comments = models.TextField(max_length=2000, null=True, blank=True, default="none")
    class Meta:
        ordering = ('id',)

    def save(self, *args, **kwargs):
        all_roommates = Roommates.objects.all()
        for a in range(1, 100):
            if all_roommates.filter(pk=a).exists():
                print("Exists, add 1 to ID: " +  str(a))
            else:
                print("changing id num??")
                self.id = a
                break
        super(Roommates, self).save(*args, **kwargs)

    def comment(self, form, *args, **kwargs):
        self.comments = form.cleaned_data['comments']
        super(Roommates, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        print("updating")
        pay = Payments.objects.all()
        maxid = 20
        total = self.totalpaid
        total = 0
        print("ROOMMATES: Interating through payments, up to maxid=" + str(maxid))
        for a in range(0, maxid):
            print("a = " + str(a))
            if pay.filter(pk=a).exists():
                if Payments.objects.get(pk=a).roommate.id == self.id:
                    total = total + Payments.objects.get(pk=a).amount
        self.totalpaid = total
        print(self.name + ": total paid = " + str(self.totalpaid))
        super(Roommates, self).save(*args, **kwargs)
    def __str__(self):
        return "Roommate #" + str(self.id) + ": " + self.name

class Payments(models.Model):
    google = "Google Wallet"
    cash   = "Cash"
    venmo  = "Venmo"
    bank   = "Bank Transfer"
    checks  = "Check"
    PAY_CHOICES = (
        (google, 'Google Wallet'),
        (cash, 'Cash'),
        (venmo, 'Venmo'),
        (bank, 'Bank'),
        (checks, 'Check')
    )
    roommate = models.ForeignKey('Roommates', on_delete=models.SET_DEFAULT, default="")
    name = models.CharField(max_length=30, null=True, blank=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    paymenttype = models.CharField(max_length=15, choices=PAY_CHOICES)
    description = models.CharField(max_length=200)
    datepaid = models.DateField(default=datetime.now, null=True, blank=True)
    stillowed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)
    checkimg = models.ImageField(max_length=144, upload_to='checks/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return str(self.id) + ": " +self.name + " - $" + str(self.amount) + " - " + self.paymenttype + " - " + str(self.datepaid)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.roommate.name
        all_payments = Payments.objects.all()
        for a in range(1, 999):
            if all_payments.filter(pk=a).exists():
                print("Exists, add 1 to ID: " +  str(a))
            else:
                self.id = a
                break
        print("MONTH running update on ROOMMATES")
        super(Payments, self).save(*args, **kwargs)
        Roommates.objects.get(pk=self.roommate.id).update()
