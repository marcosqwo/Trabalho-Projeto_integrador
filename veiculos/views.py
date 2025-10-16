from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from veiculos.forms import VeiculosModelForm
from veiculos.models import Veiculos


class VeiculosView(ListView):
    model = Veiculos
    template_name = 'veiculos.html'
    context_object_name = 'veiculos'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(VeiculosView, self).get_queryset()
        if buscar:
            qs = qs.filter(placa__icontains=buscar)
        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem Veículos cadastrados!')


class VeiculoAddView(SuccessMessageMixin, CreateView):
    model = Veiculos
    form_class = VeiculosModelForm
    template_name = 'veiculos_form.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo cadastrado com sucesso!'



class VeiculoUpdateView(SuccessMessageMixin,UpdateView):
    model = Veiculos
    form_class = VeiculosModelForm
    template_name = 'veiculos_form.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo alterado com sucesso!'


class VeiculoDeleteView(SuccessMessageMixin,DeleteView):
    model = Veiculos
    template_name = 'veiculos_apagar.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo deletado com sucesso!'
    context_object_name = 'veiculos'


