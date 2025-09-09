from django import forms
from .models import Device

class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['nombre', 'categoria', 'consumo_maximo', 'zona','estado']  # sin 'zona'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'consumo_maximo': forms.NumberInput(attrs={'class': 'form-control'}),
            'zona': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')], attrs={'class': 'form-select'})
        }

        
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres")
        
        return nombre