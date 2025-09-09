from django.db import models
from django.utils import timezone

# Modelo base con atributos comunes para heredar en otras tablas
class BaseModel(models.Model):
    ESTADOS = [
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    ]

    estado = models.CharField(max_length=10, choices=ESTADOS, default="ACTIVO")  # Estado funcional del objeto
    creado = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    actualizado = models.DateTimeField(auto_now=True)  # Fecha de última modificación
    eliminado = models.DateTimeField(null=True, blank=True)  # Fecha de eliminación lógica (opcional)

    class Meta:
        abstract = True  # Este modelo no crea tabla, solo se hereda

# Modelo: Categoría
class Category(BaseModel):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Modelo: Zona
class Zone(BaseModel):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción de la zona.")

    def __str__(self):
        return self.nombre

# Modelo: Dispositivo
class Device(BaseModel):
    nombre = models.CharField(max_length=100)
    consumo_maximo = models.IntegerField()  # Consumo en watts
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Modelo: Medición
class Measurement(BaseModel):
    dispositivo = models.ForeignKey(Device, on_delete=models.CASCADE)
    consumo_w = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Medición de {self.dispositivo.nombre} - {self.consumo_w}W"

# Modelo: Alerta
class Alert(BaseModel):
    medicion = models.OneToOneField(Measurement, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    revisada = models.BooleanField(default=False, help_text="Indica si la alerta ha sido revisada.")

    def __str__(self):
        return f"Alerta para {self.medicion.dispositivo.nombre}"

# Modelo: Organización
class Organization(BaseModel):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    zona = models.ForeignKey(Zone, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre