import os.path

from django.http import HttpResponse

from company.forms import CompanyIndexForm
from company.forms import CompanyCreateForm, CompanyUpdateForm, CompanyDetailForm
from company.models import Company
from helper import h_tag, card_row, base_form_detail
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable
import pandas as pd
base='doctris'
def index(request):
	def _callback(**kwargs):
		pass;
	return standard_index(request, CompanyIndexForm, {}, None, 'company/', base, crud_formtable, None,  table_id='employee_index_table', table_classes=('cell-border'))

def create(request):
	def _callback(**kwargs):
		pass;
	return standard_create(request, 'standard/create.html', CompanyCreateForm, None, 'company:index', {}, base, None)

def detail(request, id):
	def _callback(**kwargs):
		pass;
	return standard_detail(request, id, 'standard/detail.html', CompanyDetailForm, None, base_form_detail, base, None)

def update(request, id):
	def _callback(**kwargs):
		pass;
	return standard_update(request, id, 'standard/update.html', CompanyUpdateForm, None, 'company:index', None, base, _callback)

def delete(request, id):
	return standard_delete(request, id, Company, 'company:index', {}, None)


def sync(request):
	filepath = './project/static/project/계약서리스트.xlsx'
	df = pd.read_excel(filepath)
	customers =[]
	# 고객명이 중첩되지 않도록 집합 자료구조로 변환합니다.
	for ind, row in df.iterrows():
		customer = row.iloc[7]
		customers.append(customer)
	customers = list(set(customers))

	for ind, customer in enumerate(customers):
		company = Company(id=ind, name=customer)
		company.save()


	return HttpResponse(200)

def delete_all(request):
	Company.objects.all().delete()
	return HttpResponse(200)