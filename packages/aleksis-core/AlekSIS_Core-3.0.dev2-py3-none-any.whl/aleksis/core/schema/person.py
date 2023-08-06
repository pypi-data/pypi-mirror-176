import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

from ..forms import PersonForm
from ..models import Person


class PersonType(DjangoObjectType):
    class Meta:
        model = Person

    full_name = graphene.Field(graphene.String)

    def resolve_full_name(root: Person, info, **kwargs):
        return root.full_name


class PersonMutation(DjangoModelFormMutation):
    person = graphene.Field(PersonType)

    class Meta:
        form_class = PersonForm
