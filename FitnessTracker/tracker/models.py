from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Workout(models.Model):
    WORKOUT_TYPES = [
        ('Corsa', 'Corsa'),
        ('Camminata', 'Camminata'),
        ('Camminata_veloce', 'Camminata veloce'),
        ('Camminata_nel_bosco', 'Camminata nel bosco'),
        ('Bicicletta', 'Bicicletta'),
        ('Nuoto', 'Nuoto'),
        ('Palestra', 'Palestra'),
        ('Trekking', 'Trekking'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='workouts')
    date = models.DateField()
    workout_type = models.CharField(max_length=50, choices=WORKOUT_TYPES)
    duration = models.PositiveIntegerField()  # in minutes
    calories_burned = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.workout_type} on {self.date} by {self.profile.user.username}"

class Goal(models.Model):
    TIME_PERIODS = [
        ('daily', 'Giornaliero'),
        ('weekly', 'Settimanale'),
        ('monthly', 'Mensile'),
        ('single', 'Singolo')
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='goals')
    description = models.CharField(max_length=255)
    start_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)  # Campo per l'obiettivo singolo
    achieved = models.BooleanField(default=False)
    time_period = models.CharField(max_length=10, choices=TIME_PERIODS)
    workout_type = models.CharField(max_length=50, choices=Workout.WORKOUT_TYPES)
    sessions_target = models.PositiveIntegerField(default=0)  # Numero di sessioni desiderate
    sessions_completed = models.PositiveIntegerField(default=0)  # Numero di sessioni completate

    def __str__(self):
        return f"Goal: {self.description} for {self.profile.user.username}"

class Progress(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='progresses')
    date = models.DateField()
    progress_detail = models.TextField()

    def __str__(self):
        return f"Progress on {self.date} for goal {self.goal.description}"
