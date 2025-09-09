from django.shortcuts import get_object_or_404,render, redirect
# Import the models you want to use
from .models import Device, Measurement 
from .forms import DispositivoForm

def inicio(request):
    # This view remains the same for now.
    #dispositivos = Dispositivo.objects.all()
    dispositivos = Device.objects.select_related("categoria") #join
    
    return render(request, "dispositivos/inicio.html", {"dispositivos": dispositivos})

def panel_dispositivos(request):
    # 1. Get all 'Dispositivo' objects from the database.
    todos_los_dispositivos = Device.objects.all()
    
    # 2. You can also get other data, for example, the latest measurements.
    ultimas_mediciones = Measurement.objects.order_by('-timestamp')[:5] # Get the 5 most recent

    # 3. Pass the real data to the template.
    contexto = {
        "dispositivos": todos_los_dispositivos,
        "mediciones": ultimas_mediciones,
    }

    return render(request, "dispositivos/panel.html", contexto)

def dispositivo(request, dispositivo_id):
    dispositivo = Device.objects.get(id=dispositivo_id)

    return render(request,"dispositivos/dispositivo.html",{"dispositivo": dispositivo})

def crear_dispositivo(request):
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_dispositivos')
    else:
        form = DispositivoForm()
    
    return render(request, 'dispositivos/crear.html', {'form': form})

def listar_dispositivos(request):
    dispositivos = Device.objects.all()
    return render(request, 'dispositivos/listar.html', {'dispositivos': dispositivos})

def editar_dispositivo(request, dispositivo_id):
    dispositivo = get_object_or_404(Device, id=dispositivo_id)
    if request.method == 'POST':
        form = DispositivoForm(request.POST, instance=dispositivo)
        if form.is_valid():
            form.save()
            return redirect('listar_dispositivos')
    else:
        form = DispositivoForm(instance=dispositivo)
    return render(request, 'dispositivos/editar.html', {'form':form})

def eliminar_dispositivo(request,dispositivo_id):
    dispositivo = get_object_or_404(Device, id=dispositivo_id)
    if request.method == 'POST':
        dispositivo.delete()
        return redirect('listar_dispositivos')
    return render(request, 'dispositivos/eliminar.html',{'dispositivo': dispositivo})