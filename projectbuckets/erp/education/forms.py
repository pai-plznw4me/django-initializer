from typing import final
from helper import apply_widget_by_field, get_all_field_info
from django import forms
from .models import Education
from datetime import datetime
from django.core.exceptions import ValidationError


class EducationIndexForm(forms.ModelForm):
    class Meta:
        remove = []
        model = Education
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
        instance = super(EducationIndexForm, self).save(commit=commit)
        return instance


class EducationCreateForm(forms.ModelForm):
    class Meta:
        remove = []
        model = Education
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
        instance = super(EducationCreateForm, self).save(commit=commit)
        return instance

    def clean(self):
        employee = self.cleaned_data['employee']
        # final 이 하나 이상인지 확인합니다.
        final_edu = employee.education_set.filter(final=True)
        if len(final_edu) > 1:
            raise ValidationError('최종 학력은 하나밖에 지정되지 못합니다. 현재 {}개가 지정되어 있습니다.'.format(len(final_edu)))


class EducationDetailForm(forms.ModelForm):
    class Meta:
        remove = []
        model = Education
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
        instance = super(EducationDetailForm, self).save(commit=commit)
        return instance


class EducationUpdateForm(forms.ModelForm):
    class Meta:
        remove = []
        model = Education
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
        instance = super(EducationUpdateForm, self).save(commit=commit)
        return instance
