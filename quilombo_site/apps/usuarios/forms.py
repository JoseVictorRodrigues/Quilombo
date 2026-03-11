from django import forms
from apps.posts.models import Post, MediaPost
from apps.core.models import ConfiguracaoSite


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'resumo', 'conteudo', 'imagem_capa', 'video_url']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Título do post',
            }),
            'resumo': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Resumo curto do post...',
                'rows': 3,
                'maxlength': '500',
            }),
            'conteudo': forms.Textarea(attrs={
                'class': 'form-input form-textarea editor-content',
                'placeholder': 'Escreva o conteúdo aqui...',
                'rows': 15,
                'id': 'id_conteudo',
            }),
            'imagem_capa': forms.ClearableFileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*',
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://www.youtube.com/watch?v=...',
            }),
        }


class MediaPostForm(forms.ModelForm):
    class Meta:
        model = MediaPost
        fields = ['arquivo', 'video_url', 'tipo', 'ordem']
        widgets = {
            'arquivo': forms.ClearableFileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*,video/*',
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://www.youtube.com/watch?v=...',
            }),
            'tipo': forms.Select(attrs={'class': 'form-input'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
        }


class ConfiguracaoSiteForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoSite
        fields = [
            'logo', 'tamanho_logo', 'imagem_fundo', 'cor_fundo',
            'email_contato',
            'link_instagram', 'link_telegram', 'link_youtube',
            'google_calendar_link', 'animacao_folhas_ativa',
        ]
        widgets = {
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*',
            }),
            'tamanho_logo': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '40',
                'max': '400',
            }),
            'imagem_fundo': forms.ClearableFileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*',
            }),
            'cor_fundo': forms.TextInput(attrs={
                'class': 'form-input',
                'type': 'color',
            }),
            'link_instagram': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://instagram.com/...',
            }),
            'link_telegram': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://t.me/...',
            }),
            'link_youtube': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://youtube.com/@...',
            }),
            'google_calendar_link': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://calendar.google.com/...',
            }),
            'email_contato': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'contato@seudominio.org',
            }),
            'animacao_folhas_ativa': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
        }
