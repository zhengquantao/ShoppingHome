from django.test import TestCase
import hashlib
from global_tools.pwd import pwd
# Create your tests here.
hashs = hashlib.md5(b'123')  # 加密方法
hashs.update(bytes('a', encoding='utf-8'))
hash_pwd = hashs.hexdigest()
print(hash_pwd)
n = 1
