import logging
from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page
from apps.posts.models import Post
from apps.eventos.models import Evento
from .models import PontoMapa, ConfiguracaoSite, FotoGaleria
from .forms import ContatoForm

logger = logging.getLogger('django.security')


def home(request):
    # select_related evita N+1 queries ao acessar post.autor no template
    posts_recentes = Post.objects.filter(publicado=True).select_related('autor')[:3]
    proximos_eventos = Evento.objects.filter(data__gte=date.today()).order_by('data', 'hora')[:5]
    pontos_mapa = PontoMapa.objects.all()
    return render(request, 'core/home.html', {
        'posts_recentes': posts_recentes,
        'proximos_eventos': proximos_eventos,
        'pontos_mapa': pontos_mapa,
    })


def sobre(request):
    return render(request, 'core/sobre.html')


def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contato.')
            # Log sem expor conteúdo da mensagem (apenas email para rastreio)
            logger.info('Contato recebido de %s', form.cleaned_data['email'])
            return redirect('contato')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ContatoForm()
    return render(request, 'core/contato.html', {'form': form})


@cache_page(60 * 5)  # Cache de 5 minutos para reduzir queries repetidas
def eventos_api(request):
    """API JSON pública para o calendário de eventos do frontend."""
    eventos = Evento.objects.order_by('data', 'hora').values(
        'titulo', 'descricao', 'data', 'hora', 'local'
    )
    eventos_list = [
        {
            'title': e['titulo'],
            'description': e['descricao'] or '',
            'date': e['data'].isoformat(),
            'time': e['hora'].strftime('%H:%M') if e['hora'] else '',
            'location': e['local'] or '',
        }
        for e in eventos
    ]
    return JsonResponse(eventos_list, safe=False)


@cache_page(60 * 5)
def api_configuracoes_menu(request):
    """API JSON com configuração de posição do menu e animação."""
    config = ConfiguracaoSite.get()
    return JsonResponse({
        'posicao': config.menu_posicao,
        'animacao_folhas': config.animacao_folhas_ativa,
    })


def galeria_fotos(request):
    fotos = FotoGaleria.objects.all()
    return render(request, 'core/galeria.html', {'fotos': fotos})


def robots_txt(request):
    """Retorna o arquivo robots.txt para controle de indexação por crawlers."""
    lines = [
        'User-agent: *',
        'Disallow: /painel-equipe/',
        'Disallow: /equipe/',
        'Allow: /',
        '',
        f'Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def favicon(request):
    """Redireciona /favicon.ico para a logo do site configurada, se disponível."""
    from .models import ConfiguracaoSite
    from django.http import HttpResponseRedirect
    config = ConfiguracaoSite.get()
    if config.logo:
        return HttpResponseRedirect(config.logo.url)
    # Fallback: 204 No Content se não houver logo (evita erro 404 em logs)
    return HttpResponse(status=204)


def erro_404(request, exception=None):
    """Página de erro 404 personalizada."""
    return render(request, '404.html', status=404)


def erro_500(request):
    """Página de erro 500 personalizada."""
    return render(request, '500.html', status=500)
