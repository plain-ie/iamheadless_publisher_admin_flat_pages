from django.conf import settings as dj_settings

from .apps import IamheadlessPublisherAdminFlatPagesConfig as AppConfig


class Settings:

    APP_NAME = AppConfig.name
    ITEM_TYPE = 'flat_page'

    def __getattr__(self, name):
        return getattr(dj_settings, name)


settings = Settings()
