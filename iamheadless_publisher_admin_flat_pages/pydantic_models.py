import datetime
from typing import List, Optional

from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from pydantic import Field

from iamheadless_publisher_admin.pydantic_models import BaseItemPydanticModel, BaseItemDataPydanticModel, BaseItemContentsPydanticModel

from .conf import settings
from . import forms


class FlatPageContentPydanticModel(BaseItemContentsPydanticModel):
    title: str
    slug: str
    language: str
    content: str
    seo_keywords: Optional[str]
    seo_description: Optional[str]


class FlatPageDataPydanticModel(BaseItemDataPydanticModel):
    contents: List[FlatPageContentPydanticModel]
    published: str


class FlatPagePydanticModel(BaseItemPydanticModel):

    _content_model = FlatPageContentPydanticModel
    _data_model = FlatPageDataPydanticModel
    _display_name_plural = _('flat pages')
    _display_name_singular = _('flat page')
    _item_type = settings.ITEM_TYPE
    _project_admin_required = True
    _tenant_required = False

    data: FlatPageDataPydanticModel

    @property
    def TITLE(self):
        _data = self.DATA
        _contents = _data.get('data', {}).get('contents', [])
        _display_content = FlatPagePydanticModel.get_display_content(_contents, self._primary_language)
        return _display_content['title']

    @property
    def EDIT_URL(self):

        _data = self.DATA

        project_id = _data.get('project', None)
        item_id = _data.get('id', None)

        return reverse(
            settings.URLNAME_RETRIEVE_UPDATE_ITEM,
            kwargs={
                'project_id': project_id,
                'item_id': item_id
            }
        )

    @classmethod
    def get_item_type(cls, data):
        return data['item_type']

    @classmethod
    def render_form(
            cls,
            request,
            initial_data
            ):

        initial_item = initial_data.get('data', {})
        initial_contents = initial_data.get('data', {}).get('contents', [])
        if initial_contents == []:
            initial_contents = [{'language': cls._primary_language}]

        content_formset = forms.FlatPageContentFormSet(initial=initial_contents, prefix='content_formset')
        form = forms.FlatPageForm(initial=initial_item)

        if request.method == 'POST':
            content_formset = forms.FlatPageContentFormSet(request.POST, initial=initial_contents, prefix='content_formset')
            form = forms.FlatPageForm(request.POST, initial=initial_item)

        return render_to_string(
            'iamheadless_publisher_admin_flat_pages/form.html',
            context={
                'content_formset': content_formset,
                'form': form,
            }
        )

    @classmethod
    def validate_form(
            cls,
            request,
            initial_data
            ):

        data = {}
        if request.method == 'POST':
            data = request.POST

        initial_item = initial_data.get('data', {})
        initial_contents = initial_data.get('data', {}).get('contents', [])

        content_formset = forms.FlatPageContentFormSet(request.POST, initial=initial_contents, prefix='content_formset')
        form = forms.FlatPageForm(request.POST, initial=initial_item)

        valid = []

        valid.append(content_formset.is_valid())
        valid.append(form.is_valid())

        if False in valid:
            raise ValidationError(_('Form is invalid'))

        validated_data =  {
            'data': form.cleaned_data,
        }

        validated_data['data']['contents'] = content_formset.cleaned_data

        return validated_data

    @classmethod
    def pre_create(cls, request, data):

        #
        indexes = {
            'text': [],
            'bool': [],
        }

        # Content indexes
        for content in data['data']['contents']:
            indexes['text'].append({
                'field_name': 'slug',
                'value': content['slug'],
            })
            indexes['text'].append({
                'field_name': 'title',
                'value': content['title'],
            })

        # Published state
        published = data['data']['published'] in ['true', True, 'True', 'yes', 1, '1']
        indexes['bool'] = [{
            'field_name': 'published',
            'value': published,
        }]

        #
        data['indexes'] = indexes

        #
        return data

    @classmethod
    def pre_update(cls, request, data):
        return cls.pre_create(request, data)
