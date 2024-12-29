import os
import sys
import numpy as np
import shutil



# Django 프로젝트를 생성합니다.
def create_django_project(project_name):
    # Django 프로젝트 생성
    os.system('django-admin startproject {}'.format(project_name))


def default_setting(project_dir):
    # 셋팅 파일로 이동
    proj_name = os.path.split(project_dir)[-1]
    setting_path = os.path.join(proj_name, proj_name, 'settings.py')

    if not os.path.exists(setting_path):
        print(setting_path, '존재하지 않습니다.')

    # 문자열 수정
    with open(setting_path, 'r') as f:
        text = f.read()
        text = text.replace("'DIRS': [],", "'DIRS': [os.path.join(BASE_DIR, 'templates')],")
        text = text.replace("'OPTIONS': {", "'OPTIONS': {'libraries': {'index': 'templatetags.index'},")
    with open(setting_path, 'w') as f:
        # 문자열 저장
        f.write(text)

    # 문자열 추가
    with open(setting_path, 'r') as f:
        lines = f.readlines()
        lines.insert(0, 'import os\n')
        lines.append('DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 50\n')
        lines.append('FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 50\n')
        lines.append("MEDIA_ROOT = BASE_DIR / 'media'\n")
        lines.append("MEDIA_URL = '/media/'\n")

    with open(setting_path, 'w') as f:
        # 문자열 저장
        f.writelines(lines)


def default_url(project_dir):
    proj_name = os.path.split(project_dir)[-1]
    url_path = os.path.join(proj_name, proj_name, 'urls.py')

    # 문자열 추가
    with open(url_path, 'r') as f:
        lines = f.readlines()
        lines.insert(0, 'from {} import settings\n'.format(proj_name))
        lines.insert(0, 'from django.conf.urls.static import static\n')
        lines.insert(0, "from django.urls import include\n")

        lines.append("urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n")
    with open(url_path, 'w') as f:
        # 문자열 저장
        f.writelines(lines)

def default_filemove(project_dir):
    # 필수적인 library 및 폴더들을 옮깁니다.
    archive_root = os.path.join('django_initializer', 'archives')
    shutil.copy(os.path.join(archive_root,'helper.py'), project_dir)
    shutil.copy(os.path.join(archive_root,'standard.py'), project_dir)
    shutil.copy(os.path.join(archive_root,'tables.py'), project_dir)
    shutil.copytree(os.path.join(archive_root,'templatetags'), os.path.join(project_dir, 'templatetags') )
    shutil.copytree(os.path.join(archive_root, 'templates'), os.path.join(project_dir, 'templates'))

def version_checking_and_import():
    # Django 패키지를 가져옵니다.
    try:
        import django

        print('django version: {}'.format(django.__version__))
    except ImportError:
        django_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "django"))
        sys.path.insert(0, django_path)
        import django


def file_download(token, project_name):
    os.system('git clone https://{}@github.com/pai-seocho/django-tutorial'.format(token))
    os.chdir('django-tutorial')
    os.system('cp helper.py ../{}'.format(project_name))
    os.system('cp standard.py ../{}'.format(project_name))
    os.system('cp tables.py ../{}'.format(project_name))
    os.system('cp -R templatetags ../{}'.format(project_name))
    os.system('cp -R templates ../{}'.format(project_name))
    os.chdir('../')


def migration_migrate(project_name):
    os.chdir('{}'.format(project_name))
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate --run-sync')
    os.chdir('../')


def runserver(project_name):
    os.chdir('{}'.format(project_name))
    print(os.getcwd())
    os.system('python manage.py runserver')
    os.chdir('../')


def search(lines, str_):
    mask = [str_ in line for line in lines]
    index = list(np.where(mask)[0])
    return index

