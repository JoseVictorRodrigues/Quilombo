from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.equipe_login, name='equipe_login'),
    path('logout/', views.equipe_logout, name='equipe_logout'),
    path('', views.equipe_painel, name='equipe_painel'),
    path('novo-post/', views.equipe_criar_post, name='equipe_criar_post'),
    path('editar-post/<int:pk>/', views.equipe_editar_post, name='equipe_editar_post'),
    path('excluir-post/<int:pk>/', views.equipe_excluir_post, name='equipe_excluir_post'),
    path('excluir-midia/<int:pk>/', views.equipe_excluir_midia, name='equipe_excluir_midia'),
    path('upload-imagem/', views.equipe_upload_imagem, name='equipe_upload_imagem'),
    path('configuracoes/', views.equipe_configuracoes, name='equipe_configuracoes'),
    path('novo-evento/', views.equipe_criar_evento, name='equipe_criar_evento'),
    path('editar-evento/<int:pk>/', views.equipe_editar_evento, name='equipe_editar_evento'),
    path('excluir-evento/<int:pk>/', views.equipe_excluir_evento, name='equipe_excluir_evento'),
    path('fotos/', views.equipe_galeria, name='equipe_galeria'),
    path('nova-foto/', views.equipe_criar_foto, name='equipe_criar_foto'),
    path('editar-foto/<int:pk>/', views.equipe_editar_foto, name='equipe_editar_foto'),
    path('excluir-foto/<int:pk>/', views.equipe_excluir_foto, name='equipe_excluir_foto'),
    path('reordenar-fotos/', views.equipe_reordenar_fotos, name='equipe_reordenar_fotos'),
]
