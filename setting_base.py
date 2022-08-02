import os,platform
import locale,logging
import ctypes

OS=platform.system()
def is_os_64bit():
    return platform.machine().endswith('64')
IS64BIT=is_os_64bit()
HASHADDHEAD='45acf3a1'
HASHADDTAIL='ee65h1e6'
ISS='enosim'
JTI='YPYA7p7bUd5p8nYsYqcxk83MVBPvZUKKuAdr6dTzsMQFyuUYWhfQtBMahEznPpmy'
JWTSECRET='H2Wf32ufCv4zfqcV5HuUywy2BugNGeC7sgeEsnUVTbwZUMtaKxDg5eRzpyAkhYRU'
LEEWAY=86400

LOCAL_LIST={
    "zh_list":['zh_cn', 'zh_cn.big5', 'zh_cn.euc', 'zh_hk', 'zh_hk.big5hk', 'zh_sg', 'zh_sg.gbk' , 'zh_tw', 'zh_tw.euc', 'zh_tw.euctw'],
    "ja_list":['ja', 'ja_jp', 'ja_jp.euc', 'ja_jp.mscode', 'ja_jp.pck', 'japan', 'japanese', 'japanese-euc', 'japanese.euc', 'jp_jp']
}
def detect_lang():
    windll = ctypes.windll.kernel32
    lang=locale.windows_locale[windll.GetUserDefaultUILanguage()][0:2]
    if lang=='zh':
        return 'zh_hant'
    else:
        return 'en'
LOCALE=detect_lang()

HTTP_PWD='4hNkdU5TptG22qXfrAXpcU5xAUpneUPN'
FILE_PWD='wTss7rXSKDYPzMyHGXHSwDWHbKYyTu3F'
LEEWAY=86400

