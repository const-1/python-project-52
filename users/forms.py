# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        label=_('First name')
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        label=_('Last name')
    )

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2']
        labels = {
            'username': _('Username'), # проверить
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'username': _('Username'),
        }

