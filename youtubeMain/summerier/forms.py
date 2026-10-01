from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    conform_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields = ['username','email','password']


    def clean(self):
        cleaned_data=super().clean()
        passwrd=cleaned_data.get('password')
        conform_password=cleaned_data.get('conform_password')

        if passwrd != conform_password:
            raise forms.ValidationError("the password are mismatch")
        
        return cleaned_data
