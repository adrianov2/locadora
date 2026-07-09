from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Clientes
    path('clientes/', views.clientes_lista, name='clientes_lista'),
    path('clientes/novo/', views.cliente_form, name='cliente_novo'),
    path('clientes/<int:pk>/', views.cliente_detalhe, name='cliente_detalhe'),
    path('clientes/<int:pk>/editar/', views.cliente_form, name='cliente_editar'),
    path('clientes/<int:pk>/excluir/', views.cliente_excluir, name='cliente_excluir'),

    # Veículos
    path('veiculos/', views.veiculos_lista, name='veiculos_lista'),
    path('veiculos/novo/', views.veiculo_form, name='veiculo_novo'),
    path('veiculos/<int:pk>/', views.veiculo_detalhe, name='veiculo_detalhe'),
    path('veiculos/<int:pk>/editar/', views.veiculo_form, name='veiculo_editar'),
    path('veiculos/<int:pk>/excluir/', views.veiculo_excluir, name='veiculo_excluir'),

    # Locações
    path('locacoes/', views.locacoes_lista, name='locacoes_lista'),
    path('locacoes/nova/', views.locacao_form, name='locacao_nova'),
    path('locacoes/<int:pk>/', views.locacao_detalhe, name='locacao_detalhe'),
    path('locacoes/<int:pk>/editar/', views.locacao_form, name='locacao_editar'),
    path('locacoes/<int:pk>/finalizar/', views.locacao_finalizar, name='locacao_finalizar'),
    path('locacoes/<int:pk>/renovar/', views.locacao_renovar, name='locacao_renovar'),
    path('locacoes/<int:pk>/excluir/', views.locacao_excluir, name='locacao_excluir'),
    path('locacoes/<int:pk>/inicio/', views.locacao_editar_inicio, name='locacao_editar_inicio'),
        
    # Pagamentos
    path('pagamentos/', views.pagamentos_lista, name='pagamentos_lista'),
    path('pagamentos/novo/', views.pagamento_form, name='pagamento_novo'),
    path('pagamentos/<int:pk>/pagar/', views.pagamento_pagar, name='pagamento_pagar'),
    path('pagamentos/<int:pk>/excluir/', views.pagamento_excluir, name='pagamento_excluir'),
    # Manutenções
    path('manutencoes/', views.manutencoes_lista, name='manutencoes_lista'),
    path('manutencoes/nova/', views.manutencao_form, name='manutencao_nova'),
    path('manutencoes/<int:pk>/editar/', views.manutencao_form, name='manutencao_editar'),

    # Relatórios
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/pdf/<str:tipo>/', views.relatorio_pdf, name='relatorio_pdf'),
    path('relatorios/excel/<str:tipo>/', views.relatorio_excel, name='relatorio_excel'),

    # Financeiro
    path('financeiro/', views.financeiro, name='financeiro'),

  # Despesas
    path('despesas/', views.despesas_lista, name='despesas_lista'),
    path('despesas/nova/', views.despesa_form, name='despesa_nova'),
    path('despesas/<int:pk>/editar/', views.despesa_form, name='despesa_editar'),
    path('despesas/<int:pk>/excluir/', views.despesa_excluir, name='despesa_excluir'),
    
    # PWA
    path('manifest.json', views.manifest_json, name='manifest_json'),
    path('sw.js', views.service_worker, name='service_worker'),
]
