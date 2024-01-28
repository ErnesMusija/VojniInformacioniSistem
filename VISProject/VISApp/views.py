from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


def registration(request):
    User = get_user_model()
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        ime = request.POST['name']
        prezime = request.POST['lastname']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already in use")
                return redirect('registration')

            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already in use")
                return redirect('registration')

            else:
                korisnik = User.objects.create_user(username=username, email=email, password=password, ime=ime,
                                                    prezime=prezime,)
                korisnik.is_active = True
                korisnik.save()
                return redirect('login')

        else:
            messages.info(request, "Password not the same")
            return redirect('registration')
    else:
        return render(request, 'registration.html')


def login(request):
    if request.method == "POST":

        password = request.POST['password']
        email = request.POST['email']

        korisnik = auth.authenticate(email=email, password=password)

        if korisnik is not None:
            auth.login(request, korisnik)
            return redirect('index')

        else:
            messages.info(request, "Pogresni kredencijali")
            return redirect('login')

    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


def communicate_airforce(request):
    return render(request, 'communicate_airforce.html')


def communicate_naval_forces(request):
    return render(request, 'communicate_naval_forces.html')


def order_supply(request):
    return render(request, 'order_supply.html')


def view_map(request):
    return render(request, 'view_map.html')


def logistics(request):
    oprema_values = Oprema.objects.values_list('naziv', flat=True)
    jedinica_values = Jedinica.objects.values_list('naziv', flat=True)

    if request.method == 'POST':
        equipment_type = request.POST.get('equipment-type')
        quantity = request.POST.get('quantity')
        military_unit = request.POST.get('military-unit')

        jedinica = Jedinica.objects.get(naziv=military_unit)
        oprema = Oprema.objects.get(naziv=equipment_type)

        logistika_instance = Logistika.objects.create(
            jedinica=jedinica,
            oprema=oprema,
            kolicina=quantity
        )
        logistika_instance.save()
        return render(request, 'logistics.html', {'oprema_values': oprema_values, 'jedinica_values': jedinica_values})

    return render(request, 'logistics.html', {'oprema_values': oprema_values, 'jedinica_values': jedinica_values})


def unit_management(request):
    baza_objects = Baza.objects.all()

    if request.method == 'POST':
        unit_name = request.POST.get('unit-name')
        unit_location_name = request.POST.get('unit-location')
        unit_coordinates = request.POST.get('unit-coordinates')
        unit_home_base_name = request.POST.get('unit-home-base')

        lokacija, created = Lokacija.objects.get_or_create(
            naziv=unit_location_name,
            koordinate=unit_coordinates
        )
        baza = Baza.objects.get(naziv=unit_home_base_name)
        # Create the Jedinica object without creating a new Baza object
        jedinica = Jedinica.objects.create(
            naziv=unit_name,
            trenutna_lokacija=lokacija,
            baza=baza
        )
        jedinica.save()
        return render(request, 'unit_management.html', {'baza_objects': baza_objects})

    return render(request, 'unit_management.html', {'baza_objects': baza_objects})


def communication(request):
    direkcija_poruke = 'A'
    if request.method == "POST":
        if 'avijacija_lokacija' in request.POST:
            airforce_location_name = request.POST.get('avijacija_lokacija')
            airforce_coordinates = request.POST.get('avijacija_koordinate')
            airforce_request = request.POST.get('avijacija_zahtjev')

            lokacija = Lokacija.objects.create(naziv=airforce_location_name, koordinate=airforce_coordinates)
            lokacija.save()

            poruka = Poruka.objects.create(user=request.user, tekst=airforce_request, direkcija_poruke=direkcija_poruke)
            poruka.save()

            zahtjev = Zahtjev.objects.create(lokacija=lokacija, poruka=poruka)
            zahtjev.save()

            return render(request, 'communication.html')

        elif 'mornarica_lokacija' in request.POST:
            navy_location_name = request.POST.get('mornarica_lokacija')
            navy_coordinates = request.POST.get('mornarica_koordinate')
            navy_request = request.POST.get('mornarica_zahtjev')
            direkcija_poruke = 'M'

            lokacija = Lokacija.objects.create(naziv=navy_location_name, koordinate=navy_coordinates)
            lokacija.save()

            poruka = Poruka.objects.create(user=request.user, tekst=navy_request, direkcija_poruke=direkcija_poruke)
            poruka.save()

            zahtjev = Zahtjev.objects.create(lokacija=lokacija, poruka=poruka)
            zahtjev.save()

            return render(request, 'communication.html')

    return render(request, 'communication.html')
