from django import forms
from django.forms import formset_factory


class FlatPageContentForm(forms.Form):
    language = forms.CharField(max_length=255, widget=forms.widgets.HiddenInput(), initial='')
    title = forms.CharField(max_length=255, initial='')
    slug = forms.SlugField(max_length=255, initial='', widget=forms.widgets.TextInput(attrs={'slugfield': 'true'}))
    content = forms.CharField(widget=forms.widgets.Textarea(attrs={'readability': 'true'}))
    seo_keywords = forms.CharField(max_length=160, initial='', required=False)
    seo_description = forms.CharField(max_length=160, initial='', required=False)


FlatPageContentFormSet = formset_factory(FlatPageContentForm, extra=0)


class FlatPageForm(forms.Form):
    published = forms.ChoiceField(choices=(('false', 'No'), ('true', 'Yes')))
