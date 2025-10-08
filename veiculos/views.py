from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
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
    def form_valid(self, form):
        f = form.save(commit=False)

        clientepf = form.cleaned_data.get('cliente_fisico')
        clientepj = form.cleaned_data.get('cliente_juridico')

        if clientepf and clientepj:
           messages.error(self.request,'Não é possível selecionar tanto Pessoa Física quanto Pessoa Jurídica.')
           return super().form_invalid(form)
        elif clientepj or clientepf:
            f.save()
            messages.success(self.request,'Veículo cadastrado com sucesso!')
            return super().form_valid(form)
        else:
             messages.error(self.request,'Por favor, selecione pelo menos uma opção de cliente (Pessoa Física ou Pessoa Jurídica).')
             return super().form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())


class VeiculoUpdateView(SuccessMessageMixin,UpdateView):
    model = Veiculos
    form_class = VeiculosModelForm
    template_name = 'veiculos_form.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo alterado com sucesso!'
    def form_valid(self, form):
        f = form.save(commit=False)

        clientepf = form.cleaned_data.get('cliente_fisico')
        clientepj = form.cleaned_data.get('cliente_juridico')

        if clientepf and clientepj:
           messages.error(self.request,'Não é possível selecionar tanto Pessoa Física quanto Pessoa Jurídica.')
           return super().form_invalid(form)
        elif clientepj or clientepf:
            f.save()
            messages.success(self.request,'Veículo cadastrado com sucesso!')
            return super().form_valid(form)
        else:
             messages.error(self.request,'Por favor, selecione pelo menos uma opção de cliente (Pessoa Física ou Pessoa Jurídica).')
             return super().form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())

class VeiculoDeleteView(SuccessMessageMixin,DeleteView):
    model = Veiculos
    template_name = 'veiculos_apagar.html'
    success_url = reverse_lazy('veiculos')
    success_message = 'Veículo deletado com sucesso!'
    context_object_name = 'veiculos'


