from django.contrib.auth.forms import UserCreationForm
from django import forms
from account.models import CustomUser
from helper import get_all_field_info, apply_widget_by_field
from copy import deepcopy


class CustomUserCreationForm(UserCreationForm):
    """
    회원 가입시 사용하는 ModelForm
    """

    class Meta:
        model = CustomUser
        remove = ['id', 'password', 'last_login', 'is_staff', 'is_active', 'date_joined', 'is_superuser', 'resume']
        fields, verbose_names, field_types = get_all_field_info(model, with_id=False, remove=remove)
        field_names = fields
        fields_with_id, _, _ = get_all_field_info(model, with_id=True, remove=remove)
        widgets = apply_widget_by_field(model, field_names,
                                        DateTime=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                        Date=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        # 사용자 입력 keyword argument 처리는 user_kwargs 사용하여 처리 ex) kwargs.pop('user', [])
        kwargs.pop('user', [])

        # super().__init__ 을 실행하기 위해서는 kwargs, args 가 초기화 되어야 함
        super().__init__(*args, **kwargs)

        # form inst 변수 생성
        self.field_names = self.Meta.fields
        self.verbose_names = self.Meta.verbose_names
        self.field_types = self.Meta.field_types
        self.fields_with_id = self.Meta.fields_with_id

        # null=True로 설정한 필드에 대해 required를 False로 설정
        self.fields['id_photo'].required = False


class CustomUserProfileForm(UserCreationForm):
    """
    회원 가입시 사용하는 ModelForm
    """

    class Meta:
        model = CustomUser
        remove = ['id', 'password', 'last_login', 'is_staff', 'is_active', 'date_joined', 'is_superuser', 'resume']
        fields, verbose_names, field_types = get_all_field_info(model, with_id=False, remove=remove)
        field_names = fields
        fields_with_id, _, _ = get_all_field_info(model, with_id=True, remove=remove)
        widgets = apply_widget_by_field(model, field_names,
                                        DateTime=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                        Date=forms.widgets.DateInput(attrs={'type': 'date'}),
                                        Char=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        # 사용자 입력 keyword argument 는 모두 제거되어야 합니다. ex) kwargs.pop('user', [])
        kwargs.pop('user', [])

        # super().__init__ 을 실행하기 위해서는 kwargs, args 가 초기화 되어야 함
        super().__init__(*args, **kwargs)

        # form inst 변수 생성
        self.field_names = self.Meta.fields
        self.verbose_names = self.Meta.verbose_names
        self.field_types = self.Meta.field_types
        self.fields_with_id = self.Meta.fields_with_id
