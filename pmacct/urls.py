from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^top_prefixes$', views.top_prefixes, name='top_prefixes'),
    url(r'^top_prefixes/(?P<hours>[0-9]+)$', views.top_prefixes_hours, name='top_prefixes_hours'),
    url(r'^top_asns$', views.top_asns, name='top_asns'),
    url(r'^top_asns/(?P<hours>[0-9]+)$', views.top_asns_hours, name='top_asns_hours'),
]
