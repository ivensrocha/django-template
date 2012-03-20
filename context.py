# coding: utf-8
import settings
def custom_context(request):
    if settings.DEPLOY:
        context = {'STATIC_FILES_URL': settings.DEPLOY_PREFIX + settings.STATIC_URL, 
                   'DEPLOY': True,}
    else:
        context = {'STATIC_FILES_URL': settings.STATIC_URL, 'DEPLOY': False,}
    
    return context