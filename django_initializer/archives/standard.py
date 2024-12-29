"""
File: standard.py
Author: 김성중
Version: 1.3
Date: 2024-03-28

Description: 표준화 코드
"""

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from copy import deepcopy
from helper import get_base_url, add_content


def standard_index(request, form_class, form_additional_info, model_filter, url_path, base, generate_modelform_table,
                   callback, **kwargs):
    """
    표준 인덱스 뷰 함수입니다.

    :param request: HttpRequest 객체
    :param model: Django 모델 클래스 ex) Project
    :param model_filter: 모델 쿼리셋 필터링을 위한 *딕셔너리
    :param form_class: Django 폼 클래스 ex) ProjectCreateForm
    :param url_path: 문자열로 구성된 URL 경로 뒤에 create, read, update, delete 가 붙음
        ex) requisition_ -> requisition_create
        ex) approval/ -> approval/create
    :param base: 문자열로 구성된 기본 템플릿 경로
    :param callback: 선택적인 콜백 함수 (함수 혹은 메서드)
    :param callback_kwargs: 콜백 함수에 전달할 추가 키워드 인자들

    :return: HttpResponse 객체

    Usage:
        def _callback(**kwargs):
            crud_table_html = kwargs['crud_table_html']
            added_contents = kwargs['added_contents']
            title = h_tag(2, '프로젝트 목록')
            added_contents[0] = title + card_row((crud_table_html, 12))

        return standard_index(request, Project, {}, ProjectCreateForm, 'project', 'doctris', _callback)

    """
    if not model_filter:
        model_filter = {}

    # model instance 정보을 가져옵니다.
    added_contents = []
    model = form_class.Meta.model
    model_instances = model.objects.filter(**model_filter)

    # url
    full_url = request.build_absolute_uri()
    base_url = get_base_url(full_url)

    # crud standard table
    modelform_table_html = generate_modelform_table(base_url, model_instances, form_class, form_additional_info,
                                                    url_path, **kwargs)
    added_contents.append(modelform_table_html)

    # callback
    if callback:
        callback(request=request, model=model, model_filter=model_filter, form_class=form_class, url_path=url_path,
                 base=base, model_instances=model_instances, modelform_table_html=modelform_table_html,
                 added_contents=added_contents,
                 **kwargs)

    # render
    ret_html = add_content(request, base, *added_contents)
    return HttpResponse(ret_html)


def standard_create(request, template_name, form_class, form_additional_info, redirect_view, redirect_path_variables,
                    base, callback, **callback_kwargs):
    """
    표준 생성 폼 처리 뷰 함수입니다. 폼 처리 후 지정된 url로 리디렉션을 수행합니다.

    :param request: HttpRequest 객체
    :param template_name: 렌더링에 사용할 템플릿 이름
    :param form_class: 사용할 폼 클래스
    :param redirect_view: 폼 처리 완료 후 이동할 뷰 이름
    :param redirect_path_variables: 리디렉션 시 전달할 추가적인 경로 변수들 (딕셔너리 형태)
    :param callback: 선택적인 콜백 함수 (함수 혹은 메서드)
    :param callback_kwargs: 콜백 함수에 전달할 추가 키워드 인자들
    :return: HttpResponse 객체
    """

    form_additional_info = form_additional_info or {}
    redirect_path_variables = redirect_path_variables or {}

    if request.method == 'POST':
        # POST 요청 처리
        form_additional_info_ = deepcopy(form_additional_info)
        form = form_class(request.POST, request.FILES, **form_additional_info_)  # POST 데이터 및 파일 처리

        # 유효성 검사 통과 시
        if form.is_valid():
            form_additional_info_ = deepcopy(form_additional_info)
            valid_inst = form.save(commit=False, **form_additional_info_)

            # 콜백 함수 호출
            if callback:
                callback(request=request,
                         template_name=template_name,
                         form=form,
                         form_class=form_class,
                         redirect_view=redirect_view,
                         redirect_path_variables=redirect_path_variables,
                         valid_inst=valid_inst,
                         **callback_kwargs)

            # 데이터베이스에 저장
            valid_inst.save()  # TODO : valid_inst.save() 을 나중에 하는 이유는? callback function 위에 있어도 되지 않나?

            # 리디렉션
            return redirect(redirect_view, **redirect_path_variables)

        # 유효성 검사 실패시
        else:
            added_contents = []
            content = render(request, template_name=template_name, context={'form': form}).content.decode('utf-8')
            added_contents.append(content)
            if callback:
                callback(request=request,
                         template_name=template_name,
                         form=form,
                         form_class=form_class,
                         redirect_view=redirect_view,
                         redirect_path_variables=redirect_path_variables,
                         content=content,
                         **callback_kwargs)

            ret_html = add_content(request, base, *added_contents)
            return HttpResponse(ret_html)

    elif request.method == 'GET':  # GET 요청 처리
        form = form_class(**form_additional_info)  # POST 데이터 및 파일 처리

        # 폼을 렌더링하고 추가 콘텐츠 생성
        added_contents = []
        content = render(request, template_name=template_name, context={'form': form}).content.decode('utf-8')
        added_contents.append(content)

        # 콜백 함수 호출
        if callback:
            callback(request=request,
                     template_name=template_name,
                     form=form,
                     form_class=form_class,
                     redirect_view=redirect_view,
                     redirect_path_variables=redirect_path_variables,
                     added_contents=added_contents,
                     **callback_kwargs)

        # 최종 렌더링
        ret_html = add_content(request, base, *added_contents)
        return HttpResponse(ret_html)


def standard_update(request, id, template_name, form_class, form_additional_info, redirect_view,
                    redirect_path_variables, base,
                    callback, **callback_kwargs):
    """
    표준 업데이트 폼 처리 뷰 함수입니다. 폼 처리 후 리디렉션을 수행합니다.

    :param request: HttpRequest 객체
    :param id: 모델 인스턴스의 식별자
    :param template_name: 렌더링에 사용할 템플릿 이름
    :param model: Django 모델 클래스
    :param form_class: 사용할 폼 클래스
    :param redirect_view: 폼 처리 완료 후 이동할 뷰 이름
    :param redirect_path_variables: 리디렉션 시 전달할 추가적인 경로 변수들 (딕셔너리 형태)
    :param base: 문자열로 구성된 기본 템플릿 경로
    :param callback: 선택적인 콜백 함수 (함수 혹은 메서드)
    :param callback_kwargs: 콜백 함수에 전달할 추가 키워드 인자들
    :return: HttpResponse 객체
    :return:
    """
    model = form_class.Meta.model
    model_inst = model.objects.get(id=id)

    # POST 요청 처리
    if request.method == 'POST':
        if form_additional_info:
            form = form_class(request.POST, request.FILES, instance=model_inst,
                              **form_additional_info)  # <-- FILES 와 같이 입력이 되어야 한다.
        else:
            form = form_class(request.POST, request.FILES, instance=model_inst)
        # 유효성 검사 통과 시
        if form.is_valid():
            # 폼 저장
            if form_additional_info:
                valid_inst = form.save(commit=False, **form_additional_info)  # instance save
            else:
                valid_inst = form.save(commit=False)  # instance save
            # 콜백 함수 호출
            if callback:
                callback(request=request, id=id, template_name=template_name, model=model, form_class=form_class,
                         redirect_view=redirect_view, redirect_path_variables=redirect_path_variables, base=base,
                         valid_inst=valid_inst, **callback_kwargs)
            # 모델 저장
            valid_inst.save()  # instance save

            # 리디렉션
            if redirect_path_variables:  # redirect_path_variables 이 None 이 아니면
                return redirect(redirect_view, **redirect_path_variables)
            else:
                return redirect(redirect_view)
        # 유효성 검사 실패 시
        else:
            content = render(request, template_name=template_name, context={'form': form}).content
            ret_html = add_content(request, base, content)
            return HttpResponse(ret_html)

    # GET 요청 처리
    elif request.method == 'GET':
        added_contents = []
        if form_additional_info:
            form = form_class(instance=model_inst, **form_additional_info)  # <-- FILES 와 같이 입력이 되어야 한다.
        else:
            form = form_class(instance=model_inst)  # <-- FILES 와 같이 입력이 되어야 한다.
        content = render(request, template_name=template_name, context={'form': form}).content.decode('utf-8')
        added_contents.append(content)

        # 콜백 함수 호출
        if callback:
            callback(request=request, id=id, template_name=template_name, model=model, form_class=form_class,
                     redirect_view=redirect_view, redirect_path_variables=redirect_path_variables, base=base,
                     added_contents=added_contents, **callback_kwargs)
        # 최종 렌더링
        ret_html = add_content(request, base, *added_contents)
        return HttpResponse(ret_html)


def standard_detail(request, id, template_name, form_class, form_additional_info, form_detail, base, callback,
                    **callback_kwargs):
    """
    표준 디테일 뷰 함수입니다. 폼 정보를 시각화 합니다.

    :param request: HttpRequest 객체
    :param id: 모델 인스턴스의 식별자
    :form_additional_info: form 을 구성하기 위해 필요한 외부 정보, ex) Foreign key
    referenced 정보를 추출하기 위해
    :param model: Django 모델 클래스
    :param callback: 선택적인 콜백 함수 (함수 또는 메서드)
    :param callback_kwargs: 콜백 함수에 전달할 추가 키워드 인자들
    :return: HttpResponse 객체
    """

    # 모델 인스턴스 정보 추출
    model = form_class.Meta.model
    instance = model.objects.get(id=id)

    # 렌더링 될 Form 컨텐츠 생성
    added_contents = []
    form = form_class()  # form instance 생성

    # GET Request 처리 : 폼 정보를 표준 HTML로 출력합니다.
    if request.method == 'GET':
        # 표준 디테일 출력 함수 : 입력된 폼 클래스 정보와 모델 저장된 인스턴스 정보를 활용해 출력합니다.
        detail_content = form_detail(request, template_name, instance, form_class, form_additional_info)
        added_contents.append(detail_content)

        # 콜백 함수 호출
        if callback:
            callback(request=request, id=id, model=model, instance=instance, form_class=form_class,
                     detail_content=detail_content, added_contents=added_contents, form=form,
                     form_additional_info=form_additional_info,
                     **callback_kwargs)

        # HTML 반환
        ret_html = add_content(request, base, *added_contents)
        return HttpResponse(ret_html)
    else:
        raise NotImplementedError


def standard_delete(request, id, model, redirect_view, redirect_path_variables, callback, **callback_kwargs):
    """
    표준적인 삭제 동작을 수행합니다. 이 함수는 주어진 모델에서 특정 인스턴스를 삭제하고, 삭제 전에 사용자가 제공한 콜백 함수를 호출합니다.

    :param HttpRequest request: 요청 객체
    :param int id: 삭제할 인스턴스의 ID
    :param Model model: 삭제할 인스턴스가 속한 모델 클래스
    :param str redirect_view: 삭제 후에 리디렉션할 뷰의 이름 또는 경로
    :param dict redirect_path_variables: 리디렉션할 뷰에 전달할 추가적인 경로 변수
    :param function or None callback: 삭제 전에 실행할 콜백 함수
    :param dict callback_kwargs: 콜백 함수에 전달할 키워드 인수
    :return: 리디렉션 응답 객체
    :rtype: HttpResponseRedirect
    """
    instance = model.objects.get(id=id)
    if callback:
        callback(request=request, id=id, model=model, redirect_view=redirect_view,
                 redirect_path_variables=redirect_path_variables, instance=instance, **callback_kwargs)

    instance.delete()
    return redirect(to=redirect_view, **redirect_path_variables)
