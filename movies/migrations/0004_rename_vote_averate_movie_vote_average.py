# Generated by Django 5.2.4 on 2025-07-09 12:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0003_movie"),
    ]

    operations = [
        migrations.RenameField(
            model_name="movie",
            old_name="vote_averate",
            new_name="vote_average",
        ),
    ]
