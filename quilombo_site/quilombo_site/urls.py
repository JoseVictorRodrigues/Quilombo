"""
URL Configuration para o projeto Quilombo Araucária.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import Http404
from django.conf import settings
from django.conf.urls.static import static

# Personalização do Django Admin
admin.site.site_header = 'Quilombo Araucária - Administração'
admin.site.site_title = 'Quilombo Araucária Admin'
admin.site.index_title = 'Painel de Gestão'


def _admin_blocked(request, *args, **kwargs):
    """Bloqueia qualquer acesso à URL /admin/ com 404."""
    raise Http404


urlpatterns = [
    # Painel na URL personalizada (segurança por obscuridade)
    path('painel-equipe/', admin.site.urls),
    # Bloquear /admin/ — retorna 404 sem revelar existência do painel
    path('admin/', _admin_blocked),
    path('admin/<path:remaining>/', _admin_blocked),
    path('posts/', include('apps.posts.urls')),
    path('agenda/', include('apps.eventos.urls')),
    path('equipe/', include('apps.usuarios.urls')),
    path('', include('apps.core.urls')),
]

# Arquivos de mídia servidos pelo Django apenas em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handlers de erro personalizados
handler404 = 'apps.core.views.erro_404'
handler500 = 'apps.core.views.erro_500'
