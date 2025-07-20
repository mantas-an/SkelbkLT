from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class CustomUser (AbstractUser):
    FIRST_NAME_VALIDATOR = RegexValidator(
        regex=r'^[a-zA-ZąčęėįšųūžĄČĘĖĮŠŲŪŽ]+(?: [a-zA-ZąčęėįšųūžĄČĘĖĮŠŲŪŽ]+)*$',
        #Leidziam tik raides ir vienas tarpas tarp zodziu pavz: Jonas Petras, Ona Maria Jovita
    )
    LAST_NAME_VALIDATOR = RegexValidator(
        regex=r'^[a-zA-ZąčęėįšųūžĄČĘĖĮŠŲŪŽ]+(?:-[a-zA-ZąčęėįšųūžĄČĘĖĮŠŲŪŽ]+)?$',
    )   #pavarde gali buti su bruksneliu
    first_name = models.CharField(max_length=100, validators=[FIRST_NAME_VALIDATOR], blank=False)
    last_name = models.CharField(max_length=100, validators=[LAST_NAME_VALIDATOR], blank=False)
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=15, unique=True, help_text="+370xxxxxxxx arba 0xxxxxxxx")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    city = models.CharField(max_length=50, blank=True, help_text="Gyvenamoji vieta")
    ACCOUNT_TYPE_CHOICES = [
        ('Privatus asmuo', '(parduodu tik savo asmeninius daiktus)'),
        ('Įmonė', '(vykdau komercinę veiklą)'),
    ]
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        verbose_name='Paskyros tipas',
        help_text='Ar vartotojas yra privatus asmuo ar įmonė?'
    )