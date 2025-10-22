from django import forms
from django.utils import timezone

from estadias.models import Estadia, ValorHora


class EstadiaModelForm(forms.ModelForm):
    entrada = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now
    )
    saida = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now
    )





    class Meta:
        model = Estadia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if  self.instance and self.instance.pk:
            self.fields['entrada'].widget = forms.HiddenInput()
            self.fields['funcionario_entrada'].widget = forms.HiddenInput()
            self.fields['veiculo'].widget = forms.HiddenInput()
        else:
            self.fields['saida'].widget = forms.HiddenInput()
            self.fields['funcionario_saida'].widget = forms.HiddenInput()







class ValorHoraModelForm(forms.ModelForm):
    class Meta:
        model = ValorHora
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tipos_usados = ValorHora.objects.values_list('tipo', flat=True)
        if self.instance.pk:
            tipos_usados = tipos_usados.exclude(tipo=self.instance.tipo)
        self.fields['tipo'].choices = [(key,label) for key,label in ValorHora.TIPO_VEICULO if key not in tipos_usados]
