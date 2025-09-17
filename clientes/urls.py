from django.urls import path

from clientes.views import ClientePessoaFisicaView, ClienteAddView, ClienteUpdateView, ClienteDeleteView, \
    ClienteJuridicoAddView, \
    ClienteJuridicoUpdateView, ClienteJuridicoDeleteView, ClientePessoaJuridicaView

urlpatterns = [
    path('clientes',ClientePessoaFisicaView.as_view(), name='clientes'),
    path('clientes_juridico',ClientePessoaJuridicaView.as_view(), name='clientes_juridico'),
    path('cliente/adicionar',ClienteAddView.as_view(), name='cliente_adicionar'),
    path('<int:pk>/cliente/editar',ClienteUpdateView.as_view(), name='cliente_editar'),
    path('<int:pk>/cliente/apagar',ClienteDeleteView.as_view(), name='cliente_apagar'),
    path('cliente/adicionar_juridico',ClienteJuridicoAddView.as_view(), name='cliente_juridico_adicionar'),
    path('<int:pk>/cliente/editar_juridico',ClienteJuridicoUpdateView.as_view(), name='cliente_juridico_editar'),
    path('<int:pk>/cliente/apagar_juridico',ClienteJuridicoDeleteView.as_view(), name='cliente_juridico_apagar'),
]