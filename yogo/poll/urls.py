from django.conf.urls import include, patterns, url

from .api import PollResource


urlpatterns = patterns(
    '',
    url(r'^', include(PollResource.urls())),
)
