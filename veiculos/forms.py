from django import forms
from veiculos.models import Veiculos




class VeiculosModelForm(forms.ModelForm):
    class Meta:
        model = Veiculos
        fields = "__all__"

        error_messages = {

            # 'horario': {'required':'O horário é um campo obrigatório'},
            # 'cliente':{'required':'O cliente é um campo obrigatório'},
            # 'funcionario':{'required':'O funcionário é um campo obrigatório'}
        }