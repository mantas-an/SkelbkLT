from autoslug import AutoSlugField
from autoslug.settings import slugify
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from polymorphic.models import PolymorphicModel
from djmoney.models.fields import MoneyField


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
    city = models.CharField(max_length=50, blank=True, help_text="Gyvenamasis miestas")
    ACCOUNT_TYPE_CHOICES = [
        ('Privatus_asmuo', 'Privatus asmuo'),
        ('Įmonė', 'Įmonė'),
    ]
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        verbose_name='Paskyros tipas',
        help_text='Ar vartotojas yra privatus asmuo ar įmonė?'
    )


class Category(models.Model):
    name = models.CharField(verbose_name='Pavadinimas', max_length=50)
    parent = models.ForeignKey(
        to= 'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Tevine kategorija'
    )
    #slug = models.SlugField(unique=True) URL parodomas ne id, o pavadinimas.
    #SLUG pakeitimas su django built in autoslug, turiem nested kategorijas/ supportina uniquenes for nested strukturas
    slug = AutoSlugField(
        populate_from='name', #automatiskai generatinam slug is name kintamojo
        unique=True, #jokiu duplikatu
        slugify=slugify, #handlina lietuviskas raides
        always_update=False,#slug pasilieka toks pat jei paiskeicia name
        editable=False,

    )
    order = models.PositiveIntegerField(default=0) #Rikiavimas


    def __str__(self):
        return self.name


    def get_full_path(self): #Sitas visas pasiskolintas is AI, reikes issiaiskinti kaip veikia
        #Grąžina pilnąkategorijos kelią(pvz.: 'Transportas/Automobiliai'
        path = [self.name]
        current = self.parent
        while current:
            path.append(current.name)
            current = current.parent
        return '/'.join(reversed(path))







#-----------------------------------------------------------------------------------------
#Bazinis modelis visiem parduodamiems produktams (cards,sealed products, accessories etc)

class Product(PolymorphicModel):
    name = models.CharField(verbose_name='Produkto pavadinimas', max_length=120)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

#---------------------------------------------------------------------------------------
#-----------------------------------VISI PRODUKTAI-----------------------------------------


class Single(Product):
    image = models.ImageField(upload_to='single_pics/', blank=True)
    set_name = models.CharField(max_length=50, verbose_name='Card set name', help_text='Rinkinio pavadinimas')
    RARITY_CHOICES = [
        ('C', 'Common'),
        ('UC', 'Uncommon'),
        ('R', 'Rare'),
        ('SR', 'Super Rare'),
        ('HR', 'Holo Rare'),
        ('UR', 'Ultra Rare'),
        ('ScR', 'Secret Rare'),
        ('P', 'Promo'),


    ]
    rarity = models.CharField(max_length=3, choices=RARITY_CHOICES, default='C', verbose_name='Retumas')

    FINISH_CHOICES =[
        ('NON_HOLO', 'Non-Holo'),
        ('HOLO', 'Holo'),
        ('REVERSE_HOLO', 'Reverse Holo'),
        ('TEXTURED', 'Textured Holo'),
        ('RAINBOW', 'Rainbow Rare'),
        ('GOD', 'God Rare'),
        ('ALT_ART', 'Alternate Art'),
        ('FULL_ART', 'Full Art'),
    ]
    finish = models.CharField(max_length=13, choices=FINISH_CHOICES, default='NON_HOLO', verbose_name='Ypatybės')

    def __str__(self):
        return f"{self.name} ({self.set_name})"




class SealedProduct(Product):
    image = models.ImageField(upload_to='sealed_product_pics/', blank=True)
    set_name = models.CharField(max_length=50, verbose_name='Set name', help_text='Rinkinio pavadinimas')
    PRODUCT_TYPE =[
        ('BOOSTER_BOX', 'Booster Box'),
        ('ETB', 'Elite Trainer Box'),
        ('STARTER_DECK', 'Starter Deck'),
        ('BOOSTER_PACK', 'Booster Pack'),
        ('BUNDLE', 'Bundle')
    ]
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE)
    release_year = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.set_name})"


#-----------------------------------VISI PRODUKTAI END-----------------------------------------




#---------------------------------------LISTING ----------------------------------------------------

class Listing(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='EUR')
    CONDITION_CHOICES = [
        ('M', 'Mint'),
        ('NM', 'Near Mint'),
        ('LP', 'Lightly Played'),
        ('HP', 'Heavily Played')

    ]
    condition = models.CharField(max_length=2, choices=CONDITION_CHOICES, default='NM')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    custom_image = models.ImageField(upload_to='listing_images/', blank=True, null=True)
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('SOLD', 'Sold'),
    ]

    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='ACTIVE')
    #su meta preventinam nuo pasikartojanciu tu paciu produktu
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'seller', 'condition'], name='unique_listing')
        ]

    def __str__(self):
        return f"{self.product.name} - {self.get_condition_display()}" #get condition display parodo MUM ISKAITOMAI ne raw data is database