import re

from django import forms
from veiculos.models import Veiculos




class VeiculosModelForm(forms.ModelForm):
    placa = forms.CharField(
        max_length=7,
        min_length=7,
        label='Placa',
        help_text='A placa deve ter exatamente 7 caracteres, nos formatos AAA1234 ou AAA1A23.',
        error_messages={
            'min_length': 'A placa deve conter exatamente 7 caracteres.',
            'max_length': 'A placa deve conter exatamente 7 caracteres.',
            'required': 'A placa é obrigatória.',
        }
    )
    class Meta:
        model = Veiculos
        fields = "__all__"


    def clean_placa(self):
        placa = self.cleaned_data.get('placa').upper()

        formato_antigo = re.compile(r'^[A-Z]{3}[0-9]{4}$')
        formato_mercosul = re.compile(r'^[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}$')


        if not (formato_antigo.match(placa) or formato_mercosul.match(placa)):
            raise forms.ValidationError("A placa deve seguir os formatos AAA1234 ou AAA1A23.")

        return placa

    def clean(self):
        cleaned_data = super().clean()
        cliente_fisico = cleaned_data.get('cliente_fisico')
        cliente_juridico = cleaned_data.get('cliente_juridico')


        if not cliente_fisico and not cliente_juridico:
            raise forms.ValidationError("É necessário informar um cliente (físico ou jurídico).")


        campos_obrigatorios = ['placa', 'tipo', 'marca', 'modelo', 'ano']
        for campo in campos_obrigatorios:
            if not cleaned_data.get(campo):
             self.add_error(campo, f'O campo {campo} é obrigatório.')


        return cleaned_data