import json
import os
import shutil
from os.path import abspath

import pandas as pd
from django.views.decorators.csrf import csrf_exempt

from basicapp.apps import BasicappConfig
from basicapp.forms import BasicappIndexForm
from basicapp.forms import BasicappCreateForm, BasicappUpdateForm, BasicappDetailForm
from basicapp.models import Basicapp
from helper import h_tag, card_row, base_form_detail, create_button, add_content
from initializer.settings import PROJECT_DIR
from newapp import generate_model_base_code_lines_with_df, generate_form_base_code_lines, generate_view_base_code_lines, \
    generate_url_base_code_lines, write_settings_base_code_lines, write_view_base_code_lines, write_url_base_code_lines, \
    write_model_base_code_lines_with_df, write_form_base_code_lines
from proj.models import Proj
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable

base_template = 'doctris'


def index(request):
    def _callback(**kwargs):

        header_html = '<div class="p-4 border-bottom"><h3 class="mb-0"> 기본 앱 설치 목록</h3></div>'
        header_html = card_row((header_html, 12))
        kwargs['added_contents'].insert(0, header_html)


    form_additional_info = None
    return standard_index(request, BasicappIndexForm, form_additional_info, None, 'basicapp/', base_template,
                          crud_formtable, _callback, table_id='app_index_table', table_classes=('cell-border'))


@csrf_exempt
def create(request):
    form_additional_info = {'field_infos': BasicappConfig.FIELD_INFO}
    _callback = None

    def _callback(**kwargs):
        request = kwargs['request']
        if request.method == 'POST':
            # parsing
            app_name = request.POST.get('name')
            app_desc = request.POST.get('desc')
            db_table_name = request.POST.get('db_table_name')

            # datatable 을 가져옵니다.
            data = json.loads(request.POST.get('datatable_data'))
            datatable_df = pd.DataFrame(data)

            # project
            project_index = request.POST.get('proj')
            proj_name = Proj.objects.get(pk=project_index).name
            project_dir = abspath(os.path.join(PROJECT_DIR, proj_name))

            """
            "[{'name': 'asdfasdf', 'option': 'maxlength=100', 'type': 'CharField'}, {'name': 'asdfasdfasf', 'option': '', 'type': 'CharField'}]"
            '[{"name":"asdfasdfasdf","type":"CharField","option":"maxlength=100"},{"name":"asdfasdfas","type":"CharField","option":""}]'            
            """

            # create new app
            import subprocess
            process = subprocess.Popen(
                ['python', 'manage.py', 'startapp', app_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # move new app
            shutil.move(app_name, project_dir)
            appdir_path = os.path.join(project_dir, app_name)

            # create folder
            template_folder = os.path.join(appdir_path, 'templates', app_name)
            static_folder = os.path.join(appdir_path, 'static', app_name)
            os.makedirs(template_folder, exist_ok=True)
            os.makedirs(static_folder, exist_ok=True)


            # app/models.py 파일 변경
            write_model_base_code_lines_with_df(appdir_path, db_table_name, datatable_df)

            # app/forms.py 내 필수 코드를 생성,  crud True 시 standard CRUD 코드를 생성합니다.
            write_form_base_code_lines(appdir_path, db_table_name, app_name, crud=True)

            # app/views.py 파일에 필수 코드를 생성합니다.crud True 시 standard CRUD 코드를 생성합니다.
            write_view_base_code_lines(appdir_path, db_table_name, app_name, crud=True)

            # app/urls.py 파일 내 필수 코드를 생성합니다, crud True 시 standard CRUD 코드를 생성합니다.
            write_url_base_code_lines(appdir_path, db_table_name, app_name, crud=True)

            # project/settings.py 파일 내 필수 코드를 생성합니다.
            # 설치 하는 앱이 특정 앱 보다 나중에 설치해야 하는 경우에는 dependency 에 특정앱을 지정해주세요.
            dependency_app = 'django.contrib.staticfiles'
            write_settings_base_code_lines(project_dir, proj_name, app_name, dependency_app)


        elif kwargs['request'].method == 'GET':
            pass

    return standard_create(request, 'basicapp/create.html', BasicappCreateForm, form_additional_info,
                           'basicapp:index',
                           {},
                           base_template, _callback)


def detail(request, id):
    def _callback(**kwargs):
        pass;

    return standard_detail(request, id, 'standard/detail.html', BasicappDetailForm, None, base_form_detail,
                           base_template, None)


def update(request, id):
    def _callback(**kwargs):
        pass;

    return standard_update(request, id, 'standard/update.html', BasicappUpdateForm, None, 'basicapp:index', None,
                           base_template, _callback)


def delete(request, id):
    return standard_delete(request, id, Basicapp, 'basicapp:index', {}, None)
