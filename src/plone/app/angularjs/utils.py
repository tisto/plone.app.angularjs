# -*- coding: utf-8 -*-
from zope.schema import getFields
from zope.interface import providedBy
from plone.behavior.interfaces import IBehaviorAssignable
from plone.app.textfield import RichText
from zope.schema import Datetime


def serialize_to_json(obj):
    result = {
        '@context':
        {
            'effective': {
                "@type": "http://www.w3.org/2001/XMLSchema#dateTime"
            },
            'expires': {
                "@type": "http://www.w3.org/2001/XMLSchema#dateTime"
            },
        }
    }
    for title, schema_object in get_object_schema(obj):
        value = getattr(obj, title, None)
        if value is not None:
            # RichText
            if isinstance(schema_object, RichText):
                result[title] = value.output
            # DateTime
            elif isinstance(schema_object, Datetime):
                # Return DateTime in ISO-8601 format. See
                # https://pypi.python.org/pypi/DateTime/3.0 and
                # http://www.w3.org/TR/NOTE-datetime for details.
                # XXX: We might want to change that in the future.
                result[title] = value().ISO8601()
            # Callables
            elif callable(schema_object):
                result[title] = value()
            # Tuple
            elif isinstance(value, tuple):
                result[title] = list(value)
            # List
            elif isinstance(value, list):
                result[title] = value
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
    object_schema = set()
    for iface in providedBy(obj).flattened():
        for name, field in getFields(iface).items():
            no_underscore_method = not name.startswith('_')
            no_manage_method = not name.startswith('manage')
            if no_underscore_method and no_manage_method:
                if name not in object_schema:
                    object_schema.add(name)
                    yield name, field

    assignable = IBehaviorAssignable(obj, None)
    if assignable:
        for behavior in assignable.enumerateBehaviors():
            for name, field in getFields(behavior.interface).items():
                if name not in object_schema:
                    object_schema.add(name)
                    yield name, field


def underscore_to_camelcase(underscore_string):
    return ''.join(
        x for x in underscore_string.title() if not x.isspace()
    ).replace('_', '')
