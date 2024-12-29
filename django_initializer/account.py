import os
import shutil

from .helper import search


def account_app_install(project_name, app_dir='django_initializer/archives/account', dependency='django.contrib.staticfiles'):

    # app 이동
    app_name = os.path.split(app_dir)[-1]
    assert os.path.exists(app_dir)
    # app 폴더 이동
    shutil.copytree(app_dir, os.path.join(project_name, app_name))

    # settings.py 문자열 추가
    setting_path = os.path.join(project_name, project_name, 'settings.py')
    with open(setting_path, 'r') as f:
        # settings.py 에 추가할 내용
        lines = f.readlines()
        lines.append("AUTH_USER_MODEL = '{}.CustomUser'\n".format(app_name))
        lines.append("LOGIN_REDIRECT_URL = '/{}/profile'\n".format(app_name))

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
        lines.insert(index + 2, "path('{}/', include('django.contrib.auth.urls')), \n".format(app_name))

    with open(url_path, 'w') as f:
        f.writelines(lines)