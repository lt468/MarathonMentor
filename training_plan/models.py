from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import UserManager as DefaultUserManager

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

    dob = models.DateField(verbose_name="Date of birth") # User's date of birth - to calculate their age
    weight = models.PositiveIntegerField(help_text="Weight in kilograms", null=True, blank=True) # User's weight
    height = models.PositiveIntegerField(help_text="Height in centimeters", null=True, blank=True) # User's height
    fitness_level = models.CharField(max_length=50, choices=FITNESS_LEVEL_CHOICES) # User's fitness level
    date_of_marathon = models.DateField(auto_now=False, auto_now_add=False, help_text="Date of marathon", null=True, blank=True)

    # Override the groups and user_permissions fields to set a unique related_name
    groups = models.ManyToManyField(Group, related_name="runneruser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="runneruser_set", blank=True)

    # Creating custom superuser
    objects = RunnerUserManager()

    def __str__(self):
        if self.is_superuser:
            return f"Superuser: {self.username}, doing marathon {self.current_plan}. They have all permissions."
        return f"Username: {self.username}, doing marathon plan {self.current_plan}. They have user level permissions."

class MarathonPlan(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(RunnerUser, on_delete=models.CASCADE) # The plan for a user
    start_date = models.DateField() # Start date of plan
    end_date = models.DateField() # End date of plan - day of the martahon

    def __str__(self):
        return f"Plan {self.id} for {self.user.username}. Begins: {self.start_date}; Ends: {self.end_date}"

class ScheduledRun(models.Model):

    id = models.AutoField(primary_key=True)
    run = models.CharField(max_length=100, default="Training Run")  # Name of run
    run_feel = models.CharField(default="Training session")
    marathon_plan = models.ForeignKey(MarathonPlan, on_delete=models.CASCADE) # The plan
    date = models.DateField() # The date of the run
    distance = models.PositiveIntegerField(help_text="Distance in km") # Distance of run
    est_duration = models.PositiveIntegerField(help_text="Duration in minutes") # Time of run
    est_avg_pace = models.DurationField() # Distance of run
    on = models.PositiveIntegerField(help_text="Work time in minutes", default=0)
    off = models.PositiveIntegerField(help_text="Rest time in minutes", default=0)
    sets = models.PositiveIntegerField(help_text="Sets", default=0)

    def __str__(self):
        return f"Training run: {self.run} for {self.marathon_plan} plan on {self.date}"

class CompletedRun(models.Model):
    scheduled_run = models.OneToOneField(ScheduledRun, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    distance = models.PositiveIntegerField(help_text="Distance of completed run in km")
    duration = models.PositiveIntegerField(help_text="Duration of completed run in minutes")
    avg_pace = models.DurationField()  
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Completed run on {self.date} with pace {self.pace}"
