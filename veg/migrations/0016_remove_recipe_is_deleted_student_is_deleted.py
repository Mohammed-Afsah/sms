# Generated by Django 5.1 on 2024-08-23 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veg', '0015_recipe_is_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='is_deleted',
        ),
        migrations.AddField(
            model_name='student',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
