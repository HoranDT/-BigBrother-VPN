from django import forms
from django.contrib.auth.forms import UserCreationForm
from bigbrother.models import CustomUser
from django.core.exceptions import ValidationError
import re

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[A-Za-z0-9]+$', username):
            raise ValidationError('Username can only contain alphanumeric characters (A-Z, a-z, 0-9).')
        return username

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
