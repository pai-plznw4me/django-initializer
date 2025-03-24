import os.path

import pandas as pd

from bankbook.forms import BankbookIndexForm
from bankbook.forms import BankbookCreateForm, BankbookUpdateForm, BankbookDetailForm
from bankbook.models import Bankbook
from helper import h_tag, card_row, base_form_detail
from django.http import HttpResponse, FileResponse
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable, generate_crud_df

def index(request):
	def _callback(**kwargs):
		pass;
	return standard_index(request, BankbookIndexForm, {}, None, 'bankbook/', None, crud_formtable, None)

def create(request):
	def _callback(**kwargs):
		pass;
	return standard_create(request, 'standard/create.html', BankbookCreateForm, None, 'bankbook:index', {}, None, None)

def detail(request, id):
	def _callback(**kwargs):
		pass;
	return standard_detail(request, id, 'standard/detail.html', BankbookDetailForm, None, base_form_detail, None, None)

def update(request, id):
	def _callback(**kwargs):
		pass;
	return standard_update(request, id, 'standard/update.html', BankbookUpdateForm, None, 'bankbook:index', None, None, _callback)

def delete(request, id):
	return standard_delete(request, id, Bankbook, 'bankbook:index', {}, None)



def download(request):
	# Fixme 아래 코드는 모든 DB정보를 가져옵니다. 지정된 대상 정보만 가져오고 싶을시 아래 코드를 수정하세요. 
	objects = Bankbook.objects.all()
	form_additional_info = {} # 새로운 열(column) 추가하세요. 
	form_class = BankbookIndexForm 
	form_inst = form_class()
	if not objects:
		def _callback(**kwargs):
			error_html = '<p> 다운로드 할 데이터가 존재하지 않습니다.</p>'
			kwargs['added_contents'].append(error_html)
		BankbookIndexForm.errors = ['인덱스']
		return standard_index(request, BankbookIndexForm, {}, None, 'bankbook/', None, crud_formtable, _callback)
	object_df = generate_crud_df(objects, form_inst, form_additional_info)
	dst_dir = './bankbook/static/bankbook'
	filename = 'bankbook.csv'
	dst_path = os.path.join(dst_dir, filename)
	encoding = 'euc-kr'
	object_df.to_csv(dst_path, index=False, encoding=encoding, errors='ignore')


	return FileResponse(open(dst_path, 'rb'), as_attachment=True, filename=filename)

def sync(request):
	filepath = './bankbook/static/bankbook/은행목록.xlsx'
	df = pd.read_excel(filepath)

	for ind, row in df.iterrows():
		name, code, alias = row.loc['은행'], row.loc['계좌번호'], row.loc['별명']
		Bankbook(owner='(주)퍼블릭에이아이', bank_name=name, account_code=code, alias=alias).save()
	return HttpResponse(200)