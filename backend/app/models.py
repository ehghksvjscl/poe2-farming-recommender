from django.db import models


class Keyword(models.Model):
    """블로그 글 생성용 키워드"""
    keyword = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword


class BlogPost(models.Model):
    """AI로 생성된 블로그 글"""
    STATUS_CHOICES = [
        ('draft', '초안'),
        ('published', '발행됨'),
        ('failed', '실패'),
    ]

    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=500)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
