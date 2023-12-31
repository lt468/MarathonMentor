"""
This module defines forms used in the training_plan app.
"""
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from datetime import date, timedelta
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.helper import FormHelper

from .models import RunnerUser
from .utils import p_a_constants as c


class MergedSignUpForm(UserCreationForm):
    """
    Custom user registration form that extends the Django UserCreationForm.

    This form includes additional fields such as first name, last name, date of birth, fitness level,
    and the date of the marathon.

    Attributes:
    - helper (FormHelper): Crispy Forms helper for customizing the form's appearance.

    Example:
    
    form = MergedSignUpForm()
    

    Note:
    This form is designed to be used within the Django framework and is tied to the RunnerUser model.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with customized layout and helper settings.

        Example:
        
        form = MergedSignUpForm()
        
        """
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
                Column(Submit('submit', 'Register',
                       css_class="btn btn-dark"), css_class="form-group"),
                css_class="for-rowm m-1",
            )
        )

    email = forms.EmailField()

    class Meta:
        """
        Metadata class defining the model and fields for the form.

        Attributes:
        - model (Model): The model associated with the form.
        - fields (list): List of fields to include in the form.
        - widgets (dict): Dictionary defining widgets for specific fields.

        Example:
        
        class Meta:
            model = RunnerUser
            fields = ["first_name", "last_name", "username", "email", "password1",
                      "password2", "dob", "fitness_level", "date_of_marathon"]
            widgets = {
                "dob": forms.DateInput(attrs={"type": "date"}),
                "fitness_level": forms.Select(choices=RunnerUser.FITNESS_LEVEL_CHOICES),
                "date_of_marathon": forms.DateInput(attrs={"type": "date"}),
            }
        
        """

        model = RunnerUser
        fields = ["first_name", "last_name", "username", "email", "password1",
                  "password2", "dob", "fitness_level", "date_of_marathon"]

        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "fitness_level": forms.Select(choices=RunnerUser.FITNESS_LEVEL_CHOICES),
            "date_of_marathon": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_date_of_marathon(self):
        """
        Clean and validate the 'date_of_marathon' field.

        Returns:
        - date_of_marathon (date): Cleaned date value.

        Raises:
        - ValidationError: If the date is not in the future, not within the specified range,
          or fails other validation criteria.
        """

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
        """
        Clean and validate the 'dob' (date of birth) field.

        Returns:
        - birth_date (date): Cleaned date value.

        Raises:
        - ValidationError: If the date is missing, the user is underage, the date is in the future,
          or fails other validation criteria.
        """

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
