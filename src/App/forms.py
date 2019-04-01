from django import forms

from .models import Person

from neomodel import (StructuredNode, StructuredRel, StringProperty,
                      IntegerProperty, BooleanProperty, EmailProperty,
                      DateTimeProperty, DateProperty, UniqueIdProperty,
                      RelationshipTo, RelationshipFrom, Relationship)


def get_fields(klass):
    attrs = dir(klass)
    fields = []
    for attr in attrs:
        if isinstance(getattr(klass, attr),
                      (StringProperty, IntegerProperty, BooleanProperty,
                       EmailProperty, DateTimeProperty, DateProperty)):
            fields.append(attr)
    return fields or None


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = get_fields(model)
