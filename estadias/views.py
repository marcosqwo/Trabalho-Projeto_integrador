from django.contrib import messages
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from estadias.forms import EstadiaModelForm, SaidaModelForm
from estadias.models import Estadia
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class EstadiaView(ListView):
    model = Estadia
    template_name = 'estadia.html'
    context_object_name = 'estadias'

    def get_queryset(self):
        buscar=self.request.GET.get('buscar')
        qs = super(EstadiaView,self).get_queryset()
        if buscar:
          qs = qs.filter(nome__icontains=buscar)
        if qs.count()>0:
            paginator = Paginator(qs,10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem Funcionários cadastrados!')

class EstadiaAddView(SuccessMessageMixin,CreateView):
    model = Estadia
    form_class = EstadiaModelForm
    template_name = 'estadia_form.html'
    success_url = reverse_lazy('estadias')
    success_message = 'Estádia criada com sucesso!'

class EstadiaUpdateView(SuccessMessageMixin,UpdateView):
    model = Estadia
    form_class = EstadiaModelForm
    template_name = 'estadia_form.html'
    success_url = reverse_lazy('estadias')
    success_message = 'Estádia atualizado com sucesso!'


class SaidaEstadiaUpdateView(SuccessMessageMixin,UpdateView):
    model = Estadia
    form_class = SaidaModelForm
    template_name = 'estadia_form.html'
    success_url = reverse_lazy('estadias')
    success_message = 'Estádia atualizado com sucesso!'
    #
    # def form_valid(self, form):
    #     #tempo = data_saida - data_entrada
    #


class EstadiaDeleteView(SuccessMessageMixin,DeleteView):
    model = Estadia
    template_name = 'estadia_apagar.html'
    success_url = reverse_lazy('estadias')
    success_message = 'Estádia deletado com sucesso!'
