from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import UserManager as DefaultUserManager
from datetime import datetime

# Override and create custom superuser with default values for non-nullable fields
class RunnerUserManager(DefaultUserManager):
    """
    Custom manager for RunnerUser to provide custom superuser creation.
    """

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Creates and returns a superuser with the given username, email, and password.
        
        Parameters
        ----------
        username : str
            The desired username for the superuser.
        email : str, optional
            The email address for the superuser.
        password : str, optional
            The password for the superuser.
        extra_fields : dict, optional
            Additional fields to set for the superuser.
            
        Returns
        -------
        RunnerUser
            The created superuser.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('dob', '2000-01-01')  # Set default DOB
        extra_fields.setdefault('fitness_level', 'beginner')  # Set default fitness_level

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class RunnerUser(AbstractUser):
    """
    Custom user model for runners which extends the default Django user model.
    """

    # User fintess choices 
    FITNESS_LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    # Ensures first name and last name are required
    first_name = models.CharField(max_length=30, blank=False, error_messages={
        'blank': "This field is required.",
    })
    last_name = models.CharField(max_length=30, blank=False, error_messages={
        'blank': "This field is required.",
    })

    dob = models.DateField(verbose_name="Date of birth", help_text="You must be at least 18 years old.") # User's date of birth - to calculate their age
    fitness_level = models.CharField(max_length=50, choices=FITNESS_LEVEL_CHOICES, help_text="If you are unsure of your fitnes level, choose beginner.") # User's fitness level
    date_of_marathon = models.DateField(auto_now=False, auto_now_add=False, help_text="Date of marathon: 90-365 days from today, recommend 180+ days.")

    # Override the groups and user_permissions fields to set a unique related_name
    groups = models.ManyToManyField(Group, related_name="runneruser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="runneruser_set", blank=True)

    # Creating custom superuser
    objects = RunnerUserManager()

    def __str__(self):
        if self.is_superuser:
            return f"Superuser: {self.username}. They have all permissions."
        return f"Username: {self.username}. They have user level permissions."

class StravaUserProfile(models.Model):
    user = models.OneToOneField(RunnerUser, on_delete=models.CASCADE)
    client_id = models.BigIntegerField(null=True, blank=True)
    strava_access_token = models.CharField(max_length=200)
    strava_refresh_token = models.CharField(max_length=200)
    expires_at = models.DateTimeField()

class MarathonPlan(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(RunnerUser, on_delete=models.CASCADE) # The plan for a user
    start_date = models.DateField() # Start date of plan
    end_date = models.DateField() # End date of plan - day of the martahon

    def __str__(self):
        return f"Plan {self.id} for {self.user.username}. (Plan Begins on {self.start_date} and ends on {self.end_date})"

class ScheduledRun(models.Model):

    id = models.AutoField(primary_key=True)
    dict_id = models.PositiveIntegerField(null=True, blank=True)
    run = models.CharField(max_length=100, default="Training Run")  # Name of run
    run_feel = models.CharField(max_length=200, default="Training session")
    marathon_plan = models.ForeignKey(MarathonPlan, on_delete=models.CASCADE) # The plan
    date = models.DateField() # The date of the run
    distance = models.PositiveIntegerField(help_text="Distance in km") # Distance of run
    est_duration = models.PositiveIntegerField(help_text="Duration in minutes") # Time of run
    est_avg_pace = models.DurationField(null=True, blank=True) # Pace of run
    on = models.PositiveIntegerField(help_text="Work time in minutes", default=0)
    off = models.PositiveIntegerField(help_text="Rest time in minutes", default=0)
    sets = models.PositiveIntegerField(help_text="Sets", default=0)

    def __str__(self):
        formatted_date = self.date.strftime('%d-%m-%Y')
        return f"{self.run} on {formatted_date}"

class CompletedRun(models.Model):
    scheduled_run = models.OneToOneField(ScheduledRun, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(help_text="Date when run was completed")
    distance = models.PositiveIntegerField(help_text="Distance of completed run in km")
    duration = models.PositiveIntegerField(help_text="Duration of completed run in minutes")
    avg_pace = models.DurationField(verbose_name="Average Pace", help_text="Please format like mm:ss")  
    
    def __str__(self):
        return f"Completed run on {self.date} with pace {self.avg_pace}"
