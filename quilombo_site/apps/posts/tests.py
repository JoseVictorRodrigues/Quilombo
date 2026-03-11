from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass123')

    def test_criar_post(self):
        post = Post.objects.create(
            titulo='Mutirão de Plantio',
            conteudo='Vamos plantar árvores nativas no espaço.',
            resumo='Mutirão comunitário de plantio.',
            autor=self.user,
        )
        self.assertEqual(str(post), 'Mutirão de Plantio')
        self.assertEqual(post.slug, 'mutirao-de-plantio')
        self.assertTrue(post.publicado)

    def test_slug_unico(self):
        Post.objects.create(
            titulo='Evento',
            conteudo='Conteúdo 1',
            resumo='Resumo 1',
            autor=self.user,
        )
        post2 = Post.objects.create(
            titulo='Evento',
            conteudo='Conteúdo 2',
            resumo='Resumo 2',
            autor=self.user,
        )
        self.assertNotEqual(post2.slug, 'evento')
        self.assertTrue(post2.slug.startswith('evento-'))


class PostViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass123')
        self.post = Post.objects.create(
            titulo='Post de Teste',
            conteudo='Conteúdo completo do post de teste.',
            resumo='Resumo do post de teste.',
            autor=self.user,
        )

    def test_lista_posts_status(self):
        response = self.client.get(reverse('lista_posts'))
        self.assertEqual(response.status_code, 200)

    def test_lista_posts_template(self):
        response = self.client.get(reverse('lista_posts'))
        self.assertTemplateUsed(response, 'posts/lista.html')

    def test_detalhe_post_status(self):
        response = self.client.get(reverse('detalhe_post', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)

    def test_detalhe_post_template(self):
        response = self.client.get(reverse('detalhe_post', args=[self.post.slug]))
        self.assertTemplateUsed(response, 'posts/detalhe.html')

    def test_post_nao_publicado_404(self):
        self.post.publicado = False
        self.post.save()
        response = self.client.get(reverse('detalhe_post', args=[self.post.slug]))
        self.assertEqual(response.status_code, 404)
