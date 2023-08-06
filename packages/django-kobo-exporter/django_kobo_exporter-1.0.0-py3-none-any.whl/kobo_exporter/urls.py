from django.conf.urls import url

from . import views
from .django_compat import patterns

urlpatterns = patterns(
    "",
    url(r"^metrics/?$", views.metrics),
)
