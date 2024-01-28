from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class Manager(BaseUserManager):

    def create_superuser(self, email, username, password, ime, prezime, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, username, password, ime, prezime, **other_fields)

    def create_user(self, email, username, password, ime, prezime, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, ime=ime, prezime=prezime, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=250)
    email = models.EmailField(max_length=80, unique=True)

    ime = models.CharField(max_length=25)
    prezime = models.CharField(max_length=25)
    rank = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    Superadmin = 'A'     # moze bas sve
    Armycommander = 'C'  # sve za jednu vojsku
    Unitcommander = 'U'  # sve za jednu jedinicu

    ROLE = [
        (Superadmin, 'Superadmin'),
        (Armycommander, 'Armycommander'),
        (Unitcommander, 'Unitcommander'),
    ]

    role = models.CharField(max_length=1, choices=ROLE, default=Unitcommander,)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = Manager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'ime', 'prezime']

    def __str__(self):
        return self.username


class Lokacija(models.Model):
    naziv = models.CharField(max_length=100)
    koordinate = models.CharField(max_length=40)


class Baza(models.Model):
    naziv = models.CharField(max_length=100)
    lokacija = models.ForeignKey(Lokacija, on_delete=models.CASCADE)
    lokalni_admin = models.ForeignKey(MyUser, on_delete=models.SET_NULL, blank=True, null=True)


class Jedinica(models.Model):
    naziv = models.CharField(max_length=100)
    trenutna_lokacija = models.ForeignKey(Lokacija, on_delete=models.SET_NULL, blank=True, null=True)
    baza = models.ForeignKey(Baza, on_delete=models.SET_NULL, blank=True, null=True)


class Skladiste(models.Model):
    naziv = models.CharField(max_length=100)
    lokacija = models.ForeignKey(Lokacija, on_delete=models.CASCADE)


class Oprema(models.Model):
    naziv = models.CharField(max_length=100)
    opis = models.CharField(max_length=2500)
    mjerna_jedinica = models.CharField(max_length=50, default='kg')


class OpremaSkladiste(models.Model):
    oprema = models.ForeignKey(Oprema, on_delete=models.CASCADE)
    skladiste = models.ForeignKey(Skladiste, on_delete=models.CASCADE)


class Osoblje(models.Model):
    ime = models.CharField(max_length=60)
    prezime = models.CharField(max_length=60)
    datum_rodjenja = models.DateField()


class VojnoOsoblje(Osoblje):
    rank = models.CharField(max_length=30, blank=True, null=True)


class ITOsoblje(Osoblje):

    Nivo1 = '1'  # moze bas sve
    Nivo2 = '2'  # sve za jednu vojsku
    Nivo3 = '3'  # sve za jednu jedinicu

    SIGURNOST = [
        (Nivo1, 'Nivo1'),
        (Nivo2, 'Nivo2'),
        (Nivo3, 'Nivo3'),
    ]

    sigurnosni_nivo = models.CharField(max_length=1, choices=SIGURNOST, default=Nivo3,)
    korisnicki_profil = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class Poruka(models.Model):
    tekst = models.CharField(max_length=5000)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    u_avijaciju = 'A'
    u_mornaricu = 'M'
    iz_avijacije = 'B'
    iz_mornarice = 'N'

    DIREKCIJA = [
        (u_avijaciju, 'u_avijaciju'),
        (u_mornaricu, 'u_mornaricu'),
        (iz_avijacije, 'iz_avijacije'),
        (iz_mornarice, 'iz_mornarice'),
    ]

    direkcija_poruke = models.CharField(max_length=1, choices=DIREKCIJA, default=u_avijaciju,)


class Zahtjev(models.Model):
    poruka = models.ForeignKey(Poruka, on_delete=models.CASCADE)
    lokacija = models.ForeignKey(Lokacija, on_delete=models.SET_NULL, blank=True, null=True)
    zavrseno = models.BooleanField(default=False)


class Logistika(models.Model):
    jedinica = models.ForeignKey(Jedinica, on_delete=models.CASCADE)
    oprema = models.ForeignKey(Oprema, on_delete=models.CASCADE)
    kolicina = models.IntegerField(default=1)