from django import forms
from registration.forms import RegistrationForm

import models
from registration.models import RegistrationProfile

attrs_dict = { 'class': 'required' }

class UserRegistrationForm(RegistrationForm):
    twilio_api_key = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    twilio_api_secret = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))

    # def save(self, profile_callback=None):
    #     new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
    #     password=self.cleaned_data['password1'],
    #     email=self.cleaned_data['email'])
    #     new_profile = Teacher(user=new_user, twilio_api_key=self.cleaned_data['twilio_api_key'], twilio_api_secret=self.cleaned_data['twilio_api_secret'])
    #     return new_user