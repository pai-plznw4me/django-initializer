import os.path
from project.forms import ProjectIndexForm
from project.forms import ProjectCreateForm, ProjectUpdateForm, ProjectDetailForm
from project.models import Project
from helper import h_tag, card_row, base_form_detail
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable

def index(request):
	def _callback(**kwargs):
		pass;
	return standard_index(request, ProjectIndexForm, {}, None, 'project/', None, crud_formtable, None)

def create(request):
	def _callback(**kwargs):
		pass;
	return standard_create(request, 'standard/create.html', ProjectCreateForm, None, 'project:index', {}, None, None)

def detail(request, id):
	def _callback(**kwargs):
		pass;
	return standard_detail(request, id, 'standard/detail.html', ProjectDetailForm, None, base_form_detail, None, None)

def update(request, id):
	def _callback(**kwargs):
		pass;
	return standard_update(request, id, 'standard/update.html', ProjectUpdateForm, None, 'project:index', None, None, _callback)

def delete(request, id):
	return standard_delete(request, id, Project, 'project:index', {}, None)