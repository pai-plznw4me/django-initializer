from helper import apply_widget_by_field, get_all_field_info
from django import forms
from .models import Proj
from datetime import datetime

from .project_wizard import is_valid_django_project_name


class ProjIndexForm(forms.ModelForm):
    class Meta:
        remove = []
        model = Proj
        fields, verbose_names, field_types = get_all_field_info(model, with_id=False, remove=remove)
        field_names = fields
        fields_with_id, _, _ = get_all_field_info(model, with_id=True, remove=remove)
        widgets = apply_widget_by_field(model, field_names,
                                        DateTime=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                        Date=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        # 사용자 지정 키워드 인자는 해당 영역에서 모두 제거되어야 합니다. ex) kwargs.pop("user", [])
        super().__init__(*args, **kwargs)
        self.field_names = self.Meta.fields
        self.verbose_names = self.Meta.verbose_names
        self.field_types = self.Meta.field_types
        self.fields_with_id = self.Meta.fields_with_id

    def save(self, commit=True, **form_additional_info):
        # 폼 저장 영역
        instance = super(ProjIndexForm, self).save(commit=commit)
        return instance


class ProjCreateForm(forms.ModelForm):
    class Meta:
        remove = []
        model = Proj
        fields, verbose_names, field_types = get_all_field_info(model, with_id=False, remove=remove)
        field_names = fields
        fields_with_id, _, _ = get_all_field_info(model, with_id=True, remove=remove)
        widgets = apply_widget_by_field(model, field_names,
                                        DateTime=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                        Date=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', [])
        # 사용자 지정 키워드 인자는 해당 영역에서 모두 제거되어야 합니다. ex) kwargs.pop("user", [])
        super().__init__(*args, **kwargs)
        self.field_names = self.Meta.fields
        self.verbose_names = self.Meta.verbose_names
        self.field_types = self.Meta.field_types
        self.fields_with_id = self.Meta.fields_with_id


    def save(self, commit=True, **form_additional_info):
        # 폼 저장 영역
        instance = super(ProjCreateForm, self).save(commit=commit)
        return instance

    def clean_name(self):
        name = self.cleaned_data['name']
        flag, msg = is_valid_django_project_name(self.name)
        if not flag:
            raise forms.ValidationError(msg)
        return name


class ProjDetailForm(forms.ModelForm):
    class Meta:
        remove = []
        model = Proj
        fields, verbose_names, field_types = get_all_field_info(model, with_id=False, remove=remove)
        field_names = fields
        fields_with_id, _, _ = get_all_field_info(model, with_id=True, remove=remove)
        widgets = apply_widget_by_field(model, field_names,
                                        DateTime=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                        Date=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        # 사용자 지정 키워드 인자는 해당 영역에서 모두 제거되어야 합니다. ex) kwargs.pop("user", [])
        super().__init__(*args, **kwargs)
        self.field_names = self.Meta.fields
        self.verbose_names = self.Meta.verbose_names
        self.field_types = self.Meta.field_types
        self.fields_with_id = self.Meta.fields_with_id

    def save(self, commit=True, **form_additional_info):
        # 폼 저장 영역
        instance = super(ProjDetailForm, self).save(commit=commit)
        return instance


class ProjUpdateForm(forms.ModelForm):
    class Meta:
        remove = []
        model = Proj
        fields, verbose_names, field_types = get_all_field_info(model, with_id=False, remove=remove)
        field_names = fields
        fields_with_id, _, _ = get_all_field_info(model, with_id=True, remove=remove)
        widgets = apply_widget_by_field(model, field_names,
                                        DateTime=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                        Date=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        # 사용자 지정 키워드 인자는 해당 영역에서 모두 제거되어야 합니다. ex) kwargs.pop("user", [])
        super().__init__(*args, **kwargs)
        self.field_names = self.Meta.fields
        self.verbose_names = self.Meta.verbose_names
        self.field_types = self.Meta.field_types
        self.fields_with_id = self.Meta.fields_with_id

    def save(self, commit=True, **form_additional_info):
        # 폼 저장 영역
        instance = super(ProjUpdateForm, self).save(commit=commit)
        return instance
