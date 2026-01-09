/**
 * API 호출 유틸리티
 *
 * 백엔드 API와 통신하는 함수들을 모아둔 파일입니다.
 */

const API_BASE_URL = "http://localhost:8000/api";

/**
 * API 요청 기본 함수
 */
async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;

  const config = {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  };

  const response = await fetch(url, config);

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  // 204 No Content 처리
  if (response.status === 204) {
    return null;
  }

  return response.json();
}

/**
 * 키워드 API
 */
export const keywordApi = {
  // 키워드 목록 조회
  list: () => request("/keywords/"),

  // 키워드 생성
  create: (keyword) => request("/keywords/", {
    method: "POST",
    body: JSON.stringify({ keyword }),
  }),

  // 키워드 삭제
  delete: (id) => request(`/keywords/${id}/`, {
    method: "DELETE",
  }),
};

/**
 * 블로그 글 API
 */
export const postApi = {
  // 글 목록 조회
  list: () => request("/posts/"),

  // 글 상세 조회
  get: (id) => request(`/posts/${id}/`),

  // 키워드로 글 생성
  generate: (keyword) => request("/generate/", {
    method: "POST",
    body: JSON.stringify({ keyword }),
  }),
};

/**
 * 헬스체크 API
 */
export const healthApi = {
  check: () => request("/health/"),
};
