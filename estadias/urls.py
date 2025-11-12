from django.urls import path

from estadias.views import EstadiaView, EstadiaAddView, EstadiaUpdateView, EstadiaDeleteView, ValorHoraView, \
    ValorHoraAddView, ValorHoraUpdateView, ValorHoraDeleteView, EstadiaVisualizar

urlpatterns = [
    path('estadias', EstadiaView.as_view(), name='estadias'),
    path('<int:pk>/estadia/visualizar', EstadiaVisualizar.as_view(), name='estadias_visualizar'),
    path('valor_hora', ValorHoraView.as_view(), name='valor_hora'),
    path('estadia/adicionar',EstadiaAddView.as_view(), name='estadia_adicionar'),
    path('<int:pk>/estadia/editar', EstadiaUpdateView.as_view(), name='estadia_editar'),
    path('<int:pk>/estadia/apagar', EstadiaDeleteView.as_view(), name='estadia_apagar'),
    path('valor_hora/adicionar', ValorHoraAddView.as_view(), name='valor_hora_adicionar'),
    path('<int:pk>/valor_hora/editar', ValorHoraUpdateView.as_view(), name='valor_hora_editar'),
    path('<int:pk>/valor_hora/apagar', ValorHoraDeleteView.as_view(), name='valor_hora_apagar'),

]