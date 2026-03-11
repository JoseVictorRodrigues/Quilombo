"""
Utilitários para processamento de conteúdo de posts.
Inclui parser de URLs do YouTube e conversão para embed.
"""
import re
from urllib.parse import urlparse, parse_qs

# Padrões de URL do YouTube suportados
_YOUTUBE_PATTERNS = [
    re.compile(r'(?:https?://)?(?:www\.)?youtube\.com/watch\?.*?v=([a-zA-Z0-9_-]{11})'),
    re.compile(r'(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})'),
    re.compile(r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})'),
    re.compile(r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})'),
    re.compile(r'(?:https?://)?(?:www\.)?youtube-nocookie\.com/embed/([a-zA-Z0-9_-]{11})'),
]

_IFRAME_TEMPLATE = (
    '<div class="video-embed-responsive">'
    '<iframe width="100%" height="400" '
    'src="https://www.youtube.com/embed/{video_id}" '
    'title="YouTube video player" frameborder="0" '
    'allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
    'gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>'
    '</div>'
)

# Domínios de vídeo permitidos em iframes
DOMINIOS_VIDEO_PERMITIDOS = {
    'www.youtube.com',
    'youtube.com',
    'www.youtube-nocookie.com',
    'player.vimeo.com',
}


def extrair_youtube_id(url):
    """Extrai o ID do vídeo de qualquer formato de URL do YouTube."""
    if not url:
        return None
    url = url.strip()
    for pattern in _YOUTUBE_PATTERNS:
        match = pattern.search(url)
        if match:
            return match.group(1)
    return None


def youtube_embed_url(url):
    """Converte qualquer URL do YouTube para URL de embed."""
    video_id = extrair_youtube_id(url)
    if not video_id:
        return ''
    return f'https://www.youtube.com/embed/{video_id}'


def processar_youtube_no_conteudo(html_content):
    """
    Processa o conteúdo HTML de um post, convertendo links do YouTube
    (dentro de tags <a>) em iframes de embed responsivos.
    """
    if not html_content:
        return html_content

    # Converter <a> tags apontando para YouTube em iframes
    a_tag_pattern = re.compile(
        r'<a\s[^>]*href=["\']'
        r'(https?://(?:www\.)?(?:youtube\.com/watch\?[^"\']*v=|youtu\.be/|youtube\.com/shorts/)'
        r'([a-zA-Z0-9_-]{11})[^"\']*)["\'][^>]*>.*?</a>',
        re.IGNORECASE | re.DOTALL
    )

    def _substituir_por_embed(match):
        video_id = match.group(2)
        return _IFRAME_TEMPLATE.format(video_id=video_id)

    result = a_tag_pattern.sub(_substituir_por_embed, html_content)

    # Converter URLs soltas (texto puro entre tags) em iframes
    url_solta_pattern = re.compile(
        r'(?<=<p>)\s*'
        r'(https?://(?:www\.)?(?:youtube\.com/watch\?[^<\s]*v=|youtu\.be/|youtube\.com/shorts/)'
        r'([a-zA-Z0-9_-]{11})[^<\s]*)'
        r'\s*(?=</p>)',
        re.IGNORECASE
    )

    result = url_solta_pattern.sub(
        lambda m: _IFRAME_TEMPLATE.format(video_id=m.group(2)),
        result
    )

    return result


def validar_iframes(html_content):
    """
    Valida que todos os iframes no conteúdo apontam para domínios permitidos.
    Substitui iframes com src inválido por mensagem de aviso.
    """
    if not html_content:
        return html_content

    def _verificar_iframe(match):
        tag = match.group(0)
        src_match = re.search(r'src=["\']([^"\']+)["\']', tag)
        if not src_match:
            return '<p><em>Vídeo não disponível para reprodução no site.</em></p>'
        src = src_match.group(1)
        parsed = urlparse(src)
        if parsed.scheme == 'https' and parsed.hostname in DOMINIOS_VIDEO_PERMITIDOS:
            return tag
        return '<p><em>Vídeo não disponível para reprodução no site.</em></p>'

    return re.sub(
        r'<iframe[^>]*>.*?</iframe>',
        _verificar_iframe,
        html_content,
        flags=re.DOTALL | re.IGNORECASE
    )
