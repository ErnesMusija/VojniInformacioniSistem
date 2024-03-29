# Generated by Django 5.0 on 2024-01-28 17:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VISApp', '0007_zahtjev'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logistika',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kolicina', models.IntegerField(default=1)),
                ('jedinica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VISApp.jedinica')),
                ('oprema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VISApp.oprema')),
            ],
        ),
    ]
