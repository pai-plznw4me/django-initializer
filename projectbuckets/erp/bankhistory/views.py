import os.path
from bankhistory.forms import BankhistoryIndexForm
from bankhistory.forms import BankhistoryCreateForm, BankhistoryUpdateForm, BankhistoryDetailForm
from bankhistory.models import Bankhistory
from helper import h_tag, card_row, base_form_detail
from django.http import HttpResponse, FileResponse
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable, generate_crud_df

def index(request):
	def _callback(**kwargs):
		pass;
	return standard_index(request, BankhistoryIndexForm, {}, None, 'bankhistory/', None, crud_formtable, None)

def create(request):
	def _callback(**kwargs):
		pass;
	return standard_create(request, 'standard/create.html', BankhistoryCreateForm, None, 'bankhistory:index', {}, None, None)

def detail(request, id):
	def _callback(**kwargs):
		pass;
	return standard_detail(request, id, 'standard/detail.html', BankhistoryDetailForm, None, base_form_detail, None, None)

def update(request, id):
	def _callback(**kwargs):
		pass;
	return standard_update(request, id, 'standard/update.html', BankhistoryUpdateForm, None, 'bankhistory:index', None, None, _callback)

def delete(request, id):
	return standard_delete(request, id, Bankhistory, 'bankhistory:index', {}, None)

def download(request):
	# Fixme 아래 코드는 모든 DB정보를 가져옵니다. 지정된 대상 정보만 가져오고 싶을시 아래 코드를 수정하세요. 
	objects = Bankhistory.objects.all()
	form_additional_info = {} # 새로운 열(column) 추가하세요. 
	form_class = BankhistoryIndexForm 
	form_inst = form_class()
	if not objects:
		def _callback(**kwargs):
			error_html = '<p> 다운로드 할 데이터가 존재하지 않습니다.</p>'
			kwargs['added_contents'].append(error_html)
		BankhistoryIndexForm.errors = ['인덱스']
		return standard_index(request, BankhistoryIndexForm, {}, None, 'bankhistory/', None, crud_formtable, _callback)
	object_df = generate_crud_df(objects, form_inst, form_additional_info)
	dst_dir = './bankhistory/static/bankhistory'
	filename = 'bankhistory.csv'
	dst_path = os.path.join(dst_dir, filename)
	encoding = 'euc-kr'
	object_df.to_csv(dst_path, index=False, encoding=encoding, errors='ignore')


	return FileResponse(open(dst_path, 'rb'), as_attachment=True, filename=filename)
