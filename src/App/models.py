from datetime import datetime
from neomodel import (StructuredNode, StructuredRel, StringProperty,
                      IntegerProperty, BooleanProperty, EmailProperty,
                      DateTimeProperty, DateProperty, UniqueIdProperty,
                      RelationshipTo, RelationshipFrom,
                      ZeroOrMore, OneOrMore)

from django_neomodel import DjangoNode


class UnitRel(StructuredRel):
    TYPES = {'O': 'Owns', 'M': 'Manages', 'R': 'Rents'}
    relation = StringProperty(choices=TYPES)


class Person(DjangoNode):
    uid = UniqueIdProperty()
    email = EmailProperty()
    nickname = StringProperty()
    password = StringProperty()
    age_acknowledgment = BooleanProperty()

    units = RelationshipTo('App.models.RealEstateUnit', 'HAS_UNIT', cardinality=ZeroOrMore,
                           model=UnitRel)
    goals = RelationshipTo('App.models.Goal', 'HAS_GOAL', cardinality=ZeroOrMore)
    teams = RelationshipTo('App.models.Team', 'IS_MEMBER', cardinality=ZeroOrMore)
    neighborhoods = RelationshipTo('App.models.Neighborhood', 'IN_NEIGHBORHOOD',
                                   cardinality=ZeroOrMore)

    class Meta:
        app_label = 'App'


class PersonRel(StructuredRel):
    TYPES = {'O': 'OwnedBy', 'M': 'ManagedBy', 'R': 'RentedBy'}
    relation = StringProperty(choices=TYPES)


class RealEstateUnit(StructuredNode):
    uid = UniqueIdProperty()
    street = StringProperty(required=True)
    zipcode = StringProperty(required=True)
    number = StringProperty()
    TYPES = {'R': 'Residential', 'C': 'Commercial', 'N': 'Non-profit'}
    unittype = StringProperty(choices=TYPES)

    persons = RelationshipTo('App.models.Person', 'HAS_PERSON', cardinality=ZeroOrMore,
                             model=PersonRel)


class Team(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    description = StringProperty()

    admins = RelationshipTo('App.models.Person', 'HAS_ADMIN', cardinality=ZeroOrMore)
    members = RelationshipTo('App.models.Person', 'HAS_MEMBER', cardinality=ZeroOrMore)
    goals = RelationshipTo('App.models.Goal', 'HAS_GOAL', cardinality=ZeroOrMore)


class Goal(StructuredNode):
    uid = UniqueIdProperty()
    description = StringProperty()


class Neighborhood(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)

    admins = RelationshipTo('App.models.Person', 'HAS_ADMIN', cardinality=ZeroOrMore)
    members = RelationshipTo('App.models.Person', 'HAS_MEMBER', cardinality=ZeroOrMore)
    goals = RelationshipTo('App.models.Goal', 'HAS_GOAL', cardinality=ZeroOrMore)


class Partner(StructuredNode):
    uid = UniqueIdProperty()
    legal_name = StringProperty(required=True)
    legal_address = StringProperty(required=True)
    coverage_area = StringProperty(required=True)
    mou_signed = BooleanProperty(default=False)
    active = BooleanProperty(default=True)

    contacts = RelationshipTo('App.models.Person', 'HAS_CONTACT', cardinality=OneOrMore)
    actions = RelationshipTo('App.models.Action', 'PROVIDES', cardinality=ZeroOrMore)


class PartnerRel(StructuredRel):
    startdate = DateTimeProperty()
    enddate = DateTimeProperty()
    coverage_area = StringProperty()


class PersonActionRel(StructuredRel):
    unit_id = StringProperty()
    action_info = StringProperty()


class Action(StructuredNode):
    uid = UniqueIdProperty()
    startdate = DateTimeProperty()
    enddate = DateTimeProperty()

    tags = RelationshipTo('App.models.Tag', 'HAS_TAG', cardinality=ZeroOrMore)
    partners = RelationshipTo('App.models.Partner', 'HAS_PARTNER', cardinality=ZeroOrMore,
                              model=PartnerRel)
    persons = RelationshipTo('App.models.Person', 'TAKEN_BY', cardinality=ZeroOrMore,
                             model=PersonActionRel)


class Tag(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)


class SuperGroup(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    # includes Tags
    # excludes Tags


class ActionRel(StructuredRel):
    unit_id = StringProperty()
    reminder = BooleanProperty()


class Plans(StructuredNode):
    uid = UniqueIdProperty()

    actions = RelationshipTo('App.models.Action', 'HAS_TODO', cardinality=OneOrMore,
                             model=ActionRel)


class Items(StructuredNode):
    uid = UniqueIdProperty()
    description = StringProperty()
    TYPES = {'S': 'Story', 'N': 'News', 'R': 'Request', 'Q': 'Question',
             'C': 'Comment'}
    itemtype = StringProperty(choices=TYPES)


class Event(StructuredNode):
    uid = UniqueIdProperty()
    description = StringProperty()
    url = StringProperty()

    startdate = DateTimeProperty()
    enddate = DateTimeProperty()

    partners = RelationshipTo('App.models.Partner', 'HAS_PARTNER', cardinality=ZeroOrMore)


class Permission(StructuredNode):
    uid = UniqueIdProperty()
    description = StringProperty()
    TYPES = {'C': 'Create', 'V': 'View', 'A': 'Approve', 'E': 'Edit',
             'F': 'Fork'}
    permtype = StringProperty(choices=TYPES)


class Role(StructuredNode):
    uid = UniqueIdProperty()
    description = StringProperty()
    TYPES = {'S': 'SuperAdmin', 'N': 'Neighborhood Admin', 'T': 'Team Admin',
             'R': 'Unit Admin', 'P': 'Partner Admin'}
    roletype = StringProperty(choices=TYPES)


class Policy(StructuredNode):
    uid = UniqueIdProperty()
    who = Role()
    cando = Permission()
    withwhat = set()


class Notification(StructuredNode):
    uid = UniqueIdProperty()
