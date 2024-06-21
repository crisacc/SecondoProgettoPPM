# Generated by Django 5.0.6 on 2024-06-21 12:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('achieved', models.BooleanField(default=False)),
                ('time_period', models.CharField(choices=[('daily', 'Giornaliero'), ('weekly', 'Settimanale'), ('monthly', 'Mensile'), ('single', 'Singolo')], max_length=10)),
                ('workout_type', models.CharField(choices=[('Corsa', 'Corsa'), ('Camminata', 'Camminata'), ('Camminata_veloce', 'Camminata veloce'), ('Camminata_nel_bosco', 'Camminata nel bosco'), ('Bicicletta', 'Bicicletta'), ('Nuoto', 'Nuoto'), ('Palestra', 'Palestra'), ('Trekking', 'Trekking')], max_length=50)),
                ('sessions_target', models.PositiveIntegerField(default=0)),
                ('sessions_completed', models.PositiveIntegerField(default=0)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to='tracker.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('progress_detail', models.TextField()),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progresses', to='tracker.goal')),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('workout_type', models.CharField(choices=[('Corsa', 'Corsa'), ('Camminata', 'Camminata'), ('Camminata_veloce', 'Camminata veloce'), ('Camminata_nel_bosco', 'Camminata nel bosco'), ('Bicicletta', 'Bicicletta'), ('Nuoto', 'Nuoto'), ('Palestra', 'Palestra'), ('Trekking', 'Trekking')], max_length=50)),
                ('duration', models.PositiveIntegerField()),
                ('calories_burned', models.PositiveIntegerField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to='tracker.profile')),
            ],
        ),
    ]
