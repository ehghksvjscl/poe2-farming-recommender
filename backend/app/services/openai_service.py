import os
from openai import OpenAI


def get_client():
    """OpenAI 클라이언트 생성"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-api-key-here":
        raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    return OpenAI(api_key=api_key)


def generate_text(prompt: str, max_tokens: int = 1024) -> str:
    """
    OpenAI API로 텍스트 생성

    Args:
        prompt: 생성할 내용에 대한 프롬프트
        max_tokens: 최대 토큰 수 (기본값: 1024)

    Returns:
        생성된 텍스트
    """
    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def generate_blog_post(keyword: str) -> dict:
    """
    키워드로 블로그 글 생성

    Args:
        keyword: 블로그 글 주제 키워드

    Returns:
        {"title": "제목", "content": "본문"}
    """
    prompt = f"""다음 키워드에 대한 블로그 글을 작성해주세요.

키워드: {keyword}

요구사항:
1. SEO에 최적화된 제목 작성
2. 서론, 본론, 결론 구조
3. 자연스럽고 읽기 쉬운 문체
4. 1000-1500자 분량

다음 형식으로 작성해주세요:

제목: [제목]

[본문 내용]
"""

    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=2048,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = response.choices[0].message.content

    # 제목과 본문 분리
    lines = response_text.strip().split("\n")
    title = ""
    content_lines = []

    for i, line in enumerate(lines):
        if line.startswith("제목:"):
            title = line.replace("제목:", "").strip()
        elif title:  # 제목 이후의 모든 라인은 본문
            content_lines.append(line)

    content = "\n".join(content_lines).strip()

    return {
        "title": title,
        "content": content
    }
