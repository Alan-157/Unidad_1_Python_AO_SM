from django.shortcuts import render,redirect,get_object_or_404
from .models import Device, Measurement, Alert, Category, Zone
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomRegisterForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # o 'panel'
    else:
        form = CustomRegisterForm()
    return render(request, 'dispositivos/register.html', {'form': form})



@login_required
def dashboard(request):
    org = request.user.organization

    # Últimas mediciones
    latest_measurements = Measurement.objects.filter(organization=org).order_by('-timestamp')[:10]

    # Conteo por categoría y zona
    devices_by_category = (
        Device.objects.filter(organization=org)
        .values('category__name')
        .annotate(count=Count('id'))
    )
    devices_by_zone = (
        Device.objects.filter(organization=org)
        .values('zone__name')
        .annotate(count=Count('id'))
    )

    # Filtros de alertas
    severity = request.GET.get('severity')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    alerts = Alert.objects.filter(organization=org)

    if severity:
        alerts = alerts.filter(status=severity)
    if start_date:
        alerts = alerts.filter(timestamp__gte=start_date)
    if end_date:
        alerts = alerts.filter(timestamp__lte=end_date)

    reviewed_count = alerts.filter(reviewed=True).count()
    pending_count = alerts.filter(reviewed=False).count()
    severity_counts = alerts.values('status').annotate(count=Count('id'))
    recent_alerts = alerts.order_by('-timestamp')[:10]

    context = {
        'latest_measurements': latest_measurements,
        'devices_by_category': devices_by_category,
        'devices_by_zone': devices_by_zone,
        'reviewed_count': reviewed_count,
        'pending_count': pending_count,
        'severity_counts': severity_counts,
        'recent_alerts': recent_alerts,
        'filters': {
            'severity': severity,
            'start_date': start_date,
            'end_date': end_date
        }
    }
    return render(request, 'dispositivos/dashboard.html', context)

def inicio(request):
    return render(request, 'dispositivos/inicio.html')

@login_required
def device_list(request):
    org = request.user.organization
    category_id = request.GET.get('category')
    categories = Category.objects.filter(organization=org)

    devices = Device.objects.filter(organization=org)
    if category_id:
        devices = devices.filter(category_id=category_id)

    return render(request, 'dispositivos/device_list.html', {
        'devices': devices,
        'categories': categories
    })

@login_required    
def device_detail(request, device_id):
    org = request.user.organization
    device = get_object_or_404(Device, id=device_id, organization=org)
    measurements = Measurement.objects.filter(device=device).order_by('-timestamp')
    alerts = Alert.objects.filter(measurement__device=device).order_by('-timestamp')

    return render(request, 'dispositivos/device_detail.html', {
        'device': device,
        'measurements': measurements,
        'alerts': alerts
    })

@login_required
def measurement_list(request):
    org = request.user.organization

    # Filtros
    device_id = request.GET.get('device')
    zone_id = request.GET.get('zone')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    measurements = Measurement.objects.filter(organization=org).order_by('-timestamp')

    if device_id:
        measurements = measurements.filter(device_id=device_id)

    if zone_id:
        measurements = measurements.filter(device__zone_id=zone_id)

    if start_date:
        measurements = measurements.filter(timestamp__gte=start_date)

    if end_date:
        measurements = measurements.filter(timestamp__lte=end_date)

    paginator = Paginator(measurements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    devices = Device.objects.filter(organization=org)
    zones = Zone.objects.filter(organization=org)

    return render(request, 'dispositivos/measurement_list.html', {
        'page_obj': page_obj,
        'devices': devices,
        'zones': zones,
        'filters': {
            'device': device_id,
            'zone': zone_id,
            'start_date': start_date,
            'end_date': end_date
        }
    })

@login_required
def alert_summary(request):
    org = request.user.organization
    one_week_ago = timezone.now() - timedelta(days=7)

    alerts = Alert.objects.filter(organization=org)

    # Conteo por estado
    reviewed_count = alerts.filter(reviewed=True).count()
    pending_count = alerts.filter(reviewed=False).count()

    # Conteo por severidad (usando status)
    severity_counts = alerts.values('status').annotate(count=Count('id'))

    # Últimas alertas
    recent_alerts = alerts.order_by('-timestamp')[:10]

    return render(request, 'dispositivos/alerts_summary.html', {
        'reviewed_count': reviewed_count,
        'pending_count': pending_count,
        'severity_counts': severity_counts,
        'recent_alerts': recent_alerts
    })
