import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

"""
敏感配置加密工具。

本模块使用 Fernet 对称加密生成主密钥，并用该主密钥加密/解密
配置文件中的敏感字符串，例如 API Key、Token 等。
"""


def generate_master_key() -> str:
    """
    生成随机密钥，类型是bytes
    把bytes转成字符串
    返回字符串密钥
    """
    key_bytes = Fernet.generate_key()
    key_str = key_bytes.decode()
    return key_str



def encrypt_text(plain_text: str, master_key: str) -> str:
    """
    用generate_master_key生成的密钥
    把明文字符串(如API_KEY)加密成密文字符串

    Args:
        plain_text: 需要加密的原始文本，例如真实的 API Key。
        master_key: generate_master_key 生成并保存的 Fernet 主密钥。

    Returns:
        str: 可保存到配置文件或环境变量中的密文字符串。
    """
    # 先把字符串密钥转成bytes，然后创建一个Fernet加密实例
    fernet = Fernet(master_key.encode())
    # 把明文密码加密，明文密码也要先转成bytes，然后加密，加密后再转回成str,方便写入.env
    return fernet.encrypt(plain_text.encode()).decode()


def decrypt_text(encrypted_text: str, master_key: str) -> str:
    """
    使用主密钥解密密文字符串。

    Args:
        encrypted_text: encrypt_text 生成的密文字符串。
        master_key: 加密时使用的同一个 Fernet 主密钥。

    Returns:
        str: 解密后的原始明文。
    """

    fernet = Fernet(master_key.encode())
    return fernet.decrypt(encrypted_text.encode()).decode()


if __name__ == "__main__":
    master_key = generate_master_key()
    api_key = ""
    encrypted_api_key = encrypt_text(api_key, master_key)
    print(encrypted_api_key)
