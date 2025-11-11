from django import forms
from django.utils import timezone
from funcionarios.models import Funcionario
from clientes.models import Pessoa, PessoaJuridica
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
        fields = ['funcionario_entrada','funcionario_saida','veiculo','entrada','saida','valor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if  self.instance and self.instance.pk:
            self.fields['entrada'].widget = forms.HiddenInput()
            self.fields['funcionario_entrada'].widget = forms.HiddenInput()
            self.fields['veiculo'].widget = forms.HiddenInput()
            self.fields['valor'].widget = forms.HiddenInput()
            self.fields['funcionario_saida'].required = True

            cliente = PessoaJuridica.objects.all().filter(pk=self.instance.veiculo.proprietario.pk)

            veiculo = getattr(self.instance,'veiculo',None)
            if veiculo and isinstance(veiculo.proprietario, Pessoa) and cliente:
                    self.fields['pessoas_autorizadas'] = forms.ModelMultipleChoiceField(
                        queryset=veiculo.pessoas_autorizadas.all(),
                        widget=forms.CheckboxSelectMultiple,
                        required=True,
                        label='Pessoas autorizadas para retirada'
                    )


        else:
            self.fields['saida'].widget = forms.HiddenInput()
            self.fields['funcionario_saida'].widget = forms.HiddenInput()
            self.fields['valor'].widget = forms.HiddenInput()

    def clean(self,):
        cleaned_data = super().clean()
        entrada = cleaned_data.get('entrada')
        saida = cleaned_data.get('saida')


        if saida and entrada and saida <= entrada:
            raise forms.ValidationError(
                'A data de saída deve ser posterior à data de entrada!'
            )
        veiculo = getattr(self.instance, 'veiculo', None)
        if veiculo and isinstance(veiculo.proprietario, PessoaJuridica):
            pessoas_aut = cleaned_data.get('pessoas_autorizadas')
            if not pessoas_aut or len(pessoas_aut) == 0:
                self.add_error('pessoas_autorizadas', 'Selecione pelo menos uma pessoa autorizada.')

        return cleaned_data






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

        if not self.fields['tipo'].choices and not self.instance.pk:
            self.fields['tipo'].choices = [('', 'Todos os tipos já foram cadastrados')]
            self.fields['tipo'].disabled = True

