from .models import ConfiguracaoSite


def site_config(request):
    config = ConfiguracaoSite.get()
    return {'site_config': config}
