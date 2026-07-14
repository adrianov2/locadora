from django import forms
from .models import Cliente, Veiculo, Locacao, Pagamento, Manutencao,Despesa


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ['ativo', 'criado_em']
        widgets = {
            'foto_documento': forms.FileInput(attrs={'accept': 'image/*'}),
            'endereco': forms.TextInput(),
        }


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        exclude = ['status', 'ativo', 'criado_em']


class LocacaoForm(forms.ModelForm):
    class Meta:
        model = Locacao
        exclude = ['status', 'criado_em', 'criado_por', 'data_devolucao_real', 'hora_devolucao_real']
        widgets = {
        'data_retirada': forms.DateInput(format='%Y-m-d', attrs={'type': 'date'}),
        'hora_retirada': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        'data_prevista_devolucao': forms.DateInput(format='%Y-m-d', attrs={'type': 'date'}),
        'hora_prevista_devolucao': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        'observacoes': forms.Textarea(attrs={'rows': 3}),
    }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            veiculos_qs = Veiculo.objects.filter(status='disponivel', ativo=True)
            if self.instance and self.instance.pk:
                # Edição: inclui o veículo atual da locação, mesmo que esteja "alugado"
                veiculos_qs = veiculos_qs | Veiculo.objects.filter(pk=self.instance.veiculo_id)
            self.fields['veiculo'].queryset = veiculos_qs.distinct()
            self.fields['cliente'].queryset = Cliente.objects.filter(ativo=True)

class LocacaoFinalizarForm(forms.ModelForm):
    class Meta:
        model = Locacao
        fields = ['data_devolucao_real', 'hora_devolucao_real', 'observacoes']
        widgets = {
            'data_devolucao_real': forms.DateInput(attrs={'type': 'date'}),
            'hora_devolucao_real': forms.TimeInput(attrs={'type': 'time'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }


class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        exclude = ['situacao', 'criado_em', 'data_pagamento']
        widgets = {
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }


class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        exclude = ['criado_em']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'proxima_revisao': forms.DateInput(attrs={'type': 'date'}),
            'proxima_troca_oleo': forms.DateInput(attrs={'type': 'date'}),
            'troca_pneus': forms.DateInput(attrs={'type': 'date'}),
            'vencimento_seguro': forms.DateInput(attrs={'type': 'date'}),
            'vencimento_licenciamento': forms.DateInput(attrs={'type': 'date'}),
            'vencimento_ipva': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        exclude = ['criado_em']

        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

def add_bootstrap_classes(form):
    for field_name, field in form.fields.items():
        widget = field.widget
        css = widget.attrs.get('class', '')
        if hasattr(widget, 'choices'):
            widget.attrs['class'] = (css + ' form-select').strip()
        else:
            widget.attrs['class'] = (css + ' form-control').strip()
    return form


# Monkey-patch all forms to add bootstrap classes
_original_init_methods = {}

for form_cls in [ClienteForm, VeiculoForm, LocacaoForm, LocacaoFinalizarForm, PagamentoForm, ManutencaoForm,DespesaForm,]:
    original_init = form_cls.__init__

    def make_init(orig):
        def new_init(self, *args, **kwargs):
            orig(self, *args, **kwargs)
            add_bootstrap_classes(self)
        return new_init

    form_cls.__init__ = make_init(original_init)
