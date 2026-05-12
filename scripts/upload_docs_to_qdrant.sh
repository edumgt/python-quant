#!/usr/bin/env bash
# docs/*.md 문서를 청크/벡터화(TF-IDF)하여 Qdrant 컬렉션에 업로드합니다.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="${DOCS_DIR:-$ROOT_DIR/docs}"
QDRANT_URL="${QDRANT_URL:-http://localhost:${VECTORDB_PORT:-6333}}"
QDRANT_COLLECTION="${QDRANT_COLLECTION:-investment_docs}"
CHUNK_SIZE="${CHUNK_SIZE:-1200}"
CHUNK_OVERLAP="${CHUNK_OVERLAP:-200}"
BATCH_SIZE="${BATCH_SIZE:-128}"

usage() {
  cat <<EOF
Usage: $(basename "$0")

환경 변수:
  DOCS_DIR            Markdown 문서 디렉터리 (기본: ./docs)
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
  echo "[ERROR] DOCS_DIR 디렉터리가 없습니다: $DOCS_DIR"
  exit 1
fi

echo "[STEP] Vector DB 연결/컬렉션 조회: $QDRANT_URL"
curl -fsS "$QDRANT_URL/collections" >/dev/null
echo "[OK] Vector DB 조회 성공"

python3 - "$DOCS_DIR" "$QDRANT_URL" "$QDRANT_COLLECTION" "$CHUNK_SIZE" "$CHUNK_OVERLAP" "$BATCH_SIZE" <<'PY'
import json
import sys
import urllib.request
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer


def http_json(method: str, url: str, payload: dict | None = None) -> dict:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if chunk_overlap >= chunk_size:
        raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")
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

vectorizer = TfidfVectorizer(max_features=768)
matrix = vectorizer.fit_transform([r["text"] for r in records]).toarray().tolist()
if not matrix or not matrix[0]:
    raise SystemExit("[ERROR] 벡터 생성 실패: TF-IDF 결과가 비어 있습니다.")

dim = len(matrix[0])
print(f"[INFO] docs={len(files)}, chunks={len(records)}, dim={dim}")

http_json(
    "PUT",
    f"{base_url}/collections/{collection}",
    {"vectors": {"size": dim, "distance": "Cosine"}},
)

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
