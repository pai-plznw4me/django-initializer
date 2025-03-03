import pandas as pd
from datetime import datetime


def parse_date(date_str):
    # 월이 한 자릿수인 경우 두 자릿수로 변경
    if '.' in date_str:
        year, month = date_str.split('.')
        month = month.zfill(2)  # 한 자릿수 월을 두 자릿수로 변환
        date_str_corrected = f"{year}-{month}-01"  # 'yyyy-mm-01' 형식으로 수정
    else:
        date_str_corrected = date_str + '-01'  # 이미 yyyy-mm 형식이면 일(day)을 추가

    # datetime 객체로 변환
    return datetime.strptime(date_str_corrected, "%Y-%m-%d")

filepath = './employee/static/employee/인사카드.xlsx'
df = pd.read_excel(filepath)
df.columns = df.iloc[0]
df.drop([0], axis=0, inplace=True)
df = df.iloc[:39]
RANK_CHOICES = (('Staff', '사원'), ('Junior', '주임'), ('Assistant', '대리'), ('Manager', '과장'),
                ('Senior', '차장'), ('Deputy', '부장'),
                ('Director', '이사'), ('ExecutiveDirector', '상무'), ('ManagingDirector', '전무'),
                ('VicePresident', '부사장'), ('President', '사장'))
ROLE_CHOICES = (('CEO', '최고경영자'), ('COO', '최고운영책임자'), ('CFO', '최고재무책임자'), ('CMO', '최고마케팅책임자'),
                ('CTO', '최고기술책임자'), ('CTO', '최고전략책임자'), ('Team Leader', '팀장'), ('Team Member', '팀원'))

df['직위'] = df['직위'].replace({b: a for a, b in RANK_CHOICES})
df['직위'] = df['직위'].replace({b: a for a, b in ROLE_CHOICES})

for index, row in df.iterrows():
    name = row.이름
    identification = row.loc['직원번호']
    join = row.loc['입사 일자']
    if isinstance(join, str):
        join = datetime.strptime(join, '%Y.%m.%d')
    join = join.date().strftime('%Y-%m-%d')

    acquisition = row.loc['최종 취득일']
    address = row.loc['주소']
    phone = row.loc['전화번호']
    rank = row.loc['직급']
    role = row.loc['직급']
    resident_no = row.loc['생년월일(주민번호)']
    department = row.loc['부서']
    if department == '경영지원':
        department ='BS'
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
        type ='full time'
    elif type == '계약':
        type = 'part time'
    elif type == '프리랜서':
        type = 'freelancer'

    state = row.loc['재직여부']
    if state == '재직':
        state ='Active'
    elif state == '휴직':
        state = 'Absence'
    elif state == '퇴사':
        state = 'Departure'
