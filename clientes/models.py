from django.db import models



class Pessoa(models.Model):
    nome = models.CharField('Nome',max_length=50,help_text='Nome Completo')
    fone = models.CharField('Telefone',max_length=15,help_text='Número do Telefone')
    email = models.EmailField('E-mail',max_length=100,help_text='endereço de E-mail',unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome


class PessoaFisica(Pessoa):
    cpf = models.CharField('CPF',max_length=15,help_text='CPF Completo')


    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome


class PessoaJuridica(Pessoa):
    cnpj= models.CharField('CNPJ',max_length=15,help_text='CNPJ Completo')


    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome