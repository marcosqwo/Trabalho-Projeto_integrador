from django.db import models
from decimal import Decimal
from django.utils import timezone

class Pagamento(models.Model):
    TIPO_PAGAMENTO = (
        ('1', 'Pix'),
        ('2', 'Dinheiro'),
        ('3', 'Débito'),
        ('4', 'Crédito'),
    )
    JUROS_CREDITO = {
        1: Decimal('0.00'),
        2: Decimal('2.50'),
        3: Decimal('4.00'),
        4: Decimal('5.50'),
        5: Decimal('7.00'),
        7: Decimal('8.50'),
        8: Decimal('9.00'),
        9: Decimal('9.50'),
        10: Decimal('10.00'),
        11: Decimal('10.50'),
        12: Decimal('11.00'),
    }
    estadia = models.ForeignKey('estadias.Estadia',verbose_name='Estadia',on_delete=models.CASCADE,related_name='pagamentos')
    tipo = models.CharField('Tipo',max_length=1,default='1', choices=TIPO_PAGAMENTO ,help_text='Tipo de pagamento')
    data_pago= models.DateTimeField('Data de Pago',help_text='Data de pagamento')
    valor_original = models.DecimalField('Valor Original',max_digits=10,decimal_places=2,help_text='Valor original da venda')
    valor_final = models.DecimalField('Valor Final',max_digits=10,decimal_places=2,default=0)
    parcelas = models.PositiveIntegerField('Número de Parcelas',default=1,help_text='Número de parcelas')
    data_pago = models.DateTimeField('Data de Pagamento',default=timezone.now)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def calcular_valor_final(self):
        """
        Calcula o valor total com juros, com base na estadia e tipo de pagamento.
        """
        valor_base = self.estadia.valor or Decimal('0.00')

        if self.tipo == '4':
            juros = self.JUROS_CREDITO.get(self.parcelas, Decimal('0.00'))
            valor_final = valor_base * (1 + juros / 100)
        else:
            valor_final = valor_base

        return valor_final.quantize(Decimal('0.01'))

    def calcular_valor_parcela(self):
        """
        Calcula o valor de cada parcela (se for crédito parcelado).
        """
        valor_final = self.calcular_valor_final()
        return (valor_final / self.parcelas).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        """
        Sobrescreve o save para armazenar o valor final calculado.
        """

        self.valor_final = self.calcular_valor_final()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.tipo == '4':
            return f"{self.get_tipo_display()} - {self.parcelas}x de R$ {self.calcular_valor_parcela()}"
        return f"{self.get_tipo_display()} - R$ {self.valor_final}"