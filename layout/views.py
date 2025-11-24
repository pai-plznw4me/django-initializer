import json
import os.path
import shutil
import pandas as pd
from django.views.decorators.csrf import csrf_exempt

from layout.forms import LayoutIndexForm
from layout.forms import LayoutCreateForm, LayoutUpdateForm, LayoutDetailForm
from layout.helper import write_settings_layout_default_codes, write_urls_layout_default_codes, search
from layout.models import Layout
from helper import h_tag, card_row, base_form_detail
from django.http import HttpResponse, FileResponse

from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable, generate_crud_df
from proj.models import Proj
from initializer.settings import PROJECT_DIR, MEDIA_ROOT
from os.path import abspath, exists

base = 'doctris'
def index(request):
	def _callback(**kwargs):
		pass;
	return standard_index(request, LayoutIndexForm, {}, None, 'layout/', base, crud_formtable, None, table_id='index_table', table_classes=('cell-border'))

@csrf_exempt
def create(request):
	def _callback(**kwargs):
		request = kwargs['request']
		if request.method == 'POST':
			# form parsing
			layout_name = request.POST.get('name')
			favicon = request.FILES['favicon']
			logo = request.FILES['logo']

			# datatable 을 가져옵니다.
			# df columns : ['name', 'url' 'icon]
			data = json.loads(request.POST.get('datatable_data'))
			datatable_df = pd.DataFrame(data)

			# 생성된 정보를 활용해 layout 을 생성합니다.
			# project 폴더 접근
			project_index = request.POST.get('proj')
			proj_name = Proj.objects.get(pk=project_index).name
			project_dir = abspath(os.path.join(PROJECT_DIR, proj_name))

			# layout app을 프로젝트 폴더에 복사합니다.
			import subprocess
			process = subprocess.Popen(
				['cp', '-R', 'resources/{}'.format(layout_name), project_dir],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE)
			stdout, stderr = process.communicate()
			if stderr:
				print("Error:", stderr.decode())
			else:
				print("Success:", stdout.decode())

			# project/settings.py 파일 내 필수 코드를 생성합니다.
			write_settings_layout_default_codes(project_dir, proj_name, app_name=layout_name)

			# project/urls.py 파일 내 필수 코드를 생성합니다.
			write_urls_layout_default_codes(project_dir, proj_name, app_name=layout_name)

			# app dir을 생성합니다.
			app_dir = abspath(os.path.join(PROJECT_DIR, proj_name, layout_name))
			image_dir = os.path.join(app_dir, 'static', layout_name, 'images')

			valid_inst = kwargs['valid_inst']

			# 지정된 파일 저장
			from django.core.files.storage import default_storage
			favicon_path = default_storage.save(f"images/{favicon.name}", favicon)
			logo_path = default_storage.save(f"images/{logo.name}", logo)

			# favicon 파일 저장(media)
			dst =  os.path.join(image_dir, favicon.name)
			src = default_storage.save(f"{favicon.name}", favicon)
			src = os.path.join(MEDIA_ROOT, src)
			shutil.copy(src, dst)

			# logo 정보 변경
			dst =  os.path.join(image_dir, logo.name)
			src = default_storage.save(f"{logo.name}", logo)
			src = os.path.join(MEDIA_ROOT, src)
			shutil.copy(src, dst)

			# side navi 정보 변경
			templates_dir = os.path.join(app_dir, 'templates', layout_name)
			target_path = os.path.join(templates_dir, 'side_navi_items.html')
			with open(target_path, 'r') as f:
				# settings.py 에 추가할 내용
				lines = f.readlines()
			# item html 생성
			single_item = '<li><a href="{}"><i class="uil {} me-2 d-inline-block"></i>{}</a></li>\n'
			for ind, row in datatable_df.iterrows():
				lines.append(single_item.format(row.loc['url'], row.loc['icon'], row.loc['name']))
			with open(target_path, 'w') as f:
				f.writelines(lines)

			# item 을 doctirs 에 기입
			# favicon 변경
			target_path = os.path.join(templates_dir, 'base.html')
			with open(target_path, 'r') as f:
				# settings.py 에 추가할 내용
				lines = f.readlines()
			target_html = "  <link rel=\"shortcut icon\" type=\"image/x-icon\" href=\"{% static \'doctris_base/images/{# fixme #}\' %}\">"
			index = search(lines, target_html)[0]
			lines[index] = target_html.replace('{# fixme #}', favicon.name)
			with open(target_path, 'w') as f:
				f.writelines(lines)

			# item 을 doctirs 에 기입
			# logo 변경
			templates_dir = os.path.join(app_dir, 'templates', layout_name)
			target_path = os.path.join(templates_dir, 'side_navi.html')
			with open(target_path, 'r') as f:
				# settings.py 에 추가할 내용
				lines = f.readlines()
			target_html = "<img alt=\"\" class=\"logo-light-mode\" height=\"28\" src=\"{% static 'doctris_base/images/{# fixme #}' %}\"/>"
			index = search(lines, target_html)[0]
			lines[index] = target_html.replace('{# fixme #}', logo.name)
			with open(target_path, 'w') as f:
				f.writelines(lines)
			pass

	return standard_create(request, 'layout/create.html', LayoutCreateForm, None, 'layout:index', {}, base, _callback)

def detail(request, id):
	def _callback(**kwargs):
		pass;
	return standard_detail(request, id, 'standard/detail.html', LayoutDetailForm, None, base_form_detail, base, None)

def update(request, id):
	def _callback(**kwargs):
		pass;
	return standard_update(request, id, 'standard/update.html', LayoutUpdateForm, None, 'layout:index', None, base, _callback)

def delete(request, id):
	return standard_delete(request, id, Layout, 'layout:index', {}, None)

def download(request):
	# Fixme 아래 코드는 모든 DB정보를 가져옵니다. 지정된 대상 정보만 가져오고 싶을시 아래 코드를 수정하세요. 
	objects = Layout.objects.all()
	form_additional_info = {} # 새로운 열(column) 추가하세요. 
	form_class = LayoutIndexForm 
	form_inst = form_class()
	if not objects:
		def _callback(**kwargs):
			error_html = '<p> 다운로드 할 데이터가 존재하지 않습니다.</p>'
			kwargs['added_contents'].append(error_html)
		LayoutIndexForm.errors = ['인덱스']
		return standard_index(request, LayoutIndexForm, {}, None, 'layout/', base, crud_formtable, _callback,  table_id='index_table', table_classes=('cell-border'))
	object_df = generate_crud_df(objects, form_inst, form_additional_info)
	dst_dir = './layout/static/layout'
	filename = 'layout.csv'
	dst_path = os.path.join(dst_dir, filename)
	encoding = 'euc-kr'
	object_df.to_csv(dst_path, index=False, encoding=encoding, errors='ignore')


	return FileResponse(open(dst_path, 'rb'), as_attachment=True, filename=filename)
