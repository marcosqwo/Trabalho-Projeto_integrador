from django.urls import path

from clientes.views import ClienteView, ClienteAddView, ClienteUpdateView, ClienteDeleteView

urlpatterns = [
    path('clientes',ClienteView.as_view(), name='clientes'),
    path('cliente/adicionar',ClienteAddView.as_view(), name='cliente_adicionar'),
    path('<int:pk>/cliente/editar',ClienteUpdateView.as_view(), name='cliente_editar'),
    path('<int:pk>/cliente/apagar',ClienteDeleteView.as_view(), name='cliente_apagar'),
]