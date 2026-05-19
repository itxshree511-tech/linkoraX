from django.conf import settings


def global_links(request):
    return {
        'WHATSAPP_GROUP_LINK': getattr(settings, 'WHATSAPP_GROUP_LINK', '').strip(),
    }

