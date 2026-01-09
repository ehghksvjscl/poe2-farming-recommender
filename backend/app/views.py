from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status

from .models import Keyword, BlogPost
from .serializers import KeywordSerializer, BlogPostSerializer, GeneratePostSerializer


class HealthCheckView(APIView):
    """API 헬스체크 엔드포인트"""

    def get(self, request):
        return Response({"status": "ok", "message": "API is running"})


class KeywordViewSet(viewsets.ModelViewSet):
    """키워드 CRUD API"""
    queryset = Keyword.objects.all().order_by('-created_at')
    serializer_class = KeywordSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    """블로그 글 CRUD API"""
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer


class GeneratePostView(APIView):
    """키워드로 블로그 글 생성 API"""

    def post(self, request):
        serializer = GeneratePostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        keyword_text = serializer.validated_data['keyword']

        # 키워드 저장 (없으면 생성)
        keyword, _ = Keyword.objects.get_or_create(keyword=keyword_text)

        # AI로 글 생성 시도
        try:
            from .services.openai_service import generate_blog_post
            result = generate_blog_post(keyword_text)
            title = result['title']
            content = result['content']
        except Exception as e:
            # API 키 없거나 에러시 mock 데이터 반환
            title = f"{keyword_text} - 완벽 가이드"
            content = f"""## {keyword_text}란?

{keyword_text}에 대해 알아보겠습니다.

## 주요 특징

1. 첫 번째 특징
2. 두 번째 특징
3. 세 번째 특징

## 결론

{keyword_text}는 매우 유용합니다.

---
*이 글은 AI API 연동 전 테스트용 mock 데이터입니다.*
"""

        # 블로그 글 저장
        post = BlogPost.objects.create(
            keyword=keyword,
            title=title,
            content=content,
            status='draft'
        )

        return Response(BlogPostSerializer(post).data, status=status.HTTP_201_CREATED)
