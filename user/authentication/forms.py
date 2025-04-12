from django import forms
from .models import User

class RegisterForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
