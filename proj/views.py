import os.path

from django.http import FileResponse
from setuptools.compat.py311 import shutil_rmtree

from initializer.settings import PROJECT_DIR, MEDIA_URL
from proj.forms import ProjIndexForm
from proj.forms import ProjCreateForm, ProjUpdateForm, ProjDetailForm
from proj.models import Proj
from helper import h_tag, card_row, base_form_detail, create_button
from proj.project_wizard import create_standard_django_project, zip_folder
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable

base = 'doctris'


def index(request):
    def _callback(**kwargs):

        header_html = '<div class="p-4 border-bottom"><h3 class="mb-0">프로젝트 목록</h3></div>'
        header_html = card_row((header_html, 12))
        kwargs['added_contents'].insert(0, header_html)


    return standard_index(request, ProjIndexForm, {}, None, 'proj/', base, crud_formtable, _callback, table_id='proj_index', table_classes=('cell-border'))


def create(request):
    def _callback(**kwargs):
        if kwargs['request'].method == 'POST' and kwargs['form'].is_valid():
            proj_name = kwargs['request'].POST.get('name')
            if proj_name:
                proj_path = os.path.join(PROJECT_DIR, proj_name)
                create_standard_django_project(proj_path)

    if request.method == 'POST':
        proj_name = request.POST.get('name')
        form_additional_info = {'name': proj_name}
    else:
        form_additional_info = None

    return standard_create(request, 'standard/create.html', ProjCreateForm, form_additional_info, 'proj:index', {},
                           base, _callback)


def detail(request, id):
    def _callback(**kwargs):
        project_name = kwargs['model'].objects.get(pk=id).name
        download_url = "/proj/downloadproject/{}".format(id)
        button_tag = create_button(download_url, '프로젝트 \n 다운로드')
        kwargs['added_contents'].append(button_tag)

    return standard_detail(request, id, 'standard/detail.html', ProjDetailForm, None, base_form_detail, base, _callback)


def update(request, id):
    def _callback(**kwargs):
        pass;

    return standard_update(request, id, 'standard/update.html', ProjUpdateForm, None, 'proj:index', None, base,
                           _callback)


def delete(request, id):
    # callback(request=request, id=id, model=model, redirect_view=redirect_view,
    # 		 redirect_path_variables=redirect_path_variables, instance=instance, **callback_kwargs)
    def _callback(**kwargs):
        name = kwargs['instance'].name
        project_path = os.path.join(PROJECT_DIR, name)
        shutil_rmtree(project_path)

    return standard_delete(request, id, Proj, 'proj:index', {}, _callback)


def downloadproject(request, id):
    proj_name = Proj.objects.get(pk=id).name
    # 압축을 진행
    src = os.path.join(PROJECT_DIR, proj_name)
    filename= proj_name + '.zip'
    dst = os.path.join(PROJECT_DIR, filename)
    if not os.path.exists(dst):
        zip_folder(src, dst)

    return FileResponse(open(dst, 'rb'), as_attachment=True, filename=filename)
