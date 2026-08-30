from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from django.conf import settings


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include('dairy.urls')
    ),

]


# Serve media files through Django in all environments.
#
# Django's own `static()` helper (django.conf.urls.static.static) has a
# `DEBUG` check baked into it and silently returns no routes when
# DEBUG=False, so it can't be used here even without our own DEBUG
# guard. Routing directly to the `serve` view bypasses that.
urlpatterns += [
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]