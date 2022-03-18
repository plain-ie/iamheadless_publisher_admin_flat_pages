# iamheadless_publisher_admin_flat_pages

App to render flat-page item type in `iamheadless_publisher_admin` frontend.

## Installation

Requires `iamheadless_publisher_admin`

1. install package
2. add `iamheadless_publisher_admin_flat_pages` to `INSTALLED_APPS` in `settings.py`
3. add viewsets to `IAMHEADLESS_PUBLISHER_ADMIN_VIEWSET_LIST` in `settings.py`
```
[
    'iamheadless_publisher_admin_flat_pages.viewsets.FlatPageCreateViewSet',
    'iamheadless_publisher_admin_flat_pages.viewsets.FlatPageDeleteViewSet',
    'iamheadless_publisher_admin_flat_pages.viewsets.FlatPageRetrieveUpdateViewSet',
]
```
