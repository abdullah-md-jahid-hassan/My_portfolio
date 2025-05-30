# Generated by Django 5.2 on 2025-05-18 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0009_alter_project_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Project Category',
                'verbose_name_plural': 'Project Categories',
            },
        ),
        migrations.RemoveField(
            model_name='project',
            name='category',
        ),
        migrations.AddField(
            model_name='project',
            name='categories',
            field=models.ManyToManyField(to='portfolio.projectcategory'),
        ),
    ]
