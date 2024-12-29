"""
File: helper.py
Author: 김성중
Version: 1.6
Date: 2024-02-26

Description: 모든 앱에 공통적으로 사용되는 유틸 또는 헬퍼 func 들을 정의해 놓음.

"""

import os
from urllib.parse import urlparse
import pandas as pd
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models
from django.urls import reverse
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from django.template import loader


def create_button(url, str_):
    """
    주어진 URL과 텍스트로 이루어진 <button> 태그를 생성하는 함수입니다.

    :param url: 버튼 클릭 시 이동할 URL
    :param str_: 버튼에 표시될 텍스트
    :return: 생성된 <button> 태그 문자열
    """
    button_tag = '<button class="btn btn-secondary" onclick="location.href=\'{}\'">{}</button>'.format(url, str_)
    return button_tag


def get_base_url(full_url):
    """
    전체 URL에서 기본 URL을 추출하는 함수입니다.

    :param full_url: 전체 URL
    :return: 기본 URL
    """
    parsed_url = urlparse(full_url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc
    return base_url


def generate_url(base_url, url_path):
    """
    기본 URL과 하위 경로를 결합하여 완전한 URL을 생성하는 함수입니다.

    :param base_url: 기본 URL
    :param url_path: 하위 경로
    :return: 완전한 URL
    """
    return os.path.join(base_url, url_path)


def append_onclick_button(btn_name, df, url, button_type='btn-secondary'):
    """
    DataFrame에 <button> 태그와 onclick 속성이 추가된 열을 추가하는 함수입니다.

    :param btn_name: 버튼의 이름
    :param base_url: 기본 URL 경로
    :param df: DataFrame
    :param url_path: 버튼이 클릭되었을 때 이동할 URL 경로
    :return: 없음
    """
    # dataframe update column 에 button tag 삽입, project/delete/{id} 를 삽입
    df[btn_name] = df.id.map(
        lambda x: '<button class="btn {}" onclick="location.href=\'{}/{}\'">{}</button>'.format(button_type, url, x,
                                                                                                btn_name, ))


def add_content(request, base, *contents):
    """
    기본 HTML 템플릿에 콘텐츠를 추가합니다.

    Parameters:
    - request: HttpRequest 객체, Django의 요청 객체입니다.
    - base: str, 사용할 기본 템플릿 ('doctris' 또는 다른 것)입니다.
    - *contents: 추가할 콘텐츠를 나타내는 가변 인수입니다.

    Returns:
    - str: HTML

    Raises:
    - NotImplementedError: 인식되지 않는 기본 템플릿이 제공된 경우 발생합니다.

    Example:
        # df -> html
        table_html = target_df.to_html(escape=False)

        # create button tag
        url = generate_url(base_url, 'file', 'create')
        button_tag = create_button(url, 'create')

        ret_html = add_content(request, 'doctris', button_tag, table_html)
        return HttpResponse(ret_html)
    ```
    """

    if base == 'doctris':
        # doctris design 적용
        base_html = render(request, template_name='doctris_base/base.html').content
        # BeautifulSoup로 HTML 템플릿 파일을 읽어오기
        base_soup = BeautifulSoup(base_html, 'html.parser')  # byte or str -> bs4
        target_tag = base_soup.find('div', class_='container-fluid')
    else:
        # 디자인을 적용하지 않고 html 을 순서대로 묶어 제공합니다.
        return "".join(contents)

    for ctnt in contents:
        ctnt = BeautifulSoup(ctnt, 'html.parser')  # byte -> bs4
        target_tag.append(ctnt)
    return base_soup.prettify(formatter=None)  # bs4 -> str


def apply_widget_by_field(model, field_names, **kwargs):
    """
    주어진 Django 모델의 특정 필드에 대해 사용자 지정 위젯을 적용하는 함수입니다.

    Parameters:
    - model (django.db.models.Model): 위젯을 적용할 Django 모델 인스턴스
    - fields (List[str]): 위젯을 적용할 필드 이름들을 담은 리스트
    - kwargs: 다양한 필드 유형에 대한 위젯 인자를 지정하기 위한 키워드 인자들
        - Char (django.forms.widgets.Widget): models.CharField에 대한 위젯
        - Text (django.forms.widgets.Widget): models.TextField에 대한 위젯
        - Date (django.forms.widgets.Widget): models.DateField에 대한 위젯
        - Boolean (django.forms.widgets.Widget): models.BooleanField에 대한 위젯
        - Float (django.forms.widgets.Widget): models.FloatField에 대한 위젯
        - Integer (django.forms.widgets.Widget): models.IntegerField에 대한 위젯
        - DateTime (django.forms.widgets.Widget): models.DateTimeField에 대한 위젯
        - File (django.forms.widgets.Widget): models.FileField에 대한 위젯
        - Image (django.forms.widgets.Widget): models.ImageField에 대한 위젯

    Returns:
    - dict: 각 필드에 적용된 위젯을 담은 딕셔너리
    """

    widget_fields = field_names
    widgets = {}

    for field in widget_fields:
        if isinstance(model._meta.get_field(field), models.CharField):
            if 'Char' in kwargs.keys():
                widgets[field] = kwargs['Char']
        elif isinstance(model._meta.get_field(field), models.TextField):
            if 'Text' in kwargs.keys():
                widgets[field] = kwargs['Text']
        elif isinstance(model._meta.get_field(field), models.BooleanField):
            if 'Boolean' in kwargs.keys():
                widgets[field] = kwargs['Boolean']
        elif isinstance(model._meta.get_field(field), models.FloatField):
            if 'Float' in kwargs.keys():
                widgets[field] = kwargs['Float']
        elif isinstance(model._meta.get_field(field), models.IntegerField):
            if 'Integer' in kwargs.keys():
                widgets[field] = kwargs['Integer']
        elif isinstance(model._meta.get_field(field), models.DateTimeField):
            if 'DateTime' in kwargs.keys():
                widgets[field] = kwargs['DateTime']
        elif isinstance(model._meta.get_field(field), models.DateField):
            if 'Date' in kwargs.keys():
                widgets[field] = kwargs['Date']
        elif isinstance(model._meta.get_field(field), models.FileField):
            if 'File' in kwargs.keys():
                widgets[field] = kwargs['File']
        elif isinstance(model._meta.get_field(field), models.ImageField):
            if 'Image' in kwargs.keys():
                widgets[field] = kwargs['Image']
        elif isinstance(model._meta.get_field(field), models.ForeignKey):
            if 'Foreign' in kwargs.keys():
                widgets[field] = kwargs['Foreign']
        else:
            print(model._meta.get_field(field))
    return widgets


def get_template_path(template_name):
    """
    주어진 템플릿 이름에 대한 템플릿 파일 경로를 반환하는 함수입니다.

    Parameters:
        template_name (str): 찾고자 하는 템플릿의 이름.

    Returns:
        str: 템플릿 파일의 절대 경로. 찾지 못하면 None을 반환합니다.
    """
    try:
        template = loader.get_template(template_name)
        template_path = template.origin.name
        return template_path
    except loader.TemplateDoesNotExist:
        print(f"Template '{template_name}' does not exist.")
        return None


def save_as_html(path, html):
    """
    주어진 HTML 태그를 파일로 저장합니다.

    매개변수:
        - path (str): HTML 내용을 저장할 파일 경로입니다.
        - tags (str): 저장할 HTML 태그 또는 내용입니다.

    예시:
        save_as_html('output.html', '<p>Hello, World!</p>')
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


def wrap_with_tag(input_string, tag_name, **attr):
    """
      주어진 문자열을 지정한 HTML 태그로 감싸는 함수입니다.

      Parameters:
          - input_string (str): 감쌀 문자열입니다.
          - tag_name (str): 생성할 태그의 이름입니다.
          - **attr: 생성할 태그의 다른 속성을 지정하는 키워드 인자들입니다.

      Returns:
          str: HTML 태그로 감싸진 문자열입니다.

      Example:
          wrap_with_tag('<p>Hello, World!</p>', 'a', href='https://example.com', class_='link')
    """

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(input_string, 'html.parser')

    # <a> 태그 생성
    target_tag = soup.new_tag(name=tag_name, **attr)

    # 원래의 문자열을 <a> 태그 안으로 옮기기
    target_tag.append(soup.new_string(input_string))

    # 원래의 문자열을 <a> 태그로 대체
    soup.contents = [target_tag]

    # 결과 반환
    return str(soup)


def html_load(basepath):
    """
       주어진 파일 경로에서 HTML 파일을 읽어와 문자열로 반환하는 함수입니다.

       Parameters:
           - basepath (str): 읽어올 HTML 파일의 경로입니다.

       Returns:
           str: HTML 파일의 내용을 담은 문자열입니다.

       Example:
           html_content = html_load('path/to/your/file.html')
       """
    with open(basepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
        return html_content


def bs4_load(base_path):
    """
    주어진 파일 경로에서 HTML 파일을 읽어와 BeautifulSoup 객체로 파싱하여 반환하는 함수입니다.

    Parameters:
        - base_path (str): 읽어올 HTML 파일의 경로입니다.

    Returns:
        BeautifulSoup: HTML을 파싱한 BeautifulSoup 객체입니다.

    Example:
        soup = bs4_load('path/to/your/file.html')
    """
    html_str = html_load(base_path)
    soup = BeautifulSoup(html_str, 'html.parser')
    return soup


def insert_html_to_body(soup, target):
    """
    BeautifulSoup으로 파싱된 HTML 문서의 body 태그에 HTML을 삽입하는 함수입니다.

    :param soup: BeautifulSoup으로 파싱된 HTML 문서
    :param target: 삽입할 HTML 코드 또는 태그
    :return: HTML이 삽입된 BeautifulSoup 객체
    """
    body_tag = soup.find('body')
    first_script_tag = body_tag.find('script')
    first_script_tag.insert_before(target)
    return soup


def get_field_types(model, field_names):
    """
    주어진 모델과 필드 이름에 대한 필드 타입을 반환하는 함수입니다.

    :param model: Django 모델 클래스
    :param field_names: 모델 필드의 이름들
    :return: 필드 타입들의 리스트
    """
    types = []
    for name in field_names:
        field = model._meta.get_field(name)
        # field 가 Image type 이면 'ImageType' 으로 타입을 저장합니다.
        # 모델 필드의 내부 타입은 실제 데이터베이스에서 사용되는 타입입니다.
        # get_internal_type()으로 반환되는 값은 FileField 입니다.
        if isinstance(field, models.ImageField):
            types.append('ImageField')
        else:
            types.append(field.get_internal_type())
    return types


def get_all_field_info(model, with_foreignkey=True, remove=None, with_id=True):
    """
    주어진 Django 모델의 모든 필드 이름을 반환합니다.
    foreinkey 반환시 django 에서 참조하는 명은 '{model}_id' 입니다.
    반환시에는 _id 을 제거하고 {model} 명만 반환합니다.

    Parameters:
    - model (django.db.models.Model): 필드 이름을 가져올 Django 모델 인스턴스
    - with_foreignkey (bool) : foreinkey 포함 여부
    - remove (List): column 에서 빼버릴것들

    Returns:
    - List[str]: 모델의 모든 필드 이름을 담은 문자열 리스트
    """
    # 모든 필드를 가져옵니다.
    fields = model._meta.fields

    # remove 에 등록되어 있는 필드를 제거합니다.
    fields_without_id = [field.attname if not isinstance(field, models.ForeignKey) else
                         field.attname.replace('_id', '') for field in fields]
    fields = [field for (name, field) in zip(fields_without_id, fields) if name not in remove]

    # foreign 키를 포함 하는 모든 필드의 (이름, 별명)을 반환합니다.
    if with_foreignkey:
        if with_id:  # 반환시에는 {model}_id 형태로 반환합니다.
            names_and_verboses = [(field.attname, field.verbose_name) for field in fields]
        # field = model._meta.get_field(name)
        else:  # 반환시에는 _id 을 제거하고 {model} 명만 반환합니다.
            names_and_verboses = [(field.attname, field.verbose_name)
                                  if not isinstance(field, models.ForeignKey)
                                  else (field.attname.replace('_id', ''), field.verbose_name)
                                  for field in fields]
    # foreign 키를 제외하고 모든 필드의 (이름, 별명)을 반환합니다.
    else:
        names_and_verboses = [(field.attname, field.verbose_name) for field in fields if
                              not isinstance(field, models.ForeignKey)]

    names, verboses = zip(*names_and_verboses)
    types = get_field_types(model, names)
    return list(names), list(verboses), types


def base_form_detail(request, template_name, object, form_class, form_additional_info):
    """
    상세 페이지 HTML을 생성하여 반환합니다    .

    Usage:
        project_detail_content = detail_html(request, project)

    :param request: HTTP 요청 객체
    :param object: 상세 정보를 표시할 모델 객체
    :return: 생성된 상세 페이지 HTML 컨텐츠
    """

    # form instance 정보와 폼내 정의되어 있는 추가 정보를 받아 폼 인스턴스 생성
    form_inst = form_class(form_additional_info, instance=object)
    form_inst.data.update(form_inst.initial)

    # 필드정보 파싱
    # TODO: model 정보와 달리 id 값이 들어가 있지 않음
    field_names = list(form_inst.field_names)  # 필드 이름
    verbose_names = form_inst.verbose_names  # 필드 별명
    field_types = form_inst.field_types  # 필드 타입
    # charfield code 을 text 로 변환합니다. (ex BD => 사업계획서)
    field_values = []
    for ind, field_name in enumerate(field_names):
        field_value = form_inst.data[field_name]
        field_type = field_types[ind]
        # TODO dict mapper 으로 변환하기
        if field_type == 'CharField':
            field = form_inst.fields[field_name]
            if hasattr(field, 'choices'):
                choices = field.choices
                tmp_dict = {choice[0]: choice[1] for choice in choices}
                field_value = tmp_dict[field_value]

        field_values.append(field_value)

    # 컨텍스트 생성
    context = {'object': object, 'field_names': field_names, 'field_types': field_types, 'verbose_names': verbose_names,
               'field_values': field_values, 'form': form_inst}

    # 상세 페이지 HTML을 렌더링합니다.
    detail_content = render(request, template_name=template_name, context=context).content.decode('utf-8')
    return detail_content


def join_url_and_variables(path, variables):
    """
    usage :
    path(create_url, create, name='create'),
    path('update/<str:id>', update, name='update'),

    :param path: 'create/'
    :param variables:  ex) ['<str:id>', '<str:date>']
    :return: ex) 'create/<str:id>/<str:date>'
    """
    full_path = os.path.join(path, *variables)
    return full_path


def card_row(*args):
    """
    Bootstrap 카드로 구성된 행을 생성하는 유틸리티 함수입니다.

    :param args: (content, range_col) 튜플의 가변 인자들. content는 카드 내용, range_col은 Bootstrap 그리드 시스템에서 차지하는 칼럼 크기입니다.
    :return: Bootstrap 카드로 구성된 HTML 행
    """

    # 기본 템플릿 생성
    template_tag = '''
    <div class="row">
    </div>
    '''
    template_soup = BeautifulSoup(template_tag, 'html.parser')

    # 전달된 인자들을 이용하여 각 카드 생성 및 템플릿에 추가
    for arg in args:
        content, range_col = arg[0], arg[1]
        col_tag = "<div class='col-{}'><div class=\"card bg-white shadow rounded border-0\"><div class=\"card-body\">{}</div></div></div>".format(
            range_col, content)
        target_tag = template_soup.find('div', class_='row')
        target_tag.append(col_tag)
    # 최종 결과 반환
    return template_soup.prettify(formatter=None)


def h_tag(level, str_):
    """
    지정된 레벨의 HTML 헤딩 태그를 생성하는 함수입니다.

    :param level: 헤딩 태그의 레벨 (1~6까지 가능)
    :param str_: 헤딩 태그 내부에 들어갈 텍스트 또는 HTML 문자열
    :return: 생성된 HTML 헤딩 태그
    """

    h_tag = '''
    <h{}>{}
    </h{}>
    '''.format(level, str_, level)
    return h_tag


def extract_file_info(file):
    """
    :param file: ex) file = form.cleaned_data['filecontent']
    :return dict:
    """
    # 파일 속성 추출 및 생성
    file_ext = os.path.splitext(file.name)[1]

    # 속성 정보 저장
    return {'name': file.name, 'size': file.size, 'ext': file_ext}


def apply_datatable(table_id):
    """
     javascript DataTable을 적용합니다.

     :param table_id: DataTable이 적용될 테이블의 ID
     :type table_id: str
     :return: DataTable을 적용하는 스크립트
     :rtype: str
     """
    return "<script>var {} = $('#{}').DataTable( {{'scrollY':'200px', 'scrollCollapse':true }});</script>".format(
        table_id, table_id)


def wrapping_card(title_name, content):
    """
    제목과 내용을 갖는 HTML 카드를 생성합니다.

    :param str title_name: 카드의 제목
    :param str content: 카드에 포함될 내용
    :return str: 래핑된 카드 HTML 코드
    """
    title = h_tag(2, title_name)  # h2 tag 제목
    wrapped_content = title + card_row(
        (content, 12))  # added_contents 내 첫번째 요소 : detail_content
    return wrapped_content
