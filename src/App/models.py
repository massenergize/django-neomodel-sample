from datetime import datetime
from neomodel import (StructuredNode, StructuredRel, StringProperty,
                      IntegerProperty, BooleanProperty, EmailProperty,
                      DateTimeProperty, DateProperty, UniqueIdProperty,
                      RelationshipTo, RelationshipFrom, Relationship,
                      ZeroOrMore, OneOrMore)

from django_neomodel import DjangoNode


class BaseNode(DjangoNode):
    identifier = UniqueIdProperty()
    name = StringProperty(required=True)
    description = StringProperty()
    alternateName = StringProperty()
    image = StringProperty()
    
    sameAs = Relationship('App.models.BaseNode', 'SAME_AS')

    class Meta:
        app_label = 'App'


class UnitRel(StructuredRel):
    TYPES = {'O': 'Owns', 'M': 'Manages', 'R': 'Rents'}
    relation = StringProperty(choices=TYPES)


class Person(BaseNode):
    email = EmailProperty()
    password = StringProperty()
    age_acknowledgment = BooleanProperty()

    units = RelationshipTo('App.models.RealEstateUnit', 'HAS_UNIT', 
                           model=UnitRel)
    goals = RelationshipTo('App.models.Goal', 'HAS_GOAL', cardinality=ZeroOrMore)
    teams = RelationshipTo('App.models.Team', 'IS_MEMBER', cardinality=ZeroOrMore)
    neighborhoods = RelationshipTo('App.models.Neighborhood', 'IN_NEIGHBORHOOD',
                                   cardinality=ZeroOrMore)


class PersonRel(StructuredRel):
    TYPES = {'O': 'OwnedBy', 'M': 'ManagedBy', 'R': 'RentedBy'}
    relation = StringProperty(choices=TYPES)


class RealEstateUnit(BaseNode):
    street = StringProperty(required=True)
    zipcode = StringProperty(required=True)
    number = StringProperty()
    TYPES = {'R': 'Residential', 'C': 'Commercial', 'N': 'Non-profit'}
    unittype = StringProperty(choices=TYPES)

    persons = RelationshipTo('App.models.Person', 'HAS_PERSON', cardinality=ZeroOrMore,
                             model=PersonRel)


class Team(BaseNode):
    admins = RelationshipTo('App.models.Person', 'HAS_ADMIN', cardinality=ZeroOrMore)
    members = RelationshipTo('App.models.Person', 'HAS_MEMBER', cardinality=ZeroOrMore)
    goals = RelationshipTo('App.models.Goal', 'HAS_GOAL', cardinality=ZeroOrMore)


class Goal(BaseNode):
    pass


class Neighborhood(BaseNode):
    admins = RelationshipTo('App.models.Person', 'HAS_ADMIN', cardinality=ZeroOrMore)
    members = RelationshipTo('App.models.Person', 'HAS_MEMBER', cardinality=ZeroOrMore)
    goals = RelationshipTo('App.models.Goal', 'HAS_GOAL', cardinality=ZeroOrMore)


class Partner(BaseNode):
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


class Action(BaseNode):
    startdate = DateTimeProperty()
    enddate = DateTimeProperty()

    tags = RelationshipTo('App.models.Tag', 'HAS_TAG', cardinality=ZeroOrMore)
    partners = RelationshipTo('App.models.Partner', 'HAS_PARTNER', cardinality=ZeroOrMore,
                              model=PartnerRel)
    persons = RelationshipTo('App.models.Person', 'TAKEN_BY', cardinality=ZeroOrMore,
                             model=PersonActionRel)


class Tag(BaseNode):
    pass


class SuperGroup(BaseNode):
    pass
    # includes Tags
    # excludes Tags


class ActionRel(StructuredRel):
    unit_id = StringProperty()
    reminder = BooleanProperty()


class Plans(BaseNode):
    actions = RelationshipTo('App.models.Action', 'HAS_TODO', cardinality=OneOrMore,
                             model=ActionRel)


class Items(BaseNode):
    TYPES = {'S': 'Story', 'N': 'News', 'R': 'Request', 'Q': 'Question',
             'C': 'Comment'}
    itemtype = StringProperty(choices=TYPES)


class Event(BaseNode):
    startdate = DateTimeProperty()
    enddate = DateTimeProperty()

    partners = RelationshipTo('App.models.Partner', 'HAS_PARTNER', cardinality=ZeroOrMore)


class Permission(BaseNode):
    TYPES = {'C': 'Create', 'V': 'View', 'A': 'Approve', 'E': 'Edit',
             'F': 'Fork'}
    permtype = StringProperty(choices=TYPES)


class Role(BaseNode):
    TYPES = {'S': 'SuperAdmin', 'N': 'Neighborhood Admin', 'T': 'Team Admin',
             'R': 'Unit Admin', 'P': 'Partner Admin'}
    roletype = StringProperty(choices=TYPES)


class Policy(BaseNode):
    who = Role()
    cando = Permission()
    withwhat = set()


class Notification(BaseNode):
    pass
