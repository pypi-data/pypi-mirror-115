import re

#检测ip是否正确
def check_is_ip(ip: str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    return False

#格式化数字字母以外的字符 \u4e00-\u9fa5_
def formart_name(name: str):
    if name is None:
        return ''
    else:
        return re.sub(r'^_|_$', '', re.sub(r'[^a-zA-Z0-9_]+', '_', name.strip()))