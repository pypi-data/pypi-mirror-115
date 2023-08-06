from django.conf.urls import include, url

from kobo_exporter.django_compat import patterns

urlpatterns = patterns(
    "",
    url(r"^kobo_exporter/", include("kobo_exporter.urls")),
)
