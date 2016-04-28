from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from .exceptions import InvalidExpansion


ALLOWED_ACTIONS = ['list', 'retrieve', 'metadata']


class ExpandableViewMixin(object):
    def get_serializer(self, *args, **kwargs):
        if 'expand' in self.request.query_params:
            if self.action in ALLOWED_ACTIONS:
                expansions = self.request.query_params['expand']
                kwargs['expand'] = [
                    a.strip() for a in expansions.split(',') if a.strip()
                ]
            else:
                raise InvalidExpansion(_('Forbidden action for field '
                                         'expansion: {}.'.format(self.action)))

        return super(ExpandableViewMixin, self).get_serializer(*args, **kwargs)
