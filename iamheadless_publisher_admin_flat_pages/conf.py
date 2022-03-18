from django.conf import settings as dj_settings

from .apps import IamheadlessPublisherAdminFlatPagesConfig as AppConfig


class Settings:

    APP_NAME = AppConfig.name
    ITEM_TYPE = 'flat_page'

    URLNAME_CREATE_ITEM = f'admin-create-{ITEM_TYPE}'
    URLNAME_DELETE_ITEM = f'admin-delete-{ITEM_TYPE}'
    URLNAME_RETRIEVE_UPDATE_ITEM = f'admin-edit-{ITEM_TYPE}'

    RETRIEVE_TEMPLATE = 'iamheadless_publisher_admin/pages/item.html'

    def __getattr__(self, name):
        return getattr(dj_settings, name)


settings = Settings()
