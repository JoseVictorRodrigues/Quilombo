from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('api/eventos/', views.eventos_api, name='eventos_api'),
    path('fotos/', views.galeria_fotos, name='galeria_fotos'),
    path('api/configuracoes-menu/', views.api_configuracoes_menu, name='api_configuracoes_menu'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('favicon.ico', views.favicon, name='favicon'),
]
