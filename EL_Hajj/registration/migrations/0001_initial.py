# Generated by Django 5.0.3 on 2024-04-25 13:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tirage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_tirage', models.IntegerField(default=1)),
                ('nombre_de_place', models.IntegerField(default=0)),
                ('tranche_age', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WaitingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nin', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Winners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nin', models.CharField(max_length=150, unique=True)),
            ],
        ),
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
                ('nationality', models.CharField(choices=[('Algérienne', 'Algérien'), ('Bahreïnienne', 'Bahreïnien'), ('Bangladaise', 'Bangladais'), ('Comorienne', 'Comorien'), ('Égyptienne', 'Égyptien'), ('Émirienne', 'Émirien'), ('Indonésienne', 'Indonésien'), ('Jordanienne', 'Jordanien'), ('Koweïtienne', 'Koweïtien'), ('Libanaise', 'Libanais'), ('Libyenne', 'Libyen'), ('Malaisienne', 'Malaisien'), ('Maldivienne', 'Maldivien'), ('Malienne', 'Malien'), ('Marocaine', 'Marocain'), ('Mauritanienne', 'Mauritanien'), ('Nigérienne', 'Nigérien'), ('Omanaise', 'Omanais'), ('Pakistanaise', 'Pakistanais'), ('Palestinienne', 'Palestinien'), ('Qatarienne', 'Qatarien'), ('Saoudienne', 'Saoudien'), ('Sénégalaise', 'Sénégalais'), ('Somalienne', 'Somalien'), ('Soudanaise', 'Soudanais'), ('Syrienne', 'Syrien'), ('Tchadienne', 'Tchadien'), ('Tunisienne', 'Tunisien'), ('Turque', 'Turc'), ('Yéménite', 'Yéménite')], max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('personal_picture', models.ImageField(upload_to='haaj_pictures/')),
                ('maahram_id', models.PositiveIntegerField(default=None, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Baladiya',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('wilaya', models.IntegerField(default=None, null=True)),
                ('id_utilisateur', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('tirage', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.tirage')),
            ],
        ),
    ]
