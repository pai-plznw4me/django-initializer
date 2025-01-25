import keyword
import os
import shutil
import zipfile
from os.path import exists
from pandas.errors import EmptyDataError

def create_django_project(project_root_dir):
    """
    Django 프로젝트를 생성합니다.
    동일한 이름의 프로젝트가 이미 존재하면 새로 생성하지 않습니다.

    Args:
        project_root_dir (str): 생성할 프로젝트 경로
        ...
            |-sampleproject  <--- base_dir
                |-sampleproject
    """
    os.makedirs(project_root_dir, exist_ok=True)
    _, project_name = os.path.split(project_root_dir)[0], os.path.split(project_root_dir)[-1]
    project_dir = os.path.join(project_root_dir, project_name)
    if not exists(project_dir):
        os.system('django-admin startproject {} {}'.format(project_name, project_root_dir))
    else:
        print('Project already exists')


def default_setting(project_dir):
    """
    Django 프로젝트의 기본 설정 파일(settings.py)을 수정합니다.
    템플릿 디렉토리 설정, 템플릿 태그 추가, 업로드 용량 제한 설정 등을 포함합니다.

    Args:
        project_dir (str): 프로젝트 디렉토리 경로

    Raises:
        EmptyDataError: settings.py 파일이 존재하지 않는 경우
    """

    # 셋팅 파일로 이동
    root_dir, proj_name = os.path.split(project_dir)[0], os.path.split(project_dir)[-1]
    setting_path = os.path.join(root_dir, proj_name, proj_name, 'settings.py')

    if not os.path.exists(setting_path):
        print(setting_path, '존재하지 않습니다.')
        raise EmptyDataError

    # 문자열 수정
    with open(setting_path, 'r') as f:
        text = f.read()
        # 문자열 변경
        src = "'DIRS': [],"
        dst = "'DIRS': [os.path.join(BASE_DIR, 'templates')],"
        if src in text:
            text = text.replace(src, dst)
        else:
            print('문자열이 이미 변경되어 있습니다.')

        # 문자열 변경
        src = "'OPTIONS': {"
        dst = "'OPTIONS': {'libraries': {'index': 'templatetags.index'},"
        if dst not in text:
            text = text.replace(src, dst)
        else:
            print('문자열이 이미 변경되어 있습니다.')

    with open(setting_path, 'w') as f:
        # 문자열 저장
        f.write(text)

    # 문자열 추가
    with open(setting_path, 'r') as f:
        lines = f.readlines()
        lines.insert(0, 'import os\n')
        lines.append('DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 50\n')
        lines.append('FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 50\n')
        lines.append("MEDIA_ROOT = BASE_DIR / 'media'\n")
        lines.append("MEDIA_URL = '/media/'\n")

    with open(setting_path, 'w') as f:
        # 문자열 저장
        f.writelines(lines)


def default_url(project_dir):
    """
    Django 프로젝트의 URL 설정 파일(urls.py)을 수정합니다.
    static 및 media 파일 서빙 설정을 추가합니다.

    Args:
        project_dir (str): 프로젝트 디렉토리 경로
    """
    root_dir, proj_name = os.path.split(project_dir)[0], os.path.split(project_dir)[-1]
    url_path = os.path.join(root_dir, proj_name, proj_name, 'urls.py')

    # 문자열 추가
    with open(url_path, 'r') as f:
        lines = f.readlines()
        lines.insert(0, 'from {} import settings\n'.format(proj_name))
        lines.insert(0, 'from django.conf.urls.static import static\n')
        lines.insert(0, "from django.urls import include\n")

        lines.append("urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n")
    with open(url_path, 'w') as f:
        # 문자열 저장
        f.writelines(lines)


def default_filecopy(project_dir):
    """
    프로젝트에 필요한 기본 파일(helper.py, standard.py, tables.py)과
    디렉토리(templatetags, templates)를 복사합니다.

    Args:
        project_dir (str): 프로젝트 디렉토리 경로
    """
    # 필수적인 library 및 폴더들을 옮깁니다.
    root = os.path.join('.')
    shutil.copy(os.path.join(root,'helper.py'), project_dir)
    shutil.copy(os.path.join(root,'standard.py'), project_dir)
    shutil.copy(os.path.join(root,'tables.py'), project_dir)
    shutil.copytree(os.path.join(root,'templatetags'), os.path.join(project_dir, 'templatetags'), dirs_exist_ok=True)
    shutil.copytree(os.path.join(root, 'templates'), os.path.join(project_dir, 'templates'), dirs_exist_ok=True)

def create_standard_django_project(project_dir):
    """
    Django 프로젝트를 생성하고, 기본 설정 및 파일을 적용합니다.

    Args:
        project_name (str): 생성할 프로젝트 이름
    """
    create_django_project(project_dir)
    default_setting(project_dir)
    default_url(project_dir)
    default_filecopy(project_dir)
    print('{} 프로젝트 생성 완료'.format(project_dir))


def is_valid_django_project_name(project_name):
    """
    Django 프로젝트 이름이 명명 규칙에 맞는지 확인합니다.

    Args:
        project_name (str): Django 프로젝트 이름

    Returns:
        bool: 프로젝트 이름이 유효하면 True, 그렇지 않으면 False
        str: 유효하지 않은 경우 오류 메시지
    """
    if not project_name.isidentifier():
        return False, "프로젝트 이름은 유효한 Python 식별자여야 합니다. 알파벳, 숫자, 밑줄(_)로 구성되며 숫자로 시작할 수 없습니다."
    if keyword.iskeyword(project_name):
        return False, "프로젝트 이름은 Python 예약어가 아니어야 합니다. (예: 'class', 'def', 'import')"
    return True, "유효한 프로젝트 이름입니다."


if __name__ == '__main__':
    proj_dir = './dummy/sampleproject'
    create_django_project(proj_dir)
    default_setting(proj_dir)
    default_url(proj_dir)
    default_filecopy(proj_dir)

    test_names = [
        "sample_project",  # 유효
        "123project",      # 숫자로 시작
        "project-name",    # 하이픈 포함
        "class",           # Python 예약어
        "valid_project1"   # 유효
    ]

    for name in test_names:
        is_valid, message = is_valid_django_project_name(name)
        print(f"프로젝트 이름: {name} -> {message}")



def zip_folder(folder_path, output_zip):
    """
        주어진 폴더를 ZIP 파일로 압축합니다.

        Parameters:
        folder_path (str): 압축할 폴더의 경로
        output_zip (str): 생성될 ZIP 파일의 경로 (확장자 .zip 포함)

        예시:
        zip_folder('path/to/folder', 'output.zip')
    """
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # zipfile 내에서는 상대 경로를 사용하기 위해 파일 경로에서 폴더 부분을 제거
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)
