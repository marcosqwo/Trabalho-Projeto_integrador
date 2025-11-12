from django.urls import path

from . import views
from pagamentos.views import PagamentoView, PagamentoAddView

urlpatterns = [
    path('pagamentos',PagamentoView.as_view(), name='pagamentos'),
    path('pagamento/adicionar/<int:pk>',PagamentoAddView.as_view(), name='estadia_pagar'),
    path('pagamentos/calcular/', views.calcular_valor_final_view, name='calcular_valor'),
]