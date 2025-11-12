from django.test import Client
from django.views.generic import TemplateView

from clientes.models import PessoaFisica, PessoaJuridica
from estadias.models import Estadia
from funcionarios.models import Funcionario


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qtd_funcionarios'] = Funcionario.objects.count()
        context['qtd_clientes'] = PessoaFisica.objects.count() + PessoaJuridica.objects.count()
        context['qtd_carros'] = Estadia.objects.filter(situacao='1').count()
        return context