from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import edgar, Roommates, Payments


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

class EdgarForm(forms.ModelForm):
    class Meta:
        model = edgar
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
    class Meta:
        model = Payments
        fields = ['roommate', 'amount', 'paymenttype', 'datepaid', 'description']
