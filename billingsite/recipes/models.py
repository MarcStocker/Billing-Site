from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Bills(models.Model):
    PGE = 'PG&E'
    WATER = "CalWater"
    COMCAST = "Comcast"
    BILL_CHOICES = (
        (PGE, 'PG&E'),
        (WATER, 'CalWater'),
        (COMCAST, 'Comcast'),
    )
    category = models.CharField(max_length=8, choices=BILL_CHOICES)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    image = models.FileField(max_length=144, upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    priceper = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    month = models.ForeignKey('BillingMonth', null=True, blank=True, default="", on_delete=models.SET_DEFAULT)



    def __str__(self):
        Bills.objects.order_by('-self.date')
        return str(self.id) + " - " + str(self.category) + " - " + self.month.themonth + " - $" + str(self.amount)
    def save(self, *args, **kwargs):
        all_bills = Bills.objects.all()
        if Bills.objects.filter(month=self.month, category=self.category).exists():
            bill = Bills.objects.get(month=self.month, category=self.category)
            if str(bill.id) == str(self.id):
                print("same bill, update it")
            else:
                raise ValidationError("This Bill Already Exists")
        if self.priceper:
            self.priceper = self.amount/5
        super(Bills, self).save(*args, **kwargs)

class BillingMonth(models.Model):
    class Meta:
        ordering = ('-theyear', '-themonthnum')
    jan = "January"; feb = "Febrary"; mar = "March"; apr = "April";
    may = "May"; jun = "June"; jul = "July"; aug = "August";
    sept= "September"; octo= "October"; nov = "November"; dec = "December";
    MONTH_CHOICES = (
        (jan, 'January'), (feb, 'Febrary'), (mar, 'March'),(apr, 'April'), (may, 'May'),
        (jun, 'June'), (jul, 'July'), (aug, 'August'), (sept, 'September'),
        (octo, 'October'), (nov, 'November'), (dec, 'December'),
    )

    year_range = range(2014, 2020, 1);
    YEAR_CHOICES = ( (i, i) for i in year_range )
    # themonth = models.DateField()
    themonth = models.CharField(max_length=12, choices=MONTH_CHOICES)
    themonthnum = models.IntegerField(default="", null=True, blank=True)
    theyear = models.IntegerField(choices=YEAR_CHOICES, default="")
    priceperroomate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)
    pgebill = models.ForeignKey('Bills', null=True, blank=True, default="", on_delete=models.SET_DEFAULT, related_name="thepgebill")
    calwaterbill = models.ForeignKey('Bills', null=True, blank=True, default="", on_delete=models.SET_DEFAULT, related_name="thewaterbill")
    comcastbill = models.ForeignKey('Bills', null=True, blank=True, default="", on_delete=models.SET_DEFAULT, related_name="thecomcastbill")

    def __str__(self):
        BillingMonth.objects.all().order_by('-theyear').order_by('-themonthnum')
        # return (str(self.themonth.strftime('%b %Y')))
        pge = ""
        water = ""
        comcast = ""
        if self.pgebill:
            pge = str("$" + str(self.pgebill.amount))
        else:
            pge = "$ 0.00"
        if self.calwaterbill:
            water = str("$" + str(self.calwaterbill.amount))
        else:
            water = "$ 0.00"
        if self.comcastbill:
            comcast = str("$" + str(self.comcastbill))
        else:
            comcast = "$ 0.00"
        return str(self.theyear) + " - " + str(self.themonth) + ' - PG&E: '+ pge + ' - CalWater: ' + water + ' - Comcast: ' + comcast

    def addbill(self, instance, cat, *args, **kwargs):
        total = self.priceperroomate
        total = 0
        if cat == "none":
            print("Bill was deleted, recalculating Price Per Roommate")
        else:
            if cat == "PG&E":
                self.pgebill = Bills.objects.get(pk=instance)
            if cat == "CalWater":
                self.calwaterbill = Bills.objects.get(pk=instance)
            if cat == "Comcast":
                self.comcastbill = Bills.objects.get(pk=instance)
        if self.pgebill:
            total = total + self.pgebill.amount
        if self.calwaterbill:
            total = total + self.calwaterbill.amount
        if self.comcastbill:
            total = total + self.comcastbill.amount
        if total == 0:
            self.priceperroomate = 0
        else:
            total = total / 5
            self.priceperroomate = total
        if self.themonth == "January": self.themonthnum = 1
        elif self.themonth == "February": self.themonthnum = 2
        elif self.themonth == "March": self.themonthnum = 3
        elif self.themonth == "April": self.themonthnum = 4
        elif self.themonth == "May": self.themonthnum = 5
        elif self.themonth == "June": self.themonthnum = 6
        elif self.themonth == "July": self.themonthnum = 7
        elif self.themonth == "August": self.themonthnum = 8
        elif self.themonth == "September": self.themonthnum = 9
        elif self.themonth == "October": self.themonthnum = 10
        elif self.themonth == "November": self.themonthnum = 11
        elif self.themonth == "December": self.themonthnum = 12
        print("Added/deleted Payment, new Price_Per_Rommate: $" + str(self.priceperroomate))
        super(BillingMonth, self).save(*args, **kwargs)
    def new(self, *args, **kwargs):
        if self.themonth == "January": self.themonthnum = 1
        elif self.themonth == "February": self.themonthnum = 2
        elif self.themonth == "March": self.themonthnum = 3
        elif self.themonth == "April": self.themonthnum = 4
        elif self.themonth == "May": self.themonthnum = 5
        elif self.themonth == "June": self.themonthnum = 6
        elif self.themonth == "July": self.themonthnum = 7
        elif self.themonth == "August": self.themonthnum = 8
        elif self.themonth == "September": self.themonthnum = 9
        elif self.themonth == "October": self.themonthnum = 10
        elif self.themonth == "November": self.themonthnum = 11
        elif self.themonth == "December": self.themonthnum = 12
        print(self.themonth)
        super(BillingMonth, self).save(*args, **kwargs)
