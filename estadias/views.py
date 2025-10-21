from django.contrib import messages
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from estadias.forms import EstadiaModelForm, ValorHoraModelForm
from estadias.models import Estadia, ValorHora
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class EstadiaView(ListView):
    model = Estadia
    template_name = 'estadia.html'
    context_object_name = 'estadias'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(EstadiaView, self).get_queryset()
        if buscar:
            qs = qs.filter(veiculo__modelo__icontains=buscar)
        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem Estadias cadastradas!')

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



class EstadiaDeleteView(SuccessMessageMixin,DeleteView):
    model = Estadia
    template_name = 'estadia_apagar.html'
    success_url = reverse_lazy('estadias')
    success_message = 'Estádia deletado com sucesso!'


class ValorHoraAddView(SuccessMessageMixin,CreateView):
    model = ValorHora
    form_class =ValorHoraModelForm
    template_name = 'valor_hora_form.html'
    success_url = reverse_lazy('valor_hora')
    success_message = 'Valor de horario criado com sucesso!'

class ValorHoraUpdateView(SuccessMessageMixin,UpdateView):
    model = ValorHora
    form_class = EstadiaModelForm
    template_name = 'estadia_form.html'
    success_url = reverse_lazy('valor_hora')
    success_message = 'Estádia criada com sucesso!'

class ValorHoraView(ListView):
    model = ValorHora
    template_name = 'valor_hora.html'
    context_object_name = 'valor_hora'

