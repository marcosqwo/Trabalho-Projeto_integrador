from django.db import models
from stdimage import StdImageField

from clientes.models import PessoaFisica


class Funcionario(PessoaFisica):
    foto = StdImageField('Foto',upload_to='pessoas',delete_orphans=True,null=True,blank=True)
    funcao = models.CharField('Função', max_length=35, help_text='Função na empresa')


    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    def __str__(self):
        return super().nome