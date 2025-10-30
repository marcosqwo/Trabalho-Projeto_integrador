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
    SITUACAO_CARRO = (
        ('1','Estacionado'),
        ('2','Pago')
    )
    funcionario_entrada = models.ForeignKey('funcionarios.Funcionario',verbose_name='Funcionário Entrada',on_delete=models.CASCADE,related_name='func_entrada')
    funcionario_saida = models.ForeignKey('funcionarios.Funcionario',verbose_name='Funcionário Saida',on_delete=models.CASCADE,related_name='func_saida',null=True,blank=True)
    veiculo = models.ForeignKey('veiculos.Veiculos', on_delete=models.CASCADE)
    entrada = models.DateTimeField()
    saida = models.DateTimeField(null=True,blank=True)
    valor = models.DecimalField('Valor total',max_digits=6,decimal_places=2,default=0.00)
    situacao = models.CharField(max_length=1,choices=SITUACAO_CARRO,default='1')

    class Meta:
        verbose_name = 'Estadia'
        verbose_name_plural = 'Estadias'
        ordering = ['entrada']

    def __str__(self):
        return f'{self.veiculo.proprietario} - {self.veiculo}'



