from django import forms

from .models import PessoaFisica, PessoaJuridica


class PessoaFisicaModelForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        fields = ['nome','fone', 'email', 'cpf']


        error_messages = {
            'nome':{'required':'O nome do cliente é um campo obrigatório'},
            'fone':{'required':'O Telefone do cliente é um campo obrigatório'},
            'email':{'required':'Formato invalido para o E-mail. Exemplo: fulanodetal@dominio.com',
                     'unique':'E-mail já cadastrado'},
            'cpf':{'required':'Formato invalido de CPF. Exemplo: 000.000.000-00','unique':'CPF ja cadastrado'}

        }

class PessoaJuridicaModelForm(forms.ModelForm):
        class Meta:
            model = PessoaJuridica
            fields = ['nome','fone', 'email', 'cnpj']


        error_messages = {
            'nome':{'required':'O nome do cliente é um campo obrigatório'},
            'fone':{'required':'O Telefone do cliente é um campo obrigatório'},
            'email':{'required':'Formato invalido para o E-mail. Exemplo: fulanodetal@dominio.com',
                     'unique':'E-mail já cadastrado'},
            'cnpj':{'required':'Formato invalido de CNPJ. Exemplo: 00.000.000/0000-00','unique':'CNPJ ja cadastrado'}

        }


