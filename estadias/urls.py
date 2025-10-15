from django.urls import path

from estadias.views import EstadiaView, EstadiaAddView, EstadiaUpdateView, EstadiaDeleteView, SaidaEstadiaUpdateView

urlpatterns = [
    path('estadias', EstadiaView.as_view(), name='estadias'),
    path('estadia/adicionar',EstadiaAddView.as_view(), name='estadia_adicionar'),
    path('<int:pk>/estadia/editar', EstadiaUpdateView.as_view(), name='estadia_editar'),
    path('<int:pk>/estadia/sair', SaidaEstadiaUpdateView.as_view(), name='estadia_sair'),
    path('<int:pk>/estadia/apagar', EstadiaDeleteView.as_view(), name='estadia_apagar'),

]