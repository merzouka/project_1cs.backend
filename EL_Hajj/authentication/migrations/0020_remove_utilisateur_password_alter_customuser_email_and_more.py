# Generated by Django 5.0 on 2024-03-29 07:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0019_gestionnairetirage_gestionnairewilaya_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='password',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='email'),
        ),
    ]
