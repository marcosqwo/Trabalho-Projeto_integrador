from django import forms
from django.utils import timezone

from estadias.models import Estadia


class EstadiaModelForm(forms.ModelForm):
    entrada = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now
    )


    class Meta:
        model = Estadia
        fields = ['funcionario', 'veiculo', 'entrada']


class SaidaModelForm(forms.ModelForm):
    saida = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now
    )

    class Meta:
        model = Estadia
        fields = ['saida']
