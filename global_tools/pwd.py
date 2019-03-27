import hashlib


def hashpwd(pwd):
    hashs = hashlib.md5(b'123')
    hashs.update(bytes(pwd, encoding='utf-8'))
    hash_pwd = hashs.hexdigest()
    return hash_pwd
