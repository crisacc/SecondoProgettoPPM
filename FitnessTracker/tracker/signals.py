from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Workout, Goal
from django.utils import timezone

@receiver(post_save, sender=Workout)
def update_goals(sender, instance, **kwargs):
    goals = Goal.objects.filter(profile=instance.profile, workout_type=instance.workout_type, achieved=False)
    now = timezone.now().date()
    for goal in goals:
        if goal.start_date <= now:
            goal.sessions_completed += 1
            if goal.sessions_completed >= goal.sessions_target:
                goal.achieved = True
            goal.save()
