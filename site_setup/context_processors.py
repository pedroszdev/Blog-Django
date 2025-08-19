from site_setup.models import SiteSetup
def context(request):
    return {
        'nome': 'Pedro'
    }

def site_setup(request):
    setup=SiteSetup.objects.order_by('-id').first()
    return {
        'site_setup': setup
    }