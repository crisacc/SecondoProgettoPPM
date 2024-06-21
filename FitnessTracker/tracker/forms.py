from django import forms
from .models import Workout, Goal, Progress
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

class WorkoutForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Assicura che il campo sia reso come un campo di tipo date
    workout_type = forms.ChoiceField(choices=Workout.WORKOUT_TYPES)  # Menu a tendina per il tipo di workout

    class Meta:
        model = Workout
        fields = ['date', 'workout_type', 'duration', 'calories_burned']

class GoalForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Goal
        fields = ['description', 'start_date', 'expiration_date', 'time_period', 'workout_type', 'sessions_target']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        expiration_date = cleaned_data.get('expiration_date')
        time_period = cleaned_data.get('time_period')

        if start_date and start_date < timezone.now().date():
            self.add_error('start_date', "The start date cannot be in the past.")

        if time_period == 'single' and expiration_date:
            if expiration_date < start_date:
                self.add_error('expiration_date', "The expiration date cannot be before the start date.")
        return cleaned_data

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['date', 'progress_detail']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
