from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import homeMOTD, Roommates, Payments
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        max_length=30,
        # Attributes for bootstrap?? probably doesnt affect foundations, which is what I'm using
        # widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'})
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label="Password",
        max_length=99,
        widget=forms.PasswordInput()
        # widget=forms.PasswordInput(attrs{})
    )
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields=("username", "email", "password1", "password2")

    def save(self, commit=True):
        user=super(RegisterForm,self).save(commit=False)
        user.email=self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class homeMOTDform(forms.ModelForm):
    class Meta:
        model = homeMOTD
        fields = ['description', 'banner', 'pge_image', 'calwater_image', 'comcast_image']

class RoommatesForm(forms.ModelForm):
    comments = forms.CharField(
        label="Comments",
        widget=forms.Textarea()
        # widget=forms.PasswordInput(attrs{})
    )
    class Meta:
        model = Roommates
        fields = ['comments', 'name', 'totalpaid']

class PaymentForm(forms.ModelForm):
    datepaid = forms.DateField(
        label="Date Payment was received",
        help_text="Date Roommate paid",
        widget=DateInput()
    )
    class Meta:
        model = Payments
        fields = ['roommate', 'amount', 'paymenttype', 'datepaid', 'description']
