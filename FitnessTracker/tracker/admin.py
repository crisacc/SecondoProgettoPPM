from django.contrib import admin
from .models import Profile, Workout, Goal, Progress

admin.site.register(Profile)
admin.site.register(Workout)
admin.site.register(Goal)
admin.site.register(Progress)

