from django.urls import path
from pagamentos.views import PagamentoView, PagamentoAddView

urlpatterns = [
    path('pagamentos',PagamentoView.as_view(), name='pagamentos'),
    path('pagamento/adicionar/<int:pk>',PagamentoAddView.as_view(), name='estadia_pagar'),
]