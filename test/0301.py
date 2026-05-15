import requests
import json

# 우체국 예금 금리 Best 조회 API
# Endpoint : https://apis.data.go.kr/B552886/svc_postDepoBest
# 공공데이터포털 인증키(Decoding) 사용
#################################################################################

BASE_URL = "https://apis.data.go.kr/B552886/svc_postDepoBest"
API_KEY  = "인증키"

params = {
    "serviceKey": API_KEY,
    "numOfRows" : 10,
    "pageNo"    : 1,
    "resultType": "json",
}

print("=" * 55)
print("  우체국 예금 Best 금리 조회")
print("=" * 55)

try:
    response = requests.get(BASE_URL, params=params, timeout=10)
    print(f"상태 코드 : {response.status_code}")
    print(f"요청 URL  : {response.url}\n")

    if response.status_code == 200:
        data = response.json()

        # 응답 전문 출력
        print("[전체 응답 JSON]")
        print(json.dumps(data, ensure_ascii=False, indent=2))

        # 상품 목록 파싱 (공공데이터포털 표준 응답 구조)
        items = (
            data.get("response", {})
                .get("body", {})
                .get("items", {})
                .get("item", [])
        )
        if isinstance(items, dict):   # 단건일 때 리스트로 통일
            items = [items]

        if items:
            print("\n[우체국 예금 Best 상품 목록]")
            print(f"{'순위':<4} {'상품명':<20} {'기간':<8} {'기본금리':>8} {'최고금리':>8}")
            print("-" * 55)
            for idx, item in enumerate(items, 1):
                name     = item.get("finPrdtNm",   item.get("prdtNm",    "-"))
                period   = item.get("saveTrm",      item.get("term",      "-"))
                base_r   = item.get("intrRate",     item.get("baseRate",  "-"))
                max_r    = item.get("intrRate2",     item.get("maxRate",   "-"))
                print(f"{idx:<4} {name:<20} {str(period)+'개월':<8} {str(base_r)+'%':>8} {str(max_r)+'%':>8}")
        else:
            print("항목 데이터 없음 — 응답 구조를 직접 확인하세요.")

    else:
        print(f"API 오류: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"요청 실패: {e}")

# ── 예시 출력 (API 미응답 시 참고용) ──────────────────────────
print("\n" + "=" * 55)
print("  [예시 출력 — API 정상 응답 시 기대 형태]")
print("=" * 55)

SAMPLE = {
    "response": {
        "header": {"resultCode": "00", "resultMsg": "NORMAL SERVICE."},
        "body": {
            "totalCount": 3,
            "items": {
                "item": [
                    {"finPrdtNm": "e-Postbank 정기예금", "saveTrm": 12, "intrRate": 3.20, "intrRate2": 3.50},
                    {"finPrdtNm": "우체국 Smart 예금",   "saveTrm": 24, "intrRate": 3.10, "intrRate2": 3.40},
                    {"finPrdtNm": "우체국 Dream 적금",   "saveTrm":  6, "intrRate": 2.80, "intrRate2": 3.20},
                ]
            },
        },
    }
}

items = SAMPLE["response"]["body"]["items"]["item"]
print(f"\n총 {SAMPLE['response']['body']['totalCount']}건\n")
print(f"{'순위':<4} {'상품명':<22} {'기간':>6} {'기본금리':>8} {'최고금리':>8}")
print("-" * 55)
for idx, item in enumerate(items, 1):
    print(
        f"{idx:<4} {item['finPrdtNm']:<22}"
        f" {str(item['saveTrm'])+'개월':>6}"
        f" {str(item['intrRate'])+'%':>8}"
        f" {str(item['intrRate2'])+'%':>8}"
    )
print()
