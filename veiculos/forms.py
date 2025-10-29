import re

from django import forms

from clientes.models import PessoaFisica, PessoaJuridica, Pessoa
from funcionarios.models import Funcionario
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
    pessoas_autorizadas = forms.ModelMultipleChoiceField(
        queryset=Pessoa.objects.exclude(id__in=Funcionario.objects.values_list('id',flat=True)),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Pessoas Autorizadas",
        help_text="Selecione as pessoas autorizadas para o veículo."
    )



    class Meta:
        model = Veiculos
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



        self.fields['proprietario'].queryset = Pessoa.objects.exclude(id__in=Funcionario.objects.values_list('id',flat=True))




    def clean_placa(self):
        placa = self.cleaned_data.get('placa').upper()

        formato_antigo = re.compile(r'^[A-Z]{3}[0-9]{4}$')
        formato_mercosul = re.compile(r'^[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}$')


        if not (formato_antigo.match(placa) or formato_mercosul.match(placa)):
            raise forms.ValidationError("A placa deve seguir os formatos AAA1234 ou AAA1A23.")

        return placa

    def clean(self):
        cleaned_data = super().clean()
        proprietario = cleaned_data.get('proprietario')



        if not proprietario :
            raise forms.ValidationError("É necessário informar um Proprietário.")


        campos_obrigatorios = ['placa', 'tipo', 'marca', 'modelo', 'ano']
        for campo in campos_obrigatorios:
            if not cleaned_data.get(campo):
             self.add_error(campo, f'O campo {campo} é obrigatório.')


        return cleaned_data