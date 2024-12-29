import os

from .helper import search


def new_app_install(project_name, app_name, dependency='django.contrib.staticfiles', crud=True):
    """
    새로운 앱을 생성해 추가합니다.

    :param str project_name: 프로젝트 이름
    :param str app_name: 앱 이름
    :param dependency: settings.INSTALLED_APPS 내 리스트 원소 중 의존성이 있는 앱 지정된 앱 뒤에 본 앱이 설치됨.
    ex) INSTALLED_APPS = [ ...
        'django.contrib.staticfiles',
        'account']
    :param crud: CRUD 생성 여부
    :return:
    """
    # app dir
    os.chdir(project_name)
    os.system('python manage.py startapp {}'.format(app_name))
    print('변경후 : {}'.format(os.getcwd()))
    appdir_path = app_name
    model_name = app_name.capitalize()

    # models.py 파일 변경
    with open(os.path.join(appdir_path, 'models.py'), 'w') as f:
        model_lines = generate_model_base_code_lines(model_name)
        f.writelines(model_lines)

    # forms.py 파일 생성
    with open(os.path.join(appdir_path, 'forms.py'), 'w') as f:
        form_lines = generate_form_base_code_lines(model_name, app_name, crud=crud)
        f.writelines(form_lines)

    # views.py 파일 생성
    with open(os.path.join(appdir_path, 'views.py'), 'w') as f:
        view_lines = generate_view_base_code_lines(model_name, app_name, crud=crud)
        f.writelines(view_lines)

    # urls.py 파일 생성
    with open(os.path.join(appdir_path, 'urls.py'), 'w') as f:
        url_lines = generate_url_base_code_lines(model_name, app_name, crud=crud)
        f.writelines(url_lines)

    # 폴더 변경
    os.chdir('../')

    # settings.py 에 정보 추가 및 수정
    setting_path = os.path.join(project_name, project_name, 'settings.py')
    with open(setting_path, 'r') as f:
        # settings.py 에 추가할 내용
        lines = f.readlines()
        # app 추가
        index = search(lines, "{}".format(dependency))[0]
        lines[index] = lines[index] + "'{}' ,\n".format(app_name)
    # 문자열 저장
    with open(setting_path, 'w') as f:
        f.writelines(lines)

    # urls.py 문자열 추가
    url_path = os.path.join(project_name, project_name, 'urls.py')
    with open(url_path, 'r') as f:
        lines = f.readlines()
        index = search(lines, "path('admin/', admin.site.urls),")[0]
        lines.insert(index + 1, "path('{}/', include('{}.urls'), name='{}'),\n".format(app_name, app_name, app_name))
    with open(url_path, 'w') as f:
        f.writelines(lines)


# Model
def generate_form_base_code_lines(model_name, app_name, crud):
    index_form_code = generate_form_base_code(model_name, 'Index', True)  # IndexForm 생성
    if crud:
        create_form_code = generate_form_base_code(model_name, 'Create', False)  # CreateForm 생성
        read_form_code = generate_form_base_code(model_name, 'Detail', False)  # DetailForm 생성
        update_form_code = generate_form_base_code(model_name, 'Update', False)  # UpdateForm 생성
        form_code = index_form_code + create_form_code + read_form_code + update_form_code
    else:
        form_code = index_form_code
    return form_code


# Forms
def generate_form_base_code(model_name, form_name, include_header=True):
    base_form_header_lines = ['from helper import apply_widget_by_field, get_all_field_info\n',
                              'from django import forms\n',
                              'from .models import {}\n'.format(model_name),
                              'from datetime import datetime\n']

    base_form_body_lines = ['\nclass {}{}Form(forms.ModelForm):\n'.format(model_name, form_name),
                            '\tclass Meta:\n',
                            '\t\tremove = []\n',
                            '\t\tmodel = {}\n'.format(model_name),
                            '\t\tfields, verbose_names, field_types = get_all_field_info(model, with_id=False, remove=remove)\n',
                            '\t\tfield_names = fields\n',
                            '\t\tfields_with_id, _, _ = get_all_field_info(model, with_id=True,remove=remove)\n',
                            '\t\twidgets = apply_widget_by_field(model,field_names,DateTime=forms.widgets.DateTimeInput(attrs={\'type\': \'datetime-local\'}), Date=forms.widgets.DateInput(attrs={\'type\': \'date\'}))\n',

                            '\tdef __init__(self, *args, **kwargs):\n'
                            '\t\t# 사용자 지정 키워드 인자는 해당 영역에서 모두 제거되어야 합니다. ex) kwargs.pop("user", [])\n'
                            '\t\tsuper().__init__(*args, **kwargs)\n'
                            "\t\tself.field_names = self.Meta.fields\n",
                            "\t\tself.verbose_names = self.Meta.verbose_names\n",
                            "\t\tself.field_types = self.Meta.field_types\n",
                            "\t\tself.fields_with_id = self.Meta.fields_with_id\n",

                            '\tdef save(self, commit=True, **form_additional_info):\n'
                            '\t\t# 폼 저장 영역\n'
                            "\t\tinstance = super({}{}Form, self).save(commit=commit)\n".format(model_name, form_name),
                            "\t\treturn instance\n".format(model_name, form_name),
                            ]
    if include_header:
        return base_form_header_lines + base_form_body_lines
    else:
        return base_form_body_lines


def generate_view_base_code_lines(model_name, app_name, crud):
    # views.py 생성
    header_lines = [
        "import os.path\n",
        "from {}.forms import {}IndexForm\n".format(app_name, model_name),
        "from {}.forms import {}CreateForm, {}UpdateForm, {}DetailForm\n".format(app_name, model_name, model_name,
                                                                                 model_name),
        "from {}.models import {}\n".format(app_name, model_name),
        "from helper import h_tag, card_row, base_form_detail\n",
        "from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete\n",
        "from tables import crud_formtable\n", ]

    index_lines = [
        "\ndef index(request):\n",
        "\tdef _callback(**kwargs):\n",
        "\t\tpass;\n",
        "\treturn standard_index(request, {}IndexForm, {{}}, None, '{}/', None, crud_formtable, None)\n".format(
            model_name, app_name)]

    create_lines = [
        # create
        "\ndef create(request):\n",
        "\tdef _callback(**kwargs):\n",
        "\t\tpass;\n",
        "\treturn standard_create(request, 'standard/create.html', {}CreateForm, None, '{}:index', {{}}, None, None)\n".format(
            model_name, app_name), ]

    detail_lines = [
        # detail
        "\ndef detail(request, id):\n",
        "\tdef _callback(**kwargs):\n",
        "\t\tpass;\n",
        "\treturn standard_detail(request, id, 'standard/detail.html', {}DetailForm, None, base_form_detail, None, None)\n".format(
            model_name), ]

    update_lines = [
        "\ndef update(request, id):\n",
        "\tdef _callback(**kwargs):\n",
        "\t\tpass;\n",
        "\treturn standard_update(request, id, 'standard/update.html', {}UpdateForm, None, '{}:index', None, None, _callback)\n".format(
            model_name, app_name)]

    delete_lines = [
        "\ndef delete(request, id):\n",
        "\treturn standard_delete(request, id, {}, '{}:index', {{}}, None)".format(model_name, app_name)]

    # 코드 생성
    if crud:

        lines = header_lines + index_lines + create_lines + detail_lines + update_lines + delete_lines
    else:
        header_lines.pop(2)
        lines = header_lines + index_lines
    return lines


def generate_url_base_code_lines(model_name, app_name, crud):
    base_lines = ['from django.urls import path\n',
                  'from {}.views import index, create, detail, update, delete\n'.format(app_name),
                  'from {}.views import create, detail, update, delete\n'.format(app_name),
                  "app_name = '{}'\n".format(app_name),
                  "urlpatterns = [\n\tpath('create/', create, name='create'), ",
                  "\n\tpath('index/', index, name='index'), ",
                  "\n\tpath('detail/<int:id>', detail, name='detail'), ",
                  "\n\tpath('update/<int:id>', update, name='update'), ",
                  "\n\tpath('delete/<int:id>', delete, name='delete')",
                  "\n\t]"]
    if not crud:
        base_lines.pop(2)
        base_lines.pop(-2)  # delete delete
        base_lines.pop(-2)  # delete update
        base_lines.pop(-2)  # delete detail
    return base_lines


def generate_model_base_code_lines(model_name):
    """

    :param app_name:
    :param model_name:
    :param crud:
    :return:
    """
    base_lines = ["from django.db import models\n",
                  "class {}(models.Model):\n".format(model_name),
                  "\tname = models.CharField(max_length=100)\n",
                  "\tdesc = models.TextField(null=True, blank=True)\n", ]
    return base_lines
