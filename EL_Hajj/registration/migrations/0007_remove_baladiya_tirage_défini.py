# Generated by Django 5.0.4 on 2024-06-04 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_baladiya_tirage_défini'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baladiya',
            name='tirage_défini',
        ),
    ]
