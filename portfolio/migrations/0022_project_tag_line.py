# Generated by Django 5.2 on 2025-05-25 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0021_remove_user_temp'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='tag_line',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
