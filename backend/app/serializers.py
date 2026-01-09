from rest_framework import serializers
from .models import Keyword, BlogPost


class KeywordSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = Keyword
        fields = ['id', 'keyword', 'is_active', 'created_at', 'posts_count']
        read_only_fields = ['created_at', 'posts_count']


class BlogPostSerializer(serializers.ModelSerializer):
    keyword_text = serializers.CharField(source='keyword.keyword', read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'keyword', 'keyword_text', 'title', 'content', 'status', 'created_at', 'published_at']
        read_only_fields = ['created_at', 'published_at']


class GeneratePostSerializer(serializers.Serializer):
    """글 생성 요청용 시리얼라이저"""
    keyword = serializers.CharField(max_length=200)
