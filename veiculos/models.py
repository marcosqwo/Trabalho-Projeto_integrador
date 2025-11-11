from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from clientes.models import PessoaJuridica


class Veiculos(models.Model):
    TIPO_VEICULO = (
        ('1', 'Carro'),
        ('2', 'Moto'),
        ('3', 'Caminhonete')
    )

    proprietario = models.ForeignKey('clientes.Pessoa',verbose_name='Proprietário',help_text='Nome do Proprietário', on_delete=models.CASCADE)
    placa = models.CharField('Placa',max_length=7,help_text='Numero da Placa',unique=True)
    tipo = models.CharField('Tipo',max_length=1,default='1', choices=TIPO_VEICULO ,help_text='Classe do carro')
    marca = models.CharField('Marca',max_length=50,help_text='Marca do veiculo')
    modelo = models.CharField('Modelo',max_length=50,help_text='Modelo do veiculo')
    ano = models.IntegerField('Ano',help_text='Ano do veiculo',validators=[MinValueValidator(1900),MaxValueValidator(2100)])
    pessoas_autorizadas = models.ManyToManyField('clientes.PessoaFisica',verbose_name='Pessoas autorizadas',related_name='autorizadas',null=True,blank=True)

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'

    def __str__(self):
        return f"{self.proprietario} {self.marca} {self.modelo} ({self.placa})"

    def save(self, *args, **kwargs):
        if self.placa: 
           self.placa = self.placa.upper()
        super().save(*args, **kwargs)


