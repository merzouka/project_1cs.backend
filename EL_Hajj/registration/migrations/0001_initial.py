# Generated by Django 5.0.4 on 2024-04-04 21:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Haaj',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name_arabic', models.CharField(max_length=100)),
                ('last_name_arabic', models.CharField(max_length=100)),
                ('mother_name', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=100)),
                ('NIN', models.CharField(max_length=150, unique=True)),
                ('card_expiration_date', models.DateField()),
                ('passport_id', models.CharField(max_length=100)),
                ('passport_expiration_date', models.DateField()),
                ('nationality', models.CharField(choices=[('Algérienne', 'Algérienne'), ('Autre', 'Autre')], max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('personal_picture', models.ImageField(upload_to='haaj_pictures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='Haaja',
            fields=[
                ('haaj_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='registration.haaj')),
                ('maahram_id', models.PositiveIntegerField()),
            ],
            bases=('registration.haaj',),
        ),
    ]
