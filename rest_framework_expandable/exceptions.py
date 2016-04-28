from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import APIException


class InvalidExpansion(APIException):
    status_code = 400
    default_detail = _('Invalid expansion specified.')
