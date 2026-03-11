import logging
import os
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.cache import cache
from django.http import JsonResponse
from django.conf import settings
import bleach
from apps.posts.models import Post, MediaPost
from apps.posts.utils import processar_youtube_no_conteudo, validar_iframes
from apps.core.models import ConfiguracaoSite
from .forms import PostForm, ConfiguracaoSiteForm

logger = logging.getLogger('django.security')

# Tags e atributos HTML permitidos no conteúdo do editor
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 's', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'a', 'img', 'blockquote', 'pre', 'code', 'hr', 'span',
    'div', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'figure', 'figcaption',
    'iframe', 'video', 'source', 'sub', 'sup',
]
ALLOWED_ATTRS = {
    '*': ['class', 'style', 'id'],
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'width', 'height', 'loading'],
    'iframe': ['src', 'width', 'height', 'frameborder', 'allow', 'allowfullscreen', 'title', 'loading'],
    'video': ['src', 'controls', 'width', 'height'],
    'source': ['src', 'type'],
    'td': ['colspan', 'rowspan'],
    'th': ['colspan', 'rowspan'],
}


def sanitize_html(html_content):
    """Sanitiza HTML do editor para evitar XSS."""
    # Converter links do YouTube em iframes antes de sanitizar
    html_content = processar_youtube_no_conteudo(html_content)
    cleaned = bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True,
    )
    # Validar que iframes só apontam para domínios permitidos
    cleaned = validar_iframes(cleaned)
    return cleaned

# Limite de tentativas de login por IP antes de bloquear temporariamente
_LOGIN_MAX_ATTEMPTS = 5
_LOGIN_LOCKOUT_SECONDS = 300  # 5 minutos


def equipe_login(request):
    if request.user.is_authenticated:
        return redirect('equipe_painel')

    if request.method == 'POST':
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
        ip = ip.split(',')[0].strip()  # Apenas o IP mais à esquerda (cliente real)
        cache_key = f'login_attempts_{ip}'
        attempts = cache.get(cache_key, 0)

        # Bloquear IP com muitas tentativas falhas
        if attempts >= _LOGIN_MAX_ATTEMPTS:
            logger.warning(f'Login bloqueado por excesso de tentativas: IP={ip}')
            messages.error(request, 'Muitas tentativas. Aguarde 5 minutos e tente novamente.')
            return render(request, 'usuarios/login.html')

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login bem-sucedido: limpar contador de tentativas
            cache.delete(cache_key)
            login(request, user)
            logger.info(f'Login realizado: user={username}, IP={ip}')
            return redirect('equipe_painel')
        else:
            # Incrementar contador de falhas
            cache.set(cache_key, attempts + 1, _LOGIN_LOCKOUT_SECONDS)
            logger.warning(f'Tentativa de login falha: user={username}, IP={ip}, tentativa={attempts + 1}')
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'usuarios/login.html')


@login_required
@require_POST
def equipe_logout(request):
    logout(request)
    messages.success(request, 'Você saiu da área da equipe.')
    return redirect('home')


@login_required
def equipe_painel(request):
    posts = Post.objects.filter(autor=request.user).order_by('-data_publicacao')
    return render(request, 'usuarios/painel.html', {'posts': posts})


@login_required
def equipe_criar_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.conteudo = sanitize_html(post.conteudo)
            post.save()
            # Processar mídias (imagens e vídeos)
            _salvar_midias(request, post)
            messages.success(request, 'Post criado com sucesso!')
            return redirect('equipe_painel')
    else:
        form = PostForm()
    return render(request, 'usuarios/criar_post.html', {'form': form})


@login_required
def equipe_editar_post(request, pk):
    post = get_object_or_404(Post, pk=pk, autor=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.conteudo = sanitize_html(post.conteudo)
            post.save()
            # Processar mídias extras
            _salvar_midias(request, post)
            messages.success(request, 'Post atualizado com sucesso!')
            return redirect('equipe_painel')
    else:
        form = PostForm(instance=post)
    midias = post.midias.all()
    return render(request, 'usuarios/editar_post.html', {'form': form, 'post': post, 'midias': midias})


def _salvar_midias(request, post):
    """Salva arquivos de mídia enviados com o post."""
    imagens = request.FILES.getlist('galeria_imagens')
    videos = request.FILES.getlist('galeria_videos')
    video_urls = request.POST.getlist('video_externo_url')

    ordem = post.midias.count()
    extensoes_imagem = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    extensoes_video = {'.mp4', '.webm', '.ogg', '.mov'}

    for img in imagens:
        ext = os.path.splitext(img.name)[1].lower()
        if ext in extensoes_imagem and img.size <= 5 * 1024 * 1024:
            MediaPost.objects.create(post=post, arquivo=img, tipo='imagem', ordem=ordem)
            ordem += 1

    for vid in videos:
        ext = os.path.splitext(vid.name)[1].lower()
        if ext in extensoes_video and vid.size <= 100 * 1024 * 1024:
            MediaPost.objects.create(post=post, arquivo=vid, tipo='video', ordem=ordem)
            ordem += 1

    for url in video_urls:
        url = url.strip()
        if url:
            MediaPost.objects.create(post=post, video_url=url, tipo='video', ordem=ordem)
            ordem += 1


@login_required
@require_POST
def equipe_excluir_midia(request, pk):
    midia = get_object_or_404(MediaPost, pk=pk, post__autor=request.user)
    midia.delete()
    return JsonResponse({'ok': True})


@login_required
@require_POST
def equipe_upload_imagem(request):
    """Endpoint para upload de imagem via TinyMCE."""
    arquivo = request.FILES.get('file')
    if not arquivo:
        return JsonResponse({'error': 'Nenhum arquivo enviado.'}, status=400)

    ext = os.path.splitext(arquivo.name)[1].lower()
    extensoes_permitidas = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    if ext not in extensoes_permitidas:
        return JsonResponse({'error': 'Formato não permitido.'}, status=400)
    if arquivo.size > 5 * 1024 * 1024:
        return JsonResponse({'error': 'Imagem muito grande. Máximo: 5MB.'}, status=400)

    # Gerar nome seguro
    nome_seguro = f'{uuid.uuid4().hex}{ext}'
    caminho_relativo = os.path.join('posts', 'editor', nome_seguro)
    caminho_completo = os.path.join(settings.MEDIA_ROOT, caminho_relativo)

    os.makedirs(os.path.dirname(caminho_completo), exist_ok=True)
    with open(caminho_completo, 'wb') as f:
        for chunk in arquivo.chunks():
            f.write(chunk)

    url = f'{settings.MEDIA_URL}{caminho_relativo}'
    return JsonResponse({'location': url})


@login_required
@require_POST
def equipe_excluir_post(request, pk):
    post = get_object_or_404(Post, pk=pk, autor=request.user)
    post.delete()
    messages.success(request, 'Post excluído com sucesso!')
    return redirect('equipe_painel')


@login_required
def equipe_configuracoes(request):
    config = ConfiguracaoSite.get()
    if request.method == 'POST':
        form = ConfiguracaoSiteForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configurações atualizadas com sucesso!')
            return redirect('equipe_configuracoes')
    else:
        form = ConfiguracaoSiteForm(instance=config)
    return render(request, 'usuarios/configuracoes.html', {'form': form, 'config': config})
