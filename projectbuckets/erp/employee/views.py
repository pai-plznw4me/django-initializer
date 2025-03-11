import os

import pandas as pd
from django.http import HttpResponse, FileResponse

from employee.forms import EmployeeIndexForm
from employee.forms import EmployeeCreateForm, EmployeeUpdateForm, EmployeeDetailForm
from employee.helper import generate_edu_info, generate_history_info, remove_invalid_characters
from employee.models import Employee
from helper import card_row, base_form_detail
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable, generate_crud_df
from datetime import datetime

base = 'doctris'

def index(request):
    def _callback(**kwargs):
        pass;

    # 각 직원 별 최종 학교 정보를 가져와 학교 이름, 학과, 학위, 취득일 정보를 employee 표 옆에 붙임
    # ⚠️ [0] 을 붙이는 이유는 최종 학력은 개인당 단 하나만 있음을 가정함
    # TODO: 이 행위를 하기보다는 최종학력을 저장하는게 좋을것 같다.

    employees = Employee.objects.all()
    # 직웝별 학력 정보를 생성해 반환합니다.
    edu_info = generate_edu_info(employees)
    history_info = generate_history_info(employees)
    form_additional_info = {**edu_info, **history_info}

    def _callback(**kwargs):
        # 표 위에 헤더 정보 입니다.
        header_html = '<div class="p-2 border-bottom"><h3 class="mb-0">임직원 리스트</h3><p>직원리스트를 보여줍니다.</p></div>'
        header_html = card_row((header_html, 12))
        kwargs['added_contents'].insert(0, header_html)

    return standard_index(request, EmployeeIndexForm, form_additional_info, None, 'employee/', base, crud_formtable,
                          _callback, table_id='employee_index_table', table_classes=('cell-border'))


def create(request):
    def _callback(**kwargs):
        pass;

    return standard_create(request, 'standard/create.html', EmployeeCreateForm, None, 'employee:index', {}, base, None)


def detail(request, id):
    def _callback(**kwargs):
        pass;

    return standard_detail(request, id, 'standard/detail.html', EmployeeDetailForm, None, base_form_detail, base, None)


def update(request, id):
    def _callback(**kwargs):
        pass;

    return standard_update(request, id, 'standard/update.html', EmployeeUpdateForm, None, 'employee:index', None, base,
                           _callback)


def delete(request, id):
    return standard_delete(request, id, Employee, 'employee:index', {}, None)


def sync(request):
    filepath = './employee/static/employee/인사카드.xlsx'
    df = pd.read_excel(filepath)
    df.columns = df.iloc[0]
    df.drop([0], axis=0, inplace=True)
    df = df.iloc[:39]
    # change verbose to full name
    df['직위'] = df['직위'].replace({b: a for a, b in Employee.RANK_CHOICES})
    df['직책'] = df['직책'].replace({b: a for a, b in Employee.ROLE_CHOICES})

    for index, row in df.iterrows():
        name = row.이름
        identification = row.loc['직원번호']

        join = row.loc['입사 일자']
        # yyyy.mm.dd -> yyyy-mm-dd
        if isinstance(join, str):
            join = datetime.strptime(join, '%Y.%m.%d')
        join = join.date().strftime("%Y-%m-%d")

        address = row.loc['주소']
        phone = row.loc['전화번호']

        rank = row.loc['직위']

        role = row.loc['직책']
        resident_no = row.loc['생년월일(주민번호)']
        department = row.loc['부서']
        if department == '경영지원':
            department = 'BS'
        elif department == '기술개발':
            department = 'TD'
        elif department == '기획교육':
            department = 'PME'
        elif department == '영업':
            department = 'SAL'
        else:
            raise NotImplementedError

        type = row.loc['정규/계약']
        if type == '정규':
            type = 'full time'
        elif type == '계약':
            type = 'part time'
        elif type == '프리랜서':
            type = 'freelancer'

        state = row.loc['재직여부']
        if state == '재직':
            state = 'Active'
        elif state == '휴직':
            state = 'Absence'
        elif state == '퇴사':
            state = 'Departure'

        employee = Employee(name=name, identification=identification, join=join, address=address, phone=phone,
                            state=state, rank=rank, role=role, resident_no=resident_no, department=department, type=type)
        employee.save()
    return HttpResponse(200)

def download(request):
    employees = Employee.objects.all()
    edu_info = generate_edu_info(employees)
    history_info = generate_history_info(employees)
    form_additional_info = {**edu_info, **history_info}

    form_class = EmployeeIndexForm
    form_inst = form_class()
    object_df = generate_crud_df(employees, form_inst, form_additional_info)
    dst_dir = './employee/static/employee'
    filename = '{}.csv'.format('objects')
    dst_path = os.path.join(dst_dir, filename)
    encoding = 'euc-kr'
    # 파일을 저장합니다.
    object_df.to_csv(dst_path, index=False, encoding=encoding, errors='ignore')



    return FileResponse(open(dst_path, 'rb'), as_attachment=True, filename=filename)