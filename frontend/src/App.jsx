import { useState, useEffect } from "react";
import "./index.css";
import { postApi, keywordApi, healthApi } from "./utils/api";

export default function App() {
  // 상태 관리
  const [keyword, setKeyword] = useState("");
  const [posts, setPosts] = useState([]);
  const [selectedPost, setSelectedPost] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [serverStatus, setServerStatus] = useState("확인 중...");

  // 서버 상태 확인
  useEffect(() => {
    healthApi
      .check()
      .then(() => setServerStatus("연결됨"))
      .catch(() => setServerStatus("연결 안 됨"));
  }, []);

  // 글 목록 불러오기
  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    try {
      const data = await postApi.list();
      setPosts(data);
    } catch (err) {
      console.error("글 목록 로드 실패:", err);
    }
  };

  // 글 생성
  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!keyword.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const newPost = await postApi.generate(keyword);
      setPosts([newPost, ...posts]);
      setSelectedPost(newPost);
      setKeyword("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>블로그 자동화 테스트</h1>
        <span className={`status ${serverStatus === "연결됨" ? "connected" : "disconnected"}`}>
          서버: {serverStatus}
        </span>
      </header>

      <main className="main-content">
        {/* 글 생성 폼 */}
        <section className="generate-section">
          <h2>블로그 글 생성</h2>
          <form onSubmit={handleGenerate}>
            <input
              type="text"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder="키워드를 입력하세요 (예: 파이썬 기초)"
              disabled={loading}
            />
            <button type="submit" disabled={loading || !keyword.trim()}>
              {loading ? "생성 중..." : "글 생성"}
            </button>
          </form>
          {error && <p className="error">{error}</p>}
        </section>

        <div className="content-wrapper">
          {/* 글 목록 */}
          <section className="posts-list">
            <h2>생성된 글 목록 ({posts.length}개)</h2>
            {posts.length === 0 ? (
              <p className="empty">아직 생성된 글이 없습니다.</p>
            ) : (
              <ul>
                {posts.map((post) => (
                  <li
                    key={post.id}
                    className={selectedPost?.id === post.id ? "selected" : ""}
                    onClick={() => setSelectedPost(post)}
                  >
                    <strong>{post.title}</strong>
                    <span className="meta">
                      키워드: {post.keyword_text} | 상태: {post.status}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </section>

          {/* 글 상세 보기 */}
          <section className="post-detail">
            <h2>글 내용</h2>
            {selectedPost ? (
              <article>
                <h3>{selectedPost.title}</h3>
                <div className="post-meta">
                  <span>키워드: {selectedPost.keyword_text}</span>
                  <span>상태: {selectedPost.status}</span>
                  <span>생성일: {new Date(selectedPost.created_at).toLocaleString()}</span>
                </div>
                <div className="post-content">
                  {selectedPost.content.split("\n").map((line, i) => (
                    <p key={i}>{line || <br />}</p>
                  ))}
                </div>
              </article>
            ) : (
              <p className="empty">왼쪽 목록에서 글을 선택하세요.</p>
            )}
          </section>
        </div>
      </main>

      <footer className="footer">
        <p>블로그 자동화 시스템 - 바이브 코딩 프로젝트</p>
      </footer>
    </div>
  );
}
