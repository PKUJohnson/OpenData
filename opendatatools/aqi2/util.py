# encoding : utf-8

import base64
from Crypto.Cipher import AES, DES
import random
import hashlib

def pkcs7padding(text):
    """
    明文使用PKCS7填充
    最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
    :param text: 待加密内容(明文)
    :return:
    """
    bs = AES.block_size  # 16
    length = len(text)
    bytes_length = len(bytes(text, encoding='utf-8'))
    # tips：utf-8编码时，英文占1个byte，而中文占3个byte
    padding_size = length if(bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
    padding_text = chr(padding) * padding
    return text + padding_text

def pkcs7unpadding(text):
    """
    处理使用PKCS7填充过的数据
    :param text: 解密后的字符串
    :return:
    """
    length = len(text)
    unpadding = ord(text[length-1])
    return text[0:length-unpadding]

def aes_encrypt(key, iv, content):
    """
    AES加密
    key,iv使用同一个
    模式cbc
    填充pkcs7
    :param key: 密钥
    :param content: 加密内容
    :return:
    """
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 处理明文
    content_padding = pkcs7padding(content)
    # 加密
    encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
    # 重新编码
    result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
    return result

def aes_decrypt(key, iv, content):
    """
    AES解密
     key,iv使用同一个
    模式cbc
    去填充pkcs7
    :param key:
    :param content:
    :return:
    """
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # base64解码
    encrypt_bytes = base64.b64decode(content)
    # 解密
    decrypt_bytes = cipher.decrypt(encrypt_bytes)
    # 重新编码
    result = str(decrypt_bytes, encoding='utf8')
    # 去除填充内容
    result = pkcs7unpadding(result)
    return result

def decrypt_response(des_key, des_iv, aes_key, aes_iv, content):
    """
    AES解密
     key,iv使用同一个
    模式cbc
    去填充pkcs7
    :param key:
    :param content:
    :return:
    """
    aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    des = DES.new(des_key, DES.MODE_CBC, des_iv)
    # base64解码
    encrypt_bytes = base64.b64decode(content)
    # 解密
    decrypt_bytes = des.decrypt(encrypt_bytes)
    decrypt_bytes = base64.b64decode(decrypt_bytes)
    #decrypt_bytes = pkcs7padding(decrypt_bytes.decode()).encode("utf8")
    decrypt_bytes = aes.decrypt(decrypt_bytes)

    #base64解码
    decrypt_bytes = base64.b64decode(decrypt_bytes)
    # 重新编码
    result = str(decrypt_bytes, encoding='utf8')
    # 去除填充内容
    #result = pkcs7unpadding(result)
    return result

aes_client_key = "weJGsdsdf6FxF9=="
aes_client_iv = "sewg29nsl="
des_key = "sgfsfKsg8723jF=="
des_iv = "yfw3wexsd="
aes_server_key = "efsdsbafa6xFe8lcg=="
aes_server_iv = "o2muxyVs5cwedbQ=="

aes_client_key = hashlib.md5(aes_client_key.encode(encoding="utf8")).hexdigest()[16:32].encode("utf8")
aes_client_iv  = hashlib.md5(aes_client_iv.encode(encoding="utf8")).hexdigest()[0:16].encode("utf8")

des_key = hashlib.md5(des_key.encode(encoding="utf8")).hexdigest()[0:8].encode("utf8")
des_iv  = hashlib.md5(des_iv.encode(encoding="utf8")).hexdigest()[24:32].encode("utf8")

aes_server_key = hashlib.md5(aes_server_key.encode(encoding="utf8")).hexdigest()[16:32].encode("utf8")
aes_server_iv  = hashlib.md5(aes_server_iv.encode(encoding="utf8")).hexdigest()[0:16].encode("utf8")
