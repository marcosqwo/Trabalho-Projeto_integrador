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
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data.get('entrada'):
            form = self.veiculo.





#
# class SaidaModelForm(forms.ModelForm):
#     saida = forms.DateTimeField(
#         widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         initial=timezone.now
#     )
#
#
#     class Meta:
#         model = Estadia
#         fields = ['saida']
