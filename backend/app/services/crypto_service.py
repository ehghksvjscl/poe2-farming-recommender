"""
비밀번호 암호화/복호화 서비스

Fernet 대칭키 암호화를 사용합니다.
암호화 키는 .env의 ENCRYPTION_KEY에 저장됩니다.

사용법:
    # 키 생성 (최초 1회)
    python -c "from app.services.crypto_service import generate_key; print(generate_key())"

    # 비밀번호 암호화
    python -c "from app.services.crypto_service import encrypt; print(encrypt('비밀번호'))"

    # 비밀번호 복호화
    python -c "from app.services.crypto_service import decrypt; print(decrypt('암호화된문자열'))"
"""

import os
from cryptography.fernet import Fernet


def generate_key() -> str:
    """
    새로운 암호화 키 생성

    Returns:
        Base64 인코딩된 키 문자열

    사용법:
        키를 생성하고 .env 파일의 ENCRYPTION_KEY에 저장하세요.
    """
    key = Fernet.generate_key()
    return key.decode()


def _get_cipher():
    """Fernet 암호화 객체 생성"""
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError(
            "ENCRYPTION_KEY가 설정되지 않았습니다.\n"
            "1. 키 생성: python -c \"from app.services.crypto_service import generate_key; print(generate_key())\"\n"
            "2. .env 파일에 ENCRYPTION_KEY=생성된키 추가"
        )
    return Fernet(key.encode())


def encrypt(plain_text: str) -> str:
    """
    문자열 암호화

    Args:
        plain_text: 암호화할 문자열

    Returns:
        암호화된 문자열 (Base64)
    """
    cipher = _get_cipher()
    encrypted = cipher.encrypt(plain_text.encode())
    return encrypted.decode()


def decrypt(encrypted_text: str) -> str:
    """
    암호화된 문자열 복호화

    Args:
        encrypted_text: 암호화된 문자열

    Returns:
        복호화된 원본 문자열
    """
    cipher = _get_cipher()
    decrypted = cipher.decrypt(encrypted_text.encode())
    return decrypted.decode()


if __name__ == "__main__":
    # 테스트
    from dotenv import load_dotenv
    load_dotenv()

    print("=== 암호화 테스트 ===")

    # 키가 없으면 생성
    if not os.getenv("ENCRYPTION_KEY"):
        print(f"새 키 생성: {generate_key()}")
        print(".env 파일에 ENCRYPTION_KEY를 추가하세요.")
    else:
        test_password = "test1234"
        encrypted = encrypt(test_password)
        decrypted = decrypt(encrypted)

        print(f"원본: {test_password}")
        print(f"암호화: {encrypted}")
        print(f"복호화: {decrypted}")
        print(f"일치: {test_password == decrypted}")
