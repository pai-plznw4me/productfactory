from django import forms
from helper import get_all_field_info, apply_widget_by_field, extract_file_info
from .models import File
from datetime import datetime


class FileIndexForm(forms.ModelForm):
    class Meta:
        # model 내 정의되어 있는 fields 을 처리합니다.
        remove = []
        model = File
        fields, verbose_names, field_types = get_all_field_info(model, with_id=False, remove=remove)
        field_names = fields
        fields_with_id, _, _ = get_all_field_info(model, with_id=True, remove=remove)  # foreign key 에 _id 가 붙어 있지 않음
        widgets = apply_widget_by_field(model,
                                        field_names,
                                        DateTime=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                        Date=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        # models 내 정의되어 있는 필드 외 새로운 필드를 추가합니다.
        # 모든 필더 정보를 제공합니다.

        super().__init__(*args, **kwargs)

        # 기본 필드 정보 생성하기
        self.field_names = self.Meta.fields
        self.verbose_names = self.Meta.verbose_names
        self.field_types = self.Meta.field_types
        self.fields_with_id = self.Meta.fields_with_id


class FileCreateForm(forms.ModelForm):
    class Meta:
        # model 내 정의되어 있는 fields 을 처리합니다.
        remove = ['file_ext', 'file_size', 'file_upload_datetime']
        model = File
        fields, verbose_names, field_types = get_all_field_info(model, with_id=False, remove=remove)
        field_names = fields
        fields_with_id, _, _ = get_all_field_info(model, with_id=True, remove=remove)  # foreign key 에 _id 가 붙어 있지 않음
        widgets = apply_widget_by_field(model,
                                        field_names,
                                        DateTime=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                        Date=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        # models 내 정의되어 있는 필드 외 새로운 필드를 추가합니다.
        # 모든 필더 정보를 제공합니다.

        super().__init__(*args, **kwargs)

        # 기본 필드 정보 생성하기
        self.field_names = self.Meta.fields
        self.verbose_names = self.Meta.verbose_names
        self.field_types = self.Meta.field_types
        self.fields_with_id = self.Meta.fields_with_id

    def save(self, commit=True, **form_additional_info):
        instance = super(FileCreateForm, self).save(commit=commit)
        filecontent = self.cleaned_data['file_content']

        file_info = extract_file_info(filecontent)
        instance.name = file_info['name']
        instance.file_size = file_info['size']
        instance.file_ext = file_info['ext']
        instance.file_upload_datetime = datetime.now()

        return instance


class FileUpdateForm(forms.ModelForm):
    class Meta:
        # model 내 정의되어 있는 fields 을 처리합니다.
        remove = []
        model = File
        fields, verbose_names, field_types = get_all_field_info(model, with_id=False, remove=remove)
        field_names = fields
        fields_with_id, _, _ = get_all_field_info(model, with_id=True, remove=remove)  # foreign key 에 _id 가 붙어 있지 않음
        widgets = apply_widget_by_field(model,
                                        field_names,
                                        DateTime=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                        Date=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        # models 내 정의되어 있는 필드 외 새로운 필드를 추가합니다.
        # 모든 필더 정보를 제공합니다.

        super().__init__(*args, **kwargs)

        # 기본 필드 정보 생성하기
        self.field_names = self.Meta.fields
        self.verbose_names = self.Meta.verbose_names
        self.field_types = self.Meta.field_types
        self.fields_with_id = self.Meta.fields_with_id


class FileDetailForm(forms.ModelForm):
    class Meta:
        # model 내 정의되어 있는 fields 을 처리합니다.
        remove = []
        model = File
        fields, verbose_names, field_types = get_all_field_info(model, with_id=False, remove=remove)
        field_names = fields
        fields_with_id, _, _ = get_all_field_info(model, with_id=True, remove=remove)  # foreign key 에 _id 가 붙어 있지 않음
        widgets = apply_widget_by_field(model,
                                        field_names,
                                        DateTime=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                        Date=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        # models 내 정의되어 있는 필드 외 새로운 필드를 추가합니다.
        # 모든 필더 정보를 제공합니다.

        super().__init__(*args, **kwargs)

        # 기본 필드 정보 생성하기
        self.field_names = self.Meta.fields
        self.verbose_names = self.Meta.verbose_names
        self.field_types = self.Meta.field_types
        self.fields_with_id = self.Meta.fields_with_id
