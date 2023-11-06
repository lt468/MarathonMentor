from django import forms
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from datetime import date, timedelta
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from crispy_forms.helper import FormHelper

from .models import RunnerUser, CompletedRun, ScheduledRun
from .utils import p_a_constants as c


class MergedSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(MergedSignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "registration_form"
        self.helper.form_class = "registration_form"
        self.helper.form_method = "post"
        self.helper.form_action = "register"
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="form-group col-md-6"),
                Column("last_name", css_class="form-group col-md-6"),
                css_class="form-row m-1"
            ),
            Row(
                Column("username", css_class="form-group col-md-6"),
                Column("email", css_class="form-group col-md-6"),
                css_class="form-row m-1"
            ),
            Row(
                Column("password1", css_class="form-group col-md-6"),
                Column("password2", css_class="form-group col-md-6"),
                css_class="form-row m-1"
            ),
            Row(
                Column("dob", css_class="form-group col-md-4"),
                Column("fitness_level", css_class="form-group col-md-4"),
                Column("date_of_marathon", css_class="form-group col-md-4"),
                css_class="form-row m-1"
            ),
            Row(
                Column(Submit('submit', 'Register', css_class="btn btn-dark"), css_class="form-group"),
                css_class="for-rowm m-1",
            )
        )

    email = forms.EmailField()

    class Meta:
        model = RunnerUser
        fields = ["first_name", "last_name", "username", "email", "password1",
                  "password2", "dob", "fitness_level", "date_of_marathon"]

        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "fitness_level": forms.Select(choices=RunnerUser.FITNESS_LEVEL_CHOICES),
            "date_of_marathon": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_date_of_marathon(self):
        date_of_marathon = self.cleaned_data.get("date_of_marathon")
        today = date.today()

        if date_of_marathon and date_of_marathon <= today:
            raise ValidationError(
                "The date of the marathon must be in the future.")

        if date_of_marathon and date_of_marathon < today + timedelta(days=c.MIN_DAYS):
            raise ValidationError(
                f"The date of the marathon must be at least {c.MIN_DAYS} days from today.")

        if date_of_marathon and date_of_marathon > today + timedelta(days=c.MAX_DAYS):
            raise ValidationError(
                f"The date of the marathon must be less than {c.MAX_DAYS} days from today.")

        return date_of_marathon

    def clean_dob(self):
        birth_date = self.cleaned_data.get("dob")
        today = date.today()

        if birth_date is None:
            raise ValidationError("Date of birth required")

        DATE_LIMIT = today - timedelta(days=365*120)
        age = today.year - birth_date.year - \
            ((today.month, today.day) < (birth_date.month, birth_date.day))

        if age < 18:
            raise ValidationError(
                "You must be at least 18 years old to register.")

        if birth_date >= today:
            raise ValidationError("Your date of birth cannot be in the future")

        if birth_date < DATE_LIMIT:
            raise ValidationError(f"Please enter a valid date of birth")

        return birth_date

class CompletedRunForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(CompletedRunForm, self).__init__(*args, **kwargs)
        self.user = user

        if user is not None:
            today = date.today()
            scheduled_run = ScheduledRun.objects.get(
                marathon_plan__user=user, date=today)
            if scheduled_run:
                self.fields["scheduled_run"].initial = scheduled_run
                self.fields["scheduled_run"].widget.attrs['readonly'] = True  # Make the field view-only
            else:
                self.fields["scheduled_run"].widget = forms.HiddenInput()
                self.fields["scheduled_run"].required = False

        self.helper = FormHelper()
        self.helper.form_id = "completed_run_form"
        self.helper.form_class = "completed_run_form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column('scheduled_run', css_class="form-group col-md-6", readonly=True),
                Column('date', css_class="form-group col-md-6"),
                css_class="form-row m-1"
            ),
            Row(
                Column('distance', css_class="form-group col-md-6"),
                Column('duration', css_class="form-group col-md-6"),
                css_class="form-row m-1"
            ),
            Field('avg_pace', css_class="form-group"),
            Submit('submit', 'Save', css_class="btn btn-dark"),
        )

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > timezone.now().date():
            raise forms.ValidationError("Date cannot be in the future.")
        return date

    def clean_avg_pace(self):
        avg_pace = self.cleaned_data['avg_pace']
        # Validate avg_pace format (mm:ss)
        if not re.match(r'^[0-5]\d:[0-5]\d$', str(avg_pace)):
            raise forms.ValidationError("Invalid pace format. Please use mm:ss.")
        return avg_pace

    class Meta:
        model = CompletedRun
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        fields = ['scheduled_run', 'date', 'distance', 'duration', 'avg_pace']

"""Leave if you want two sign-up pages"""
# For initial sign-up
# class SignUpForm(UserCreationForm):
#    email = forms.EmailField()
#
#    class Meta:
#        model = RunnerUser
#        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]
#
# For additional user details
# class RunnerUserDetailForm(forms.ModelForm):
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
