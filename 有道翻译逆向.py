import time
import requests
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json


#语言映射
Language = {'German':'de', 'Russian':'ru', 'French':'fr', 'Korean':'ko', 'Portuguese':'pt', 'Japanese':'ja', 'Thai':'th', 'Spanish':'es', 'Italian':'it', 'English':'en', 'Chinese':'zh-CHS', 'Vietnamese':'vi', 'Arabic':'ar', 'Polish':'pl', 'Dutch':'nl', 'Swedish':'sv'}

# 获取sign
def get_sign():
    timestamp = int(time.time() * 1000)
    e = f'client=fanyideskweb&mysticTime={timestamp}&product=webfanyi&key=fsdsogkndfokasodnaso'
    sign = hashlib.md5(e.encode()).hexdigest()
    return sign

# 获取数据
def get_response(text, from_code, to_code):
    headers = {
        'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=1948382659.381789; OUTFOX_SEARCH_USER_ID=1775497575@183.219.26.105; __yadk_uid=5QwMgTGcByPM5Fdhip58d5m1lBPBpGCW; rollNum=true; ___rl__test__cookies=1708157820132',
        'Referer': 'https://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    #'from': 'auto',
    data = {
        'i': text,
        'from': from_code,
        'to': to_code,
        'domain': '0',
        'dictResult': 'true',
        'keyid': 'webfanyi',
        'sign': get_sign(),
        'client': 'fanyideskweb',
        'product': 'webfanyi',
        'appVersion': '1.0.0',
        'vendor': 'web',
        'pointParam': 'client,mysticTime,product',
        'mysticTime': str(int(time.time() * 1000)),
        'keyfrom': 'fanyi.web',
        'mid': '1',
        'screen': '1',
        'model': '1',
        'network': 'wifi',
        'abtest': '0',
        'yduuid': 'abcdefg',
    }
    response = requests.post('https://dict.youdao.com/webtranslate', headers=headers, data=data).text
    return response
    
def encrypt_data(response):
    key = hashlib.md5("ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl".encode()).digest()
    iv = hashlib.md5("ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4".encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = base64.urlsafe_b64decode(response)

    #print(f"密文长度: {len(ciphertext)} 字节")

    if len(ciphertext) % AES.block_size != 0:
        raise ValueError("无法解密，长度错误")

    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    data = json.loads(plaintext.decode())

    #print(f"明文长度: {len(plaintext)} 字节")

    return data['translateResult'][0][0]['tgt']

if __name__ == '__main__':
    text = '吃饭了吗？'
    froms = None
    if froms is None:
        from_code = 'auto'
    else:
        from_code = Language[froms]
    to = 'Korean'
    to_code = Language[to]
    response = get_response(text, from_code, to_code)
    print(f"""{{
    "code": 200,
    "msg": "操作成功",
    "data": {{
        "text": {text},
        "from": "{froms}",
        "to": "{to}",
        "translation": "{encrypt_data(response)}"
    }}
}}""")
