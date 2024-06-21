# tracker/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # URL per la pagina iniziale
    path('home/', views.home, name='home'),  # URL per la home page
    path('workout/new/', views.WorkoutCreateView.as_view(), name='workout_new'),  # URL per la creazione del workout
    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),  # URL per la lista dei workout
    path('goal/new/', views.GoalCreateView.as_view(), name='goal_new'),
    path('goals/', views.GoalListView.as_view(), name='goal_list'),
    path('goal/remove/<int:goal_id>/', views.remove_goal, name='remove_goal'),
    path('progress/new/', views.ProgressCreateView.as_view(), name='progress_new'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Utilizza la vista personalizzata per il login
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]

