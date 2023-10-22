from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from datetime import date, timedelta

from .models import RunnerUser
from .utils import p_a_constants as c

class MergedSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = RunnerUser
        fields = ["first_name", "last_name", "username", "email", "password1", "password2", "dob", "fitness_level", "date_of_marathon"]

        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "fitness_level": forms.Select(choices=RunnerUser.FITNESS_LEVEL_CHOICES),
            "date_of_marathon": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_date_of_marathon(self):
        date_of_marathon = self.cleaned_data.get("date_of_marathon")
        today = date.today()

        if date_of_marathon and date_of_marathon <= today:
            raise ValidationError("The date of the marathon must be in the future.")

        if date_of_marathon and date_of_marathon < today + timedelta(days=c.MIN_DAYS):
            raise ValidationError(f"The date of the marathon must be at least {c.MIN_DAYS} days from today.")

        if date_of_marathon and date_of_marathon > today + timedelta(days=c.MAX_DAYS):
            raise ValidationError(f"The date of the marathon must be less than {c.MAX_DAYS} days from today.")

        return date_of_marathon

"""Leave if you want two sign-up pages"""
## For initial sign-up
#class SignUpForm(UserCreationForm):
#    email = forms.EmailField()
#
#    class Meta:
#        model = RunnerUser
#        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]
#
## For additional user details
#class RunnerUserDetailForm(forms.ModelForm):
#    class Meta:
#        model = RunnerUser
#        fields = ["dob", "weight", "height", "fitness_level", "date_of_marathon"]
#
#        widgets = {
#            "dob": forms.DateInput(attrs={"type": "date"}),
#            "weight": forms.NumberInput(attrs={"placeholder": "Weight in kg"}),
#            "height": forms.NumberInput(attrs={"placeholder": "Height in cm"}),
#            "fitness_level": forms.Select(choices=RunnerUser.FITNESS_LEVEL_CHOICES),
#            "date_of_marathon": forms.DateInput(attrs={"type": "date"})
#        }
#
#    # Check that the date is valid and is between the min and max times
#    def clean_date_of_marathon(self):
#        date_of_marathon = self.cleaned_data.get("date_of_marathon")
#        today = date.today()
#
#        if date_of_marathon <= today:
#            raise ValidationError("The date of the marathon must be in the future.")
#
#        if date_of_marathon < today + timedelta(days=plan_algo.MIN_DAYS):
#            raise ValidationError(f"The date of the marathon must be at least {plan_algo.MIN_DAYS} days from today.")
#
#        if date_of_marathon > today + timedelta(days=plan_algo.MAX_DAYS):
#            raise ValidationError(f"The date of the marathon must be less than {plan_algo.MAX_DAYS} days from today.")
#
#        return date_of_marathon
