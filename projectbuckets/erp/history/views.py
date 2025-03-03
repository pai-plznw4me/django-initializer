import os.path
from history.forms import HistoryIndexForm
from history.forms import HistoryCreateForm, HistoryUpdateForm, HistoryDetailForm
from history.models import History
from helper import h_tag, card_row, base_form_detail
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable
base = 'doctris'
def index(request):
	def _callback(**kwargs):
		pass;
	return standard_index(request, HistoryIndexForm, {}, None, 'history/', base, crud_formtable, None, table_id='history_index_table', table_classes=('cell-border'))

def create(request):
	def _callback(**kwargs):
		pass;
	return standard_create(request, 'standard/create.html', HistoryCreateForm, None, 'history:index', {}, base, None)

def detail(request, id):
	def _callback(**kwargs):
		pass;
	return standard_detail(request, id, 'standard/detail.html', HistoryDetailForm, None, base_form_detail, base, None)

def update(request, id):
	def _callback(**kwargs):
		pass;
	return standard_update(request, id, 'standard/update.html', HistoryUpdateForm, None, 'history:index', None, base, _callback)

def delete(request, id):
	return standard_delete(request, id, History, 'history:index', {}, None)