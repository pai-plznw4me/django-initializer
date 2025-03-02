def generate_sidenavi_items(**kwargs):
    """
    sidenavi item 추가 코드를 생성하여 반환합니다.
    item 종류는 크게 single 과 nested 가 있습니다.

    single item
        name : 항목 이름
        url : 항목 클릭시 이동할 url
        icon : 항목 옆에 보여지는 아이콘

    nested item
        name : 항목 이름
        icon : 항목 옆에 보여지는 아이콘
        sub name : 서브항목 이름
        sub url : 서브항목 url

    kwargs
        single item
            {이름 : (url, icon)}
        nested item
            {이름 : (icon , ((sub 이름, sub url),(sub 이름, sub url) ... (sub 이름, sub url))) }

    :return:
    """
    # sidenavi 에 item을 추가합니다.

    menu_bucket = []
    for key, value in kwargs.items():
        if isinstance(value[1][0], tuple) and len(value[1][0]) == 2:  # nested item
            icon = value[0]
            nested_contents = []
            for item in value[1]:
                name, url = item[0], item[1]
                nested_content = """<li><a href={}>{}</a></li>""".format(url, name)
                nested_contents.append(nested_content)
            nested_contents = "".join(nested_contents)  # 한 줄로 병합합니다.
            menu = """<li class="sidebar-dropdown"><a href="javascript:void(0)"><i class="uil {} me-2 d-inline-block"></i>{}</a><div class="sidebar-submenu"><ul>{}</ul></div></li>""" \
                .format(icon, key, nested_contents)

        elif isinstance(value[0], str) and len(value) == 2:  # single item
            url, icon = value[0], value[1]
            menu = """<li><a href={}><i class="uil {} me-2 d-inline-block"></i>{}</a></li>""". \
                format(url, icon, key)
        else:
            raise ValueError
        menu_bucket.append(menu)
    return "".join(menu_bucket)


def write_code(filepath, code):
    """
    파일에 지정된 코드를 작성합니다.
    :param str filepath:
    :param str code:
    :return:
    """

    f = open(filepath, 'w')
    f.write(code)
    f.close()


if __name__ == '__main__':
    items = {
        '프로필' : ('\"{% url \'account:profile\' %}\"' , 'uil-user'),
        '프로젝트': ('\"{% url \'proj:index\' %}\"', 'uil-folder-network')
    }
    code = generate_sidenavi_items(**items)
    write_code('./templates/doctris_base/side_navi_items.html', code)
    print(code)