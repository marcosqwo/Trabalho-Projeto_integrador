from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from clientes.forms import PessoaFisicaModelForm , PessoaJuridicaModelForm
from clientes.models import PessoaFisica, PessoaJuridica
from funcionarios.models import Funcionario


class ClientePessoaFisicaView(ListView):
    model = PessoaFisica
    template_name = 'clientes.html'
    context_object_name = 'pessoafisica'

    def get_queryset(self):
        buscar=self.request.GET.get('buscar')
        qs = super(ClientePessoaFisicaView,self).get_queryset()
        if buscar:
          qs = qs.filter(nome__icontains=buscar)

        if qs.count()>0:
            qs = qs.exclude(id__in=Funcionario.objects.values_list('id',flat=True))
            paginator = Paginator(qs,1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem Clientes cadastrados!')


class ClientePessoaJuridicaView(ListView):
    model = PessoaJuridica
    template_name = 'clientes_juridicos.html'
    context_object_name = 'pessoajuridica'

    def get_queryset(self):
        buscar=self.request.GET.get('buscar')
        qs = super(ClientePessoaJuridicaView,self).get_queryset()
        if buscar:
          qs = qs.filter(nome__icontains=buscar)
        if qs.count()>0:
            paginator = Paginator(qs,1)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem Clientes cadastrados!')



class ClienteAddView(SuccessMessageMixin,CreateView):
    model = PessoaFisica
    form_class = PessoaFisicaModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente criado com sucesso!'


class ClienteJuridicoAddView(SuccessMessageMixin,CreateView):
    model = PessoaJuridica
    form_class = PessoaJuridicaModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes_juridico')
    success_message = 'Cliente criado com sucesso!'

class ClienteJuridicoUpdateView(SuccessMessageMixin,UpdateView):
    model = PessoaJuridica
    form_class = PessoaJuridicaModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes_juridico')
    success_message = 'Cliente atualizado com sucesso!'


class ClienteUpdateView(SuccessMessageMixin,UpdateView):
    model = PessoaFisica
    form_class = PessoaFisicaModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente atualizado com sucesso!'

class ClienteDeleteView(SuccessMessageMixin,DeleteView):
    model = PessoaFisica
    template_name = 'cliente_apagar.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente deletado com sucesso!'


class ClienteJuridicoDeleteView(SuccessMessageMixin,DeleteView):
    model = PessoaJuridica
    template_name = 'cliente_apagar.html'
    success_url = reverse_lazy('clientes_juridico')
    success_message = 'Cliente deletado com sucesso!'

