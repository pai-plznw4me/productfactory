import os

from .helper import search


def approval_app_install(project_name, app_dir='PurchaseSalesRequest/approval',
                         dependency='django.contrib.staticfiles'):
    app_name = os.path.split(app_dir)[-1]

    # app 폴더 이동
    os.chdir('django-tutorial')
    os.system('cp -R {} ../{}'.format(app_dir, project_name))
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

    # urls.py 내 정보 추가 및 수정
    url_path = os.path.join(project_name, project_name, 'urls.py')
    with open(url_path, 'r') as f:
        lines = f.readlines()
        index = search(lines, "path('admin/', admin.site.urls),")[0]
        lines.insert(index + 1, "path('{}/', include('{}.urls'), name='{}'),\n".format(app_name, app_name, app_name))
    with open(url_path, 'w') as f:
        f.writelines(lines)
