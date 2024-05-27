"""from django.contrib import admin
from django.urls import path, include
from parking import views

urlpatterns = [
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/create/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/update/<int:pk>/', views.vehicle_update, name='vehicle_update'),
]
+++++++++++++++++++

from django.contrib import admin
from django.urls import path
from parking import views 

app_name = 'parking'

urlpatterns = [
    path('', views.parking_table, name='table'),
    path('entry/', views.parking_entry, name='entry'),
    path('exit/', views.parking_exit, name='exit'),
]
"""
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.home, name='home'),
    path('parking_table/', views.parking_table, name='parking_table'),
    path('parking_entries/', views.parking_entries, name='parking_entries'),
    path('parking_exits/', views.parking_exits, name='parking_exits'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('delete_vehicle/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('delete_vehicle1/<int:vehicle_id>/', views.delete_vehicle1, name='delete_vehicle1'),
    path('delete_vehicle2/<int:vehicle_id>/', views.delete_vehicle2, name='delete_vehicle2'),
    path('vehicle_list/', views.vehicle_list, name='vehicle_list'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]

"""
from django.urls import path
from . import views
from .views import AdminLoginView

app_name = 'parking'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('home/', views.home, name='home'),
    path('parking_table/', views.parking_table, name='parking_table'),
    path('parking_entries/', views.parking_entries, name='parking_entries'),
    path('parking_exits/', views.parking_exits, name='parking_exits'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('delete_vehicle/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('vehicle_list/', views.vehicle_list, name='vehicle_list'),
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
]

"""

