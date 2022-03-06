from .apps import IamheadlessPublisherAdminFlatPagesConfig


class Settings:

    APP_NAME = IamheadlessPublisherAdminFlatPagesConfig.name
    ITEM_TYPE = 'flat_page'

    def __getattr__(self, name):
        return getattr(dj_settings, name)


settings = Settings()
