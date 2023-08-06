from django.apps import apps

import graphene
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet
from haystack.utils.loading import UnifiedIndex

from ..models import Notification, Person, TaskUserAssignment
from ..util.apps import AppConfig
from ..util.core_helpers import get_allowed_object_ids, get_app_module, get_app_packages, has_person
from .celery_progress import CeleryProgressFetchedMutation, CeleryProgressType
from .group import GroupType  # noqa
from .installed_apps import AppType
from .notification import MarkNotificationReadMutation, NotificationType
from .person import PersonMutation, PersonType
from .search import SearchResultType
from .system_properties import SystemPropertiesType


class Query(graphene.ObjectType):
    ping = graphene.String(default_value="pong")

    notifications = graphene.List(NotificationType)

    persons = graphene.List(PersonType)
    person_by_id = graphene.Field(PersonType, id=graphene.ID())
    who_am_i = graphene.Field(PersonType)

    system_properties = graphene.Field(SystemPropertiesType)
    installed_apps = graphene.List(AppType)

    celery_progress_by_task_id = graphene.Field(CeleryProgressType, task_id=graphene.String())
    celery_progress_by_user = graphene.List(CeleryProgressType)

    search_snippets = graphene.List(
        SearchResultType, query=graphene.String(), limit=graphene.Int(required=False)
    )

    def resolve_notifications(root, info, **kwargs):
        # FIXME do permission stuff
        return Notification.objects.all()

    def resolve_persons(root, info, **kwargs):
        # FIXME do permission stuff
        return Person.objects.all()

    def resolve_person_by_id(root, info, id):  # noqa
        return Person.objects.get(pk=id)

    def resolve_who_am_i(root, info, **kwargs):
        if has_person(info.context.user):
            return info.context.user.person
        else:
            return None

    def resolve_system_properties(root, info, **kwargs):
        return True

    def resolve_installed_apps(root, info, **kwargs):
        return [app for app in apps.get_app_configs() if isinstance(app, AppConfig)]

    def resolve_celery_progress_by_task_id(root, info, task_id, **kwargs):
        task = TaskUserAssignment.objects.get(task_result__task_id=task_id)

        if not info.context.user.has_perm("core.view_progress_rule", task):
            return None
        progress = task.get_progress_with_meta()
        return progress

    def resolve_celery_progress_by_user(root, info, **kwargs):
        tasks = TaskUserAssignment.objects.filter(user=info.context.user)
        return [
            task.get_progress_with_meta()
            for task in tasks
            if task.get_progress_with_meta()["complete"] is False
        ]

    def resolve_search_snippets(root, info, query, limit=-1, **kwargs):
        indexed_models = UnifiedIndex().get_indexed_models()
        allowed_object_ids = get_allowed_object_ids(info.context.user, indexed_models)
        results = SearchQuerySet().filter(id__in=allowed_object_ids).filter(text=AutoQuery(query))

        if limit < 0:
            return results

        return results[:limit]


class Mutation(graphene.ObjectType):
    update_person = PersonMutation.Field()

    mark_notification_read = MarkNotificationReadMutation.Field()

    celery_progress_fetched = CeleryProgressFetchedMutation.Field()


def build_global_schema():
    """Build global GraphQL schema from all apps."""
    query_bases = [Query]
    mutation_bases = [Mutation]

    for app in get_app_packages():
        schema_mod = get_app_module(app, "schema")
        if not schema_mod:
            # The app does not define a schema
            continue

        if AppQuery := getattr(schema_mod, "Query", None):
            query_bases.append(AppQuery)
        if AppMutation := getattr(schema_mod, "Mutation", None):
            mutation_bases.append(AppMutation)

    # Define classes using all query/mutation classes as mixins
    #  cf. https://docs.graphene-python.org/projects/django/en/latest/schema/#adding-to-the-schema
    GlobalQuery = type("GlobalQuery", tuple(query_bases), {})
    GlobalMutation = type("GlobalMutation", tuple(mutation_bases), {})

    return graphene.Schema(query=GlobalQuery, mutation=GlobalMutation)


schema = build_global_schema()
