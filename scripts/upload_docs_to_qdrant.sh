#!/usr/bin/env bash
# docs/*.md 문서를 청크/벡터화(해시 임베딩)하여 Qdrant 컬렉션에 업로드합니다.
# 참고: 해시 임베딩은 경량/무의존성 목적의 베이스라인이며, 고품질 의미 검색은 전용 임베딩 모델 사용을 권장합니다.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="${DOCS_DIR:-$ROOT_DIR/docs}"
VECTORDB_PORT="${VECTORDB_PORT:-6333}"
QDRANT_URL="${QDRANT_URL:-http://localhost:${VECTORDB_PORT}}"
QDRANT_COLLECTION="${QDRANT_COLLECTION:-investment_docs}"
CHUNK_SIZE="${CHUNK_SIZE:-1200}"
CHUNK_OVERLAP="${CHUNK_OVERLAP:-200}"
BATCH_SIZE="${BATCH_SIZE:-128}"

usage() {
  cat <<EOF
Usage: $(basename "$0")

환경 변수:
  DOCS_DIR            Markdown 문서 폴더 (기본: ./docs)
  QDRANT_URL          Qdrant HTTP URL (기본: http://localhost:6333)
  QDRANT_COLLECTION   컬렉션 이름 (기본: investment_docs)
  CHUNK_SIZE          문서 청크 크기(문자 수, 기본: 1200)
  CHUNK_OVERLAP       청크 오버랩(문자 수, 기본: 200)
  BATCH_SIZE          업로드 배치 크기(기본: 128)
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

for cmd in curl python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[ERROR] $cmd 이(가) 설치되어 있지 않습니다."
    exit 1
  fi
done

if [[ ! -d "$DOCS_DIR" ]]; then
  echo "[ERROR] DOCS_DIR 폴더가 없습니다: $DOCS_DIR"
  exit 1
fi

echo "[STEP] Vector DB 연결/컬렉션 조회: $QDRANT_URL"
if ! curl -fsS "$QDRANT_URL/collections" >/dev/null; then
  echo "[ERROR] Qdrant 조회 실패: $QDRANT_URL/collections"
  exit 1
fi
echo "[OK] Vector DB 조회 성공"

python3 - "$DOCS_DIR" "$QDRANT_URL" "$QDRANT_COLLECTION" "$CHUNK_SIZE" "$CHUNK_OVERLAP" "$BATCH_SIZE" <<'PY'
# stdin 코드(heredoc) + sys.argv 인자 방식으로 파이썬에 전달합니다.
import hashlib
import json
import math
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

class QdrantHTTPError(RuntimeError):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


def http_json(method: str, url: str, payload: dict | None = None) -> dict:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="ignore")
        raise QdrantHTTPError(exc.code, f"Qdrant API 오류({exc.code}): {method} {url} :: {err_body[:300]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Qdrant 연결 실패: {method} {url} :: {exc.reason}") from exc


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if chunk_overlap >= chunk_size:
        raise ValueError(f"CHUNK_OVERLAP ({chunk_overlap}) must be less than CHUNK_SIZE ({chunk_size})")
    chunks: list[str] = []
    step = chunk_size - chunk_overlap
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start += step
    return chunks


TOKEN_PATTERN = re.compile(r"[0-9A-Za-z가-힣_]+")


def embed_text(text: str, dim: int = 384) -> list[float]:
    """무의존성 베이스라인 해시 임베딩(384차원).

    운영 환경에서 의미 기반 검색 품질이 필요하면 전용 임베딩 모델로 교체하는 것을 권장합니다.
    각 토큰의 sha256 해시로 벡터 인덱스(mod dim)와 부호(bit) 를 정해 누적한 뒤 L2 정규화합니다.
    """
    vec = [0.0] * dim
    tokens = TOKEN_PATTERN.findall(text.lower())
    if not tokens:
        return vec
    for token in tokens:
        # sha256 digest는 항상 32바이트이므로 digest[:4], digest[4] 접근이 안전합니다.
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:4], "big") % dim
        sign = 1.0 if (digest[4] & 1) == 0 else -1.0
        vec[idx] += sign
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec


def has_nonzero_vector(vectors: list[list[float]]) -> bool:
    return any(any(v != 0.0 for v in vec) for vec in vectors)


docs_dir = Path(sys.argv[1])
base_url = sys.argv[2].rstrip("/")
collection = sys.argv[3]
chunk_size = int(sys.argv[4])
chunk_overlap = int(sys.argv[5])
batch_size = int(sys.argv[6])

files = sorted(docs_dir.glob("*.md"))
if not files:
    raise SystemExit(f"[ERROR] markdown 파일이 없습니다: {docs_dir}")

records: list[dict] = []
for file_path in files:
    content = file_path.read_text(encoding="utf-8")
    chunks = chunk_text(content, chunk_size, chunk_overlap)
    for idx, chunk in enumerate(chunks):
        records.append(
            {
                "source_doc": file_path.name,
                "chunk_index": idx,
                "text": chunk,
            }
        )

if not records:
    raise SystemExit("[ERROR] 업로드할 문서 청크가 없습니다.")

matrix = [embed_text(r["text"]) for r in records]
if not matrix or not has_nonzero_vector(matrix):
    raise SystemExit("[ERROR] 벡터 생성 실패: 임베딩 결과가 비어 있습니다.")

dim = len(matrix[0])
print(f"[INFO] docs={len(files)}, chunks={len(records)}, dim={dim}")

try:
    http_json("DELETE", f"{base_url}/collections/{collection}")
except QdrantHTTPError as exc:
    if exc.code != 404:
        raise

http_json("PUT", f"{base_url}/collections/{collection}", {"vectors": {"size": dim, "distance": "Cosine"}})

for start in range(0, len(records), batch_size):
    end = min(len(records), start + batch_size)
    points = []
    for i in range(start, end):
        points.append(
            {
                "id": i + 1,
                "vector": matrix[i],
                "payload": records[i],
            }
        )
    http_json(
        "PUT",
        f"{base_url}/collections/{collection}/points?wait=true",
        {"points": points},
    )
    print(f"[INFO] upserted {end}/{len(records)}")

result = http_json("GET", f"{base_url}/collections/{collection}")
count = result.get("result", {}).get("points_count")
print(f"[OK] 업로드 완료: collection={collection}, points_count={count}")
PY
