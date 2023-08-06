import graphene
from graphene_django import DjangoObjectType

from ..models import Notification


class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification


class MarkNotificationReadMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()  # noqa

    notification = graphene.Field(NotificationType)

    @classmethod
    def mutate(cls, root, info, id):  # noqa
        notification = Notification.objects.get(pk=id)
        # FIXME permissions
        notification.read = True
        notification.save()

        return notification
