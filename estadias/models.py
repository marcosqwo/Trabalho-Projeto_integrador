from django.db import models

from funcionarios.models import Funcionario

class ValorHora(models.Model):
    TIPO_VEICULO = (
        ('1', 'Carro'),
        ('2', 'Moto'),
        ('3', 'Caminhonete')
    )
    valor_da_hora = models.DecimalField('Valor total',max_digits=6,decimal_places=2,default=0.00)
    tipo = models.CharField('Tipo',max_length=1,default='1', choices=TIPO_VEICULO ,help_text='Classe do carro')




class Estadia(models.Model):
    funcionario = models.ForeignKey('funcionarios.Funcionario', on_delete=models.CASCADE)
    veiculo = models.ForeignKey('veiculos.Veiculos', on_delete=models.CASCADE)
    entrada = models.DateTimeField(null=True, blank=True)
    saida = models.DateTimeField(null=True,blank=True)
    valor = models.DecimalField('Valor total',max_digits=6,decimal_places=2,default=0.00)

    class Meta:
        verbose_name = 'Estadia'
        verbose_name_plural = 'Estadias'
        ordering = ['entrada']





