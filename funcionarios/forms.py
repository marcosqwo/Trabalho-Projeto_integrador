from django import forms

from funcionarios.models import Funcionario


class FuncionarioModelForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome','funcao','fone','cpf', 'email', 'foto']


        error_messages = {
            'nome':{'required':'O nome do funcionário(a) é um campo obrigatório'},
            'funcao':{'required':'A função do funcionário(a) é um campo obrigatório'},
            'fone':{'required':'O Telefone do funcionário(a) é um campo obrigatório'},
            'cpf': {'required': 'Formato invalido de CPF. Exemplo: 000.000.000-00', 'unique': 'CPF ja cadastrado'},
            'email':{'required':'Formato invalido para o E-mail. Exemplo: fulanodetal@dominio.com',
                     'unique':'E-mail já cadastrado'}
        }