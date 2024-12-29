import ast
import os.path

from django_initializer.account import account_app_install
from django_initializer.doctris_base import doctris_base_app_install
from django_initializer.helper import create_django_project, default_setting, default_url, migration_migrate, \
	file_download, default_filemove
from project_wizard.forms import Project_wizardIndexForm
from project_wizard.forms import Project_wizardCreateForm, Project_wizardUpdateForm, Project_wizardDetailForm
from project_wizard.models import Project_wizard
from helper import h_tag, card_row, base_form_detail
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable

def index(request):
	def _callback(**kwargs):
		pass;
	return standard_index(request, Project_wizardIndexForm, {}, None, 'project_wizard/', 'doctris',  crud_formtable, None)

def create(request):
	def _callback(**kwargs):
		if kwargs['request'].method == 'POST':

			# default django project 생성
			project_name = kwargs['request'].POST.get('name')
			create_django_project(kwargs['request'].POST.get('name'))
			default_setting(project_name)
			default_url(project_name)
			default_filemove(project_name)


			# 계정 관리 시스템 추가
			if kwargs['request'].POST.get('authtype') == 'sss':
				account_app_install(project_name)

			# ⚠️'(a, b, c)' => (a, b, c), 해당 코드는 내부적으로 eval 을 사용하는 코드로서 수정해야함
			sidenavi_list = kwargs['request'].POST.get('sidenavi')
			sidenavi_list = ast.literal_eval(sidenavi_list)
			if kwargs['request'].POST.get('template') == 'doc':
				# doctoris template 적용
				# menu_infos = [("프로필", 'uil-user', "{% url 'account:profile' %}")]
				doctris_base_app_install(project_name, menu_infos=sidenavi_list)
			migration_migrate(project_name)

	return standard_create(request, 'standard/create.html', Project_wizardCreateForm, None, 'project_wizard:index', {}, 'doctris', _callback)

def detail(request, id):
	def _callback(**kwargs):
		pass;
	return standard_detail(request, id, 'standard/detail.html', Project_wizardDetailForm, None, base_form_detail, 'doctris', None)

def update(request, id):
	def _callback(**kwargs):
		pass;
	return standard_update(request, id, 'standard/update.html', Project_wizardUpdateForm, None, 'project_wizard:index', None, 'doctris', _callback)

def delete(request, id):
	return standard_delete(request, id, Project_wizard, 'project_wizard:index', {}, None)