# Documentação Técnica — Quilombo Araucária

> Guia completo para programadores que desejam entender, manter ou estender o site.

---

## 1. Visão Geral da Arquitetura

O site é uma aplicação **Django 5.2** com arquitetura MVC (Model-View-Template), usando:

- **Backend**: Django (Python)
- **Frontend**: HTML5 + CSS3 + JavaScript vanilla (sem frameworks JS)
- **Banco de dados**: SQLite (dev) / PostgreSQL via `dj-database-url` (produção)
- **Servidor**: Gunicorn (produção) / Django dev server (local)
- **Arquivos estáticos**: WhiteNoise
- **Deploy**: Vercel (configurado)

---

## 2. Estrutura de Pastas

```
quilombo_site/
├── manage.py                    # CLI Django
├── db.sqlite3                   # Banco SQLite local
├── requirements.txt             # Dependências Python
├── vercel.json                  # Configuração deploy Vercel
├── build_files.sh               # Script de build para Vercel
├── Procfile                     # Configuração Heroku/Railway
│
├── quilombo_site/               # Projeto Django (settings)
│   ├── settings.py              # Configurações centrais
│   ├── urls.py                  # Rotas principais
│   ├── wsgi.py                  # Entry point WSGI
│   └── asgi.py                  # Entry point ASGI
│
├── apps/                        # Aplicações Django
│   ├── core/                    # App principal (home, contato, configurações)
│   │   ├── models.py            # ConfiguracaoSite, Contato, PontoMapa
│   │   ├── views.py             # home, sobre, contato, API eventos/menu, robots.txt
│   │   ├── forms.py             # ContatoForm (com honeypot anti-spam)
│   │   ├── context_processors.py # Injeta site_config em todos os templates
│   │   ├── admin.py             # Registro dos modelos no Django Admin
│   │   └── urls.py              # Rotas da app core
│   │
│   ├── posts/                   # App de blog/posts
│   │   ├── models.py            # Post, MediaPost
│   │   ├── views.py             # Lista e detalhe de posts
│   │   ├── utils.py             # Parser YouTube, validação de iframes
│   │   ├── templatetags/        # Filtros de template
│   │   │   └── youtube_tags.py  # Filtro |youtube_embed
│   │   └── urls.py              # Rotas de posts
│   │
│   ├── eventos/                 # App de eventos/agenda
│   │   ├── models.py            # Evento (com google_event_id)
│   │   ├── views.py             # Agenda, detalhe de evento
│   │   ├── sync_calendar.py     # Sincronização com Google Calendar ICS
│   │   ├── management/commands/ # Comando sync_calendar
│   │   └── urls.py              # Rotas de eventos
│   │
│   └── usuarios/                # App de autenticação e painel da equipe
│       ├── models.py            # (vazio — usa User do Django)
│       ├── views.py             # Login, logout, CRUD posts, configurações
│       ├── forms.py             # PostForm, MediaPostForm, ConfiguracaoSiteForm
│       └── urls.py              # Rotas da equipe
│
├── templates/                   # Templates HTML (Jinja-like)
│   ├── base.html                # Template base (header, footer, JS/CSS)
│   ├── 404.html / 500.html      # Páginas de erro
│   ├── core/                    # Templates da app core
│   ├── posts/                   # Templates de posts
│   ├── eventos/                 # Templates de eventos
│   └── usuarios/                # Templates do painel da equipe
│
├── static/                      # Arquivos estáticos
│   ├── css/style.css            # Folha de estilos principal
│   ├── js/main.js               # JavaScript principal
│   └── images/                  # Imagens estáticas
│
├── media/                       # Uploads de usuários
│   └── site/                    # Logo, imagem de fundo
│
└── logs/                        # Logs da aplicação
```

---

## 3. Modelos do Banco de Dados

### ConfiguracaoSite (Singleton)
Armazena todas as configurações visuais e de integração do site. Apenas uma instância (pk=1).

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `logo` | ImageField | Logo circular do site |
| `tamanho_logo` | PositiveIntegerField | Tamanho em px (padrão: 120) |
| `imagem_fundo` | ImageField | Imagem de fundo com overlay |
| `cor_fundo` | CharField | Cor hex de fundo (padrão: #f5f1eb) |
| `link_instagram` | URLField | URL do Instagram |
| `link_telegram` | URLField | URL do Telegram |
| `link_youtube` | URLField | URL do YouTube |
| `google_calendar_link` | URLField | URL pública do Google Calendar |
| `email_contato` | EmailField | E-mail de contato |
| `animacao_folhas_ativa` | BooleanField | Liga/desliga animação de folhas globalmente |
| `menu_posicao` | CharField | `'topo'` (horizontal) ou `'lateral'` (vertical direita) |

Acesso: `ConfiguracaoSite.get()` — cria ou retorna a instância singleton.

### Post
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `titulo` | CharField(200) | Título do post |
| `slug` | SlugField | URL amigável (auto-gerado) |
| `resumo` | TextField | Resumo curto |
| `conteudo` | TextField | Conteúdo HTML (sanitizado com bleach) |
| `imagem_capa` | ImageField | Imagem da capa |
| `video_url` | URLField | URL de vídeo do YouTube (opcional) |
| `autor` | ForeignKey(User) | Autor do post |
| `publicado` | BooleanField | Se está visível ao público |
| `data_publicacao` | DateTimeField | Data de publicação |

### MediaPost
Galeria de mídias associadas a um post (imagens e vídeos).

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `post` | ForeignKey(Post) | Post associado |
| `arquivo` | FileField | Arquivo de mídia |
| `video_url` | URLField | URL de vídeo externo |
| `tipo` | CharField | `'imagem'` ou `'video'` |
| `ordem` | PositiveIntegerField | Ordem de exibição |

### Evento
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `titulo` | CharField(200) | Nome do evento |
| `descricao` | TextField | Descrição (opcional) |
| `data` | DateField | Data do evento |
| `data_fim` | DateField | Data de término (opcional) |
| `hora` | TimeField | Horário (opcional) |
| `local` | CharField | Local (opcional) |
| `google_event_id` | CharField | ID do evento no Google Calendar |

### Contato
Mensagens recebidas pelo formulário de contato.

### PontoMapa
Pontos exibidos no mapa Leaflet da página inicial.

---

## 4. Sistema de Upload e Mídia

- **Imagens**: Validadas por extensão (`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`) e tamanho (máx. 5MB)
- **Vídeos**: Extensões permitidas: `.mp4`, `.webm`, `.ogg`, `.mov` (máx. 100MB)
- **Upload via TinyMCE**: Endpoint `equipe/upload-imagem/` gera nomes seguros com UUID
- **Armazenamento**: Pasta `media/` localmente; recomendado usar CDN em produção
- **Sanitização HTML**: Todo conteúdo do editor passa por `bleach.clean()` com lista restrita de tags/atributos
- **Iframes**: Apenas domínios permitidos (`youtube.com`, `youtube-nocookie.com`, `player.vimeo.com`)

---

## 5. Integração com Google Calendar

### Embed (Frontend)
A página de agenda (`/agenda/`) incorpora o Google Calendar público via iframe:
```
https://calendar.google.com/calendar/embed?src=EMAIL&ctz=America/Sao_Paulo
```

### Sincronização ICS (Backend)
- Serviço: `apps/eventos/sync_calendar.py`
- Comando: `python manage.py sync_calendar`
- Busca o feed ICS público e cria/atualiza eventos no banco
- Requisitos: Calendário deve ser público no Google Calendar
- Cache: Agenda view sincroniza automaticamente a cada 30 minutos

---

## 6. Componentes de Frontend

### Menu de Navegação
- **Posição**: Configurável pelo painel da equipe (horizontal topo / vertical lateral direita)
- **Mobile**: Sempre no topo com botão hamburger
- **CSS**: Classes `.main-header`, `.menu-lateral`, `body[data-menu="lateral"]`
- **Visual**: Textura de madeira araucária com gradientes

### Animação de Folhas
- Folhas emoji (🍂🍃🍁) caem pela tela
- **Controle global**: `ConfiguracaoSite.animacao_folhas_ativa` (painel da equipe)
- **Controle individual**: Botão de acessibilidade com persistência via `localStorage`
- Máximo 12 folhas simultâneas, intervalo de 2.5s

### Painel de Acessibilidade
Localizado no canto superior direito, com 5 botões:
1. **A+** — Aumentar fonte (até 1.5x)
2. **A-** — Diminuir fonte (até 0.8x)
3. **Contraste** — Alternar alto contraste
4. **Tema** — Alternar claro/escuro
5. **Folhas** — Pausar/retomar animação de folhas

Todas as preferências são persistidas via `localStorage`.

### Tema Escuro/Claro
- Atributo `data-theme="light|dark"` na tag `<html>`
- CSS usa custom properties (variáveis CSS) para cores
- Alto contraste via `data-contrast="high"`

### Ícones
- **Font Awesome 6**: Ícones de acessibilidade e redes sociais
- **Lucide Icons**: Ícones de navegação e interface
- **Emoji**: Folhas na animação

---

## 7. Segurança

### URL do Admin
- Painel administrativo movido para `/painel-equipe/`
- `/admin/` e `/admin/<qualquer-coisa>/` retornam **404**
- `robots.txt` bloqueia indexação de `/painel-equipe/` e `/equipe/`

### Autenticação
- Login com rate limiting: 5 tentativas falhas = bloqueio de 5 minutos por IP
- Sessão Django padrão com cookies seguros (em produção)
- Logout via POST (proteção CSRF)

### Sanitização
- Todo HTML do editor é sanitizado com `bleach`
- Iframes validados contra lista de domínios permitidos
- Uploads validados por extensão e tamanho
- Formulário de contato com honeypot anti-spam

### Headers de Segurança (Produção)
- HSTS ativado (`SECURE_HSTS_SECONDS`)
- Cookies seguros (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)
- Redirecionamento HTTPS (`SECURE_SSL_REDIRECT`)
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`

---

## 8. Configurações CSS/JS

### Variáveis CSS Principais
O site usa custom properties definidas em `:root` e `[data-theme="dark"]`:
- `--color-primary`, `--color-primary-dark`, `--color-primary-light`
- `--color-bg`, `--color-bg-card`, `--color-text`
- `--shadow-card`, `--shadow-md`
- `--radius-sm`, `--radius-md`, `--radius-full`
- `--transition-fast`, `--transition-normal`
- `--font-scale` (controlada pelo JS de acessibilidade)

### Responsividade
- **1024px**: Layout de grid se adapta (agenda, footer)
- **768px**: Menu mobile ativado, sidebar reverte para topo
- **480px**: Ajustes de font-size e padding

---

## 9. Fluxo do Código

```
Usuário acessa URL
    ↓
Django URL Dispatcher (urls.py)
    ↓
View function (views.py)
    ↓
Consulta ao banco (models.py)
    ↓
Renderiza template (templates/*.html)
    ↓
Template base.html inclui CSS/JS
    ↓
Browser renderiza HTML
    ↓
main.js inicializa:
  - Lucide icons
  - Acessibilidade (tema, fonte, contraste, folhas)
  - Navbar (scroll, mobile toggle)
  - Scroll animations (IntersectionObserver)
  - Falling leaves (se ativo)
  - Menu lateral (se configurado)
    ↓
Interações do usuário
  - Cliques → navegação / formulários
  - Acessibilidade → localStorage + CSS
  - Admin → CRUD via Django views
```

---

## 10. Guia para Programadores

### Como adicionar um novo post
1. Fazer login em `/equipe/login/`
2. Clicar em "Novo Post" no painel
3. Preencher título, resumo, conteúdo (editor TinyMCE)
4. Opcionalmente: adicionar imagem de capa, URL de vídeo YouTube, galeria
5. Marcar como "Publicado" e salvar

### Como adicionar novos usuários staff
1. Acessar `/painel-equipe/` (Django Admin)
2. Ir em "Usuários" > "Adicionar usuário"
3. Criar com senha e marcar "É da equipe" (is_staff)
4. Salvar — o novo usuário pode acessar `/equipe/login/`

### Como alterar tema, animação e layout
1. Fazer login em `/equipe/login/`
2. Ir em "Configurações"
3. Alterar:
   - **Logo**: Upload de imagem (recomendado 200x200px)
   - **Imagem de fundo**: Upload com overlay automático
   - **Cor de fundo**: Seletor de cor (se não houver imagem)
   - **Animação de folhas**: Checkbox para ativar/desativar globalmente
   - **Posição do menu**: Horizontal (topo) ou Vertical (lateral direita)

### Como configurar Google Calendar embed
1. No Google Calendar, tornar o calendário **público**:
   - Configurações > Configurações do calendário > Disponibilizar para o público
2. Copiar o endereço de e-mail do calendário
3. O embed na página `/agenda/` já usa esse endereço

### Como estender funcionalidades
1. **Nova app**: `python manage.py startapp nome_app` dentro de `apps/`
2. **Registrar** em `settings.py` > `INSTALLED_APPS`
3. **Criar modelos**, **views**, **templates** e **URLs**
4. **Incluir URLs** no `quilombo_site/urls.py`
5. **Criar migrations**: `python manage.py makemigrations nome_app`
6. **Aplicar**: `python manage.py migrate`

### Comandos úteis
```bash
# Iniciar servidor de desenvolvimento
python manage.py runserver

# Criar migration após alterar models
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Sincronizar eventos do Google Calendar
python manage.py sync_calendar

# Verificar configuração
python manage.py check

# Verificar segurança para produção
python manage.py check --deploy

# Coletar arquivos estáticos
python manage.py collectstatic
```

### Variáveis de ambiente (produção)
```
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=seudominio.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

---

## 11. Dependências (requirements.txt)

| Pacote | Uso |
|--------|-----|
| Django | Framework web |
| Pillow | Processamento de imagens |
| gunicorn | Servidor WSGI (produção) |
| whitenoise | Servir estáticos em produção |
| bleach | Sanitização de HTML |
| icalendar | Parser de arquivos ICS |
| requests | Requisições HTTP (sync calendar) |
| dj-database-url | Parse de DATABASE_URL |
| psycopg2-binary | Driver PostgreSQL |

---

## 12. API Endpoints

| Endpoint | Método | Descrição | Cache |
|----------|--------|-----------|-------|
| `/api/eventos/` | GET | Lista de eventos em JSON | 5 min |
| `/api/configuracoes-menu/` | GET | Posição do menu e status da animação | 5 min |
| `/robots.txt` | GET | Arquivo robots.txt dinâmico | — |
| `/favicon.ico` | GET | Redireciona para logo configurada | — |
