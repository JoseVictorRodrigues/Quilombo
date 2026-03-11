# Quilombo Araucária 🌿

Site institucional e comunitário do projeto **Quilombo Araucária** — comunidade, cultura e natureza.

## Tecnologias

- **Backend:** Python + Django 5.2
- **Frontend:** HTML5, CSS3, JavaScript
- **Ícones:** Lucide Icons
- **Mapa:** Leaflet.js
- **Calendário:** Calendário mensal customizado em JS
- **Banco de dados:** SQLite (dev) / PostgreSQL (prod)

## Funcionalidades

- Página inicial com hero, posts recentes, agenda, mapa e seção de convite
- Página Sobre Nós com história, propósito e valores
- Sistema de Posts gerenciável pelo admin
- Agenda de eventos com calendário mensal interativo
- Mapa interativo com pontos de interesse (Leaflet.js)
- Formulário de contato com proteção anti-spam (honeypot)
- Painel administrativo Django personalizado
- Tema claro/escuro
- Alto contraste
- Aumento/diminuição de fonte
- Responsivo (celular, tablet, desktop)
- Animações suaves ao rolar

## Como Rodar

### 1. Criar ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Executar migrações

```bash
python manage.py migrate
```

### 4. Criar superusuário

```bash
python manage.py createsuperuser
```

### 5. Rodar servidor local

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

### 6. Painel administrativo

Acesse: http://127.0.0.1:8000/admin/

## Verificação de Segurança

```bash
python manage.py check --deploy
```

## Rodar Testes

```bash
python manage.py test apps
```

## Estrutura do Projeto

```
quilombo_site/
├── manage.py
├── requirements.txt
├── quilombo_site/         # Configuração Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── core/              # Páginas principais, contato, mapa
│   ├── posts/             # Sistema de posts/blog
│   └── eventos/           # Agenda e eventos
├── templates/             # Templates HTML
│   ├── base.html
│   ├── core/
│   ├── posts/
│   └── eventos/
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
└── logs/
```

## Segurança

- Proteção CSRF ativa
- Honeypot anti-spam no formulário
- Validação e sanitização de formulários
- Headers de segurança HTTP
- HTTPS em produção (HSTS, SSL redirect)
- Hash seguro de senhas (PBKDF2)
- Proteção contra XSS (auto-escaping do Django)
- Proteção contra SQL Injection (ORM do Django)
- Validação de uploads de imagem
- Limite de tamanho de upload (5MB)
- Logs de segurança
- SECRET_KEY via variável de ambiente

## Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```
SECRET_KEY=sua-chave-secreta
DEBUG=False
ALLOWED_HOSTS=seudominio.com
```

## Licença

Projeto comunitário do Quilombo Araucária.
