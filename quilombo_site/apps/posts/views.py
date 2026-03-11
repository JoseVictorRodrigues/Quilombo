from django.shortcuts import render, get_object_or_404
from .models import Post


def lista_posts(request):
    posts = Post.objects.filter(publicado=True)
    return render(request, 'posts/lista.html', {'posts': posts})


def detalhe_post(request, slug):
    post = get_object_or_404(Post, slug=slug, publicado=True)
    midias_imagens = post.midias.filter(tipo='imagem')
    midias_videos = post.midias.filter(tipo='video')
    return render(request, 'posts/detalhe.html', {
        'post': post,
        'midias_imagens': midias_imagens,
        'midias_videos': midias_videos,
    })
