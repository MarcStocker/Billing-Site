from django import forms
from .models import Bills, BillingMonth

import os
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Bills
        fields = [
            'category','description',
            'date', 'image','amount','priceper', 'month'
        ]
    def update(self, instance, thefile, commit=True):
        thisrecipe = Bills(pk=instance)
        thisrecipe.category = self.cleaned_data['category']
        thisrecipe.description = self.cleaned_data['description']
        thisrecipe.date = self.cleaned_data['date']
        thisrecipe.image = self.cleaned_data['image']
        thisrecipe.amount = self.cleaned_data['amount']
        if self.cleaned_data['month'] != "None":
            thisrecipe.month = self.cleaned_data['month']
            print(str(thisrecipe.month.id))

        if thisrecipe.amount > 0:
            thisrecipe.priceper = thisrecipe.amount / 5
        else:
            thisrecipe.priceper < 1;
        print("whats happening?")
        if commit:
            thisrecipe.save()
        return thisrecipe
    def save(self, self2, commit):
        thisrecipe = Bills()
        thisrecipe.category = self.cleaned_data['category']
        thisrecipe.description = self.cleaned_data['description']
        thisrecipe.date = self.cleaned_data['date']
        thisrecipe.image = self.cleaned_data['image']
        thisrecipe.amount = self.cleaned_data['amount']
        if self.cleaned_data['month'] != "None":
            thisrecipe.month = self.cleaned_data['month']
        if thisrecipe.amount > 0:
            thisrecipe.priceper = thisrecipe.amount / 5
        else:
            thisrecipe.priceper = 0
        print("whats happening?")
        if commit:
            thisrecipe.save()
        return thisrecipe


class MonthForm(forms.ModelForm):
    # themonth = forms.DateField(input_formats=['%m'])
    class Meta:
        model = BillingMonth
        fields = [
            'themonth', 'theyear', 'priceperroomate',
            'pgebill', 'calwaterbill', 'comcastbill'
        ]
    def addingbill(self, self2, instance, commit):
        thisrecipe = BillingMonth.objects.get(pk=instance.month.id)
        num = 0
        if Bills.objects.get(pk=instance.id):
            bill = Bills.objects.get(pk=instance.id)
            if bill.category == "PG&E":
                thisrecipe.pgebill = bill
                num = 1
            if bill.category == "CalWater":
                thisrecipe.calwaterbill = bill
                num = 2
            if bill.category == "Comcast":
                thisrecipe.comcastbill
                num = 3
        if commit:
            thisrecipe.save()
        return thisrecipe
