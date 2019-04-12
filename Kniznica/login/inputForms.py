from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LogUser(forms.Form):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Prihlasovacie meno',
        'class': 'form-control'
    }))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'placeholder': 'Heslo',
        'class': 'form-control'
    }))
    pic1 = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def clean(self):
        input_username = self.cleaned_data.get('username')
        input_password = self.cleaned_data.get('password')
        input_picture = self.cleaned_data.get('pic1')
        user = authenticate(username=input_username, password=input_password)

        if not input_picture:
            if not user or not user.is_active:
                raise forms.ValidationError(u'Nesprávne prihlasovacie údaje.')
            else:
                return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
