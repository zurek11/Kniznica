from django import forms
from django.contrib.auth.forms import UserCreationForm
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

    def clean_username(self):
        valid_name = self.cleaned_data['username']
        if not User.objects.filter(username=valid_name).exists():
            raise forms.ValidationError(u'Username "%s" is not recognized.' % valid_name)
        return valid_name

    # def clean_password(self):
    #     valid_password = self.cleaned_data['password']
    #     if not User.objects.filter(password=valid_password).exists():
    #         raise forms.ValidationError(u'Password is not recognized.')
    #     return valid_password
