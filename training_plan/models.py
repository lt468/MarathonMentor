"""
This module defines the data models for the training_plan app.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import UserManager as DefaultUserManager

# Override and create custom superuser with default values for non-nullable fields


class RunnerUserManager(DefaultUserManager):
    """
    Custom manager for the RunnerUser model.

    This manager provides a method to create a superuser with default values for specific fields.

    Example:
    
    manager = RunnerUserManager()
    manager.create_superuser(username='admin', password='admin')
    
    """

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('dob', '2000-01-01')  # Set default DOB
        # Set default fitness_level
        extra_fields.setdefault('fitness_level', 'beginner')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class RunnerUser(AbstractUser):
    """
    Custom user model for runners.

    This model extends Django's AbstractUser and includes additional fields such as date of birth,
    fitness level, and date of the marathon.

    Attributes:
    - FITNESS_LEVEL_CHOICES (list): Choices for the 'fitness_level' field.
    - first_name (CharField): First name of the user.
    - last_name (CharField): Last name of the user.
    - dob (DateField): Date of birth of the user.
    - fitness_level (CharField): Fitness level of the user.
    - date_of_marathon (DateField): Date of the marathon for the user.

    Example:
    
    user = RunnerUser.objects.create(username='JohnDoe', email='john@example.com', password='secret')
    

    Note:
    This model is designed to be used within the Django framework and is used as the authentication
    model for the training_plan app.
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

    # User's date of birth - to calculate their age
    dob = models.DateField(verbose_name="Date of birth",
                           help_text="You must be at least 18 years old.")
    fitness_level = models.CharField(max_length=50, choices=FITNESS_LEVEL_CHOICES,
                                     help_text="If you are unsure of your fitnes level, choose beginner.")  # User's fitness level
    date_of_marathon = models.DateField(auto_now=False, auto_now_add=False,
                                        help_text="Date of marathon: 90-365 days from today, recommend 180+ days.")

    # Override the groups and user_permissions fields to set a unique related_name
    groups = models.ManyToManyField(
        Group, related_name="runneruser_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="runneruser_set", blank=True)

    # Creating custom superuser
    objects = RunnerUserManager()

    def __str__(self):
        if self.is_superuser:
            return f"Superuser: {self.username}. They have all permissions."
        return f"Username: {self.username}. They have user level permissions."


class StravaUserProfile(models.Model):
    """
    Model representing a Strava user profile associated with a RunnerUser.

    Attributes:
    - user (OneToOneField): Reference to the associated RunnerUser.
    - client_id (BigIntegerField): Strava client ID.
    - strava_access_token (CharField): Strava access token.
    - strava_refresh_token (CharField): Strava refresh token.
    - expires_at (DateTimeField): Expiry date and time.

    Example:
    
    profile = StravaUserProfile.objects.create(user=my_runner_user, client_id=123, strava_access_token='xyz', strava_refresh_token='abc', expires_at=datetime.now())
    

    """

    user = models.OneToOneField(RunnerUser, on_delete=models.CASCADE)
    client_id = models.BigIntegerField(null=True, blank=True)
    strava_access_token = models.CharField(max_length=200)
    strava_refresh_token = models.CharField(max_length=200)
    expires_at = models.DateTimeField()


class MarathonPlan(models.Model):
    """
    Model representing a training plan for a RunnerUser.

    Attributes:
    - id (AutoField): Auto-incremented primary key.
    - user (ForeignKey): Reference to the associated RunnerUser.
    - start_date (DateField): Start date of the training plan.
    - end_date (DateField): End date of the training plan.

    Example:
    
    plan = MarathonPlan.objects.create(user=my_runner_user, start_date='2023-01-01', end_date='2023-12-31')
    

    Note:
    As of v0.1.0, a user can have only one marathon plan. If you wish to create a new plan for a user, ensure the old one is deleted first
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        RunnerUser, on_delete=models.CASCADE)  # The plan for a user
    start_date = models.DateField()  # Start date of plan
    end_date = models.DateField()  # End date of plan - day of the martahon

    def __str__(self):
        return f"Plan {self.id} for {self.user.username}. (Plan Begins on {self.start_date} and ends on {self.end_date})"


class ScheduledRun(models.Model):
    """
    Model representing a scheduled run within a training plan.

    Attributes:
    - id (AutoField): Auto-incremented primary key.
    - dict_id (PositiveIntegerField): Nullable field for a dictionary ID.
    - run (CharField): Name of the run.
    - run_feel (CharField): Description of the run.
    - marathon_plan (ForeignKey): Reference to the associated MarathonPlan.
    - date (DateField): Date of the run.
    - distance (PositiveIntegerField): Distance of the run.
    - est_duration (PositiveIntegerField): Estimated duration of the run in minutes.
    - est_avg_pace (DurationField, optional): Estimated average pace of the run.
    - on (PositiveIntegerField, default=0): Work time in minutes.
    - off (PositiveIntegerField, default=0): Rest time in minutes.
    - sets (PositiveIntegerField, default=0): Number of sets.

    Example:
    python
    run = ScheduledRun.objects.create(
        run='Training Run',
        marathon_plan=my_marathon_plan,
        date='2023-05-01',
        distance=10,
        est_duration=60,
        est_avg_pace='06:00',
        on=30,
        off=15,
        sets=3
    )
    

    This model represents a scheduled run within a training plan. It includes details such as the name of the run,
    its description, associated marathon plan, date, distance, estimated duration, estimated average pace (optional),
    work time, rest time, and the number of sets.

    Note:
    - The est_avg_pace field is optional and can be left blank.
    - The date field represents the date of the scheduled run.
    - The est_avg_pace field is the estimated average pace of the run and is expressed as a duration.
    """

    id = models.AutoField(primary_key=True)
    dict_id = models.PositiveIntegerField(null=True, blank=True)
    run = models.CharField(
        max_length=100, default="Training Run")  # Name of run
    run_feel = models.CharField(max_length=200, default="Training session")
    marathon_plan = models.ForeignKey(
        MarathonPlan, on_delete=models.CASCADE)  # The plan
    date = models.DateField()  # The date of the run
    distance = models.PositiveIntegerField(
        help_text="Distance in km")  # Distance of run
    est_duration = models.PositiveIntegerField(
        help_text="Duration in minutes")  # Time of run
    est_avg_pace = models.DurationField(null=True, blank=True)  # Pace of run
    on = models.PositiveIntegerField(
        help_text="Work time in minutes", default=0)
    off = models.PositiveIntegerField(
        help_text="Rest time in minutes", default=0)
    sets = models.PositiveIntegerField(help_text="Sets", default=0)

    def __str__(self):
        formatted_date = self.date.strftime('%d-%m-%Y')
        return f"{self.run} on {formatted_date}"


class CompletedRun(models.Model):
    """
    Model representing a completed run.

    Attributes:
    - scheduled_run (OneToOneField): Reference to the associated ScheduledRun.
    - date (DateField): Date when the run was completed.
    - distance (PositiveIntegerField): Distance of the completed run.
    - duration (PositiveIntegerField): Duration of the completed run.
    - avg_pace (DurationField): Average pace of the completed run.

    Example:
    
    completed_run = CompletedRun.objects.create(scheduled_run=my_scheduled_run, date='2023-05-01', distance=10, duration=60, avg_pace='06:00')
    
    """
    scheduled_run = models.OneToOneField(
        ScheduledRun, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(help_text="Date when run was completed")
    distance = models.PositiveIntegerField(
        help_text="Distance of completed run in km")
    duration = models.PositiveIntegerField(
        help_text="Duration of completed run in minutes")
    avg_pace = models.DurationField(
        verbose_name="Average Pace", help_text="Please format like mm:ss")

    def __str__(self):
        return f"Completed run on {self.date} with pace {self.avg_pace}"
