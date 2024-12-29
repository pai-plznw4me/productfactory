from .account import account_app_install
from .approval import approval_app_install
from .apps import new_app_install
from .doctris_base import doctris_base_app_install
from .file import file_app_install
from .helper import create_django_project, default_setting, default_url, file_download, migration_migrate, runserver, \
    version_checking_and_import
from .twproject import twproject_app_install


if __name__ == "__main__":
    version_checking_and_import()
    project_name = input("Enter the project name: ")
    create_django_project(project_name)
    default_setting(project_name)
    default_url(project_name)
    token = input("Enter git token: ")
    file_download(token, project_name)
    account_app_install(project_name)
    file_app_install(project_name)
    # approval_app_install(project_name)
    twproject_app_install(project_name)
    menu_infos = [("프로필", 'uil-user', "{% url 'account:profile' %}"),
                  # ("구매 요청 관리", 'uil-transaction', "{% url 'approval:requisition_index' %}"),
                  ("프로젝트 관리", 'uil-apps', " "),
                  ("결제 관리", 'uil-transaction', ('구매', ' '), ('판매', ' ')),
                  ("자원 관리", 'uil-archive', " "),
                  ("산출물 관리", 'uil-files-landscapes-alt', " "),
                  ("인력 관리", 'uil-user-arrows', " ")]
    doctris_base_app_install(project_name, menu_infos=menu_infos)
    new_app_install(project_name, 'project_wizard')
    migration_migrate(project_name)
    runserver(project_name)
