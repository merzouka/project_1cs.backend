# Generated by Django 4.2.11 on 2024-05-01 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_personal_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('administrateur', 'administrateur'), ('responsable tirage', 'responsable tirage'), ('medecin', 'medecin'), ('Hedj', 'Hedj'), ('banquier', 'banquier')]),
        ),
    ]
