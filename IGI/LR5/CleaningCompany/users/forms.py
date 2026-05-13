import re
from django import forms
from django.core.exceptions import ValidationError
from .models import User


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'middle_name',  'email', 'phone_number', 'date_of_birth', 'password', 'client_type', 'company_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['middle_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['phone_number'].widget.attrs.update({
            'pattern': r'\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}',
            'title': 'Format: +375 (29) 123-45-67',
            'required': True,
        })
        self.fields['email'].widget.attrs['required'] = True

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        pattern = r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, phone_number):
            raise ValidationError('Format: +375 (29) XXX-XX-XX')
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        client_type = cleaned_data.get('client_type')
        company_name = cleaned_data.get('company_name')

        if client_type == 'legal' and not company_name:
            self.add_error('company_name', ValidationError('Please enter a company name'))

        if client_type == 'individual' and company_name:
            self.add_error('company_name', ValidationError("Individual can't have a company name"))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.user_type = 'client'
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'email', 'phone_number', 'date_of_birth']