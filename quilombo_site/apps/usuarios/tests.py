from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.posts.models import Post
from apps.core.models import ConfiguracaoSite


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('equipe', 'equipe@test.com', 'senhaforte123')

    def test_login_page_get(self):
        response = self.client.get(reverse('equipe_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/login.html')

    def test_login_valido(self):
        response = self.client.post(reverse('equipe_login'), {
            'username': 'equipe',
            'password': 'senhaforte123',
        })
        self.assertRedirects(response, reverse('equipe_painel'))

    def test_login_invalido(self):
        response = self.client.post(reverse('equipe_login'), {
            'username': 'equipe',
            'password': 'errada',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_redireciona_autenticado(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.get(reverse('equipe_login'))
        self.assertRedirects(response, reverse('equipe_painel'))


class PainelViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('equipe', 'equipe@test.com', 'senhaforte123')

    def test_painel_requer_login(self):
        response = self.client.get(reverse('equipe_painel'))
        self.assertEqual(response.status_code, 302)

    def test_painel_autenticado(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.get(reverse('equipe_painel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/painel.html')


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('equipe', 'equipe@test.com', 'senhaforte123')

    def test_logout(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.post(reverse('equipe_logout'))
        self.assertRedirects(response, reverse('home'))


class CriarPostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('equipe', 'equipe@test.com', 'senhaforte123')

    def test_criar_post_requer_login(self):
        response = self.client.get(reverse('equipe_criar_post'))
        self.assertEqual(response.status_code, 302)

    def test_criar_post_get(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.get(reverse('equipe_criar_post'))
        self.assertEqual(response.status_code, 200)

    def test_criar_post_valido(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.post(reverse('equipe_criar_post'), {
            'titulo': 'Novo Post de Teste',
            'resumo': 'Resumo do post.',
            'conteudo': 'Conteúdo completo do post de teste.',
        })
        self.assertRedirects(response, reverse('equipe_painel'))
        self.assertTrue(Post.objects.filter(titulo='Novo Post de Teste').exists())


class EditarPostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('equipe', 'equipe@test.com', 'senhaforte123')
        self.other = User.objects.create_user('outro', 'outro@test.com', 'senhaforte123')
        self.post = Post.objects.create(
            titulo='Post Existente',
            resumo='Resumo.',
            conteudo='Conteúdo.',
            autor=self.user,
        )

    def test_editar_post_requer_login(self):
        response = self.client.get(reverse('equipe_editar_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_editar_post_dono(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.get(reverse('equipe_editar_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_editar_post_outro_usuario_404(self):
        self.client.login(username='outro', password='senhaforte123')
        response = self.client.get(reverse('equipe_editar_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 404)

    def test_editar_post_valido(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.post(reverse('equipe_editar_post', args=[self.post.pk]), {
            'titulo': 'Título Atualizado',
            'resumo': 'Novo resumo.',
            'conteudo': 'Novo conteúdo.',
        })
        self.assertRedirects(response, reverse('equipe_painel'))
        self.post.refresh_from_db()
        self.assertEqual(self.post.titulo, 'Título Atualizado')


class ExcluirPostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('equipe', 'equipe@test.com', 'senhaforte123')
        self.other = User.objects.create_user('outro', 'outro@test.com', 'senhaforte123')
        self.post = Post.objects.create(
            titulo='Post Para Excluir',
            resumo='Resumo.',
            conteudo='Conteúdo.',
            autor=self.user,
        )

    def test_excluir_post_requer_login(self):
        response = self.client.post(reverse('equipe_excluir_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_excluir_post_get_nao_permitido(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.get(reverse('equipe_excluir_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 405)

    def test_excluir_post_dono(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.post(reverse('equipe_excluir_post', args=[self.post.pk]))
        self.assertRedirects(response, reverse('equipe_painel'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_excluir_post_outro_usuario_404(self):
        self.client.login(username='outro', password='senhaforte123')
        response = self.client.post(reverse('equipe_excluir_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())


class ConfiguracoesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('equipe', 'equipe@test.com', 'senhaforte123')

    def test_configuracoes_requer_login(self):
        response = self.client.get(reverse('equipe_configuracoes'))
        self.assertEqual(response.status_code, 302)

    def test_configuracoes_get(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.get(reverse('equipe_configuracoes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/configuracoes.html')

    def test_configuracoes_salvar_redes_sociais(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.post(reverse('equipe_configuracoes'), {
            'tamanho_logo': '120',
            'cor_fundo': '#f5f1eb',
            'link_instagram': 'https://instagram.com/quilombo',
            'link_telegram': 'https://t.me/quilombo',
            'link_youtube': 'https://youtube.com/@quilombo',
            'google_calendar_link': '',
            'animacao_folhas_ativa': 'on',
        })
        self.assertRedirects(response, reverse('equipe_configuracoes'))
        config = ConfiguracaoSite.get()
        self.assertEqual(config.link_instagram, 'https://instagram.com/quilombo')
        self.assertEqual(config.link_telegram, 'https://t.me/quilombo')

    def test_configuracoes_desativar_folhas(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.post(reverse('equipe_configuracoes'), {
            'tamanho_logo': '120',
            'cor_fundo': '#f5f1eb',
            'link_instagram': '',
            'link_telegram': '',
            'link_youtube': '',
            'google_calendar_link': '',
            # animacao_folhas_ativa omitted = False
        })
        self.assertRedirects(response, reverse('equipe_configuracoes'))
        config = ConfiguracaoSite.get()
        self.assertFalse(config.animacao_folhas_ativa)

    def test_configuracoes_salvar_google_calendar(self):
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.post(reverse('equipe_configuracoes'), {
            'tamanho_logo': '120',
            'cor_fundo': '#f5f1eb',
            'link_instagram': '',
            'link_telegram': '',
            'link_youtube': '',
            'google_calendar_link': 'https://calendar.google.com/calendar/embed?src=test',
            'animacao_folhas_ativa': 'on',
        })
        self.assertRedirects(response, reverse('equipe_configuracoes'))
        config = ConfiguracaoSite.get()
        self.assertEqual(config.google_calendar_link, 'https://calendar.google.com/calendar/embed?src=test')

    def test_configuracoes_salvar_email_contato(self):
        """Editar email_contato no painel da equipe persiste e aparece no rodapé."""
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.post(reverse('equipe_configuracoes'), {
            'tamanho_logo': '120',
            'cor_fundo': '#f5f1eb',
            'email_contato': 'novo@quilombo.org',
            'link_instagram': '',
            'link_telegram': '',
            'link_youtube': '',
            'google_calendar_link': '',
            'animacao_folhas_ativa': 'on',
        })
        self.assertRedirects(response, reverse('equipe_configuracoes'))
        config = ConfiguracaoSite.get()
        self.assertEqual(config.email_contato, 'novo@quilombo.org')
        # Verifica renderização no rodapé
        response_home = self.client.get(reverse('home'))
        self.assertContains(response_home, 'novo@quilombo.org')
        self.assertContains(response_home, 'mailto:novo@quilombo.org')

    def test_configuracoes_email_invalido_rejeitado(self):
        """Email inválido deve ser rejeitado no formulário."""
        self.client.login(username='equipe', password='senhaforte123')
        response = self.client.post(reverse('equipe_configuracoes'), {
            'tamanho_logo': '120',
            'cor_fundo': '#f5f1eb',
            'email_contato': 'isso-nao-e-email',
            'link_instagram': '',
            'link_telegram': '',
            'link_youtube': '',
            'google_calendar_link': '',
            'animacao_folhas_ativa': 'on',
        })
        # Não deve redirecionar — fica na página de configurações com erro
        self.assertEqual(response.status_code, 200)
