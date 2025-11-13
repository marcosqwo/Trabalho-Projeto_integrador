from decimal import Decimal
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone



class ValorHora(models.Model):
    TIPO_VEICULO = (
        ('1', 'Carro'),
        ('2', 'Moto'),
        ('3', 'Caminhonete')
    )
    valor_da_hora = models.DecimalField('Valor total',max_digits=6,decimal_places=2,default=0.00,validators=[MinValueValidator(Decimal('0.01'))])
    tipo = models.CharField('Tipo',max_length=1,default='1', choices=TIPO_VEICULO ,help_text='Classe do carro')

    class Meta:
        verbose_name = 'Valor por Hora'
        verbose_name_plural = 'Valores por Hora'

    def __str__(self):
        return f"{self.get_tipo_display()} - R$ {self.valor_da_hora}/hora"



class Estadia(models.Model):
    SITUACAO_CARRO = (
        ('1','Estacionado'),
        ('2','Pago')
    )
    funcionario_entrada = models.ForeignKey('funcionarios.Funcionario',verbose_name='Funcionário Entrada',on_delete=models.CASCADE,related_name='func_entrada')
    funcionario_saida = models.ForeignKey('funcionarios.Funcionario',verbose_name='Funcionário Saida',on_delete=models.CASCADE,related_name='func_saida',null=True,blank=True)
    veiculo = models.ForeignKey('veiculos.Veiculos',verbose_name='Proprietário/Veiculo ', on_delete=models.CASCADE)
    entrada = models.DateTimeField()
    saida = models.DateTimeField(null=True,blank=True)
    valor = models.DecimalField('Valor total',max_digits=6,decimal_places=2,default=0.00)
    situacao = models.CharField(max_length=1,choices=SITUACAO_CARRO,default='1')
    valor_tipo_veiculo = models.DecimalField('Valor por hora aplicado',max_digits=6,decimal_places=2,default=0.00)

    class Meta:
        verbose_name = 'Estadia'
        verbose_name_plural = 'Estadias'
        ordering = ['-entrada']

    def calcular_valor(self):


        if not self.saida:
            raise ValidationError('Não é possível calcular valor sem data de saída.')


        if self.saida < self.entrada:
            raise ValidationError('A data de saída não pode ser anterior à entrada.')


        from estadias.models import ValorHora

        valor_hora_obj = ValorHora.objects.filter(tipo=self.veiculo.tipo).first()

        if not valor_hora_obj:
            self.valor_tipo_veiculo = Decimal('0.00')
            raise ValidationError(
                f'Não existe valor por hora cadastrado para veículos do tipo '
                f'"{self.veiculo.get_tipo_display()}". '
                f'Cadastre um valor em Admin > Valores por Hora.'
            )
        valor_por_hora = valor_hora_obj.valor_da_hora
        self.valor_tipo_veiculo = valor_por_hora

        if valor_por_hora <= 0:
            raise ValidationError(
                f'O valor por hora para {self.veiculo.get_tipo_display()} '
                f'é inválido: R$ {valor_por_hora}'
            )


        tempo_permanencia = self.saida - self.entrada
        horas_totais = Decimal(str(tempo_permanencia.total_seconds() / 3600))
        if tempo_permanencia.total_seconds() < 900:
            return Decimal('0.00')
        valor_total = valor_por_hora * horas_totais

        return valor_total.quantize(Decimal('0.01'))


    def save(self, *args, **kwargs):

        if self.saida:
            if self.saida > self.entrada:
                try:
                    if not self.valor or self.valor == Decimal('0.00'):
                        self.valor = self.calcular_valor()
                except ValidationError:
                    self.valor = Decimal('0.00')
            else:
                self.saida = None
                self.valor = Decimal('0.00')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.funcionario_entrada,self.funcionario_saida,self.veiculo,self.entrada,self.saida,self.valor,self.situacao}"

    def enviar_email(self):

            cliente = self.veiculo.proprietario
            email_destino = self.veiculo.proprietario.email

            dados = {
                'cliente': cliente,
                'entrada': self.entrada,
                'saida': self.saida,
                'valor': self.valor,
                'funcionario': self.funcionario_entrada,
            }

            texto_email = render_to_string('emails/texto_email.txt', dados)
            html_email = render_to_string('emails/texto_email.html', dados)

            send_mail(
                subject='Estacione Bem - Pagamento Concluído',
                message=texto_email,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email_destino],
                html_message=html_email,
                fail_silently=False,
            )

