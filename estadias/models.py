from django.db import models

from funcionarios.models import Funcionario


class Estadia(models.Model):
    funcionario = models.ForeignKey('funcionarios.Funcionario', on_delete=models.CASCADE)
    veiculo = models.ForeignKey('veiculos.Veiculos', on_delete=models.CASCADE)
    entrada = models.DateField()
    saida = models.DateField()


    class Meta:
        verbose_name = 'Estadia'
        verbose_name_plural = 'Estadias'
        ordering = ['entrada']