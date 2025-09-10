from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from clientes.forms import PessoaFisicaModelForm
from clientes.models import PessoaFisica

class ClienteView(ListView):
    model = PessoaFisica
    template_name = 'clientes.html'


    def get_queryset(self):
        buscar=self.request.GET.get('buscar')
        qs = super(ClienteView,self).get_queryset()
        if buscar:
             qs.filter(nome__icontains=buscar)
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

