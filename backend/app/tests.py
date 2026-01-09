"""
블로그 자동화 시스템 API 테스트

이 파일은 블로그 자동화 시스템의 모든 API가 정상적으로 작동하는지 확인하는 테스트입니다.
테스트 실행: python manage.py test app
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Keyword, BlogPost


# =============================================================================
# 모델 테스트
# =============================================================================

class KeywordModelTest(TestCase):
    """
    키워드 모델 테스트

    키워드 모델이 데이터를 올바르게 저장하고 관리하는지 확인합니다.
    """

    def test_키워드_생성(self):
        """
        [테스트] 키워드가 정상적으로 생성되는지 확인

        시나리오:
        1. "파이썬 기초"라는 키워드를 생성한다
        2. 키워드가 데이터베이스에 저장되었는지 확인한다
        3. 기본값으로 is_active가 True인지 확인한다
        """
        keyword = Keyword.objects.create(keyword="파이썬 기초")

        self.assertEqual(keyword.keyword, "파이썬 기초")
        self.assertTrue(keyword.is_active)
        self.assertIsNotNone(keyword.created_at)

    def test_키워드_문자열_표현(self):
        """
        [테스트] 키워드 모델의 __str__ 메서드가 키워드 텍스트를 반환하는지 확인

        시나리오:
        1. 키워드를 생성한다
        2. str(키워드)가 키워드 텍스트와 같은지 확인한다

        왜 필요한가:
        - Django Admin에서 키워드를 표시할 때 사용됨
        - 디버깅할 때 객체를 쉽게 식별할 수 있음
        """
        keyword = Keyword.objects.create(keyword="Django 튜토리얼")

        self.assertEqual(str(keyword), "Django 튜토리얼")


class BlogPostModelTest(TestCase):
    """
    블로그 글 모델 테스트

    블로그 글 모델이 데이터를 올바르게 저장하고,
    키워드와의 관계가 정상적으로 작동하는지 확인합니다.
    """

    def setUp(self):
        """
        테스트 시작 전 준비 작업

        모든 블로그 글 테스트에는 키워드가 필요하므로,
        테스트마다 사용할 기본 키워드를 미리 생성해둡니다.
        """
        self.keyword = Keyword.objects.create(keyword="테스트 키워드")

    def test_블로그_글_생성(self):
        """
        [테스트] 블로그 글이 정상적으로 생성되는지 확인

        시나리오:
        1. 키워드와 연결된 블로그 글을 생성한다
        2. 제목, 본문, 상태가 올바르게 저장되었는지 확인한다
        3. 기본 상태가 'draft'(초안)인지 확인한다
        """
        post = BlogPost.objects.create(
            keyword=self.keyword,
            title="테스트 제목",
            content="테스트 본문입니다."
        )

        self.assertEqual(post.title, "테스트 제목")
        self.assertEqual(post.content, "테스트 본문입니다.")
        self.assertEqual(post.status, "draft")  # 기본값 확인
        self.assertEqual(post.keyword, self.keyword)

    def test_키워드와_블로그_글_관계(self):
        """
        [테스트] 하나의 키워드로 여러 블로그 글을 생성할 수 있는지 확인

        시나리오:
        1. 같은 키워드로 3개의 블로그 글을 생성한다
        2. 키워드.posts.count()가 3인지 확인한다

        왜 필요한가:
        - 같은 키워드로 여러 버전의 글을 생성할 수 있어야 함
        - 키워드별로 글 개수를 파악할 수 있어야 함
        """
        BlogPost.objects.create(keyword=self.keyword, title="글 1", content="내용 1")
        BlogPost.objects.create(keyword=self.keyword, title="글 2", content="내용 2")
        BlogPost.objects.create(keyword=self.keyword, title="글 3", content="내용 3")

        self.assertEqual(self.keyword.posts.count(), 3)

    def test_키워드_삭제시_블로그_글도_삭제(self):
        """
        [테스트] 키워드를 삭제하면 연결된 블로그 글도 함께 삭제되는지 확인

        시나리오:
        1. 키워드에 연결된 블로그 글 2개를 생성한다
        2. 키워드를 삭제한다
        3. 연결된 블로그 글도 모두 삭제되었는지 확인한다

        왜 필요한가:
        - 고아 데이터(키워드 없는 글)가 남으면 안 됨
        - on_delete=CASCADE 설정이 제대로 작동하는지 확인
        """
        BlogPost.objects.create(keyword=self.keyword, title="글 1", content="내용 1")
        BlogPost.objects.create(keyword=self.keyword, title="글 2", content="내용 2")

        keyword_id = self.keyword.id
        self.keyword.delete()

        # 키워드 삭제 후 관련 글도 삭제되었는지 확인
        self.assertEqual(BlogPost.objects.filter(keyword_id=keyword_id).count(), 0)


# =============================================================================
# API 테스트
# =============================================================================

class KeywordAPITest(APITestCase):
    """
    키워드 API 테스트

    키워드 CRUD(생성, 조회, 수정, 삭제) API가 정상적으로 작동하는지 확인합니다.
    """

    def test_키워드_목록_조회(self):
        """
        [테스트] GET /api/keywords/ - 키워드 목록을 조회할 수 있는지 확인

        시나리오:
        1. 키워드 3개를 생성한다
        2. GET /api/keywords/ 요청을 보낸다
        3. 응답 상태 코드가 200인지 확인한다
        4. 응답에 3개의 키워드가 포함되어 있는지 확인한다

        API 응답 예시:
        [
            {"id": 1, "keyword": "파이썬", "is_active": true, ...},
            {"id": 2, "keyword": "장고", "is_active": true, ...},
            {"id": 3, "keyword": "React", "is_active": true, ...}
        ]
        """
        Keyword.objects.create(keyword="파이썬")
        Keyword.objects.create(keyword="장고")
        Keyword.objects.create(keyword="React")

        response = self.client.get("/api/keywords/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_키워드_생성(self):
        """
        [테스트] POST /api/keywords/ - 새로운 키워드를 생성할 수 있는지 확인

        시나리오:
        1. POST 요청으로 "블로그 자동화" 키워드를 생성한다
        2. 응답 상태 코드가 201(Created)인지 확인한다
        3. 데이터베이스에 키워드가 저장되었는지 확인한다

        요청 예시:
        POST /api/keywords/
        {"keyword": "블로그 자동화"}
        """
        data = {"keyword": "블로그 자동화"}

        response = self.client.post("/api/keywords/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Keyword.objects.count(), 1)
        self.assertEqual(Keyword.objects.first().keyword, "블로그 자동화")

    def test_키워드_상세_조회(self):
        """
        [테스트] GET /api/keywords/{id}/ - 특정 키워드를 조회할 수 있는지 확인

        시나리오:
        1. 키워드를 생성한다
        2. GET /api/keywords/{id}/ 요청을 보낸다
        3. 응답에 해당 키워드 정보가 포함되어 있는지 확인한다
        """
        keyword = Keyword.objects.create(keyword="SEO 최적화")

        response = self.client.get(f"/api/keywords/{keyword.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["keyword"], "SEO 최적화")

    def test_키워드_수정(self):
        """
        [테스트] PATCH /api/keywords/{id}/ - 키워드를 수정할 수 있는지 확인

        시나리오:
        1. "파이썬" 키워드를 생성한다
        2. PATCH 요청으로 키워드를 "파이썬 고급"으로 수정한다
        3. 데이터베이스에 수정된 내용이 반영되었는지 확인한다

        왜 PATCH를 사용하나:
        - PUT은 모든 필드를 보내야 함
        - PATCH는 변경할 필드만 보내면 됨 (부분 수정)
        """
        keyword = Keyword.objects.create(keyword="파이썬")

        response = self.client.patch(
            f"/api/keywords/{keyword.id}/",
            {"keyword": "파이썬 고급"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        keyword.refresh_from_db()  # DB에서 최신 데이터 다시 로드
        self.assertEqual(keyword.keyword, "파이썬 고급")

    def test_키워드_삭제(self):
        """
        [테스트] DELETE /api/keywords/{id}/ - 키워드를 삭제할 수 있는지 확인

        시나리오:
        1. 키워드를 생성한다
        2. DELETE 요청으로 키워드를 삭제한다
        3. 응답 상태 코드가 204(No Content)인지 확인한다
        4. 데이터베이스에서 키워드가 삭제되었는지 확인한다
        """
        keyword = Keyword.objects.create(keyword="삭제할 키워드")

        response = self.client.delete(f"/api/keywords/{keyword.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Keyword.objects.count(), 0)

    def test_키워드_비활성화(self):
        """
        [테스트] 키워드의 is_active를 False로 변경할 수 있는지 확인

        시나리오:
        1. 활성화된 키워드를 생성한다 (is_active=True가 기본값)
        2. PATCH 요청으로 is_active를 False로 변경한다
        3. 키워드가 비활성화되었는지 확인한다

        왜 필요한가:
        - 키워드를 삭제하지 않고 비활성화만 하고 싶을 때
        - 나중에 다시 활성화할 수 있음
        """
        keyword = Keyword.objects.create(keyword="비활성화할 키워드")

        response = self.client.patch(
            f"/api/keywords/{keyword.id}/",
            {"is_active": False}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        keyword.refresh_from_db()
        self.assertFalse(keyword.is_active)


class BlogPostAPITest(APITestCase):
    """
    블로그 글 API 테스트

    블로그 글 조회 및 글 생성 API가 정상적으로 작동하는지 확인합니다.
    """

    def setUp(self):
        """테스트용 키워드 생성"""
        self.keyword = Keyword.objects.create(keyword="테스트 키워드")

    def test_블로그_글_목록_조회(self):
        """
        [테스트] GET /api/posts/ - 블로그 글 목록을 조회할 수 있는지 확인

        시나리오:
        1. 블로그 글 2개를 생성한다
        2. GET /api/posts/ 요청을 보낸다
        3. 응답에 2개의 글이 포함되어 있는지 확인한다
        """
        BlogPost.objects.create(keyword=self.keyword, title="글 1", content="내용 1")
        BlogPost.objects.create(keyword=self.keyword, title="글 2", content="내용 2")

        response = self.client.get("/api/posts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_블로그_글_상세_조회(self):
        """
        [테스트] GET /api/posts/{id}/ - 특정 블로그 글을 조회할 수 있는지 확인

        시나리오:
        1. 블로그 글을 생성한다
        2. GET /api/posts/{id}/ 요청을 보낸다
        3. 응답에 제목, 본문, 키워드 정보가 포함되어 있는지 확인한다
        """
        post = BlogPost.objects.create(
            keyword=self.keyword,
            title="상세 조회 테스트",
            content="본문 내용입니다."
        )

        response = self.client.get(f"/api/posts/{post.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "상세 조회 테스트")
        self.assertEqual(response.data["content"], "본문 내용입니다.")
        self.assertEqual(response.data["keyword_text"], "테스트 키워드")


class GeneratePostAPITest(APITestCase):
    """
    블로그 글 생성 API 테스트

    키워드를 입력하면 AI가 블로그 글을 생성하는 API가 정상적으로 작동하는지 확인합니다.
    (현재 AI API 키가 없으면 mock 데이터로 동작합니다)
    """

    def test_키워드로_블로그_글_생성(self):
        """
        [테스트] POST /api/generate/ - 키워드로 블로그 글을 생성할 수 있는지 확인

        시나리오:
        1. POST 요청으로 "파이썬 기초" 키워드를 보낸다
        2. 응답 상태 코드가 201(Created)인지 확인한다
        3. 응답에 제목과 본문이 포함되어 있는지 확인한다
        4. 키워드와 블로그 글이 데이터베이스에 저장되었는지 확인한다

        요청 예시:
        POST /api/generate/
        {"keyword": "파이썬 기초"}

        응답 예시:
        {
            "id": 1,
            "keyword": 1,
            "keyword_text": "파이썬 기초",
            "title": "파이썬 기초 - 완벽 가이드",
            "content": "## 파이썬 기초란?...",
            "status": "draft",
            ...
        }
        """
        data = {"keyword": "파이썬 기초"}

        response = self.client.post("/api/generate/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("title", response.data)
        self.assertIn("content", response.data)
        self.assertEqual(response.data["status"], "draft")

        # 데이터베이스 저장 확인
        self.assertEqual(Keyword.objects.count(), 1)
        self.assertEqual(BlogPost.objects.count(), 1)

    def test_같은_키워드로_여러_글_생성(self):
        """
        [테스트] 같은 키워드로 여러 번 글을 생성할 수 있는지 확인

        시나리오:
        1. "Django" 키워드로 글을 2번 생성한다
        2. 키워드는 1개만 생성되어야 한다 (중복 생성 안 됨)
        3. 블로그 글은 2개가 생성되어야 한다

        왜 필요한가:
        - 같은 키워드로 여러 버전의 글을 생성하고 비교할 수 있어야 함
        - 마음에 드는 글이 나올 때까지 여러 번 생성할 수 있어야 함
        """
        self.client.post("/api/generate/", {"keyword": "Django"})
        self.client.post("/api/generate/", {"keyword": "Django"})

        self.assertEqual(Keyword.objects.count(), 1)  # 키워드는 중복 안 됨
        self.assertEqual(BlogPost.objects.count(), 2)  # 글은 2개

    def test_빈_키워드로_글_생성_실패(self):
        """
        [테스트] 빈 키워드로는 글을 생성할 수 없는지 확인

        시나리오:
        1. 빈 문자열로 글 생성 요청을 보낸다
        2. 응답 상태 코드가 400(Bad Request)인지 확인한다

        왜 필요한가:
        - 유효하지 않은 입력에 대한 에러 처리가 되어야 함
        - 빈 키워드로 글을 생성하면 의미가 없음
        """
        response = self.client.post("/api/generate/", {"keyword": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_키워드_없이_글_생성_실패(self):
        """
        [테스트] 키워드 필드 없이 요청하면 실패하는지 확인

        시나리오:
        1. 키워드 필드 없이 글 생성 요청을 보낸다
        2. 응답 상태 코드가 400(Bad Request)인지 확인한다

        왜 필요한가:
        - 필수 필드가 없을 때 적절한 에러 응답을 해야 함
        """
        response = self.client.post("/api/generate/", {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HealthCheckAPITest(APITestCase):
    """
    헬스체크 API 테스트

    서버가 정상적으로 작동하는지 확인하는 헬스체크 API를 테스트합니다.
    """

    def test_헬스체크(self):
        """
        [테스트] GET /api/health/ - 서버가 정상 작동하는지 확인

        시나리오:
        1. GET /api/health/ 요청을 보낸다
        2. 응답 상태 코드가 200인지 확인한다
        3. 응답에 status가 "ok"인지 확인한다

        왜 필요한가:
        - 배포 후 서버가 살아있는지 모니터링할 때 사용
        - 로드밸런서가 서버 상태를 체크할 때 사용
        """
        response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "ok")
