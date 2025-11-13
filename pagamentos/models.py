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
    PARCELAS_CHOICES = (
        (1, '1x'),
        (2, '2x'),
        (3, '3x'),
        (4, '4x'),
        (5, '5x'),
        (6, '6x'),
        (7, '7x'),
        (8, '8x'),
        (9, '9x'),
        (10, '10x'),
        (11, '11x'),
        (12, '12x'),
    )

    JUROS_CREDITO = {
        1: Decimal('0.00'),
        2: Decimal('2.50'),
        3: Decimal('3.00'),
        4: Decimal('3.50'),
        5: Decimal('4.00'),
        6: Decimal('8.50'),
        7: Decimal('9.00'),
        8: Decimal('9.50'),
        9: Decimal('10.00'),
        10: Decimal('10.50'),
        11: Decimal('11.00'),
        12: Decimal('12.50'),
    }

    estadia = models.ForeignKey('estadias.Estadia',verbose_name='Estadia',on_delete=models.CASCADE,related_name='pagamentos')
    tipo = models.CharField('Tipo',max_length=1,default='1', choices=TIPO_PAGAMENTO ,help_text='Tipo de pagamento')
    valor_original = models.DecimalField('Valor Original',max_digits=10,decimal_places=2,help_text='Valor original da venda')
    valor_final = models.DecimalField('Valor Final',max_digits=10,decimal_places=2,default=0)
    parcelas = models.IntegerField('Parcelas', choices=PARCELAS_CHOICES, default=1)
    data_pago = models.DateTimeField('Data de Pagamento',default=timezone.now)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def calcular_valor_final(self):
        valor_base = self.valor_original or Decimal('0.00')

        if self.tipo == '4':
            juros = self.JUROS_CREDITO.get(self.parcelas, Decimal('0.00'))
            valor_final = valor_base * (Decimal('1') + juros / Decimal('100'))
        elif self.tipo == '1':
            desconto = valor_base * Decimal('0.10')
            valor_final = valor_base - desconto

        else:
            valor_final = valor_base

        return valor_final.quantize(Decimal('0.01'))

    def calcular_valor_parcela(self):
        valor_final = self.calcular_valor_final()
        return (valor_final / self.parcelas).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        self.valor_final = self.calcular_valor_final()
        super().save(*args, **kwargs)
        if self.estadia:
            self.estadia.situacao = 2
            self.estadia.save()
            self.estadia.enviar_email()

    def __str__(self):
        if self.tipo == '4':
            return f"{self.get_tipo_display()} - {self.parcelas}x de R$ {self.calcular_valor_parcela()}"
        return f"{self.get_tipo_display()} - R$ {self.valor_final}"