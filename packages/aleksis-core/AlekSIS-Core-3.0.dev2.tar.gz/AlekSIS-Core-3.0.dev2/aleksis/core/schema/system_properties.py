from django.conf import settings
from django.utils import translation

import graphene

from ..util.frontend_helpers import get_language_cookie


class LanguageType(graphene.ObjectType):
    code = graphene.String(required=True)
    name = graphene.String(required=True)
    name_local = graphene.String(required=True)
    name_translated = graphene.String(required=True)
    bidi = graphene.Boolean(required=True)
    cookie = graphene.String(required=True)


class SystemPropertiesType(graphene.ObjectType):
    current_language = graphene.String(required=True)
    available_languages = graphene.List(LanguageType)

    def resolve_current_language(parent, info, **kwargs):
        return info.context.LANGUAGE_CODE

    def resolve_available_languages(parent, info, **kwargs):
        return [
            translation.get_language_info(code) | {"cookie": get_language_cookie(code)}
            for code, name in settings.LANGUAGES
        ]
