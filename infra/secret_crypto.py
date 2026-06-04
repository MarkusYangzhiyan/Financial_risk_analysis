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
    生成 Fernet 主密钥。

    该密钥只需要生成一次，后续应保存为 APP_SECRET_KEY，
    用来加密新的明文配置，或解密已经保存的密文配置。

    Returns:
        str: URL-safe base64 编码后的 Fernet 密钥字符串。
    """
    return Fernet.generate_key().decode()


def encrypt_text(plain_text: str, master_key: str) -> str:
    """
    使用主密钥加密明文字符串。

    Args:
        plain_text: 需要加密的原始文本，例如真实的 API Key。
        master_key: generate_master_key 生成并保存的 Fernet 主密钥。

    Returns:
        str: 可保存到配置文件或环境变量中的密文字符串。
    """
    # Fernet 接收 bytes 类型密钥，因此先将字符串形式的主密钥编码。
    fernet = Fernet(master_key.encode())
    # 加密结果也是 bytes，解码为字符串后便于写入 .env 或其他配置。
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
    # 解密必须使用与加密时完全相同的主密钥。
    fernet = Fernet(master_key.encode())
    return fernet.decrypt(encrypted_text.encode()).decode()


if __name__ == "__main__":
    # 该脚本块用于本地初始化，不会在作为模块导入时执行。

    # 第一步：一次性生成主密钥，并将输出值保存为 APP_SECRET_KEY。
    master_key = generate_master_key()
    print("APP_SECRET_KEY=", master_key)

    # 第二步：用主密钥加密真实的 DeepSeek API Key。
    # 这里使用占位值演示流程，实际使用时替换为真实密钥。
    api_key = "sk-123456789"
    encrypted_api_key = encrypt_text(api_key, master_key)
    print("DEEPSEEK_API_KEY_ENC=", encrypted_api_key)
