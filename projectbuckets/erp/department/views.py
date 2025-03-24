import os.path
from department.forms import DepartmentIndexForm
from department.forms import DepartmentCreateForm, DepartmentUpdateForm, DepartmentDetailForm
from department.models import Department
from helper import h_tag, card_row, base_form_detail
from django.http import HttpResponse, FileResponse
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable, generate_crud_df

base='doctris'
def index(request):
	def _callback(**kwargs):
		pass;
	return standard_index(request, DepartmentIndexForm, {}, None, 'department/', base, crud_formtable, None,  table_id='employee_index_table', table_classes=('cell-border'))

def create(request):
	def _callback(**kwargs):
		pass;
	return standard_create(request, 'standard/create.html', DepartmentCreateForm, None, 'department:index', {}, base, None)

def detail(request, id):
	def _callback(**kwargs):
		pass;
	return standard_detail(request, id, 'standard/detail.html', DepartmentDetailForm, None, base_form_detail, base, None)

def update(request, id):
	def _callback(**kwargs):
		pass;
	return standard_update(request, id, 'standard/update.html', DepartmentUpdateForm, None, 'department:index', None, base, _callback)

def delete(request, id):
	return standard_delete(request, id, Department, 'department:index', {}, None)

def download(request):
	# Fixme 아래 코드는 모든 DB정보를 가져옵니다. 지정된 대상 정보만 가져오고 싶을시 아래 코드를 수정하세요. 
	objects = Department.objects.all()
	form_additional_info = {} # 새로운 열(column) 추가하세요. 
	form_class = DepartmentIndexForm 
	form_inst = form_class()
	if not objects:
		def _callback(**kwargs):
			error_html = '<p> 다운로드 할 데이터가 존재하지 않습니다.</p>'
			kwargs['added_contents'].append(error_html)
		DepartmentIndexForm.errors = ['인덱스']
		return standard_index(request, DepartmentIndexForm, {}, None, 'department/', None, crud_formtable, _callback)
	object_df = generate_crud_df(objects, form_inst, form_additional_info)
	dst_dir = './department/static/department'
	filename = 'department.csv'
	dst_path = os.path.join(dst_dir, filename)
	encoding = 'euc-kr'
	object_df.to_csv(dst_path, index=False, encoding=encoding, errors='ignore')


	return FileResponse(open(dst_path, 'rb'), as_attachment=True, filename=filename)


def sync(request):
	Department(name='경영지원부', desc='경영지원부').save()
	Department(name='기술개발부', desc='기술개발부').save()
	Department(name='기획교육부', desc='기획교육부').save()
	Department(name='영업부', desc='영업부').save()

	return HttpResponse(200)
