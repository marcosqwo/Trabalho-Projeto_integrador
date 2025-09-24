from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from funcionarios.forms import FuncionarioModelForm
from funcionarios.models import Funcionario


class FuncionarioView(ListView):
    model = Funcionario
    template_name = 'funcionarios.html'
    context_object_name = 'funcionarios'

    def get_queryset(self):
        buscar=self.request.GET.get('buscar')
        qs = super(FuncionarioView,self).get_queryset()
        if buscar:
          qs = qs.filter(nome__icontains=buscar)
        if qs.count()>0:
            paginator = Paginator(qs,10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem Funcionários cadastrados!')

class FuncionarioAddView(SuccessMessageMixin,CreateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionarios_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário criado com sucesso!'

class FuncionarioUpdateView(SuccessMessageMixin,UpdateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionarios_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário atualizado com sucesso!'

class FuncionarioDeleteView(SuccessMessageMixin,DeleteView):
    model = Funcionario
    template_name = 'funcionario_apagar.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário deletado com sucesso!'
