from django.test import TestCase, Client
from django.urls import reverse
from .models import Contato, PontoMapa, ConfiguracaoSite
from .forms import ContatoForm


class CoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_status(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_sobre_page_status(self):
        response = self.client.get(reverse('sobre'))
        self.assertEqual(response.status_code, 200)

    def test_contato_page_status(self):
        response = self.client.get(reverse('contato'))
        self.assertEqual(response.status_code, 200)

    def test_eventos_api_status(self):
        response = self.client.get(reverse('eventos_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_robots_txt(self):
        response = self.client.get(reverse('robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response['Content-Type'])
        self.assertContains(response, 'Disallow: /admin/')
        self.assertContains(response, 'Disallow: /equipe/')

    def test_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'core/home.html')

    def test_contato_form_valid(self):
        data = {
            'nome': 'Maria Silva',
            'email': 'maria@exemplo.com',
            'mensagem': 'Gostaria de participar das atividades do projeto.',
            'website': '',
        }
        response = self.client.post(reverse('contato'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contato.objects.filter(email='maria@exemplo.com').exists())

    def test_contato_form_honeypot(self):
        data = {
            'nome': 'Bot',
            'email': 'bot@spam.com',
            'mensagem': 'Spam message with enough characters here.',
            'website': 'http://spam.com',
        }
        response = self.client.post(reverse('contato'), data)
        self.assertEqual(response.status_code, 200)  # Fica na página, não redireciona
        self.assertFalse(Contato.objects.filter(email='bot@spam.com').exists())

    def test_contato_form_invalid_short_name(self):
        form = ContatoForm(data={
            'nome': 'A',
            'email': 'a@b.com',
            'mensagem': 'Mensagem válida com mais de dez caracteres.',
            'website': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)

    def test_contato_form_invalid_short_message(self):
        form = ContatoForm(data={
            'nome': 'Maria',
            'email': 'maria@b.com',
            'mensagem': 'Curta',
            'website': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('mensagem', form.errors)


class ContatoModelTest(TestCase):
    def test_criar_contato(self):
        contato = Contato.objects.create(
            nome='João',
            email='joao@teste.com',
            mensagem='Quero participar do projeto comunitário.',
        )
        self.assertEqual(str(contato), f'João - joao@teste.com ({contato.data_envio:%d/%m/%Y})')
        self.assertFalse(contato.lida)


class PontoMapaModelTest(TestCase):
    def test_criar_ponto(self):
        ponto = PontoMapa.objects.create(
            nome='Horta Comunitária',
            descricao='Espaço para cultivo coletivo',
            latitude=-25.5935,
            longitude=-49.4069,
        )
        self.assertEqual(str(ponto), 'Horta Comunitária')


class ConfiguracaoSiteModelTest(TestCase):
    def test_singleton(self):
        c1 = ConfiguracaoSite.get()
        c2 = ConfiguracaoSite.get()
        self.assertEqual(c1.pk, c2.pk)
        self.assertEqual(c1.pk, 1)

    def test_str(self):
        c = ConfiguracaoSite.get()
        self.assertEqual(str(c), 'Configuração do Site')

    def test_campos_padrao(self):
        c = ConfiguracaoSite.get()
        self.assertEqual(c.tamanho_logo, 120)
        self.assertEqual(c.cor_fundo, '#f5f1eb')
        self.assertTrue(c.animacao_folhas_ativa)
        self.assertEqual(c.link_instagram, '')
        self.assertEqual(c.link_telegram, '')
        self.assertEqual(c.link_youtube, '')
        self.assertEqual(c.google_calendar_link, '')

    def test_salvar_redes_sociais(self):
        c = ConfiguracaoSite.get()
        c.link_instagram = 'https://instagram.com/quilombo'
        c.link_telegram = 'https://t.me/quilombo'
        c.link_youtube = 'https://youtube.com/@quilombo'
        c.save()
        c.refresh_from_db()
        self.assertEqual(c.link_instagram, 'https://instagram.com/quilombo')
        self.assertEqual(c.link_telegram, 'https://t.me/quilombo')

    def test_desativar_folhas(self):
        c = ConfiguracaoSite.get()
        c.animacao_folhas_ativa = False
        c.save()
        c.refresh_from_db()
        self.assertFalse(c.animacao_folhas_ativa)

    def test_google_calendar_link(self):
        c = ConfiguracaoSite.get()
        c.google_calendar_link = 'https://calendar.google.com/calendar/embed?src=test'
        c.save()
        c.refresh_from_db()
        self.assertEqual(c.google_calendar_link, 'https://calendar.google.com/calendar/embed?src=test')


class MapRenderingTest(TestCase):
    def test_home_page_has_map_container(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'id="map"')

    def test_home_page_has_map_coordinates(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, '-23.6513')
        self.assertContains(response, '-46.7490')

    def test_home_page_has_map_points_data(self):
        PontoMapa.objects.create(
            nome='Teste', descricao='Desc', latitude=-23.65, longitude=-46.75
        )
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'map-points-data')
        self.assertContains(response, 'Teste')


class AddressUpdateTest(TestCase):
    def test_footer_has_new_address(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Rua Ecaúna, 137')
        self.assertContains(response, 'São Paulo - SP')

    def test_contato_has_new_address(self):
        response = self.client.get(reverse('contato'))
        self.assertContains(response, 'Rua Ecaúna, 137')

    def test_footer_social_links_dynamic(self):
        config = ConfiguracaoSite.get()
        config.link_instagram = 'https://instagram.com/quilombo'
        config.save()
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'https://instagram.com/quilombo')

    def test_folhas_desativadas_no_html(self):
        config = ConfiguracaoSite.get()
        config.animacao_folhas_ativa = False
        config.save()
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'id="falling-leaves"')


class EmailContatoTest(TestCase):
    """Testa o campo email_contato dinâmico no rodapé e na página de contato."""

    def test_email_padrao_no_rodape(self):
        """Sem email configurado, o rodapé usa o email padrão."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'quilomboaraucaria.org')

    def test_email_dinamico_no_rodape(self):
        config = ConfiguracaoSite.get()
        config.email_contato = 'novo@exemplo.org'
        config.save()
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'novo@exemplo.org')
        self.assertContains(response, 'mailto:novo@exemplo.org')

    def test_email_dinamico_na_pagina_contato(self):
        config = ConfiguracaoSite.get()
        config.email_contato = 'teste@quilombo.org'
        config.save()
        response = self.client.get(reverse('contato'))
        self.assertContains(response, 'teste@quilombo.org')
        self.assertContains(response, 'mailto:teste@quilombo.org')

    def test_favicon_view_sem_logo(self):
        """favicon view retorna 204 quando não há logo configurada."""
        response = self.client.get(reverse('favicon'))
        self.assertIn(response.status_code, [204, 302])

    def test_painel_acessibilidade_presente(self):
        """O HTML deve conter o painel de acessibilidade com todos os botões."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'accessibility-panel')
        self.assertContains(response, 'btn-increase-font')
        self.assertContains(response, 'btn-decrease-font')
        self.assertContains(response, 'btn-toggle-contrast')
        self.assertContains(response, 'btn-toggle-theme')
        self.assertContains(response, 'btn-reset-font')
