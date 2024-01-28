# Generated by Django 5.0 on 2024-01-07 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VISApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='broj_telefona',
        ),
        migrations.AddField(
            model_name='myuser',
            name='rank',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='role',
            field=models.CharField(choices=[('A', 'Superadmin'), ('C', 'Armycommander'), ('U', 'Unitcommander')], default='U', max_length=1),
        ),
    ]