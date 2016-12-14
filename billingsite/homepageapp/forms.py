
from django.contrib.auth.forms import AuthenticationForm
from django import forms


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
