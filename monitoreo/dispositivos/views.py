from django.shortcuts import render,redirect, get_object_or_404
from .models import Device
from .forms import DispositivoForm
# Create your views here.
def inicio(request):
    #dispositivos = Dispositivo.objects.all()
    dispositivos = Device.objects.select_related("categoria")
    return render(request, "dispositivos/inicio.html",{"dispositivos": dispositivos
    })

def panel_dispositivos(request):
    dispositivos = [
        {"nombre": "Sensor Temperatura", "consumo": 50},
        {"nombre": "Medidor Solar", "consumo": 120},
        {"nombre": "Sensor Movimiento", "consumo": 30},
        {"nombre": "Calefactor", "consumo": 200},
        {"nombre": "AA", "consumo":1000}
    ]
    
    consumo_maximo = 100
    
    return render(request, "dispositivos/panel.html",{
        "dispositivos": dispositivos,
        "consumo_maximo": consumo_maximo
    })

def detalle_dispositivo(request, dispositivo_id):
    dispositivo = Device.objects.get(id=dispositivo_id)
    return render(request, "dispositivos/detalle.html", {"dispositivo": dispositivo})    

def listar_dispositivos(request):
    dispositivos = Device.objects.all()
    return render(request, "dispositivos/listado.html", {"dispositivos": dispositivos})


def crear_dispositivo(request):
    if request.method == "POST":
        form = DispositivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_dispositivos")
    else:
        form = DispositivoForm()
    
    return render(request, 'dispositivos/crear.html', {'form': form})