from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from .exceptions import InvalidExpansion


class ExpandableViewMixin(object):
    expandable_actions = ['list', 'retrieve', 'metadata']

    @property
    def _is_allowed_to_expand(self):
        return self.action in self.expandable_actions

    def initial(self, request, *args, **kwargs):
        super(ExpandableViewMixin, self).initial(request, *args, **kwargs)

        # We must do the allowed check here because the REST framework uses the
        # get_queryset method internally with custom actions defined, meaning
        # the InvalidExpansion exception will be raised when it shouldn't.
        if 'expand' in request.query_params:
            if self._is_allowed_to_expand:
                raw_expansions = self.request.query_params['expand']
                self.expansions = [
                    a.strip() for a in raw_expansions.split(',') if a.strip()]
            else:
                raise InvalidExpansion(_('Forbidden action for field '
                                         'expansion: {}.'.format(self.action)))

    def get_serializer(self, *args, **kwargs):
        # There are certain cases (e.g. when the get_serializer method is called
        # outside the regular request-response flow) where self.expansions is
        # set but expansion isn't allowed.
        if hasattr(self, 'expansions') and self._is_allowed_to_expand:
            kwargs['expand'] = self.expansions

        return super(ExpandableViewMixin, self).get_serializer(*args, **kwargs)
