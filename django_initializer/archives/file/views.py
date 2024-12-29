import os.path

from django.contrib.auth.decorators import login_required

from file.forms import FileCreateForm, FileUpdateForm, FileIndexForm, FileDetailForm
from file.models import File
from helper import h_tag, card_row, base_form_detail
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable


def index(request):
    return standard_index(request, FileIndexForm, {}, None, 'file/', None, crud_formtable, None)


def create(request):
    return standard_create(request, 'standard/create.html', FileCreateForm, None, 'file:index', {}, None, None)


def detail(request, id):
    return standard_detail(request, id, 'standard/detail.html', FileDetailForm, None, base_form_detail, None, None)


def update(request, id):
    def _callback(**kwargs):
        if kwargs['request'].method == 'GET':
            title = h_tag(2, '프로젝트 업데이트')
            kwargs['added_contents'][0] = title + card_row((kwargs['added_contents'][0], 12))

    return standard_update(request,
                           id,
                           'standard/update.html',
                           FileUpdateForm,
                           None,
                           'file:index',
                           None,
                           None,
                           _callback)


def delete(request, id):
    return standard_delete(request, id, File, 'file:index', {}, None)
