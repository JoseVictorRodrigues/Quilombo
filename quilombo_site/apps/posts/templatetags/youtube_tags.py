from django import template
from apps.posts.utils import youtube_embed_url as _youtube_embed_url

register = template.Library()


@register.filter(name='youtube_embed')
def youtube_embed(url):
    """Converte URL do YouTube para URL de embed. Uso: {{ url|youtube_embed }}"""
    return _youtube_embed_url(url)
