#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEFAULT_SQL_FILE="$ROOT_DIR/app/backend/quiz_seed.sql"
DAY2_SQL_FILE="$ROOT_DIR/app/backend/02.sql"
DAY3_SQL_FILE="$ROOT_DIR/app/backend/03.sql"
DAY4_SQL_FILE="$ROOT_DIR/app/backend/04.sql"
SQL_FILE="${QUIZ_SQL_FILE:-$DEFAULT_SQL_FILE}"
MONGODB_URL="${MONGODB_URL:-mongodb://localhost:27017}"
MONGODB_DB="${MONGODB_DB:-investment_db}"
MONGODB_COLLECTION="${MONGODB_COLLECTION:-quiz_questions}"

usage() {
  cat <<EOF
Usage: $(basename "$0") [--sql-file <path>] [--day2] [--day3] [--day4]

Options:
  --sql-file <path>   사용할 SQL 파일 경로 지정
  --day2              app/backend/02.sql 사용
  --day3              app/backend/03.sql 사용
  --day4              app/backend/04.sql 사용
  -h, --help          도움말 출력
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --sql-file)
      if [[ $# -lt 2 ]]; then
        echo "[ERROR] --sql-file 옵션에는 경로가 필요합니다."
        usage
        exit 1
      fi
      SQL_FILE="$2"
      shift 2
      ;;
    --day2)
      SQL_FILE="$DAY2_SQL_FILE"
      shift
      ;;
    --day3)
      SQL_FILE="$DAY3_SQL_FILE"
      shift
      ;;
    --day4)
      SQL_FILE="$DAY4_SQL_FILE"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[ERROR] 알 수 없는 옵션: $1"
      usage
      exit 1
      ;;
  esac
done

if ! command -v mongosh >/dev/null 2>&1; then
  echo "[ERROR] mongosh 가 설치되어 있지 않습니다."
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "[ERROR] python3 가 설치되어 있지 않습니다."
  exit 1
fi

if [[ ! -f "$SQL_FILE" ]]; then
  echo "[ERROR] SQL 파일이 없습니다: $SQL_FILE"
  exit 1
fi

TMP_JSON="$(mktemp)"
trap 'rm -f "$TMP_JSON"' EXIT

python3 - "$SQL_FILE" "$TMP_JSON" <<'PY'
import json
import sqlite3
import sys
from pathlib import Path

sql_file = Path(sys.argv[1])
out_file = Path(sys.argv[2])

conn = sqlite3.connect(":memory:")
try:
    conn.executescript(sql_file.read_text(encoding="utf-8"))
    rows = conn.execute(
        """
        SELECT day, question_no, source_doc, topic, question,
               choice_1, choice_2, choice_3, choice_4,
               answer, explanation
          FROM quiz_questions
         ORDER BY day, question_no
        """
    ).fetchall()
finally:
    conn.close()

docs = []
for (
    day,
    question_no,
    source_doc,
    topic,
    question,
    choice_1,
    choice_2,
    choice_3,
    choice_4,
    answer,
    explanation,
) in rows:
    docs.append(
        {
            "day": int(day),
            "question_no": int(question_no),
            "source_doc": source_doc,
            "topic": topic,
            "question": question,
            "choices": [choice_1, choice_2, choice_3, choice_4],
            "answer": int(answer),
            "explanation": explanation,
        }
    )

out_file.write_text(json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"prepared_docs={len(docs)}")
PY

mongosh "$MONGODB_URL/$MONGODB_DB" --quiet --eval "db.createCollection('$MONGODB_COLLECTION');" >/dev/null 2>&1 || true
mongosh "$MONGODB_URL/$MONGODB_DB" --quiet --eval "db.getCollection('$MONGODB_COLLECTION').createIndex({day:1,question_no:1},{unique:true});" >/dev/null

mongosh "$MONGODB_URL/$MONGODB_DB" --quiet --eval "
const fs = require('fs');
const docs = JSON.parse(fs.readFileSync('$TMP_JSON', 'utf8'));
const coll = db.getCollection('$MONGODB_COLLECTION');
let inserted = 0;
for (const doc of docs) {
  const result = coll.updateOne(
    { day: doc.day, question_no: doc.question_no },
    { \$setOnInsert: doc },
    { upsert: true }
  );
  if (result.upsertedCount > 0) inserted += 1;
}
printjson({ inserted, total: coll.countDocuments({}) });
"

echo "[OK] MongoDB 초기화/데이터 적재 완료"
