from _decimal import Decimal
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
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

    def form_valid(self, form):
        form.instance.saida = None
        form.instance.valor = Decimal('0.00')
        form.instance.situacao = '1'

        return super().form_valid(form)

class EstadiaUpdateView(SuccessMessageMixin,UpdateView):
    model = Estadia
    form_class = EstadiaModelForm
    template_name = 'estadia_form.html'
    success_url = reverse_lazy('estadias')
    success_message = 'Estádia atualizado com sucesso!'

    def form_valid(self, form):

        try:
            form.instance.valor = form.instance.calcular_valor()
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

        return super().form_valid(form)



class EstadiaDeleteView(SuccessMessageMixin,DeleteView):
    model = Estadia
    template_name = 'estadia_apagar.html'
    success_url = reverse_lazy('estadias')
    success_message = 'Estádia deletado com sucesso!'

class EstadiaVisualizar(DetailView):
    model = Estadia
    template_name = 'estadia_visualizar.html'
    context_object_name = 'estadia'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        try:
            context['pagamento'] = self.object.pagamentos.first()
        except Exception:
            context['pagamento'] = None

        return context

class ValorHoraAddView(SuccessMessageMixin,CreateView):
    model = ValorHora
    form_class = ValorHoraModelForm
    template_name = 'valor_hora_form.html'
    success_url = reverse_lazy('valor_hora')
    success_message = 'Valor de horario criado com sucesso!'

class ValorHoraUpdateView(SuccessMessageMixin,UpdateView):
    model = ValorHora
    form_class = ValorHoraModelForm
    template_name = 'valor_hora_form.html'
    success_url = reverse_lazy('valor_hora')
    success_message = 'Valor de Horário atualizada com sucesso!'



class ValorHoraDeleteView(SuccessMessageMixin,DeleteView):
    model = ValorHora
    success_url = reverse_lazy('valor_hora')
    success_message = 'Valor de Horário deletado com sucesso!'



class ValorHoraView(ListView):
    model = ValorHora
    template_name = 'valor_hora.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estadias_ativas'] = Estadia.objects.filter(situacao='1').exists()
        return context




