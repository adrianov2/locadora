# 🚗 LL Locadora — Sistema de Gestão para Locadora de Veículos

Sistema completo para gerenciar clientes, veículos, locações, pagamentos e manutenções.
Desenvolvido em **Django + SQLite** (desenvolvimento) e **PostgreSQL** (produção).
Compatível com iPad como PWA instalável.

---

## ⚡ Início Rápido

### 1. Criar ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar banco de dados
Por padrão usa SQLite (sem configuração extra).  
Para PostgreSQL, edite `core/settings.py` e configure `DATABASES`.

### 4. Executar migrações
```bash
python manage.py migrate
```

### 5. Criar usuário administrador
```bash
python manage.py createsuperuser
```
Ou edite e rode o script de dados de exemplo.

### 6. Iniciar servidor
```bash
python manage.py runserver
```
Acesse: **http://localhost:8000**

Login padrão (se usou dados de exemplo): `admin` / `admin123`

---

## 🐳 Deploy com Docker

```bash
docker-compose up -d
```
Acessa em: http://seu-ip:8000

---

## 📱 Instalar como app no iPad (PWA)

1. Acesse o sistema pelo **Safari** no iPad
2. Toque no ícone de **Compartilhar** (quadrado com seta)
3. Selecione **"Adicionar à Tela de Início"**
4. Toque em **"Adicionar"**

O app aparecerá na tela inicial com ícone próprio, abrindo em tela cheia.

> ⚠️ **HTTPS é obrigatório** para instalar como PWA em produção.  
> Para desenvolvimento local, o Safari no iPad precisará acessar via IP da rede local.

---

## 🔒 Produção com HTTPS (Nginx + Gunicorn)

```nginx
server {
    listen 443 ssl;
    server_name seudominio.com;
    ssl_certificate /etc/letsencrypt/live/seudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seudominio.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ { alias /app/staticfiles/; }
    location /media/  { alias /app/media/; }
}
```

---

## 📁 Estrutura do Projeto

```
locadora/
├── core/           # Configurações Django
├── gestao/         # App principal
│   ├── models.py   # Modelos (Cliente, Veículo, Locação, Pagamento, Manutenção)
│   ├── views.py    # Views e lógica de negócio
│   ├── forms.py    # Formulários
│   └── urls.py     # Rotas
├── templates/      # Templates HTML
├── static/         # CSS, JS, ícones PWA
└── manage.py
```

---

## 🎯 Funcionalidades

| Módulo | Recursos |
|--------|----------|
| 🏠 Dashboard | KPIs, gráficos 6 meses, alertas automáticos |
| 👥 Clientes | CRUD completo, histórico de locações, alerta CNH |
| 🚗 Veículos | CRUD, status em tempo real, histórico |
| 🔑 Locações | Nova locação, finalização, pagamento automático |
| 💰 Pagamentos | Controle de situação, marcação de pago |
| 🔧 Manutenções | Registro, alertas de vencimento (IPVA, seguro, licenciamento) |
| 📊 Financeiro | Fluxo de caixa mensal |
| 📋 Relatórios | PDF e Excel para todos os módulos |
| 📱 PWA | Instalável no iPad via Safari |

---

## 🚨 Alertas Automáticos

O sistema detecta e exibe automaticamente no dashboard:
- 🔴 **Pagamentos atrasados**
- 🟡 **Pagamentos vencem hoje**
- 🔴 **CNH de clientes vencida**
- 🟡 **CNH vencendo em 30 dias**
- 🟡 **Revisão, seguro, IPVA, licenciamento vencendo**

---

Desenvolvido para uso pessoal do proprietário da locadora. 🚗
