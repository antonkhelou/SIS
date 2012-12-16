from django.conf.urls import patterns, include, url, static
from django.conf import settings


urlpatterns = patterns('sis.views.main',
	url(r'^$', 'home', name='home'),
)

#For serving stuff under MEDIA_ROOT in debug mode only
if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)