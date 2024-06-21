from django_cron import CronJobBase, Schedule
from django.utils import timezone
from .models import Goal
from datetime import timedelta
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.core.mail import send_mail

class CheckGoalsCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # Esegui ogni ora

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'tracker.check_goals'  # Codice univoco per il cron job

    def do(self):
        now = timezone.now()
        today = now.date()
        goals = Goal.objects.filter(achieved=False)
        for goal in goals:
            user = goal.profile.user
            if goal.time_period == 'single' and goal.expiration_date < today and not goal.achieved:
                # Notifica l'utente che l'obiettivo singolo è scaduto e verrà rimosso
                self.notify_user(user, goal, f"Your single goal '{goal.description}' has expired and will be removed.")
                goal.delete()
            elif goal.time_period == 'daily' and goal.start_date <= today:
                if now.hour == 22:
                    self.notify_user(user, goal, "Your daily goal is due in 2 hours!")
                if goal.start_date <= today:
                    # Reset giornaliero
                    goal.achieved = False
                    goal.start_date = today + timedelta(days=1)
                    goal.save()
            elif goal.time_period == 'weekly' and goal.start_date <= today:
                if today == goal.start_date + timedelta(days=6):
                    self.notify_user(user, goal, "Your weekly goal is due tomorrow!")
                if goal.start_date <= today - timedelta(days=7):
                    # Reset settimanale
                    goal.achieved = False
                    goal.start_date = today + timedelta(days=7)
                    goal.save()
            elif goal.time_period == 'monthly' and goal.start_date <= today:
                if today == goal.start_date + timedelta(days=28):
                    self.notify_user(user, goal, "Your monthly goal is due tomorrow!")
                if goal.start_date <= today - timedelta(days=30):
                    # Reset mensile
                    goal.achieved = False
                    goal.start_date = today + timedelta(days=30)
                    goal.save()


    def notify_user(self, user, goal, message):
        # Invia un'email all'utente
        send_mail(
            'Goal Reminder',
            f'Hi {user.username},\n\n{message}\n\nGoal: {goal.description}\n',
            'admin@fitnesstracker.com',
            [user.email],
            fail_silently=False,
        )
        # Notifica nell'app
        self.add_message_to_user_sessions(user, message)

    def add_message_to_user_sessions(self, user, message):
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions:
            data = session.get_decoded()
            if data.get('_auth_user_id') == str(user.id):
                messages.add_message(messages.WARNING, message)
                session.save()