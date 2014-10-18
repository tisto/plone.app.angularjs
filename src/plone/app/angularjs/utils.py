# -*- coding: utf-8 -*-
from zope.schema import getFields
from zope.interface import providedBy
from plone.behavior.interfaces import IBehaviorAssignable
from plone.app.textfield import RichText
from zope.schema import Datetime


def serialize_to_json(obj):
    result = {}
    for title, schema_object in get_object_schema(obj):
        value = getattr(obj, title, None)
        no_underscore_method = not title.startswith('_')
        no_manage_method = not title.startswith('manage')
        if value and no_underscore_method and no_manage_method:
            # RichText
            if isinstance(schema_object, RichText):
                result[title] = value.output
            # DateTime
            elif isinstance(schema_object, Datetime):
                # XXX: Time string needs to be localized!
                result[title] = str(value())
            # Callables
            elif callable(schema_object):
                result[title] = value()
            # Tuple
            elif isinstance(value, tuple):
                result[title] = list(value)
            # String
            elif isinstance(value, str):
                result[title] = value
            # Unicode
            elif isinstance(value, unicode):
                result[title] = value
            else:
                result[title] = str(value)
    return result


def get_object_schema(obj):
    for iface in providedBy(obj).flattened():
        for name, field in getFields(iface).items():
            yield name, field

    assignable = IBehaviorAssignable(obj, None)
    if assignable:
        for behavior in assignable.enumerateBehaviors():
            for name, field in getFields(behavior.interface).items():
                yield name, field


def underscore_to_camelcase(underscore_string):
    return ''.join(
        x for x in underscore_string.title() if not x.isspace()
    ).replace('_', '')
