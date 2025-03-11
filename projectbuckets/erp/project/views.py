import os.path
from datetime import datetime

import pandas as pd
from django.http import HttpResponse

from company.models import Company
from project.forms import ProjectIndexForm
from project.forms import ProjectCreateForm, ProjectUpdateForm, ProjectDetailForm
from project.models import Project
from helper import h_tag, card_row, base_form_detail
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable

base = 'doctris'


def index(request):
    def _callback(**kwargs):
        pass;

    return standard_index(request, ProjectIndexForm, {}, None, 'project/', base, crud_formtable, None,
                          table_id='edu_index_table', table_classes=('cell-border'))


def create(request):
    def _callback(**kwargs):
        pass;

    return standard_create(request, 'standard/create.html', ProjectCreateForm, None, 'project:index', {}, base, None)


def detail(request, id):
    def _callback(**kwargs):
        pass;

    return standard_detail(request, id, 'standard/detail.html', ProjectDetailForm, None, base_form_detail, base, None)


def update(request, id):
    def _callback(**kwargs):
        pass;

    return standard_update(request, id, 'standard/update.html', ProjectUpdateForm, None, 'project:index', None, base,
                           _callback)


def delete(request, id):
    return standard_delete(request, id, Project, 'project:index', {}, None)

def delete_all(request):
    Project.objects.all().delete()
    return HttpResponse(200)

def download(request):
    Project.objects.all().delete()
    return HttpResponse(200)



def sync(request):
    filepath = './project/static/project/계약서리스트.xlsx'
    df = pd.read_excel(filepath)
    for ind, (_, row) in enumerate(df.iterrows()):
        code, name, alias, start, end, size, customer = row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[4], row.iloc[5], \
            row.iloc[6], row.iloc[8]
        # 날짜가 아니면 None 으로 변환
        if not isinstance(start, datetime):
            start=None
        if not isinstance(end, datetime):
            end=None
        state = 'EOB'
        # 숫자가 아니면 None 으로 변환
        if not isinstance(size, int):
            size = None
        customer = Company.objects.get(name=customer)
        project = Project(code=code, name=name, alias=alias, start=start, end=end, size=size, state=state, customer=customer)

        project.save()

    return HttpResponse(200)

