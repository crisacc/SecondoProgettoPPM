from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Workout, Goal, Progress, Profile
from .forms import WorkoutForm, GoalForm, ProgressForm, UserRegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django import forms
from django.contrib.auth.views import LogoutView


class CustomLogoutView(LogoutView):
    next_page = 'index'


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'


@login_required
def remove_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, profile=request.user.profile, time_period='single')
    goal.delete()
    messages.success(request, 'Goal removed successfully.')
    return redirect('goal_list')

@login_required
def home(request):
    now = timezone.now().date()
    goals = Goal.objects.filter(profile=request.user.profile, achieved=False, start_date__lte=now)
    for goal in goals:
        if goal.time_period == 'daily' and goal.start_date == now:
            messages.warning(request, f"Your daily goal for {goal.workout_type} is due today!")
        elif goal.time_period == 'weekly' and goal.start_date <= now + timedelta(days=7):
            messages.warning(request, f"Your weekly goal for {goal.workout_type} is due within the next week!")
        elif goal.time_period == 'monthly' and goal.start_date <= now + timedelta(days=30):
            messages.warning(request, f"Your monthly goal for {goal.workout_type} is due within the next month!")
    return render(request, 'home.html')


class WorkoutListView(View):
    @method_decorator(login_required)
    def get(self, request):
        workouts = Workout.objects.filter(profile=request.user.profile)
        return render(request, 'workout_list.html', {'workouts': workouts})

class WorkoutForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Assicura che il campo sia reso come un campo di tipo date

    class Meta:
        model = Workout
        fields = ['date', 'workout_type', 'duration', 'calories_burned']


class WorkoutCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = WorkoutForm()
        return render(request, 'workout_form.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.profile = request.user.profile
            workout.save()

            # Aggiornare il progresso degli obiettivi
            goals = Goal.objects.filter(profile=workout.profile, workout_type=workout.workout_type, achieved=False)
            now = timezone.now().date()
            for goal in goals:
                if goal.start_date <= now:
                    goal.sessions_completed += 1
                    if goal.sessions_completed >= goal.sessions_target:
                        goal.achieved = True
                        messages.success(request, f"Congratulations! You have achieved your goal: {goal.description}")
                    goal.save()
            return redirect('workout_list')
        return render(request, 'workout_form.html', {'form': form})

class GoalCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = GoalForm()
        return render(request, 'goal_form.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.profile = request.user.profile
            goal.save()
            return redirect('goal_list')
        return render(request, 'goal_form.html', {'form': form})

class GoalListView(View):
    @method_decorator(login_required)
    def get(self, request):
        goals = Goal.objects.filter(profile=request.user.profile)
        return render(request, 'goal_list.html', {'goals': goals})


class ProgressCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = ProgressForm()
        return render(request, 'progress_form.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.goal = Goal.objects.get(pk=request.POST.get('goal_id'))
            progress.save()
            return redirect('progress_list')  # Assume that there's a progress list view
        return render(request, 'progress_form.html', {'form': form})

class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        return render(request, 'register.html', {'form': form})
