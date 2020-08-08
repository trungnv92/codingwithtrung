from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account
from django.core.validators import RegexValidator
from captcha.fields import CaptchaField

class RegistrationAccountForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Bạn phải nhập địa chỉ email đúng định dạng')
    captcha = CaptchaField()
    class Meta:
        model = Account
        fields = ("email", "phone","username", "password1", "password2", "captcha")


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    class Meta:
        model = Account
        #fields = ("email", "password")
        fields = ("phone", "password")
        
    
    def clean(self):
        #email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        password = self.cleaned_data['password']
        
        if not authenticate(phone=phone, password=password):
            raise forms.ValidationError("phone or password wrong!!!")
        
        
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("phone","email", "username")
    
    def clean_phone(self):
        if self.is_valid():  
            phone = self.cleaned_data['phone']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(phone=phone)
            except Account.DoesNotExist: 
                return email
            raise forms.ValidationError('Email %s is already in use.', email)

    def clean_email(self):
        if self.is_valid():  
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist: 
                return email
            raise forms.ValidationError('Email %s is already in use.', email)
    
    def clean_username(self):
        if self.is_valid():  
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username %s is already in use.', username)
    