# Python & ML Education Repo 가이드

이 저장소는 **Python 기반 머신러닝 실습 → 컴퓨터 비전(OpenCV) → 생성형 AI(Diffusers)**까지 이어지는 교육용 예제를 담고 있습니다.  
유튜브 채널 강의 흐름에 맞춰, 짧고 독립 실행 가능한 스크립트 중심으로 구성되어 있습니다.

- 강의 채널: https://www.youtube.com/@softwareedumgt152
- 대상: Python 입문자, ML/딥러닝 실습을 처음 시작하는 학습자

---

## 1) 저장소 구성

```text
.
├── CrossValid.py         # 교차검증(K-Fold) 기초 실습
├── DecisionBoundary.py   # 로지스틱 회귀 + 결정경계 시각화
├── RandomForest.py       # 랜덤포레스트 분류 실습
├── OpenCVCPU.py          # OpenCV 기반 CPU 영상 생성
├── HuggingFaceGPU.py     # Stable Diffusion GPU 이미지 생성
└── Readme.md
```

---

## 2) 기술 스택(Tech Stack)

### 언어/런타임
- **Python 3.10+ 권장** (3.11/3.12도 가능)

### 핵심 라이브러리
- **데이터/수치 계산**: `numpy`, `pandas`
- **머신러닝**: `scikit-learn`
- **시각화**: `matplotlib`
- **컴퓨터 비전**: `opencv-python`
- **생성형 AI**: `torch`, `diffusers`, `transformers`, `accelerate`, `safetensors`

### 실행 환경
- **CPU 실습**: CrossValid, DecisionBoundary, RandomForest, OpenCVCPU
- **GPU 실습(CUDA 필요)**: HuggingFaceGPU

---

## 3) 빠른 시작 (환경 설정)

아래는 공통적인 설치 예시입니다.

### 3-1. 가상환경 생성 및 활성화

#### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### 3-2. CPU 실습용 패키지 설치
```bash
pip install numpy pandas scikit-learn matplotlib opencv-python
```

### 3-3. 생성형 AI(GPU) 실습용 패키지 설치
> 아래는 CUDA 기반 GPU 환경 기준입니다.

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install diffusers transformers accelerate safetensors
```

> GPU 드라이버/CUDA 버전과 PyTorch wheel(`cu118`, `cu121` 등)은 반드시 맞춰 주세요.

---

## 4) 예제별 상세 설명 및 실행 방법

## A. `CrossValid.py` — K-Fold 교차검증 실습

### 학습 목표
- `make_classification`으로 가상 분류 데이터 생성
- `LogisticRegression` 모델 학습
- `cross_val_score`로 5-Fold 성능 평가
- 각 Fold 정확도와 평균 정확도 이해

### 실행
```bash
python CrossValid.py
```

### 기대 결과
- 콘솔에 각 Fold의 정확도 배열과 평균 정확도가 출력됩니다.
- 단일 Train/Test split보다 더 안정적인 성능 추정 개념을 익힐 수 있습니다.

---

## B. `DecisionBoundary.py` — 결정경계(Decision Boundary) 시각화

### 학습 목표
- 2차원 분류 데이터 생성
- Train/Test 분리 후 로지스틱 회귀 학습
- `meshgrid` 기반으로 분류 경계 시각화
- 일반화(Train/Test 분포) 직관적 이해

### 실행
```bash
python DecisionBoundary.py
```

### 기대 결과
- matplotlib 창이 열리고, 배경의 색 영역(예측 클래스) + 산점도(실제 데이터)가 함께 보입니다.

### 참고
- GUI 환경이 없는 서버/원격 터미널에서는 창이 뜨지 않을 수 있습니다.
- 필요 시 `plt.show()` 대신 `plt.savefig("decision_boundary.png")`로 저장 방식 사용을 권장합니다.

---

## C. `RandomForest.py` — 랜덤포레스트 분류 실습

### 학습 목표
- 간단한 고객 이탈(churn) 형태의 표 데이터 구성
- `RandomForestClassifier` 학습
- 정확도(`accuracy_score`)와 분류 리포트(`classification_report`) 해석

### 실행
```bash
python RandomForest.py
```

### 기대 결과
- 콘솔에 정확도와 정밀도/재현율/F1-score가 출력됩니다.
- 트리 앙상블 기반 분류기의 기본 사용법을 익힐 수 있습니다.

---

## D. `OpenCVCPU.py` — OpenCV로 애니메이션(mp4) 생성

### 학습 목표
- NumPy 배열을 프레임 이미지로 생성
- OpenCV `VideoWriter`로 프레임을 mp4로 저장
- 반지름이 변하는 원 애니메이션 제작

### 실행
```bash
python OpenCVCPU.py
```

### 산출물
- 실행 후 루트 경로에 `circle_animation.mp4` 파일이 생성됩니다.

### 주의사항
- 스크립트 마지막의 `os.startfile(output_path)`는 **Windows 전용**입니다.
- macOS/Linux에서는 해당 줄을 주석 처리하거나 아래처럼 대체하세요.
  - macOS: `subprocess.run(["open", output_path])`
  - Linux: `subprocess.run(["xdg-open", output_path])`

---

## E. `HuggingFaceGPU.py` — Stable Diffusion GPU 추론

### 학습 목표
- Hugging Face Diffusers 파이프라인 로드
- CUDA + `float16` 기반 이미지 생성
- 프롬프트 엔지니어링 기초 체험

### 실행
```bash
python HuggingFaceGPU.py
```

### 산출물
- 실행 후 `test.png`가 저장됩니다.

### 필수 조건
- NVIDIA GPU + CUDA 환경
- GPU VRAM 여유(해상도 720x1280 설정으로 메모리 요구량 큼)
- 초기 실행 시 모델 다운로드를 위한 인터넷 연결

### 문제 해결 팁
- `CUDA out of memory` 발생 시:
  - 해상도(`height`, `width`)를 낮추세요.
  - 불필요한 앱을 종료해 VRAM을 확보하세요.
- `torch.cuda.is_available()`가 `False`이면:
  - CUDA 드라이버/런타임/PyTorch CUDA wheel 호환 여부를 먼저 점검하세요.

---

## 5) Python ML 실습 학습 로드맵 (권장 순서)

1. `CrossValid.py`  
   → 모델 성능을 신뢰성 있게 평가하는 방법 이해
2. `DecisionBoundary.py`  
   → 분류기의 동작 원리를 시각적으로 이해
3. `RandomForest.py`  
   → 실무형 표 데이터 분류 파이프라인 경험
4. `OpenCVCPU.py`  
   → ML 외 이미지/영상 처리 흐름 체험
5. `HuggingFaceGPU.py`  
   → 생성형 AI 파이프라인으로 확장

---

## 6) 자주 묻는 질문(FAQ)

### Q1. 처음에는 어떤 파일부터 실행하면 좋나요?
- `CrossValid.py` → `DecisionBoundary.py` → `RandomForest.py` 순서를 추천합니다.

### Q2. GPU가 없어도 학습 가능한가요?
- 네. 본 저장소의 대부분 예제는 CPU만으로 실행 가능합니다.
- 단, `HuggingFaceGPU.py`는 GPU 환경이 사실상 필수입니다.

### Q3. 강의 실습을 확장하려면?
- `RandomForest.py`에 실제 CSV 로딩(`pandas.read_csv`)을 추가해 보세요.
- `DecisionBoundary.py`에서 다른 분류기(SVM, KNN)로 모델을 바꿔 비교해 보세요.
- `HuggingFaceGPU.py`에서 프롬프트/시드/스텝 수를 바꿔 결과 차이를 기록해 보세요.

---

## 7) 권장 추가 파일 (선택)

실습 재현성을 높이려면 다음 파일을 함께 관리하는 것을 권장합니다.
- `requirements.txt`: 의존성 버전 고정
- `notebooks/`: 실습 노트북 정리
- `data/`: 샘플 데이터셋 저장
- `outputs/`: 이미지/영상 결과물 관리

---

## 8) 마무리

이 저장소는 “이론 설명 + 바로 실행 가능한 코드”를 목표로 합니다.  
각 예제를 작게 수정하면서 **성능 지표 해석**, **시각화 해석**, **실행 환경 이해(CPU/GPU)**를 함께 학습해 보세요.
