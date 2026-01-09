"""
티스토리 자동화 서비스 (Selenium)

티스토리에 자동으로 로그인하고 글을 발행하는 서비스입니다.
카카오 계정으로 로그인합니다.

사용법:
    from app.services.tistory_service import TistoryService

    service = TistoryService()
    service.login()  # 첫 로그인 (쿠키 저장됨)
    service.publish_post("제목", "본문 내용")
    service.close()
"""

import os
import time
import pickle
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class TistoryService:
    """
    티스토리 자동화 서비스

    Selenium을 사용하여 티스토리에 글을 자동으로 발행합니다.
    """

    # 쿠키 저장 경로
    COOKIE_PATH = Path(__file__).parent.parent.parent / "data" / "tistory_cookies.pkl"

    def __init__(self, headless: bool = False):
        """
        서비스 초기화

        Args:
            headless: True면 브라우저 창 없이 실행 (배포용)
                      False면 브라우저 창 띄워서 실행 (디버깅용)
        """
        self.blog_name = os.getenv("TISTORY_BLOG_NAME")
        self.kakao_email = os.getenv("KAKAO_EMAIL")

        # 암호화된 비밀번호 복호화
        encrypted_password = os.getenv("KAKAO_PASSWORD_ENCRYPTED")
        if encrypted_password:
            from .crypto_service import decrypt
            self.kakao_password = decrypt(encrypted_password)
        else:
            # 암호화 안 된 경우 (이전 버전 호환)
            self.kakao_password = os.getenv("KAKAO_PASSWORD")

        if not self.blog_name:
            raise ValueError("TISTORY_BLOG_NAME이 설정되지 않았습니다. .env 파일을 확인하세요.")

        self.driver = self._create_driver(headless)
        self.wait = WebDriverWait(self.driver, 10)

    def _create_driver(self, headless: bool) -> webdriver.Chrome:
        """Chrome 드라이버 생성"""
        options = Options()

        if headless:
            options.add_argument("--headless")

        # 기본 옵션
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        # 봇 탐지 우회 옵션
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # User-Agent 설정
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # 봇 탐지 우회
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver

    def _save_cookies(self):
        """쿠키 저장 (다음 로그인 시 재사용)"""
        self.COOKIE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(self.COOKIE_PATH, "wb") as f:
            pickle.dump(self.driver.get_cookies(), f)
        print(f"쿠키 저장됨: {self.COOKIE_PATH}")

    def _load_cookies(self) -> bool:
        """저장된 쿠키 로드"""
        if not self.COOKIE_PATH.exists():
            return False

        try:
            with open(self.COOKIE_PATH, "rb") as f:
                cookies = pickle.load(f)

            # 먼저 티스토리 도메인 접속 (쿠키 설정 전 필요)
            self.driver.get("https://www.tistory.com")
            time.sleep(1)

            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception:
                    pass  # 일부 쿠키는 도메인 문제로 실패할 수 있음

            return True
        except Exception as e:
            print(f"쿠키 로드 실패: {e}")
            return False

    def is_logged_in(self) -> bool:
        """로그인 상태 확인"""
        self.driver.get(f"https://{self.blog_name}.tistory.com/manage")
        time.sleep(2)

        # 관리 페이지에 접속 가능하면 로그인 상태
        return "manage" in self.driver.current_url and "login" not in self.driver.current_url

    def login(self) -> bool:
        """
        티스토리 로그인 (카카오 계정)

        Returns:
            로그인 성공 여부
        """
        # 1. 저장된 쿠키로 로그인 시도
        if self._load_cookies() and self.is_logged_in():
            print("쿠키로 로그인 성공")
            return True

        # 2. 쿠키 없으면 카카오 로그인
        if not self.kakao_email or not self.kakao_password:
            raise ValueError(
                "KAKAO_EMAIL, KAKAO_PASSWORD가 설정되지 않았습니다. "
                ".env 파일을 확인하세요."
            )

        print("카카오 로그인 시도...")

        try:
            # 티스토리 로그인 페이지
            self.driver.get("https://www.tistory.com/auth/login")
            time.sleep(2)

            # 카카오 로그인 버튼 클릭
            kakao_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn_login.link_kakao_id"))
            )
            kakao_btn.click()
            time.sleep(2)

            # 카카오 로그인 페이지에서 이메일 입력
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='loginId']"))
            )
            email_input.clear()
            email_input.send_keys(self.kakao_email)

            # 비밀번호 입력
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            password_input.clear()
            password_input.send_keys(self.kakao_password)

            # 로그인 버튼 클릭
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_btn.click()

            time.sleep(3)

            # 로그인 성공 확인
            if self.is_logged_in():
                print("로그인 성공!")
                self._save_cookies()
                return True
            else:
                print("로그인 실패 - 2차 인증이 필요하거나 비밀번호가 틀렸을 수 있습니다.")
                return False

        except TimeoutException:
            print("로그인 실패 - 페이지 로딩 타임아웃")
            return False
        except Exception as e:
            print(f"로그인 실패: {e}")
            return False

    def publish_post(self, title: str, content: str, category: str = None) -> dict:
        """
        티스토리에 글 발행

        Args:
            title: 글 제목
            content: 글 본문 (HTML 가능)
            category: 카테고리 이름 (선택)

        Returns:
            {"success": True/False, "url": "발행된 글 URL", "message": "결과 메시지"}
        """
        try:
            # 로그인 확인
            if not self.is_logged_in():
                if not self.login():
                    return {"success": False, "url": None, "message": "로그인 실패"}

            # 글쓰기 페이지 이동
            write_url = f"https://{self.blog_name}.tistory.com/manage/newpost"
            self.driver.get(write_url)
            time.sleep(3)

            # 제목 입력
            title_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#post-title-inp"))
            )
            title_input.clear()
            title_input.send_keys(title)

            # 본문 입력 (에디터 iframe 내부)
            # 티스토리는 에디터가 iframe 안에 있음
            try:
                # 기본 에디터 모드
                editor_iframe = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#tinymce-editor_ifr"))
                )
                self.driver.switch_to.frame(editor_iframe)

                body = self.driver.find_element(By.CSS_SELECTOR, "body")
                body.clear()

                # HTML 컨텐츠 입력
                self.driver.execute_script(
                    "arguments[0].innerHTML = arguments[1];",
                    body,
                    content.replace("\n", "<br>")
                )

                self.driver.switch_to.default_content()
            except:
                # 마크다운 에디터 모드일 경우
                try:
                    textarea = self.driver.find_element(By.CSS_SELECTOR, "textarea.CodeMirror-textarea")
                    textarea.send_keys(content)
                except:
                    print("에디터를 찾을 수 없습니다.")
                    return {"success": False, "url": None, "message": "에디터를 찾을 수 없음"}

            time.sleep(1)

            # 발행 버튼 클릭
            publish_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#publish-layer-btn"))
            )
            publish_btn.click()
            time.sleep(1)

            # 발행 확인 버튼 클릭
            confirm_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#publish-btn"))
            )
            confirm_btn.click()
            time.sleep(3)

            # 발행 완료 확인 (URL 변경 확인)
            current_url = self.driver.current_url

            if "tistory.com" in current_url and "/manage" not in current_url:
                print(f"글 발행 성공: {current_url}")
                return {"success": True, "url": current_url, "message": "발행 성공"}
            else:
                # 발행 후 관리 페이지로 리다이렉트된 경우
                return {"success": True, "url": None, "message": "발행 완료 (URL 확인 필요)"}

        except TimeoutException:
            return {"success": False, "url": None, "message": "페이지 로딩 타임아웃"}
        except Exception as e:
            return {"success": False, "url": None, "message": f"발행 실패: {str(e)}"}

    def close(self):
        """브라우저 종료"""
        if self.driver:
            self.driver.quit()
            print("브라우저 종료됨")


# 테스트용 함수
def test_login():
    """로그인 테스트 (브라우저 창 띄워서 확인)"""
    from dotenv import load_dotenv
    load_dotenv()

    service = TistoryService(headless=False)  # 브라우저 창 띄움

    try:
        if service.login():
            print("로그인 성공!")
            input("브라우저 확인 후 Enter를 누르세요...")
        else:
            print("로그인 실패!")
    finally:
        service.close()


def test_publish():
    """글 발행 테스트"""
    from dotenv import load_dotenv
    load_dotenv()

    service = TistoryService(headless=False)

    try:
        result = service.publish_post(
            title="테스트 글입니다",
            content="이 글은 자동으로 작성되었습니다.\n\n테스트 내용입니다."
        )
        print(f"결과: {result}")
    finally:
        service.close()


if __name__ == "__main__":
    test_login()
