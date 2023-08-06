from django import VERSION as DJANGOVERSION

if DJANGOVERSION[0:3] < (1, 8, 0):  # pragma: no cover
    from django.conf.urls import patterns  # pylint: disable=no-name-in-module
else:

    def patterns(_dummy, *args):
        return list(args)


__all__ = ["patterns"]
