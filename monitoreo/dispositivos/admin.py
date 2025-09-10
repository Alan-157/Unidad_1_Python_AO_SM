from django.contrib import admin
from .models import Category, Zone, Device, Measurement, Alert, Organization

#Registro del modelo Categoria
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'created_at', 'organization')
    search_fields = ('name',)
    list_filter = ('status', 'organization')

#Registro del modelo Zona
@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'created_at', 'organization')
    search_fields = ('name',)
    list_filter = ('status', 'organization')

#Registro del modelo Dispositivo
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_consumption', 'category', 'zone', 'status', 'created_at', 'organization')
    search_fields = ('name',)
    list_filter = ('category', 'zone', 'status', 'organization')

#Registro del modelo Medicion
@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('device', 'consumption_w', 'timestamp', 'status', 'organization')
    list_filter = ('device', 'timestamp', 'organization')
    search_fields = ('device__name',)

#Registro del modelo Alerta
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('measurement', 'message', 'timestamp', 'reviewed', 'status', 'organization')
    list_filter = ('reviewed', 'timestamp', 'organization')
    search_fields = ('message', 'measurement__device__name')

#REgistro del modelo Organizacion
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'description', 'status', 'created_at')
    search_fields = ('name',)
    list_filter = ('zone', 'status')