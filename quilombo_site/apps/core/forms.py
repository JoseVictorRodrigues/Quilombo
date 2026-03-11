import re
from django import forms
from .models import Contato


class ContatoForm(forms.ModelForm):
    # Campo honeypot anti-spam (deve ficar vazio)
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'autocomplete': 'off', 'tabindex': '-1'}),
        label=''
    )

    class Meta:
        model = Contato
        fields = ['nome', 'email', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Seu nome completo',
                'maxlength': '150',
                'aria-label': 'Nome completo',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'seu@email.com',
                'aria-label': 'E-mail',
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Sua mensagem...',
                'rows': 5,
                'maxlength': '2000',
                'aria-label': 'Mensagem',
            }),
        }

    def clean_website(self):
        """Honeypot anti-spam: se preenchido, é bot."""
        if self.cleaned_data.get('website'):
            raise forms.ValidationError('Erro de validação.')
        return ''

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        if len(nome) < 2:
            raise forms.ValidationError('Nome deve ter ao menos 2 caracteres.')
        if not re.match(r'^[\w\s\-\.àáâãéêíóôõúüçÀÁÂÃÉÊÍÓÔÕÚÜÇ]+$', nome):
            raise forms.ValidationError('Nome contém caracteres inválidos.')
        return nome

    def clean_mensagem(self):
        mensagem = self.cleaned_data.get('mensagem', '').strip()
        if len(mensagem) < 10:
            raise forms.ValidationError('Mensagem deve ter ao menos 10 caracteres.')
        return mensagem
