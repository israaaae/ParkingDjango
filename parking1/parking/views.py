from django.shortcuts import get_object_or_404, redirect
from .forms import ParkingEntryForm, ParkingExitForm, VehicleForm
from .models import ParkingEntry, ParkingExit, Vehicle
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from .forms import VehicleForm
from .models import Vehicle
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required  # Assure que seuls les utilisateurs connectés peuvent accéder au tableau de bord
def dashboard(request):
    # Code pour récupérer les données à afficher sur le tableau de bord
    return render(request, 'dashboard.html')




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Rediriger vers la page de tableau de bord après la connexion réussie
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})




@login_required  
def parking_table(request):
    entries = ParkingEntry.objects.all()
    exits = ParkingExit.objects.all()
    return render(request, 'parking_table.html', {'entries': entries, 'exits': exits})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')




@login_required  
def parking_entries(request):
    if request.method == 'POST':
        form = ParkingEntryForm(request.POST)
        if form.is_valid():
            matricule = form.cleaned_data['vehicle'].matricule
            location = form.cleaned_data['location']
            
            # Vérifier si le véhicule n'existe pas dans la table d'entrée ou existe dans la table de sortie avec le même emplacement
            if not ParkingEntry.objects.filter(vehicle__matricule=matricule, location=location).exists() or ParkingExit.objects.filter(parking_entry__vehicle__matricule=matricule, parking_entry__location=location).exists():
                form.save()
                return redirect('parking_entries')
            else:
                form.add_error('vehicle', 'Ce véhicule est déjà entré dans le parking ou est en cours de sortie avec le même emplacement.')
    else:
        form = ParkingEntryForm()
    entries = ParkingEntry.objects.filter(status='Entrant')
    return render(request, 'parking_entries.html', {'form': form, 'entries': entries})








@login_required  
def parking_exits(request):
    if request.method == 'POST':
        form = ParkingExitForm(request.POST)
        if form.is_valid():
            parking_exit = form.save(commit=False)
            parking_exit.exit_time = timezone.now()  # Utilisez timezone.now() au lieu de datetime.now()
            parking_exit.price = calculate_parking_price(parking_exit.parking_entry.entry_time, parking_exit.exit_time)
            parking_exit.save()
            return redirect('parking_exits')
    else:
        form = ParkingExitForm()
    exits = ParkingExit.objects.all()
    return render(request, 'parking_exits.html', {'form': form, 'exits': exits})





def calculate_parking_price(entry_time, exit_time):
    duration = exit_time - entry_time
    hours = duration.total_seconds() / 3600
    price_per_hour = 5  # Prix par heure de stationnement
    price = price_per_hour * hours
    return round(price, 2)



@login_required  
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    
    vehicles = Vehicle.objects.all()
    context = {'form': form, 'vehicles': vehicles}
    return render(request, 'add_vehicle.html', context)

@login_required  
def vehicle_list(request):
    search_query = request.GET.get('search', '')
    vehicles = Vehicle.objects.filter(matricule__icontains=search_query)
    context = {'vehicles': vehicles, 'search_query': search_query}
    return render(request, 'vehicle_list.html', context)


@login_required  
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('parking_table')
    return render(request, 'delete_vehicle.html', {'vehicle': vehicle})

@login_required  
def delete_vehicle1(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_list')
    return render(request, 'delete_vehicle1.html', {'vehicle': vehicle})

@login_required  
def delete_vehicle2(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        parking_entry = ParkingEntry.objects.filter(vehicle=vehicle, status='Entrant').first()
        if parking_entry:
            parking_entry.delete()
        return redirect('parking_entries')
    return render(request, 'delete_vehicle2.html', {'vehicle': vehicle})

