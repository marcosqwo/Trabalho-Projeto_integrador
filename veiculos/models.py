from django.db import models

class Veiculos(models.Model):
    TIPO_VEICULO = (
        ('1', 'Carro'),
        ('2', 'Moto'),
        ('3', 'Caminhoneta')
    )

    cliente_fisico = models.ForeignKey('clientes.PessoaFisica',verbose_name='Cliente',help_text='Nome do Cliente', on_delete=models.CASCADE,null=True,blank=True)
    cliente_juridico = models.ForeignKey('clientes.PessoaJuridica',verbose_name='Cliente jurídico',help_text='Nome do Jurídica', on_delete=models.CASCADE,null=True,blank=True)
    placa = models.CharField('Placa',max_length=7,help_text='Numero da Placa',unique=True)
    tipo = models.CharField('Tipo',max_length=1,default='1', choices=TIPO_VEICULO ,help_text='Classe do carro')
    marca = models.CharField('Marca',max_length=50,help_text='Marca do veiculo')
    modelo = models.CharField('Modelo',max_length=50,help_text='Modelo do veiculo')
    ano = models.CharField('Ano',max_length=4,help_text='Ano do veiculo')

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'

    def __str__(self):
        return self.marca