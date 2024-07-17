from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _

from main.models import MedicalInstitution

User = get_user_model()

class UserCreationForm(UserCreationForm):

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"})
    )


    user_code = forms.CharField(max_length=30, required=True)
    is_role = forms.IntegerField(required=True)



    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "user_code", "is_role")

















