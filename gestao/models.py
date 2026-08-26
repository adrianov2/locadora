from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError


class Usuario(AbstractUser):
    PERFIL_CHOICES = [('admin', 'Administrador'), ('funcionario', 'Funcionário')]
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, default='funcionario')
    telefone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class LogAcesso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    acao = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-data_hora']
        verbose_name = 'Log de Acesso'


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100, blank=True)
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=300, blank=True)
    foto_documento = models.ImageField(upload_to='clientes/documentos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Cliente'

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'.strip()



class Veiculo(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('alugado', 'Alugado'),
        ('manutencao', 'Em Manutenção'),
    ]
    nome = models.CharField(max_length=100, help_text='Ex: Onix, HB20, Civic')
    modelo = models.CharField(max_length=100, help_text='Ex: LT, Sense, EXL')
    cor = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome', 'modelo']
        verbose_name = 'Veículo'

    def __str__(self):
        return f'{self.nome} {self.modelo} - {self.placa}'

class Peca(models.Model):
    nome = models.CharField(max_length=150)
    quantidade = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Peça'
        verbose_name_plural = 'Peças'

    def __str__(self):
        return f'{self.nome} ({self.quantidade} un.)'

class Manutencao(models.Model):
    TIPO_CHOICES = [
        ('revisao', 'Revisão'),
        ('oleo', 'Troca de Óleo'),
        ('pneu', 'Troca de Pneus'),
        ('seguro', 'Seguro'),
        ('licenciamento', 'Licenciamento'),
        ('ipva', 'IPVA'),
        ('outros', 'Outros'),
    ]
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='manutencoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True)
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    oficina = models.CharField(max_length=200, blank=True)
    proxima_revisao = models.DateField(null=True, blank=True)
    proxima_troca_oleo = models.DateField(null=True, blank=True)
    troca_pneus = models.DateField(null=True, blank=True)
    vencimento_seguro = models.DateField(null=True, blank=True)
    vencimento_licenciamento = models.DateField(null=True, blank=True)
    vencimento_ipva = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Manutenção'

    def __str__(self):
        return f'{self.veiculo} - {self.get_tipo_display()} - {self.data}'


class Locacao(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]
    PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('pix', 'PIX'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('transferencia', 'Transferência'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='locacoes')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='locacoes')
    data_retirada = models.DateField()
    hora_retirada = models.TimeField()
    data_prevista_devolucao = models.DateField()
    hora_prevista_devolucao = models.TimeField()
    data_devolucao_real = models.DateField(null=True, blank=True)
    hora_devolucao_real = models.TimeField(null=True, blank=True)
    valor_combinado = models.DecimalField(max_digits=10, decimal_places=2)
    PERIODICIDADE_CHOICES = [
        (7, 'A cada 7 dias'),
        (8, 'A cada 8 dias'),
        (15, 'A cada 15 dias'),
        (30, 'A cada 30 dias'),
    ]
    periodicidade_dias = models.IntegerField(
        choices=PERIODICIDADE_CHOICES,
        default=8
    )
    forma_pagamento = models.CharField(max_length=20, choices=PAGAMENTO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

    data_inicio_real = models.DateField(
        null=True, blank=True,
        help_text="Preencha só se o cliente já está com o carro há mais tempo do que a data de retirada cadastrada"
    )

    class Meta:
        ordering = ['-data_retirada']
        verbose_name = 'Locação'
        constraints = [
            models.UniqueConstraint(
                fields=['cliente'],
                condition=models.Q(status='ativa'),
                name='unique_locacao_ativa_por_cliente'
            )
        ]

    def __str__(self):
        return f'{self.cliente} - {self.veiculo} - {self.data_retirada}'

    def clean(self):
        if self.status == 'ativa':
            ja_tem_ativa = Locacao.objects.filter(
                cliente=self.cliente,
                status='ativa'
            ).exclude(pk=self.pk).exists()

            if ja_tem_ativa:
                raise ValidationError(
                    f'O cliente {self.cliente} já possui uma locação ativa. '
                    'Finalize ou cancele a locação atual antes de cadastrar uma nova.'
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Pagamento(models.Model):
    SITUACAO_CHOICES = [
        ('pago', 'Pago'),
        ('pendente', 'Pendente'),
        ('atrasado', 'Atrasado'),
    ]
    FORMA_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('pix', 'PIX'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('transferencia', 'Transferência'),
    ]
    locacao = models.ForeignKey(Locacao, on_delete=models.CASCADE, related_name='pagamentos')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_CHOICES)
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default='pendente')
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

class Despesa(models.Model):
    TIPO_CHOICES = [
        ('manutencao', 'Manutenção'),
        ('oleo', 'Troca de Óleo'),
        ('pneu', 'Pneus'),
        ('lavagem', 'Lavagem'),
        ('combustivel', 'Combustível'),
        ('seguro', 'Seguro'),
        ('ipva', 'IPVA'),
        ('licenciamento', 'Licenciamento'),
        ('multa', 'Multa'),
        ('guincho', 'Guincho'),
        ('pecas', 'Peças'),
        ('acessorios', 'Acessórios'),
        ('outros', 'Outros'),
    ]

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name='despesas'
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES
    )

    descricao = models.TextField(blank=True)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    data = models.DateField()

    observacoes = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'

    def __str__(self):
        return (
            f'{self.veiculo} - '
            f'{self.get_tipo_display()} - '
            f'R$ {self.valor:.2f}'
        )
    