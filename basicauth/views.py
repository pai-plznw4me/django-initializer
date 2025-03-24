import os.path
from basicauth.forms import BasicauthIndexForm
from basicauth.forms import BasicauthCreateForm, BasicauthUpdateForm, BasicauthDetailForm
from basicauth.helper import write_settings_basicauth_default_codes, write_urls_basicauth_default_codes
from basicauth.models import Basicauth
from helper import h_tag, card_row, base_form_detail
from proj.models import Proj
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable
from initializer.settings import PROJECT_DIR
from os.path import abspath

"""
  def _callback(**kwargs):

        header_html = '<div class="p-4 border-bottom"><h3 class="mb-0"> 기본 앱 설치 목록</h3></div>'
        header_html = card_row((header_html, 12))
        kwargs['added_contents'].insert(0, header_html)


    form_additional_info = None
    return standard_index(request, BasicappIndexForm, form_additional_info, None, 'basicapp/', base_template,
                          crud_formtable, _callback, table_id='app_index_table', table_classes=('cell-border'))

"""
def index(request):

	def _callback(**kwargs):
		header_html = '<div class="p-4 border-bottom"><h3 class="mb-0"> 기본 앱 설치 목록</h3></div>'
		header_html = card_row((header_html, 12))
		kwargs['added_contents'].insert(0, header_html)

	return standard_index(request, BasicauthIndexForm, {}, None, 'basicauth/', 'doctris', crud_formtable, _callback, table_id='basicauth_index_table', table_classes=('cell-border'))

def create(request):

	def _callback(**kwargs):
		request = kwargs['request']
		if request.method == 'POST':
			app_desc = request.POST.get('desc')

			# project 폴더 접근
			project_index = request.POST.get('proj')
			proj_name = Proj.objects.get(pk=project_index).name
			project_dir = abspath(os.path.join(PROJECT_DIR, proj_name))

			# copy basicauth app
			import subprocess
			process = subprocess.Popen(
				['cp', '-R', 'resources/account', project_dir],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE)
			stdout, stderr = process.communicate()
			if stderr:
				print("Error:", stderr.decode())
			else:
				print("Success:", stdout.decode())

			# project/settings.py 파일 내 필수 코드를 생성합니다.
			write_settings_basicauth_default_codes(project_dir, proj_name)

			# project/urls.py 파일 내 필수 코드를 생성합니다.
			write_urls_basicauth_default_codes(project_dir, proj_name)


	return standard_create(request, 'standard/create.html', BasicauthCreateForm, None, 'basicauth:index', {}, 'doctris', _callback)

def detail(request, id):
	def _callback(**kwargs):
		pass;
	return standard_detail(request, id, 'standard/detail.html', BasicauthDetailForm, None, base_form_detail, 'doctris', None)

def update(request, id):
	def _callback(**kwargs):
		pass;
	return standard_update(request, id, 'standard/update.html', BasicauthUpdateForm, None, 'basicauth:index', None, 'doctris', _callback)

def delete(request, id):
	return standard_delete(request, id, Basicauth, 'basicauth:index', {}, None)