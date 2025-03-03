import pandas as pd
from django.http import HttpResponse

from employee.forms import EmployeeIndexForm
from employee.forms import EmployeeCreateForm, EmployeeUpdateForm, EmployeeDetailForm
from employee.models import Employee
from helper import h_tag, card_row, base_form_detail
from standard import standard_index, standard_detail, standard_create, standard_update, standard_delete
from tables import crud_formtable
from datetime import datetime

base = 'doctris'


def index(request):
    def _callback(**kwargs):
        pass;

    # 각 직원 별 최종 학교 정보를 가져와 학교 이름, 학과, 학위, 취득일 정보를 employee 표 옆에 붙임
    # ⚠️ [0] 을 붙이는 이유는 최종 학력은 개인당 단 하나만 있음을 가정함
    # TODO: 이 행위를 하기보다는 최종학력을 저장하는게 좋을것 같다.
    employees = Employee.objects.all()
    final_educations = [
        employee.education_set.filter(final=True)[0] if employee.education_set.filter(final=True) else None for employee
        in employees]
    final_edu_names = []
    final_edu_level = []
    final_edu_department = []
    final_edu_acquisition = []
    for final_education in final_educations:
        if final_education:
            name, level, department, acquisition = final_education.name, final_education.level, final_education.department, final_education.acquisition
        else:
            name, level, department, acquisition = None, None, None, None

        final_edu_names.append(name)
        final_edu_level.append(level)
        final_edu_department.append(department)
        final_edu_acquisition.append(acquisition)
    form_additional_info = {'최종 학교': final_edu_names, '최종 학과': final_edu_department, '최종 학위': final_edu_level,
                            '최종 취득일': final_edu_acquisition}

    # 기존 경력과 현재 경력을 취합합니다.
    history_bucket = [employee.history_set.all() for employee in employees]
    period_dates = []
    for historys in history_bucket:
        period_date = 0
        for history in historys:
            join_date = history.join
            quit_date = history.quit
            period_date += (quit_date - join_date).days
        period_dates.append(period_date)
    form_additional_info['과거 경력'] = period_dates

    # 현재 경력을 취합합니다.
    now_dates = [
        (employee.quit - employee.join).days if employee.quit else (datetime.today().date() - employee.join).days for
        employee in employees]
    assert len(employees) == len(period_dates)
    form_additional_info['현재 경력'] = now_dates

    return standard_index(request, EmployeeIndexForm, form_additional_info, None, 'employee/', base, crud_formtable,
                          None, table_id='employee_index_table', table_classes=('cell-border'))


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