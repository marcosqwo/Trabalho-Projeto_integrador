from django.urls import path

from veiculos.views import VeiculosView, VeiculoAddView, VeiculoUpdateView, VeiculoDeleteView

urlpatterns = [
    path('veiculos',VeiculosView.as_view(), name='veiculos'),
    path('Veiculo/adicionar',VeiculoAddView.as_view(), name='veiculo_adicionar'),
    path('<int:pk>/Veiculo/editar',VeiculoUpdateView.as_view(), name='veiculo_editar'),
    path('<int:pk>/Veiculo/apagar',VeiculoDeleteView.as_view(), name='veiculo_apagar'),
]
