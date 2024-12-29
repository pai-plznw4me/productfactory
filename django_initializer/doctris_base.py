import os
from bs4 import BeautifulSoup
from .helper import search
import shutil


def doctris_base_app_install(project_name, app_dir='django_initializer/archives/doctris_base', dependency='django.contrib.staticfiles',
                             menu_infos=None):
    """

    :param project_name:
    :param app_dir:
    :param dependency:
    :param menu_infos:
        (main_menu_name, uil_id (name, url), (name, url) ...  (name, url)) or
        (menu_name, uil_id url)
    :return:
    """
    app_name = os.path.split(app_dir)[-1]
    assert os.path.exists(app_dir)
    # app 폴더 이동
    shutil.copytree(app_dir, os.path.join(project_name, app_name))

    # settings.py 에 정보 추가 및 수정
    setting_path = os.path.join(project_name, project_name, 'settings.py')
    with open(setting_path, 'r') as f:
        lines = f.readlines()
        index = search(lines, "{}".format(dependency))[0]
        lines[index] = lines[index] + "'{}' ,\n".format(app_name)
    with open(setting_path, 'w') as f:  # 문자열 저장
        f.writelines(lines)

    # urls.py 내 정보 추가 및 수정
    url_path = os.path.join(project_name, project_name, 'urls.py')
    with open(url_path, 'r') as f:
        lines = f.readlines()
        index = search(lines, "path('admin/', admin.site.urls),")[0]
        lines.insert(index + 1, "path('{}/', include('{}.urls'), name='{}'),\n".format(app_name, app_name, app_name))
    with open(url_path, 'w') as f:  # 문자열 저장
        f.writelines(lines)

    # doctris_menu 추가
    if menu_infos:
        side_navi_path = "{}/doctris_base/templates/doctris_base/side_navi.html".format(project_name)
        with open(side_navi_path, 'r', encoding="utf-8") as f:
            html_code = f.read()
            side_nvai_soup = BeautifulSoup(html_code, 'html.parser')
            # 메뉴 초기화, <ul> 태그 내 모든 <li> 삭제
            ul_tag = side_nvai_soup.find('ul', class_='sidebar-menu')
            for li_tag in ul_tag.find_all('li'):
                li_tag.decompose()
            # 메뉴 태그 생성
            menu_tags = []
            for menu_info in menu_infos:
                if isinstance(menu_info[2], tuple):  # nested menu tag 생성
                    menu_tag = generate_nested_menu(menu_info[0], menu_info[1], *menu_info[2:])
                elif isinstance(menu_info[2], str):  # single menu tag 생성
                    menu_tag = generate_single_menu(menu_info[0], menu_info[1], menu_info[2])
                else:
                    print('format이 잘못되었습니다.')
                menu_tags.append(menu_tag)
            joined_menu_tags = ''.join(menu_tags)
            # 생성된 메뉴 태그 추가
            menu_soup = BeautifulSoup(joined_menu_tags, 'html.parser')
            ul_tag.append(menu_soup)
            html_code = side_nvai_soup.prettify()
        with open(side_navi_path, 'w', encoding="utf-8") as f:
            f.write(html_code)



def generate_nested_menu(main_menu_name, uil_id, *sub_menu_infos):
    """
    Description:

    :param main_menu_name:
    :param uil_id:
    :arg sub_menu_infos: (name, url)
    :return:
    """

    # nested tag
    main_menu_tag = """
    <li class="sidebar-dropdown">
        <a href="javascript:void(0)"><i class="uil {} me-2 d-inline-block"></i>{}</a>
        <div class="sidebar-submenu">
            <ul>
            </ul>
        </div>
    </li>
    """.format(uil_id, main_menu_name)

    sub_menu_tags = []
    for sub_menu_info in sub_menu_infos:
        tmp_tag = "<li><a href='{}'>{}</a></li>".format(sub_menu_info[1], sub_menu_info[0])
        sub_menu_tags.append(tmp_tag)
    joined_sub_menu_tags = ''.join(sub_menu_tags)

    main_soup = BeautifulSoup(main_menu_tag, 'html.parser')
    sub_soup = BeautifulSoup(joined_sub_menu_tags, 'html.parser')
    ul_tag = main_soup.find('ul')
    ul_tag.append(sub_soup)
    return main_soup.prettify()


def generate_single_menu(menu_name, uil_id, url):
    """

    :param menu_name:
    :param uil_id:
    :param url:
    :return:
    """
    single_menu_skeleton = """<li><a href="{}"><i class="uil {} me-2 d-inline-block"></i>{}</a></li>""". \
        format(url, uil_id, menu_name)
    return single_menu_skeleton
