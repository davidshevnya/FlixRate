# Generated by Django 5.2.4 on 2025-07-09 07:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="genre",
            name="slug",
            field=models.SlugField(default="slug", unique=True),
            preserve_default=False,
        ),
    ]
