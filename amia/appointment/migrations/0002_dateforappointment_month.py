# Generated by Django 3.2.3 on 2021-05-17 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dateforappointment',
            name='month',
            field=models.IntegerField(default=0, verbose_name='Номер месяца'),
        ),
    ]
