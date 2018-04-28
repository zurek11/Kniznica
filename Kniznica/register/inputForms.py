from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class NewUser(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Prihlasovacie meno',
        'class': 'form-control'
    }))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control'
    }))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Heslo',
        'class': 'form-control'
    }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Heslo znovu',
        'class': 'form-control'
    }))
    pic1 = forms.CharField(required=True)
    pic2 = forms.CharField(required=True)
    pic3 = forms.CharField(required=True)
    pic4 = forms.CharField(required=True)
    pic5 = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(NewUser, self).__init__(*args, **kwargs)
        self.fields['pic5'].error_messages = {'required': 'You must capture yourself 5 times to register.'}

    def clean_username(self):
        valid_name = self.cleaned_data['username']
        if User.objects.filter(username=valid_name).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % valid_name)
        return valid_name

    def clean_email(self):
        valid_email = self.cleaned_data['email']
        if User.objects.filter(email=valid_email).exists():
            raise forms.ValidationError(u'Email "%s" is already in use.' % valid_email)
        return valid_email

