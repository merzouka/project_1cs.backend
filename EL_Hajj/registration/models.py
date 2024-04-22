from django.db import models

from django.db import models
from authentication.models import utilisateur  

Nationalities = [
    ('Algérienne', 'Algérien'),
    ('Bahreïnienne', 'Bahreïnien'),
    ('Bangladaise', 'Bangladais'),
    ('Comorienne', 'Comorien'),
    ('Égyptienne', 'Égyptien'),
    ('Émirienne', 'Émirien'),
    ('Indonésienne', 'Indonésien'),
    ('Jordanienne', 'Jordanien'),
    ('Koweïtienne', 'Koweïtien'),
    ('Libanaise', 'Libanais'),
    ('Libyenne', 'Libyen'),
    ('Malaisienne', 'Malaisien'),
    ('Maldivienne', 'Maldivien'),
    ('Malienne', 'Malien'),
    ('Marocaine', 'Marocain'),
    ('Mauritanienne', 'Mauritanien'),
    ('Nigérienne', 'Nigérien'),
    ('Omanaise', 'Omanais'),
    ('Pakistanaise', 'Pakistanais'),
    ('Palestinienne', 'Palestinien'),
    ('Qatarienne', 'Qatarien'),
    ('Saoudienne', 'Saoudien'),
    ('Sénégalaise', 'Sénégalais'),
    ('Somalienne', 'Somalien'),
    ('Soudanaise', 'Soudanais'),
    ('Syrienne', 'Syrien'),
    ('Tchadienne', 'Tchadien'),
    ('Tunisienne', 'Tunisien'),
    ('Turque', 'Turc'),
    ('Yéménite', 'Yéménite')
]


class Haaj(models.Model):
    user = models.OneToOneField(utilisateur,  on_delete=models.CASCADE)
    first_name_arabic = models.CharField(max_length=100)
    last_name_arabic = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    NIN = models.CharField(max_length=150, unique=True)
    card_expiration_date = models.DateField()
    passport_id = models.CharField(max_length=100)
    passport_expiration_date = models.DateField()
    nationality = models.CharField(max_length=100, choices=Nationalities)
    phone_number = models.CharField(max_length=20)
    personal_picture = models.ImageField(upload_to='haaj_pictures/')

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super(Haaj, self).save(*args, **kwargs)
        self.user.nombreInscription += 1
        self.user.save() 
        
class Haaja(models.Model):
    user = models.OneToOneField(utilisateur,  on_delete=models.CASCADE)
    first_name_arabic = models.CharField(max_length=100)
    last_name_arabic = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    NIN = models.CharField(max_length=150, unique=True)
    card_expiration_date = models.DateField()
    passport_id = models.CharField(max_length=100)
    passport_expiration_date = models.DateField()
    nationality = models.CharField(max_length=100, choices=Nationalities)
    phone_number = models.CharField(max_length=20)
    personal_picture = models.ImageField(upload_to='haaj_pictures/')
    maahram_id = models.PositiveIntegerField()
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        super(Haaja, self).save(*args, **kwargs)
        self.user.nombreInscription += 1
        self.user.save()  
