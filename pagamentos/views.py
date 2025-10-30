from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from estadias.models import Estadia
from pagamentos.forms import PagamentoModelForm
from pagamentos.models import Pagamento


class PagamentoView(ListView):
    model = Pagamento
    template_name = 'pagamentos.html'
    context_object_name = 'pagamento'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(PagamentoView, self).get_queryset()
        if buscar:
            qs = qs.filter(estadia__veiculo__proprietario__icontains=buscar)
        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem Pagamentos cadastrados!')

class PagamentoAddView(SuccessMessageMixin,CreateView):
    model = Pagamento
    form_class = PagamentoModelForm
    template_name = 'pagamento_form.html'
    success_url = reverse_lazy('pagamentos')
    success_message = 'Pagamento criado com sucesso!'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        estadia_id = self.request.GET.get('estadia_id') or self.kwargs.get('estadia_id')
        if estadia_id:
            from estadias.models import Estadia
            kwargs['estadia'] = Estadia.objects.get(pk=estadia_id)
        return kwargs

    def form_valid(self, form):
        if not form.instance.estadia_id and 'estadia' in form.initial:
            form.instance.estadia = form.initial['estadia']
        return super().form_valid(form)
