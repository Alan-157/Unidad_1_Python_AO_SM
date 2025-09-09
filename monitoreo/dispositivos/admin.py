from django.contrib import admin
from .models import Category, Zone, Device, Measurement, Alert, Organization

# Registro del modelo: Categoría
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'estado', 'creado')
    search_fields = ('nombre',)
    list_filter = ('estado',)

# Registro del modelo: Zona
@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'estado', 'creado')
    search_fields = ('nombre',)
    list_filter = ('estado',)

# Registro del modelo: Dispositivo
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'consumo_maximo', 'categoria', 'estado', 'creado')
    search_fields = ('nombre',)
    list_filter = ('categoria', 'estado')

# Registro del modelo: Medición
@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('dispositivo', 'consumo_w', 'timestamp', 'estado')
    list_filter = ('dispositivo', 'timestamp')
    search_fields = ('dispositivo__nombre',)

# Registro del modelo: Alerta
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('medicion', 'mensaje', 'timestamp', 'revisada', 'estado')
    list_filter = ('revisada', 'timestamp')
    search_fields = ('mensaje', 'medicion__dispositivo__nombre')

# Registro del modelo: Organización
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'zona', 'descripcion', 'estado', 'creado')
    search_fields = ('nombre',)
    list_filter = ('zona', 'estado')