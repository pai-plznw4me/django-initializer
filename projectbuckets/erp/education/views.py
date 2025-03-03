import os.path

from django.http import HttpResponse

from education.forms import EducationIndexForm
from education.forms import EducationCreateForm, EducationUpdateForm, EducationDetailForm
from education.models import Education
from employee.models import Employee
from helper import h_tag, card_row, base_form_detail
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable
from datetime import datetime
import pandas as pd

base = 'doctris'


def index(request):
    def _callback(**kwargs):
        pass;

    return standard_index(request, EducationIndexForm, {}, None, 'education/', base, crud_formtable, None,
                          table_id='edu_index_table', table_classes=('cell-border'))


def create(request):
    def _callback(**kwargs):
        pass;

    return standard_create(request, 'standard/create.html', EducationCreateForm, None, 'education:index', {}, base,
                           None)


def detail(request, id):
    def _callback(**kwargs):
        pass;

    return standard_detail(request, id, 'standard/detail.html', EducationDetailForm, None, base_form_detail, base, None)


def update(request, id):
    def _callback(**kwargs):
        pass;

    return standard_update(request, id, 'standard/update.html', EducationUpdateForm, None, 'education:index', None,
                           base, _callback)


def delete(request, id):
    return standard_delete(request, id, Education, 'education:index', {}, None)


def sync(request):
    filepath = './employee/static/employee/인사카드.xlsx'
    df = pd.read_excel(filepath)
    df.columns = df.iloc[0]
    df.drop([0], axis=0, inplace=True)
    df = df.iloc[:39]
    # change verbose name to full name
    mapepr = {b: a for (a, b) in Education.LEVEL_CHOICES}
    df.loc[:, '최종 학력'] = df.loc[:, '최종 학력'].replace(mapepr)

    for index, row in df.iterrows():
        acquisition = row.loc['최종 취득일']
        # 취득일이 날짜가 아니면 None 으로 합니다.
        if not isinstance(acquisition, datetime):
            acquisition = None

        kwargs = {
            'employee': Employee.objects.get(identification=row.loc['직원번호']),
            'name': row.loc['최종학교'],
            'department': row.loc['학과'],
            'acquisition': acquisition,
            'level': row.loc['최종 학력'],
        }
        edu = Education(**kwargs)
        edu.save()
    return HttpResponse(200)