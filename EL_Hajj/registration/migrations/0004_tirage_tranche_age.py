# Generated by Django 5.0.3 on 2024-04-24 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_waitinglist_winners'),
    ]

    operations = [
        migrations.AddField(
            model_name='tirage',
            name='tranche_age',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
