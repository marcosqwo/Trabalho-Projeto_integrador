from django import forms


from pagamentos.models import Pagamento


class PagamentoModelForm(forms.ModelForm):
    valor_original = forms.DecimalField(
        label="Valor Original da Estadia",
        disabled=True,
        required=False,
        decimal_places=2,
        max_digits=6
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parcelas'].widget = forms.Select(choices=[(k,f'{v}x')for k,v in Pagamento.JUROS_CREDITO.items()])

        # # Se a estadia foi passada pela view (novo pagamento)
        # if estadia:
        #     self.fields['estadia'].initial = estadia
        #     self.fields['valor_original'].initial = estadia.valor
        #
        # # Se for edição (pagamento existente)
        # elif self.instance and self.instance.pk:
        #     estadia = self.instance.estadia
        #     self.fields['estadia'].initial = estadia
        #     self.fields['valor_original'].initial = estadia.valor



    class Meta:
        model = Pagamento
        verbose_name='Pagamento'
        verbose_name_plural='Pagamentos'
        fields=[ 'estadia', 'tipo', 'parcelas', 'data_pago', 'valor_final']
