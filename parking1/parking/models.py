from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import random


class Vehicle(models.Model):
    matricule = models.CharField(max_length=20)

    def __str__(self):
        return self.matricule

class ParkingEntry(models.Model):
    STATUS_CHOICES = [
        ('Entrant', 'Entrant'),
        ('Sortant', 'Sortant'),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    entry_time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.vehicle.matricule} - Entry Time: {self.entry_time}"

    def save(self, *args, **kwargs):
        if self.status == 'Entrant' and not self.location:
            occupied_locations = ParkingEntry.objects.filter(status='Entrant').values_list('location', flat=True)
            all_locations = set(range(1, 101))  # Emplacements disponibles de 1 à 100 (vous pouvez les ajuster selon vos besoins)
            free_locations = list(all_locations - set(occupied_locations))
            if free_locations:
                self.location = random.choice(free_locations)
            else:
                raise ValidationError("Parking is full")
        elif self.status == 'Entrant' and self.location:
            if ParkingEntry.objects.filter(status='Entrant', location=self.location).exists():
                raise ValidationError("This location is already occupied")
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['location', 'status'], name='unique_location_status')
        ]



class ParkingExit(models.Model):
    parking_entry = models.OneToOneField(ParkingEntry, on_delete=models.CASCADE)
    exit_time = models.DateTimeField(default=timezone.now)
    freed_location = models.CharField(max_length=50, )
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.parking_entry.vehicle.matricule} - Exit Time: {self.exit_time}"

    def save(self, *args, **kwargs):
        self.freed_location = self.parking_entry.location
        self.price = self.calculate_parking_price()
        super().save(*args, **kwargs)

    def calculate_parking_price(self):
        duration = self.exit_time - self.parking_entry.entry_time
        hours = duration.total_seconds() / 3600
        price_per_hour = 10  # Prix par heure de stationnement
        price = price_per_hour * hours
        return round(price, 2)

