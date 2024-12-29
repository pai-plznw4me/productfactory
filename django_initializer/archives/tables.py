"""
File: tables.py
Author: 김성중
Version: 1.4
Date: 2024-02-24
Description: 모든 앱에 공통적으로 사용되는 유틸 또는 헬퍼 func 들을 정의해 놓음.
"""

import os
import pandas as pd

from helper import append_onclick_button, generate_url, create_button, wrap_with_tag


def generate_crud_table(base_url, objects, field_names, url_path, **kwargs):
    """
    제공된 객체와 필드 이름을 기반으로 한 CRUD 테이블을 HTML 형식으로 생성합니다.
    생성될 table 가장 오른쪽 field Detail,  Update , Delete field 을 생성하고 button 을 생성합니다.
	+----------+
    | create   |
    | <button> |
    +--------+-------+----------+----------+----------+
    | Object | Field | Detail   | Update   | Delete   |
    +--------+-------+----------+----------+----------+
    | Object1| Field1| <button> | <button> | <button> |
    | Object2| Field2| <button> | <button> | <button> |
    +--------+-------+----------+----------+----------+

    create, Detail, update, delete button 은 아래와 같은 link 가 연결되어 있습니다.
	- create: {base_url}/*paths/create
    - Detail: {base_url}/*paths/detail
    - update: {base_url}/*paths/update
    - delete: {base_url}/*paths/delete

    매개변수:
    - base_url (str): ex) http://localhost:8000
    - objects (QuerySet 또는 None): 테이블에 표시할 객체가 포함된 쿼리셋입니다.
    - field_names (list): 테이블에 포함될 필드 이름의 목록입니다.
    - url_path: 업데이트, 삭제 및 상세 정보 URL을 생성하는 데 사용되는 가변 길이 인수 목록입니다. https://localhost:8000/{*paths}
        *paths = 'project'
        ex) https://localhost:8000/project


    반환값:
    str: CRUD 테이블의 HTML 표현입니다.

    사용 예시:
    ```python
        table_html = generate_crud_table(request, my_objects, ['name', 'age', 'location'], project)
    ```
    """

    field_names = field_names + ['detail', 'update', 'delete']
    if objects:  # 테이블 내 instance 존재 시 아래 코드 수행
        object_df = pd.DataFrame.from_records(objects.values())

        # detail button (read)
        append_onclick_button('detail', object_df, os.path.join(base_url, url_path, 'detail'))

        # generate update urls, (update)
        append_onclick_button('update', object_df, os.path.join(base_url, url_path, 'update'))

        # delete button (delete)
        append_onclick_button('delete', object_df, os.path.join(base_url, url_path, 'delete'))


    else:  # 테이블이 하나도 존재하지 않으면 아래 코드 수행
        object_df = pd.DataFrame(columns=field_names)

    object_df = object_df.loc[:, field_names]
    # df -> html
    table_html = object_df.to_html(escape=False)

    # create button
    url = generate_url(base_url, os.path.join(url_path, 'create'))
    button_tag = create_button(url, 'create')
    crud_table = button_tag + table_html
    return crud_table


def generate_crud_filetable(base_url, objects, field_names, url_path, **kwargs):
    """
    다운로드 링크를 제공합니다.
    제공된 객체와 필드 이름을 기반으로 한 CRUD 테이블을 HTML 형식으로 생성합니다.
    생성될 table 가장 오른쪽 field Detail,  Update , Delete field 을 생성하고 button 을 생성합니다.
    +----------+
    | create   |
    | <button> |
    +--------+-------+----------+----------+----------+
    | Object | Field | Detail   | Update   | Delete   |
    +--------+-------+----------+----------+----------+
    | Object1| Field1| <button> | <button> | <button> |
    | Object2| Field2| <button> | <button> | <button> |
    +--------+-------+----------+----------+----------+

    """
    target_colname = kwargs['target_colname']
    field_names = field_names + ['detail', 'update', 'delete']

    if objects:  # 테이블 내 instance 존재 시 아래 코드 수행
        # 파일 다운로드를 위한 URL 리스트 생성
        urls = [file.filecontent.url for file in objects]
        # filecontent column 에 파일 다운로드 링크 생성
        object_df = pd.DataFrame.from_records(objects.values())
        target_series = object_df.loc[:, target_colname]
        url_tags = [wrap_with_tag(str(ele), tag_name='a', href=url) for ele, url in zip(target_series, urls)]
        object_df.loc[:, target_colname] = url_tags

        # detail button (read)
        append_onclick_button('detail', object_df, os.path.join(base_url, url_path, 'detail'))

        # generate update urls, (update)
        append_onclick_button('update', object_df, os.path.join(base_url, url_path, 'update'))

        # delete button (delete)
        append_onclick_button('delete', object_df, os.path.join(base_url, url_path, 'delete'))



    else:  # 테이블이 하나도 존재하지 않으면 아래 코드 수행
        object_df = pd.DataFrame(columns=field_names)

    object_df = object_df.loc[:, field_names]
    # df -> html
    table_html = object_df.to_html(escape=False)

    # create button
    url = generate_url(base_url, os.path.join(url_path, 'create'))
    button_tag = create_button(url, 'create')
    crud_table = button_tag + table_html
    return crud_table


def approval_crud_formtable(base_url, objects, form_class, url_path, **kwargs):
    """
    form 정보를 기반으로 html table 을 생성해 반환합니다.
    :param base_url:
    :param objects:
    :param form_class:
    :param url_path:
    :param kwargs:
    :return:
    """

    field_names = form_class.Meta.fields_with_id + ['approval', 'detail', 'update', 'delete']

    if objects:  # 테이블 내 instance 존재 시 아래 코드 수행
        object_df = pd.DataFrame.from_records(objects.values())
        append_onclick_button('approval', object_df, os.path.join(base_url, url_path, 'approval'))

        # detail button (read)
        append_onclick_button('detail', object_df, os.path.join(base_url, url_path, 'detail'))

        # generate update urls, (update)
        append_onclick_button('update', object_df, os.path.join(base_url, url_path, 'update'))

        # delete button (delete)
        append_onclick_button('delete', object_df, os.path.join(base_url, url_path, 'delete'))


    else:  # 테이블이 하나도 존재하지 않으면 아래 코드 수행
        object_df = pd.DataFrame(columns=field_names)
    column_names = form_class.Meta.field_names + ['승인', '상세', '업데이트', '제거']
    object_df = object_df.loc[:, field_names]
    object_df.columns = column_names

    # df -> html
    table_html = object_df.to_html(escape=False)

    # create button
    url = generate_url(base_url, os.path.join(url_path, 'create'))
    button_tag = create_button(url, 'create')
    crud_table = button_tag + table_html
    return crud_table


def gantt_crud_formtable(base_url, objects, form_class, form_additional_info, url_path, **kwargs):
    """
    form 정보를 기반으로 html table 을 생성해 반환합니다.
    :param base_url:
    :param objects:
    :param form_class:
    :param form_additional_info:
    :param url_path:
    :param kwargs:
    :return:
    """

    form_inst = form_class()
    table_columns = form_inst.verbose_names + ['간트차트', '상세', '업데이트', '제거']

    if objects:  # 테이블 내 instance 존재 시 아래 코드 수행
        # remove 내 등록되어 있는 필드 제거
        object_df = pd.DataFrame.from_records(objects.values()).loc[:, form_class.Meta.fields_with_id]

        # form 에 정의된 추가 필드 정보를 DataFrame 에 추가함
        if form_additional_info:
            for key, value in form_additional_info.items():
                object_df[key] = value

        append_onclick_button('gantt', object_df, os.path.join(base_url, 'twproject', 'load'))

        # detail button (read)
        append_onclick_button('detail', object_df, os.path.join(base_url, url_path) + 'detail')

        # generate update urls, (update)
        append_onclick_button('update', object_df, os.path.join(base_url, url_path) + 'update')

        # delete button (delete)
        append_onclick_button('delete', object_df, os.path.join(base_url, url_path) + 'delete')

        object_df.columns = table_columns

        # char field 내 정보 중 코드 정보를 텍스트로 변경 (BD => '사업계획서')
        for ind, type_ in enumerate(form_inst.field_types):
            if type_ == 'CharField':
                name = form_inst.field_names[ind]
                verbose_name = form_inst.verbose_names[ind]
                field = form_inst.fields[name]
                if hasattr(field, 'choices'):
                    choices = field.choices
                    tmp_dict = {choice[0]: choice[1] for choice in choices}
                    object_df.loc[:, verbose_name] = object_df.loc[:, verbose_name].replace(to_replace=tmp_dict)



    else:  # 테이블이 하나도 존재하지 않으면 아래 코드 수행
        object_df = pd.DataFrame(columns=table_columns)

    # df -> html
    table_id = kwargs.pop('table_id', [])
    if table_id:
        table_html = object_df.to_html(escape=False, table_id=table_id)
    else:
        table_html = object_df.to_html(escape=False)

    # create button
    url = generate_url(base_url, os.path.join(url_path, 'create'))
    button_tag = create_button(url, 'create')
    crud_table = button_tag + table_html
    return crud_table


def gantt_crud_formtable_with_variable(base_url, objects, form_class, form_additional_info, url_path, **kwargs):
    """
    form 정보를 기반으로 html table 을 생성해 반환합니다.
    :param base_url:
    :param objects:
    :param form_class:
    :param form_additional_info:
    :param url_path:
    :param kwargs:
    :return:
    """

    form_inst = form_class()
    table_columns = form_inst.verbose_names + ['간트차트', '상세', '업데이트', '제거']

    if objects:  # 테이블 내 instance 존재 시 아래 코드 수행
        # remove 내 등록되어 있는 필드 제거
        object_df = pd.DataFrame.from_records(objects.values()).loc[:, form_class.Meta.fields_with_id]

        # form 에 정의된 추가 필드 정보를 DataFrame 에 추가함
        if form_additional_info:
            for key, value in form_additional_info.items():
                object_df[key] = value

        append_onclick_button('gantt', object_df, os.path.join(base_url, 'twproject', 'load'))

        # detail button (read)
        append_onclick_button('detail', object_df,
                              os.path.join(base_url, url_path) + 'detail' + '/' + str(kwargs['path_variable']))

        # generate update urls, (update)
        append_onclick_button('update', object_df,
                              os.path.join(base_url, url_path) + 'update' + '/' + str(kwargs['path_variable']))

        # delete button (delete)
        append_onclick_button('delete', object_df,
                              os.path.join(base_url, url_path) + 'delete' + '/' + str(kwargs['path_variable']))

        object_df.columns = table_columns

        # char field 내 정보 중 코드 정보를 텍스트로 변경 (BD => '사업계획서')
        for ind, type_ in enumerate(form_inst.field_types):
            if type_ == 'CharField':
                name = form_inst.field_names[ind]
                verbose_name = form_inst.verbose_names[ind]
                field = form_inst.fields[name]
                if hasattr(field, 'choices'):
                    choices = field.choices
                    tmp_dict = {choice[0]: choice[1] for choice in choices}
                    object_df.loc[:, verbose_name] = object_df.loc[:, verbose_name].replace(to_replace=tmp_dict)
            if type_ == 'ForeignKey':  # foreignkey id 을 str(foreignkey) 으로 변경
                name = form_inst.field_names[ind]
                verbose_name = form_inst.verbose_names[ind]
                field = form_inst.fields[name]
                tmp_dict = {query.id: str(query) for query in field.queryset.all()}
                object_df.loc[:, verbose_name] = object_df.loc[:, verbose_name].replace(to_replace=tmp_dict)


    else:  # 테이블이 하나도 존재하지 않으면 아래 코드 수행
        object_df = pd.DataFrame(columns=table_columns)

    # df -> html
    table_id = kwargs.pop('table_id', [])
    if table_id:
        table_html = object_df.to_html(escape=False, table_id=table_id)
    else:
        table_html = object_df.to_html(escape=False)

    # create button
    url = os.path.join(base_url, url_path) + 'create' + '/' + str(kwargs['path_variable'])
    button_tag = create_button(url, 'create')
    crud_table = button_tag + table_html
    return crud_table


def crud_formtable(base_url, objects, form_class, form_additional_info, url_path, **kwargs):
    """
    form 정보를 기반으로 html table 을 생성해 반환합니다.

    :param base_url:
    :param objects:
    :param form_class:
    :param form_additional_info
    :param url_path:
    :param kwargs:
    :return:
    """
    # form instance 생성
    form_inst = form_class()

    table_columns = form_inst.verbose_names + ['상세', '업데이트', '제거']

    # 모델 인스턴스 => DataFrame
    if objects:  # 테이블 내 instance 존재 시 아래 코드 수행
        object_df = pd.DataFrame.from_records(objects.values()).loc[:, form_class.Meta.fields_with_id]

        # form 에 정의된 추가 필드 정보를 DataFrame 에 추가함
        if form_additional_info:
            for key, value in form_additional_info.items():
                object_df[key] = value

        # detail button (read)
        append_onclick_button('detail', object_df, os.path.join(base_url, url_path) + 'detail', )

        # generate update urls, (update)
        append_onclick_button('update', object_df, os.path.join(base_url, url_path) + 'update')

        # delete button (delete)
        append_onclick_button('delete', object_df, os.path.join(base_url, url_path) + 'delete', 'btn-danger')

        object_df.columns = table_columns

        # charfield 에서 CHOICE 사용시 Text 로 변환 (BD => 사업계획서)
        for ind, type_ in enumerate(form_inst.field_types):
            if type_ == 'CharField':
                name = form_inst.field_names[ind]
                verbose_name = form_inst.verbose_names[ind]
                field = form_inst.fields[name]
                if hasattr(field, 'choices'):
                    choices = field.choices
                    tmp_dict = {choice[0]: choice[1] for choice in choices}
                    object_df.loc[:, verbose_name] = object_df.loc[:, verbose_name].replace(to_replace=tmp_dict)
            if type_ == 'ForeignKey':  # foreignkey id 을 str(foreignkey) 으로 변경
                name = form_inst.field_names[ind]
                verbose_name = form_inst.verbose_names[ind]
                field = form_inst.fields[name]
                tmp_dict = {query.id: str(query) for query in field.queryset.all()}
                object_df.loc[:, verbose_name] = object_df.loc[:, verbose_name].replace(to_replace=tmp_dict)

    else:  # 테이블이 하나도 존재하지 않으면 아래 코드 수행
        object_df = pd.DataFrame(columns=table_columns)

    # df -> html
    table_id = kwargs.pop('table_id', [])
    if table_id:
        table_html = object_df.to_html(escape=False, table_id=table_id)
    else:
        table_html = object_df.to_html(escape=False)

    # create button
    url = generate_url(base_url, os.path.join(url_path) + 'create')
    button_tag = create_button(url, 'create')
    crud_table = button_tag + table_html

    return crud_table


def instance_table(instances):
    """
    모델 인스턴스를 포함하는 테이블을 생성합니다.

    :param instances: 모델 인스턴스의 쿼리셋
    :type instances: django.db.models.query.QuerySet
    :return: 테이블을 나타내는 HTML 문자열
    :rtype: str
    """
    verbose_names = [field.verbose_name for field in instances.model._meta.fields]
    object_df = pd.DataFrame.from_records(instances.values())
    object_df.columns = verbose_names
    table_html = object_df.to_html(escape=False)
    return table_html


def crud_formtable_with_variables(base_url, objects, form_class, form_additional_info, url_path, **kwargs):
    """
    form 정보를 기반으로 html table 을 생성해 반환합니다.

    :param base_url:
    :param objects:
    :param form_class:
    :param form_additional_info
    :param url_path:
    :param kwargs:
    :return:
    """
    # form instance 생성
    form_inst = form_class()

    table_columns = form_inst.verbose_names + ['상세', '업데이트', '제거']

    # 모델 인스턴스 => DataFrame
    if objects:  # 테이블 내 instance 존재 시 아래 코드 수행
        # remove 내 등록되어 있는 필드 제거
        object_df = pd.DataFrame.from_records(objects.values()).loc[:, form_class.Meta.fields_with_id]

        # form 에 정의된 추가 필드 정보를 DataFrame 에 추가함
        if form_additional_info:
            for key, value in form_additional_info.items():
                object_df[key] = value

        # detail button (read)
        append_onclick_button('detail', object_df,
                              os.path.join(base_url, url_path) + 'detail' + '/' + str(kwargs['path_variable']))

        # generate update urls, (update)
        append_onclick_button('update', object_df,
                              os.path.join(base_url, url_path) + 'update' + '/' + str(kwargs['path_variable']))

        # delete button (delete)
        append_onclick_button('delete', object_df,
                              os.path.join(base_url, url_path) + 'delete' + '/' + str(kwargs['path_variable']))

        object_df.columns = table_columns

        # char field 내 정보 중 코드 정보를 텍스트로 변경 (BD => '사업계획서')
        for ind, type_ in enumerate(form_inst.field_types):
            # Charfield 가 CHOICES 을 사용하고 있으면 코드를 텍스트로 변환 (BD => '사업계획서')
            if type_ == 'CharField':
                name = form_inst.field_names[ind]
                verbose_name = form_inst.verbose_names[ind]
                field = form_inst.fields[name]
                if hasattr(field, 'choices'):
                    choices = field.choices
                    tmp_dict = {choice[0]: choice[1] for choice in choices}
                    object_df.loc[:, verbose_name] = object_df.loc[:, verbose_name].replace(to_replace=tmp_dict)
            if type_ == 'ForeignKey':  # foreignkey id 을 str(foreignkey) 으로 변경
                name = form_inst.field_names[ind]
                verbose_name = form_inst.verbose_names[ind]
                field = form_inst.fields[name]
                tmp_dict = {query.id: str(query) for query in field.queryset.all()}
                object_df.loc[:, verbose_name] = object_df.loc[:, verbose_name].replace(to_replace=tmp_dict)


    else:  # 테이블이 하나도 존재하지 않으면 아래 코드 수행
        object_df = pd.DataFrame(columns=table_columns)

    # df -> html
    table_id = kwargs.pop('table_id', [])
    if table_id:
        table_html = object_df.to_html(escape=False, table_id=table_id)
    else:
        table_html = object_df.to_html(escape=False)

    # create button
    url = generate_url(base_url, os.path.join(url_path) + 'create' + '/' + str(kwargs['path_variable']))
    button_tag = create_button(url, 'create')
    crud_table = button_tag + table_html

    return crud_table
