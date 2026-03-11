from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_configuracaosite_animacao_folhas_ativa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracaosite',
            name='email_contato',
            field=models.EmailField(
                blank=True,
                default='',
                help_text='E-mail exibido no rodapé e na página de contato.',
                max_length=254,
                verbose_name='E-mail de contato',
            ),
        ),
    ]
