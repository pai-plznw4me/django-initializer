import os
import numpy as np


def search(lines, str_, ignore_space=False):
    if ignore_space:
        mask = [str_.replace(' ', '').replace('\t', '').replace('\n', '') in line.replace(' ', '').replace('\t', '').replace('\n', '') for line in lines]
    else:
        mask = [str_ in line for line in lines]

    index = list(np.where(mask)[0])
    return index


def write_settings_layout_default_codes(project_dir, project_name, app_name,
dependency='django.contrib.staticfiles'):
    """
    project dir 내 settings.py 에 아래 순서대로 코드를 생성 및 추가합니다.
    1. app 추가
    2. app url 등록
    :param project_name:
    :param app_name:
    :param dependency:
    :return:
    """

    setting_path = os.path.join(project_dir, project_name, 'settings.py')
    with open(setting_path, 'r') as f:
        # settings.py 에 추가할 내용
        lines = f.readlines()

        # app 추가, dependency 코드 아래에 추가합니다. app 코드를 추가합니다.
        index = search(lines, "{}".format(dependency))[0]
        if index:
            lines[index] = lines[index] + "'{}' ,\n".format(app_name)
        else:
            raise ValueError('적절한 dependency 코드를 찾지 못하였습니다. \n적절한 코드를 임력해주세요. ex)django.contrib.staticfiles')
            # 문자열 저장

        # 코드 등록
        lines.append("AUTH_USER_MODEL = 'account.CustomUser' \n")
        if not search(lines, 'MEDIA_ROOT'):
            lines.append("MEDIA_ROOT = BASE_DIR / 'media' \n")
        if not search(lines, 'MEDIA_URL'):
            lines.append("MEDIA_URL = '/media/' # <-- 추가된 코드 \n")
        lines.append("LOGIN_REDIRECT_URL = '/account/profile' #\n")

    with open(setting_path, 'w') as f:
        f.writelines(lines)


def write_urls_layout_default_codes(project_dir, project_name, app_name):
    """
    project dir 내 urls.py 에 layout.urls 정보를 등록합니다.

    :param str project_dir: 프로젝트 폴더 명
    :param str project_name: 프로젝트 명
    :param str app_name: 앱 이름 (account로 기본 고정)
    :return:
    """
    # urls.py 문자열 추가
    url_path = os.path.join(project_dir, project_name, 'urls.py')
    with open(url_path, 'r') as f:
        lines = f.readlines()

        index = search(lines, "path('admin/', admin.site.urls),")[0]
        lines.insert(index + 1, "path('{}/', include('{}.urls'), name='{}'),\n".format(app_name, app_name, app_name))

        if not search(lines, "urlpatterns += static"):
            lines.append("urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n")
    with open(url_path, 'w') as f:
        f.writelines(lines)
