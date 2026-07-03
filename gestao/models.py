from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



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
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    endereco = models.CharField(max_length=300, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    cep = models.CharField(max_length=9, blank=True)
    cnh = models.CharField(max_length=20, blank=True)
    categoria_cnh = models.CharField(max_length=5, blank=True)
    validade_cnh = models.DateField(null=True, blank=True)
    foto_cnh = models.ImageField(upload_to='cnh/', blank=True, null=True)
    observacoes = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Cliente'

    def __str__(self):
        return self.nome

    @property
    def cnh_vencida(self):
        if self.validade_cnh:
            return self.validade_cnh < timezone.now().date()
        return False

    @property
    def cnh_vencendo(self):
        if self.validade_cnh:
            dias = (self.validade_cnh - timezone.now().date()).days
            return 0 <= dias <= 30
        return False



class Veiculo(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('alugado', 'Alugado'),
        ('manutencao', 'Em Manutenção'),
    ]
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    placa = models.CharField(max_length=10, unique=True)
    cor = models.CharField(max_length=50)
    renavam = models.CharField(max_length=20, blank=True)
    chassi = models.CharField(max_length=17, blank=True)
    quilometragem = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    foto = models.ImageField(upload_to='veiculos/', blank=True, null=True)
    observacoes = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['marca', 'modelo']
        verbose_name = 'Veículo'

    def __str__(self):
        return f'{self.marca} {self.modelo} - {self.placa}'


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
    periodicidade_dias = models.IntegerField(
        default=8,
        help_text='A cada quantos dias o pagamento se renova (padrão: 8 dias)'
    )
    forma_pagamento = models.CharField(max_length=20, choices=PAGAMENTO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-data_retirada']
        verbose_name = 'Locação'

    def __str__(self):
        return f'{self.cliente} - {self.veiculo} - {self.data_retirada}'

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
    

    
    class Meta:
        ordering = ['-data']
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'

    def __str__(self):
        return f'{self.locacao} - R$ {self.valor} - {self.situacao}'

    def atualizar_situacao(self):
        hoje = timezone.now().date()
        if self.situacao != 'pago':
            if self.data_vencimento < hoje:
                self.situacao = 'atrasado'
                self.save()

