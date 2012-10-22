# coding: utf-8

import sys

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from djangobb_forum import settings as forum_settings
from forms import RegistrationFormUtfUsername
from sitemap import SitemapForum, SitemapTopic



admin.autodiscover()

sitemaps = {
    'forum': SitemapForum,
    'topic': SitemapTopic,
}

urlpatterns = patterns('',
    # Admin
    (r'^admin/', include(admin.site.urls)),

    # Sitemap
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    # Apps
    (r'^forum/account/', include('django_authopenid.urls')),
    (r'^forum/', include('djangobb_forum.urls', namespace='djangobb')),
)

# PM Extension
if (forum_settings.PM_SUPPORT):
    urlpatterns += patterns('',
        (r'^forum/pm/', include('django_messages.urls')),
   )

# serve static files
if settings.RUN_WITH_DEV_SERVER and "--insecure" in sys.argv and "--nostatic" in sys.argv:
    # The automatic static serve is without index views.
    # We add 'django.views.static.serve' here, to add show_indexes==True
    #
    # The developer server must be start with --insecure and --nostatic e.g.:
    #     ./manage.py runserver --insecure --nostatic
    #
    # https://docs.djangoproject.com/en/1.4/ref/contrib/staticfiles/#runserver
    print " *** Serve static files from %r at %r ***" % (settings.STATIC_ROOT, settings.STATIC_URL)
    urlpatterns += patterns('',
        url('^%s/(?P<path>.*)$' % settings.STATIC_URL.strip("/"), 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    )
    print " *** Serve media files from %r at %r ***" % (settings.MEDIA_ROOT, settings.MEDIA_URL)
    urlpatterns += patterns('',
        url('^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip("/"), 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
