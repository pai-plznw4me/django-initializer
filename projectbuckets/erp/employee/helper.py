from datetime import datetime
import re

def generate_edu_info(employees):
    """
    직웝별 학력 정보를 생성해 반환합니다.

    Args:
        employees Querydict:
        ex) employees = Employee.objects.all()

    Returns dict:
        info_dict = {'최종 학교': final_edu_names, '최종 학과': final_edu_department, '최종 학위': final_edu_level,
                            '최종 취득일': final_edu_acquisition}
    """
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
    info_dict = {'최종 학교': final_edu_names, '최종 학과': final_edu_department, '최종 학위': final_edu_level,
                            '최종 취득일': final_edu_acquisition}
    return info_dict

def generate_history_info(employees):
    """
    직웝별 학력 정보를 생성해 반환합니다.

    Args:
        employees Querydict:
        ex) employees = Employee.objects.all()

    Returns dict:
        form_additional_info = {'최종 학교': final_edu_names, '최종 학과': final_edu_department, '최종 학위': final_edu_level,
                            '최종 취득일': final_edu_acquisition}
    """

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
    info_dict= {'과거 경력' : period_dates}

    # 현재 경력을 취합합니다.
    now_dates = [
        (employee.quit - employee.join).days if employee.quit else (datetime.today().date() - employee.join).days for
        employee in employees]
    assert len(employees) == len(period_dates)
    info_dict['현재 경력'] = now_dates
    return info_dict


def remove_invalid_characters(input_str):
    """
    주어진 문자열을 `euc-kr` 인코딩으로 변환할 수 있는지 확인하고,
    변환할 수 없는 문자가 있으면 이를 제거한 새로운 문자열을 반환합니다.

    `euc-kr` 인코딩으로 변환할 수 없는 문자는 일반적으로 유니코드 문자 중
    `euc-kr`에서 지원하지 않는 문자들입니다. 이 함수는 이러한 문자를 찾아서 제거합니다.

    Parameters:
    input_str (str): 유효성 검사 및 정제를 할 문자열.

    Returns:
    str: `euc-kr` 인코딩이 가능한 문자들만 포함된 문자열.

    예외:
    - `euc-kr`로 인코딩할 수 없는 문자가 있을 경우, 해당 문자는 제거되고 반환됩니다.
    """
    try:
        input_str.encode('euc-kr')  # euc-kr로 인코딩 시도
    except UnicodeEncodeError:
        # 인코딩이 불가능한 문자 제거
        # euc-kr에서 유효하지 않은 문자는 제거
        invalid_characters = re.compile('[^\x00-\x7F\xA1-\xFE]+')  # euc-kr의 유효한 문자 범위
        input_str = re.sub(invalid_characters, '', input_str)
    return input_str