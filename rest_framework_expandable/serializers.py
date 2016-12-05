from __future__ import absolute_import, unicode_literals
from importlib import import_module

from django.utils.translation import ugettext_lazy as _

from six import text_type

from .exceptions import InvalidExpansion


def parse_expansions(items):
    expansions = {}

    for item in items:
        item = item.split('.', 1)

        sub_fields = expansions.setdefault(item.pop(0), [])

        if item:
            sub_fields.extend(item)

    return expansions


def load_serializer(path, package):
    relative = False
    if path.startswith('.'):
        relative = True

    split_path = path.rsplit('.', 1)
    if len(split_path) == 1:
        module_path = '.'
        serializer_name = split_path[0]
    elif split_path[0] == '':
        module_path = '.'
        serializer_name = split_path[1]
    else:
        module_path, serializer_name = split_path

    module = import_module(module_path, package)
    return getattr(module, serializer_name)


class ExpandableSerializerMixin(object):
    def __init__(self, *args, **kwargs):
        self.expanded_fields = kwargs.pop('expand', [])

        super(ExpandableSerializerMixin, self).__init__(*args, **kwargs)

        expandable_fields = getattr(self.Meta, 'expandable_fields', {})

        for field, child_expansions in parse_expansions(
                self.expanded_fields).items():
            if not expandable_fields or field not in expandable_fields:
                raise InvalidExpansion(_('The field {} does not allow '
                                         'expansion.'.format(field)))

            # NOTE: serializer_kwargs is a reference
            serializer, serializer_args, serializer_kwargs = expandable_fields[
                field]

            if isinstance(serializer, text_type):
                package = self.__module__
                serializer = load_serializer(serializer, package)

            if child_expansions:
                # Nested expansions are a bad idea if the serializer isn't
                # expandable. It will raise a rather unhelpful exception, so
                # let's help a bit instead.
                if not issubclass(serializer, ExpandableSerializerMixin):
                    raise InvalidExpansion(
                        _('The field {} does not allow nested '
                          'expansions.'.format(field)))

                # serializer_kwargs is a *reference* to the dict in
                # expandable_fields. We must make a copy to not mess things up
                # real bad. For performance, we only do it now when we have to.
                serializer_kwargs = dict(serializer_kwargs)

                serializer_kwargs['expand'] = child_expansions

            self.fields[field] = serializer(*serializer_args,
                                            **serializer_kwargs)
