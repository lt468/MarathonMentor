from django.db import models

class Run(models.Model):
    ZONE_CHOICES = [
        (1, 'Z1 - Recovery'),
        (2, 'Z2 - Base'),
        (3, 'Z3 - Tempo'),
        (4, 'Z4 - High Tempo'),
        (5, 'Z5 - Interval/Anaerobic'),
    ]

    FEEL_CHOICES = [
        ('recovery', 'Recovery'),
        ('base', 'Base'),
        ('hard', 'Hard'),
        ('max-effort', 'Max Effort'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="Unnamed Run")  # A name for the specific run template, e.g., "recovery1"
    zone = models.PositiveSmallIntegerField(choices=ZONE_CHOICES)
    feel = models.CharField(max_length=20, choices=FEEL_CHOICES)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    distance = models.PositiveIntegerField(help_text="Distance in km")

    def __str__(self):
        return f"Run name: {self.name}; Zone: {self.zone}"


