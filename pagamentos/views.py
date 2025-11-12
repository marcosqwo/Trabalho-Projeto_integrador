from decimal import Decimal
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from estadias.models import Estadia

from pagamentos.models import Pagamento
from trabalho_final import settings


class PagamentoView(ListView):
    model = Pagamento
    template_name = 'pagamentos.html'
    context_object_name = 'pagamento'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(PagamentoView, self).get_queryset()
        if buscar:
            qs = qs.filter(estadia__veiculo__proprietario__nome__icontains=buscar)
        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem Pagamentos cadastrados!')


def calcular_valor_final_view(request):

    valor_str = request.GET.get('valor', '0').replace(',', '.')
    valor = Decimal(valor_str)
    tipo = request.GET.get('tipo', '1')
    parcelas = int(request.GET.get('parcelas', 1))


    p = Pagamento(valor_original=valor, tipo=tipo, parcelas=parcelas)

    return JsonResponse({
        'valor_final': str(p.calcular_valor_final()),
        'valor_parcela': str(p.calcular_valor_parcela()),
    })

class PagamentoAddView(SuccessMessageMixin,CreateView):
    model = Pagamento
    fields = ['tipo','parcelas']
    template_name = 'pagamento_form.html'
    success_url = reverse_lazy('estadias')
    success_message = 'Pagamento feito com sucesso!'

    def dispatch(self, request, *args, **kwargs):
        self.estadia = get_object_or_404(Estadia, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estadia'] = self.estadia
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context

    def form_valid(self, form):
        form.instance.estadia = self.estadia
        form.instance.valor_original = self.estadia.valor

        return super().form_valid(form)


