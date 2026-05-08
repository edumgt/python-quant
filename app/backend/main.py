from __future__ import annotations

import base64
import io
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

try:
    import orjson
except ImportError:
    DEFAULT_RESPONSE_CLASS = JSONResponse
else:
    class FastORJSONResponse(Response):
        media_type = "application/json"

        def render(self, content: object) -> bytes:
            return orjson.dumps(content)

    DEFAULT_RESPONSE_CLASS = FastORJSONResponse

ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT_DIR / "app" / "frontend"
GENERATED_DIR = ROOT_DIR / "app" / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
_MATPLOTLIB_FONT_CONFIGURED = False


def configure_matplotlib_korean_font(plt) -> None:
    """Use an installed Korean font when Matplotlib renders Korean labels."""
    global _MATPLOTLIB_FONT_CONFIGURED
    if _MATPLOTLIB_FONT_CONFIGURED:
        return

    import matplotlib.font_manager as fm

    candidates = [
        Path("/usr/share/fonts/truetype/nanum/NanumGothic.ttf"),
        Path("/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    ]
    for font_path in candidates:
        if font_path.exists():
            fm.fontManager.addfont(str(font_path))
            font_name = fm.FontProperties(fname=str(font_path)).get_name()
            plt.rcParams["font.family"] = font_name
            break
    plt.rcParams["axes.unicode_minus"] = False
    _MATPLOTLIB_FONT_CONFIGURED = True


app = FastAPI(
    title="Python Education Cloud API",
    version="2.0.0",
    description=(
        "교육용 ML/DL API 서버 | Educational ML/DL API server. "
        "Supports: Cross-Validation, Decision Boundary, Random Forest, "
        "KMeans Clustering, SVM, MLP Neural Network, Linear/Polynomial Regression, "
        "Text Classification (NLP), OpenCV Animation, HuggingFace Diffusion, "
        "1D CNN Time Series, LSTM Predictor, Transformer Time Series."
    ),
    default_response_class=DEFAULT_RESPONSE_CLASS,
)

app.add_middleware(GZipMiddleware, minimum_size=1024)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CrossValidationRequest(BaseModel):
    n_samples: int = Field(default=1000, ge=200, le=20000)
    n_features: int = Field(default=10, ge=2, le=100)
    cv: int = Field(default=5, ge=3, le=10)


class RandomForestRequest(BaseModel):
    test_size: float = Field(default=0.3, ge=0.1, le=0.5)


class CircleAnimationRequest(BaseModel):
    width: int = Field(default=512, ge=128, le=1920)
    height: int = Field(default=512, ge=128, le=1080)
    fps: int = Field(default=30, ge=10, le=60)


class KMeansRequest(BaseModel):
    n_samples: int = Field(default=400, ge=100, le=5000)
    n_clusters: int = Field(default=4, ge=2, le=10)
    cluster_std: float = Field(default=0.8, ge=0.1, le=3.0)


class SVMRequest(BaseModel):
    kernel: str = Field(default="rbf", pattern="^(rbf|linear|poly)$")
    C: float = Field(default=1.0, ge=0.01, le=100.0)


class MLPRequest(BaseModel):
    hidden_layers: str = Field(default="128,64,32", pattern=r"^\d+(,\d+)*$")
    max_iter: int = Field(default=300, ge=50, le=1000)
    n_samples: int = Field(default=1000, ge=200, le=10000)


class LinearRegressionRequest(BaseModel):
    degree: int = Field(default=1, ge=1, le=5)
    n_samples: int = Field(default=200, ge=50, le=2000)
    noise: float = Field(default=3.0, ge=0.0, le=20.0)


class TextClassifyRequest(BaseModel):
    texts: list[str] = Field(default=["The team played amazing hockey tonight!"])
    max_features: int = Field(default=5000, ge=500, le=20000)


class DiffusionRequest(BaseModel):
    prompt: str = Field(default="A futuristic city skyline at sunset")
    height: int = Field(default=512, ge=256, le=1024)
    width: int = Field(default=512, ge=256, le=1024)
    guidance_scale: float = Field(default=8.0, ge=1.0, le=15.0)


class BacktestRequest(BaseModel):
    fast: int = Field(default=5, ge=2, le=50, description="단기 이동평균 기간")
    slow: int = Field(default=20, ge=5, le=200, description="장기 이동평균 기간")
    n_days: int = Field(default=1260, ge=252, le=3780, description="시뮬레이션 일수 (252=1년)")
    annual_return: float = Field(default=0.08, ge=-0.2, le=0.5)
    annual_vol: float = Field(default=0.20, ge=0.05, le=1.0)
    risk_free: float = Field(default=0.03, ge=0.0, le=0.1)


class PortfolioRequest(BaseModel):
    n_portfolios: int = Field(default=3000, ge=500, le=10000)
    risk_free: float = Field(default=0.03, ge=0.0, le=0.1)


class RiskRequest(BaseModel):
    annual_vol: float = Field(default=0.25, ge=0.05, le=1.0)
    capital: float = Field(default=10_000_000, ge=1_000_000, le=1_000_000_000)
    risk_pct: float = Field(default=0.01, ge=0.001, le=0.05)
    confidence: float = Field(default=0.95, ge=0.90, le=0.99)
    atr_multiplier: float = Field(default=2.0, ge=1.0, le=5.0)


class TVAlertRequest(BaseModel):
    action: str = Field(default="buy", pattern="^(buy|sell)$")
    ticker: str = Field(default="AAPL", max_length=20)
    price: float = Field(default=0.0, ge=0.0)
    rsi: float | None = Field(default=None)


class CNNTimeSeriesRequest(BaseModel):
    window: int = Field(default=20, ge=10, le=60, description="입력 창 길이 (거래일)")
    n_samples: int = Field(default=2000, ge=500, le=10000, description="합성 데이터 샘플 수")
    epochs: int = Field(default=20, ge=5, le=50, description="학습 에폭 수")


class LSTMRequest(BaseModel):
    seq_len: int = Field(default=30, ge=10, le=60, description="LSTM 입력 시퀀스 길이")
    n_days: int = Field(default=2000, ge=500, le=5000, description="시뮬레이션 일수")
    hidden_size: int = Field(default=64, ge=16, le=256, description="LSTM 은닉 유닛 수")
    epochs: int = Field(default=30, ge=10, le=80, description="학습 에폭 수")


class TransformerTSRequest(BaseModel):
    seq_len: int = Field(default=40, ge=20, le=80, description="인코더 입력 창 길이")
    pred_steps: int = Field(default=5, ge=1, le=10, description="예측 스텝 수")
    d_model: int = Field(default=32, ge=16, le=128, description="Transformer d_model 차원")
    epochs: int = Field(default=30, ge=10, le=80, description="학습 에폭 수")


class DartCompanySearchRequest(BaseModel):
    company_name: str = Field(default="삼성전자", min_length=1, max_length=80)
    limit: int = Field(default=10, ge=1, le=30)


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


def _dart_api_key() -> str:
    key = os.getenv("DART_API_KEY") or os.getenv("OPENDART_API_KEY")
    if not key:
        raise HTTPException(
            status_code=503,
            detail="DART_API_KEY 또는 OPENDART_API_KEY 환경변수를 설정하세요.",
        )
    return key


@lru_cache(maxsize=1)
def _load_dart_corp_codes() -> list[dict[str, str]]:
    key = _dart_api_key()
    url = "https://opendart.fss.or.kr/api/corpCode.xml?" + urllib.parse.urlencode({"crtfc_key": key})
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            payload = response.read()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"DART 회사코드 목록 수신 실패: {exc}") from exc

    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as zf:
            xml_name = zf.namelist()[0]
            xml_bytes = zf.read(xml_name)
    except zipfile.BadZipFile as exc:
        message = payload[:200].decode("utf-8", errors="ignore")
        raise HTTPException(status_code=502, detail=f"DART 응답을 해석할 수 없습니다: {message}") from exc

    root = ET.fromstring(xml_bytes)
    rows: list[dict[str, str]] = []
    for item in root.findall("list"):
        corp_code = (item.findtext("corp_code") or "").strip()
        corp_name = (item.findtext("corp_name") or "").strip()
        stock_code = (item.findtext("stock_code") or "").strip()
        modify_date = (item.findtext("modify_date") or "").strip()
        if corp_code and corp_name:
            rows.append({
                "corp_code": corp_code,
                "corp_name": corp_name,
                "stock_code": stock_code,
                "modify_date": modify_date,
            })
    return rows


@lru_cache(maxsize=4096)
def _resolve_krx_yahoo_ticker(stock_code: str) -> dict[str, object]:
    if not stock_code:
        return {"ticker": None, "candidates": []}

    candidates = [f"{stock_code}.KS", f"{stock_code}.KQ"]
    found: list[str] = []
    for ticker in candidates:
        chart_url = (
            "https://query1.finance.yahoo.com/v8/finance/chart/"
            + urllib.parse.quote(ticker)
            + "?range=5d&interval=1d"
        )
        try:
            with urllib.request.urlopen(chart_url, timeout=4) as response:
                text = response.read(5000).decode("utf-8", errors="ignore")
            if '"regularMarketPrice"' in text or '"timestamp"' in text:
                found.append(ticker)
        except Exception:
            continue

    return {"ticker": found[0] if found else f"{stock_code}.KS", "candidates": found or candidates}


@app.post("/api/dart/company-search")
def dart_company_search(req: DartCompanySearchRequest) -> dict[str, object]:
    query = req.company_name.strip()
    normalized = query.replace(" ", "").lower()
    if not normalized:
        raise HTTPException(status_code=400, detail="회사명을 입력하세요.")

    rows = _load_dart_corp_codes()
    listed = [row for row in rows if row["stock_code"]]
    exact = [row for row in listed if row["corp_name"].replace(" ", "").lower() == normalized]
    partial = [row for row in listed if normalized in row["corp_name"].replace(" ", "").lower()]
    matches = (exact + [row for row in partial if row not in exact])[: req.limit]

    results = []
    for row in matches:
        ticker_info = _resolve_krx_yahoo_ticker(row["stock_code"])
        results.append({
            **row,
            "ticker": ticker_info["ticker"],
            "ticker_candidates": ticker_info["candidates"],
            "display": f'{ticker_info["ticker"] or row["stock_code"]}, {row["corp_name"]}',
        })

    return {
        "query": query,
        "count": len(results),
        "results": results,
        "source": "OpenDART corpCode.xml",
        "notes": [
            "DART 회사코드 목록에서 상장기업(stock_code 보유 기업)만 검색합니다.",
            "DART는 .KS/.KQ suffix를 제공하지 않아 조회 가능한 Yahoo ticker 후보로 보완 표시합니다.",
        ],
    }


@app.post("/api/ml/cross-validation")
def cross_validation(req: CrossValidationRequest) -> dict[str, object]:
    import numpy as np
    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score

    X, y = make_classification(
        n_samples=req.n_samples,
        n_features=req.n_features,
        n_informative=max(2, req.n_features // 2),
        n_redundant=max(1, req.n_features // 5),
        n_classes=2,
        random_state=42,
    )

    model = LogisticRegression(max_iter=1000)
    scores = cross_val_score(model, X, y, cv=req.cv)
    return {
        "fold_scores": [float(s) for s in scores],
        "mean_accuracy": float(np.mean(scores)),
        "std_accuracy": float(np.std(scores)),
    }


@app.get("/api/ml/decision-boundary")
def decision_boundary_image() -> dict[str, str]:
    import matplotlib
    import numpy as np
    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    X, y = make_classification(
        n_samples=240,
        n_features=2,
        n_redundant=0,
        n_informative=2,
        n_clusters_per_class=1,
        random_state=42,
    )
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 400), np.linspace(y_min, y_max, 400))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, marker="o", edgecolors="k", label="Train")
    ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, marker="x", label="Test")
    ax.set_title("Decision Boundary")
    ax.legend()
    ax.grid(True)

    buffer = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buffer, format="png", dpi=140)
    plt.close(fig)
    image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {"image_base64": image_b64}


@app.post("/api/ml/random-forest")
def random_forest(req: RandomForestRequest) -> dict[str, object]:
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.model_selection import train_test_split

    data = {
        "age": [22, 45, 33, 35, 52, 23, 43, 56, 48, 29, 33, 53, 56, 58, 29],
        "monthly_spend": [10, 200, 100, 150, 300, 15, 180, 400, 250, 35, 150, 300, 15, 180, 99],
        "months_active": [1, 36, 24, 30, 60, 2, 33, 72, 50, 5, 33, 72, 50, 5, 12],
        "churn": [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    }

    df = pd.DataFrame(data)
    X = df[["age", "monthly_spend", "months_active"]]
    y = df["churn"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=req.test_size, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True)
    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "report": report,
    }


@app.post("/api/cv/circle-animation")
def circle_animation(req: CircleAnimationRequest) -> dict[str, str]:
    import cv2
    import numpy as np

    output_path = GENERATED_DIR / "circle_animation.mp4"

    writer = cv2.VideoWriter(
        str(output_path), cv2.VideoWriter_fourcc(*"mp4v"), req.fps, (req.width, req.height)
    )
    for radius in list(np.linspace(20, min(req.width, req.height) // 3, 30)) + list(
        np.linspace(min(req.width, req.height) // 3, 20, 30)
    ):
        image = np.zeros((req.height, req.width, 3), dtype=np.uint8)
        image[:] = (255, 0, 0)
        cv2.circle(image, (req.width // 2, req.height // 2), int(radius), (255, 255, 255), -1)
        writer.write(image)

    writer.release()
    return {"video_url": "/files/circle_animation.mp4"}


@app.post("/api/ml/kmeans")
def kmeans_clustering(req: KMeansRequest) -> dict[str, object]:
    import matplotlib
    import numpy as np
    from sklearn.cluster import KMeans
    from sklearn.datasets import make_blobs
    from sklearn.metrics import silhouette_score
    from sklearn.preprocessing import StandardScaler

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    X, _ = make_blobs(
        n_samples=req.n_samples,
        centers=req.n_clusters,
        cluster_std=req.cluster_std,
        random_state=42,
    )
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=req.n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    centers = kmeans.cluster_centers_
    sil = float(silhouette_score(X_scaled, labels))

    # Elbow data
    inertias = []
    ks = list(range(2, min(req.n_clusters + 4, 10)))
    for ki in ks:
        km = KMeans(n_clusters=ki, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(float(km.inertia_))

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap="tab10", alpha=0.7, s=12)
    axes[0].scatter(centers[:, 0], centers[:, 1], c="red", marker="X", s=200, zorder=5)
    axes[0].set_title(f"KMeans (k={req.n_clusters})  Silhouette={sil:.3f}")
    axes[0].grid(True)
    axes[1].plot(ks, inertias, "bo-")
    axes[1].set_xlabel("k")
    axes[1].set_ylabel("Inertia")
    axes[1].set_title("Elbow Method")
    axes[1].grid(True)
    plt.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=120)
    plt.close(fig)

    return {
        "image_base64": base64.b64encode(buffer.getvalue()).decode(),
        "silhouette_score": sil,
        "inertia": float(kmeans.inertia_),
        "elbow": {"ks": ks, "inertias": inertias},
    }


@app.post("/api/ml/svm")
def svm_classifier(req: SVMRequest) -> dict[str, object]:
    import matplotlib
    import numpy as np
    from sklearn.datasets import make_classification
    from sklearn.inspection import DecisionBoundaryDisplay
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVC

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    X, y = make_classification(
        n_samples=300, n_features=2, n_redundant=0, n_informative=2,
        n_clusters_per_class=1, random_state=42,
    )
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    svm = SVC(kernel=req.kernel, C=req.C, gamma="scale", random_state=42)
    svm.fit(X_train, y_train)
    y_pred = svm.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    accuracy = float(accuracy_score(y_test, y_pred))
    n_support = int(np.sum(svm.n_support_))

    fig, ax = plt.subplots(figsize=(7, 5))
    DecisionBoundaryDisplay.from_estimator(
        svm, X_scaled, ax=ax, alpha=0.3, cmap=plt.cm.coolwarm, response_method="predict"
    )
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=plt.cm.coolwarm, edgecolors="k", s=25, label="Train")
    ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=plt.cm.coolwarm, marker="^", edgecolors="k", s=25, label="Test")
    ax.scatter(
        svm.support_vectors_[:, 0], svm.support_vectors_[:, 1],
        s=100, linewidth=1.5, facecolors="none", edgecolors="k", label="Support Vectors",
    )
    ax.set_title(f"SVM ({req.kernel} kernel, C={req.C})  Acc={accuracy:.3f}")
    ax.legend(fontsize=8)
    ax.grid(True)
    plt.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=140)
    plt.close(fig)

    return {
        "image_base64": base64.b64encode(buffer.getvalue()).decode(),
        "accuracy": accuracy,
        "n_support_vectors": n_support,
        "report": report,
    }


@app.post("/api/ml/mlp")
def mlp_classifier(req: MLPRequest) -> dict[str, object]:
    import matplotlib
    from sklearn.datasets import make_classification
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.model_selection import train_test_split
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    hidden_layers = tuple(int(x) for x in req.hidden_layers.split(","))

    X, y = make_classification(
        n_samples=req.n_samples, n_features=10, n_informative=6,
        n_redundant=2, n_classes=2, random_state=42,
    )
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    mlp = MLPClassifier(
        hidden_layer_sizes=hidden_layers, activation="relu", solver="adam",
        max_iter=req.max_iter, random_state=42,
    )
    mlp.fit(X_train, y_train)
    y_pred = mlp.predict(X_test)
    accuracy = float(accuracy_score(y_test, y_pred))
    report = classification_report(y_test, y_pred, output_dict=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(mlp.loss_curve_, linewidth=2, color="#2563eb")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Loss")
    ax.set_title(f"MLP Loss Curve  (layers={hidden_layers})  Acc={accuracy:.3f}")
    ax.grid(True)
    plt.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=140)
    plt.close(fig)

    return {
        "image_base64": base64.b64encode(buffer.getvalue()).decode(),
        "accuracy": accuracy,
        "n_iterations": mlp.n_iter_,
        "report": report,
    }


@app.post("/api/ml/linear-regression")
def linear_regression(req: LinearRegressionRequest) -> dict[str, object]:
    import matplotlib
    import numpy as np
    from sklearn.linear_model import LinearRegression as LR
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import PolynomialFeatures

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(42)
    X = rng.uniform(0, 10, size=(req.n_samples, 1))
    # True underlying function: mixture so poly can shine
    y = sum(
        c * X.ravel() ** i
        for i, c in enumerate([10, -4, 0.5][: req.degree + 1])
    ) + rng.normal(0, req.noise, req.n_samples)

    model = make_pipeline(
        PolynomialFeatures(degree=req.degree, include_bias=False),
        LR(),
    )
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = float(r2_score(y, y_pred))
    mse = float(mean_squared_error(y, y_pred))

    X_plot = np.linspace(0, 10, 200).reshape(-1, 1)
    y_plot = model.predict(X_plot)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(X, y, alpha=0.4, s=15, label="Data")
    ax.plot(X_plot, y_plot, "r-", linewidth=2, label=f"Poly degree={req.degree}")
    ax.set_title(f"Regression (degree={req.degree})  R²={r2:.3f}  MSE={mse:.2f}")
    ax.set_xlabel("X")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=140)
    plt.close(fig)

    return {
        "image_base64": base64.b64encode(buffer.getvalue()).decode(),
        "r2_score": r2,
        "mse": mse,
        "degree": req.degree,
    }


@app.post("/api/nlp/text-classify")
def text_classify(req: TextClassifyRequest) -> dict[str, object]:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline

    # Inline bilingual training corpus — sports vs. politics
    _TRAIN_TEXTS = [
        # Sports (label 0)
        "The hockey team scored three goals in the final period to win the championship.",
        "Basketball playoffs begin next week with exciting matchups across the league.",
        "The pitcher threw a no-hitter in yesterday's baseball game.",
        "Football season kicks off with record-breaking ticket sales.",
        "The swimmer broke the world record in the 100m freestyle at the Olympics.",
        "Tennis star wins Grand Slam after coming back from injury.",
        "Ice hockey league announces expansion teams in new cities.",
        "The marathon runner finished in record time despite difficult conditions.",
        "Soccer World Cup qualifying matches start this weekend.",
        "Gold medals were awarded in gymnastics and rowing at the games.",
        # Politics (label 1)
        "The senator proposed a new budget policy for healthcare reform.",
        "Parliament voted on the controversial immigration bill last night.",
        "The president signed an executive order on environmental regulations.",
        "Political debates are heating up ahead of the upcoming election.",
        "The government announced a new economic stimulus package.",
        "Opposition leaders called for an emergency session of parliament.",
        "Tax reform legislation passed the Senate with bipartisan support.",
        "Foreign policy discussions dominated the United Nations summit.",
        "The prime minister addressed the nation about the economic crisis.",
        "Congressional hearings on data privacy began on Monday.",
    ]
    _TRAIN_LABELS = [0] * 10 + [1] * 10
    _LABEL_NAMES = ["rec.sport", "politics"]

    pipe = make_pipeline(
        TfidfVectorizer(max_features=req.max_features, ngram_range=(1, 2), stop_words="english"),
        LogisticRegression(max_iter=1000),
    )
    pipe.fit(_TRAIN_TEXTS, _TRAIN_LABELS)

    predictions = []
    for text in req.texts:
        pred_idx = int(pipe.predict([text])[0])
        prob = pipe.predict_proba([text])[0]
        predictions.append({
            "text": text[:200],
            "label": _LABEL_NAMES[pred_idx],
            "confidence": float(prob[pred_idx]),
        })

    return {"predictions": predictions, "categories": _LABEL_NAMES}


@app.post("/api/genai/text-to-image")
def text_to_image(req: DiffusionRequest) -> dict[str, str]:
    try:
        import torch
        from diffusers import StableDiffusionPipeline
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=503, detail=f"Missing dependency: {exc}") from exc

    if not torch.cuda.is_available():
        raise HTTPException(status_code=503, detail="CUDA GPU is not available in this environment.")

    model_id = os.getenv("DIFFUSERS_MODEL_ID", "runwayml/stable-diffusion-v1-5")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")

    image = pipe(
        req.prompt,
        guidance_scale=req.guidance_scale,
        height=req.height,
        width=req.width,
    ).images[0]

    output_path = GENERATED_DIR / "diffusion_result.png"
    image.save(output_path)
    return {"image_url": "/files/diffusion_result.png"}


@app.get("/files/{file_name}")
def get_generated_file(file_name: str) -> FileResponse:
    target = GENERATED_DIR / file_name
    if not target.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=target)


@app.post("/api/dl/cnn-timeseries")
def cnn_timeseries(req: CNNTimeSeriesRequest) -> dict[str, object]:
    """
    1D CNN으로 주가 패턴(상승·횡보·하락)을 분류합니다. (Day036 대응)
    """
    try:
        import torch
        import torch.nn as nn
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Missing dependency: {exc}") from exc

    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    SEED = 42
    rng_ = np.random.default_rng(SEED)

    windows, labels = [], []
    for _ in range(req.n_samples):
        mu_ = rng_.uniform(-0.0003, 0.0003)
        sigma_ = rng_.uniform(0.01, 0.025)
        returns = rng_.normal(mu_, sigma_, req.window + 1)
        prices = 100 * np.exp(np.cumsum(returns))
        next_ret = (prices[req.window] - prices[req.window - 1]) / prices[req.window - 1]
        windows.append(prices[: req.window])
        labels.append(2 if next_ret > 0.01 else (0 if next_ret < -0.01 else 1))

    X_raw = np.array(windows, dtype=np.float32)
    y_arr = np.array(labels, dtype=np.int64)
    X_norm = StandardScaler().fit_transform(X_raw).astype(np.float32)
    X_tr, X_te, y_tr, y_te = train_test_split(X_norm, y_arr, test_size=0.2, stratify=y_arr, random_state=SEED)

    Xtr = torch.tensor(X_tr).unsqueeze(1)
    Xte = torch.tensor(X_te).unsqueeze(1)
    ytr = torch.tensor(y_tr)
    yte = torch.tensor(y_te)

    class _CNN1D(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.net = nn.Sequential(
                nn.Conv1d(1, 32, 3, padding=1), nn.ReLU(),
                nn.Conv1d(32, 64, 3, padding=1), nn.ReLU(),
                nn.AdaptiveAvgPool1d(1), nn.Flatten(),
                nn.Linear(64, 32), nn.ReLU(), nn.Dropout(0.3), nn.Linear(32, 3),
            )
        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.net(x)

    torch.manual_seed(SEED)
    model = _CNN1D()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    crit = nn.CrossEntropyLoss()
    ds = torch.utils.data.TensorDataset(Xtr, ytr)
    dl = torch.utils.data.DataLoader(ds, batch_size=64, shuffle=True)

    train_acc_hist = []
    for _ in range(req.epochs):
        model.train()
        correct, total = 0, 0
        for xb, yb in dl:
            opt.zero_grad()
            out = model(xb)
            loss = crit(out, yb)
            loss.backward()
            opt.step()
            correct += (out.argmax(1) == yb).sum().item()
            total += len(yb)
        train_acc_hist.append(correct / total)

    model.eval()
    with torch.no_grad():
        val_preds = model(Xte).argmax(1).numpy()
    val_acc = float(np.mean(val_preds == y_te))

    label_names = ["하락", "횡보", "상승"]
    class_counts = {label_names[i]: int(np.sum(val_preds == i)) for i in range(3)}

    return {
        "val_accuracy": val_acc,
        "train_accuracy_final": float(train_acc_hist[-1]),
        "predicted_class_counts": class_counts,
        "train_accuracy_history": [round(a, 4) for a in train_acc_hist],
    }


@app.post("/api/dl/lstm-predictor")
def lstm_predictor(req: LSTMRequest) -> dict[str, object]:
    """
    LSTM으로 다음 날 주가 수익률을 예측합니다. (Day037 대응)
    """
    try:
        import torch
        import torch.nn as nn
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Missing dependency: {exc}") from exc

    import numpy as np
    from sklearn.preprocessing import StandardScaler

    SEED = 42
    rng_ = np.random.default_rng(SEED)
    daily_ret = rng_.normal(0.0002, 0.015, req.n_days)
    prices = 1000 * np.exp(np.cumsum(daily_ret))
    returns = (np.diff(prices) / prices[:-1]).astype(np.float32)

    def _make_seq(series: np.ndarray, seq_len: int):
        X_, y_ = [], []
        for i in range(len(series) - seq_len):
            X_.append(series[i : i + seq_len])
            y_.append(series[i + seq_len])
        return np.array(X_, dtype=np.float32), np.array(y_, dtype=np.float32)

    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X_raw, y_raw = _make_seq(returns, req.seq_len)
    X_norm = scaler_X.fit_transform(X_raw).astype(np.float32)
    y_norm = scaler_y.fit_transform(y_raw.reshape(-1, 1)).ravel().astype(np.float32)

    split = int(len(X_norm) * 0.8)
    Xtr = torch.tensor(X_norm[:split]).unsqueeze(-1)
    Xte = torch.tensor(X_norm[split:]).unsqueeze(-1)
    ytr = torch.tensor(y_norm[:split])
    yte_raw = y_raw[split:]

    class _LSTM(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.lstm = nn.LSTM(1, req.hidden_size, 2, batch_first=True, dropout=0.2)
            self.fc = nn.Sequential(nn.Linear(req.hidden_size, 32), nn.ReLU(), nn.Linear(32, 1))
        def forward(self, x: torch.Tensor) -> torch.Tensor:
            out, _ = self.lstm(x)
            return self.fc(out[:, -1, :]).squeeze(-1)

    torch.manual_seed(SEED)
    model = _LSTM()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    crit = nn.MSELoss()
    ds = torch.utils.data.TensorDataset(Xtr, ytr)
    dl = torch.utils.data.DataLoader(ds, batch_size=64, shuffle=True)
    val_losses = []

    for _ in range(req.epochs):
        model.train()
        for xb, yb in dl:
            opt.zero_grad()
            loss = crit(model(xb), yb)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
        model.eval()
        with torch.no_grad():
            vl = crit(model(Xte), torch.tensor(y_norm[split:])).item()
        val_losses.append(float(vl))

    model.eval()
    with torch.no_grad():
        y_pred_norm = model(Xte).numpy()
    y_pred_raw = scaler_y.inverse_transform(y_pred_norm.reshape(-1, 1)).ravel()
    dir_acc = float(np.mean(np.sign(y_pred_raw) == np.sign(yte_raw)))

    return {
        "direction_accuracy": dir_acc,
        "val_loss_final": val_losses[-1],
        "val_loss_history": [round(v, 6) for v in val_losses],
    }


@app.post("/api/dl/transformer-timeseries")
def transformer_timeseries(req: TransformerTSRequest) -> dict[str, object]:
    """
    Transformer Encoder로 멀티스텝 주가를 예측합니다. (Day038-039 대응)
    """
    try:
        import math
        import torch
        import torch.nn as nn
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Missing dependency: {exc}") from exc

    import numpy as np
    from sklearn.preprocessing import MinMaxScaler

    SEED = 42
    rng_ = np.random.default_rng(SEED)
    t = np.arange(2500)
    seasonal = 0.02 * np.sin(2 * np.pi * t / 252)
    log_returns = 0.0001 + seasonal * 0.005 + rng_.normal(0, 0.012, 2500)
    prices = 1000 * np.exp(np.cumsum(log_returns))
    scaler_ = MinMaxScaler()
    prices_norm = scaler_.fit_transform(prices.reshape(-1, 1)).ravel().astype(np.float32)

    X_list, y_list = [], []
    for i in range(len(prices_norm) - req.seq_len - req.pred_steps):
        X_list.append(prices_norm[i : i + req.seq_len])
        y_list.append(prices_norm[i + req.seq_len : i + req.seq_len + req.pred_steps])
    X_all = np.array(X_list, dtype=np.float32)
    y_all = np.array(y_list, dtype=np.float32)

    split = int(len(X_all) * 0.8)
    Xtr = torch.tensor(X_all[:split]).unsqueeze(-1)
    Xte = torch.tensor(X_all[split:]).unsqueeze(-1)
    ytr = torch.tensor(y_all[:split])
    yte = torch.tensor(y_all[split:])

    class _PE(nn.Module):
        def __init__(self, d: int, max_len: int = 200) -> None:
            super().__init__()
            pe = torch.zeros(max_len, d)
            pos = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
            div = torch.exp(torch.arange(0, d, 2, dtype=torch.float) * (-math.log(10000.0) / d))
            pe[:, 0::2] = torch.sin(pos * div)
            pe[:, 1::2] = torch.cos(pos * div)
            self.register_buffer("pe", pe.unsqueeze(0))
        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return x + self.pe[:, : x.size(1), :]

    class _TransformerModel(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.proj = nn.Linear(1, req.d_model)
            self.pe = _PE(req.d_model)
            nhead = max(1, req.d_model // 8)
            enc_layer = nn.TransformerEncoderLayer(
                d_model=req.d_model, nhead=nhead,
                dim_feedforward=req.d_model * 4, dropout=0.1, batch_first=True,
            )
            self.enc = nn.TransformerEncoder(enc_layer, num_layers=2)
            self.head = nn.Linear(req.d_model, req.pred_steps)
        def forward(self, x: torch.Tensor) -> torch.Tensor:
            x = self.pe(self.proj(x))
            return self.head(self.enc(x)[:, -1, :])

    torch.manual_seed(SEED)
    model = _TransformerModel()
    opt = torch.optim.AdamW(model.parameters(), lr=5e-4)
    crit = nn.MSELoss()
    ds = torch.utils.data.TensorDataset(Xtr, ytr)
    dl = torch.utils.data.DataLoader(ds, batch_size=64, shuffle=True)
    val_losses = []

    for _ in range(req.epochs):
        model.train()
        for xb, yb in dl:
            opt.zero_grad()
            loss = crit(model(xb), yb)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
        model.eval()
        with torch.no_grad():
            vl = crit(model(Xte), yte).item()
        val_losses.append(float(vl))

    model.eval()
    with torch.no_grad():
        y_pred = model(Xte).numpy()

    y_pred_orig = scaler_.inverse_transform(y_pred[:, 0].reshape(-1, 1)).ravel()
    y_true_orig = scaler_.inverse_transform(yte[:, 0].numpy().reshape(-1, 1)).ravel()
    last_input = scaler_.inverse_transform(X_all[split:, -1].reshape(-1, 1)).ravel()
    dir_acc = float(np.mean(np.sign(y_pred_orig - last_input) == np.sign(y_true_orig - last_input)))

    return {
        "direction_accuracy_step1": dir_acc,
        "val_loss_final": val_losses[-1],
        "val_loss_history": [round(v, 6) for v in val_losses],
    }


# ─── Quant Strategy Models ────────────────────────────────────────────────────

class BacktestRequest(BaseModel):
    fast_ma: int = Field(default=20, ge=5, le=60)
    slow_ma: int = Field(default=60, ge=20, le=200)
    n_days: int = Field(default=1260, ge=252, le=5040)


class PortfolioRequest(BaseModel):
    n_simulations: int = Field(default=3000, ge=500, le=10000)
    risk_free: float = Field(default=0.03, ge=0.0, le=0.1)


class RiskRequest(BaseModel):
    confidence: float = Field(default=0.95, ge=0.90, le=0.99)
    n_scenarios: int = Field(default=10000, ge=1000, le=100000)
    portfolio_value: float = Field(default=100_000_000, ge=1_000_000)


class PipelineRequest(BaseModel):
    ticker: str = Field(default="SPY")
    fast_ma: int = Field(default=20, ge=5, le=60)
    slow_ma: int = Field(default=60, ge=20, le=200)


class FinancialKnowledgeRequest(BaseModel):
    focus: str = Field(default="balanced", pattern="^(balanced|products|allocation)$")
    n_simulations: int = Field(default=3000, ge=500, le=10000)
    risk_free: float = Field(default=0.03, ge=0.0, le=0.1)


# ─── Quant Endpoints ──────────────────────────────────────────────────────────

@app.post("/api/quant/backtest")
def quant_backtest(req: BacktestRequest) -> dict[str, object]:
    """MA 크로스오버 전략 백테스트 (Day041·57 대응)"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import numpy as np
    import pandas as pd
    configure_matplotlib_korean_font(plt)

    rng = np.random.default_rng(42)
    dt = 1 / 252
    mu, sigma = 0.08, 0.20
    daily_r = rng.normal((mu - 0.5 * sigma**2) * dt, sigma * np.sqrt(dt), req.n_days)
    prices = pd.Series(
        100 * np.exp(np.cumsum(daily_r)),
        index=pd.date_range("2020-01-01", periods=req.n_days, freq="B"),
        name="Close",
    )

    df = pd.DataFrame({"Close": prices})
    df["MA_fast"] = df["Close"].rolling(req.fast_ma).mean()
    df["MA_slow"] = df["Close"].rolling(req.slow_ma).mean()
    df["Signal"] = (df["MA_fast"] > df["MA_slow"]).astype(float)
    df["Position"] = df["Signal"].shift(1).fillna(0)
    df["Ret"] = df["Close"].pct_change()
    df["Strat_Ret"] = df["Position"] * df["Ret"]
    df["BH_Ret"] = df["Ret"]
    df["Strat_Cum"] = (1 + df["Strat_Ret"]).cumprod()
    df["BH_Cum"] = (1 + df["BH_Ret"]).cumprod()
    df = df.dropna()

    ret = df["Strat_Ret"]
    n_years = len(ret) / 252
    cum = df["Strat_Cum"]
    cagr = float(cum.iloc[-1] ** (1 / n_years) - 1) if n_years > 0 else 0
    excess = ret - 0.03 / 252
    sharpe = float(excess.mean() / excess.std() * np.sqrt(252)) if excess.std() > 0 else 0
    rolling_max = cum.cummax()
    dd = (cum - rolling_max) / rolling_max
    mdd = float(dd.min())
    wins = ret[ret > 0]
    losses = ret[ret < 0]
    win_rate = len(wins) / max(len(ret[ret != 0]), 1)
    pf = float(wins.sum() / abs(losses.sum())) if len(losses) > 0 and losses.sum() != 0 else 9.99
    n_trades = int(df["Position"].diff().abs()[lambda x: x > 0].count())
    total_ret = float(cum.iloc[-1] - 1)
    bh_ret = float(df["BH_Cum"].iloc[-1] - 1)

    fig = plt.figure(figsize=(14, 9), facecolor="#0f172a")
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.3)
    text_c = "#e2e8f0"
    grid_c = "#1e293b"

    for ax in [fig.add_subplot(gs[r, c]) for r in range(3) for c in range(2)]:
        ax.set_facecolor("#1e293b")
    plt.clf()

    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor("#1e293b")
    ax1.plot(df.index, df["Close"], color="#64748b", lw=0.8, label="주가")
    ax1.plot(df.index, df["MA_fast"], color="#3b82f6", lw=1.5, label=f"MA{req.fast_ma}")
    ax1.plot(df.index, df["MA_slow"], color="#f97316", lw=1.5, label=f"MA{req.slow_ma}")
    buy_m = (df["Position"] == 1) & (df["Position"].shift(1) == 0)
    sell_m = (df["Position"] == 0) & (df["Position"].shift(1) == 1)
    ax1.scatter(df.index[buy_m], df["Close"][buy_m], marker="^", color="#22c55e", s=50, zorder=5, label="매수")
    ax1.scatter(df.index[sell_m], df["Close"][sell_m], marker="v", color="#ef4444", s=50, zorder=5, label="매도")
    ax1.set_title(f"MA 크로스오버 전략 (MA{req.fast_ma}/MA{req.slow_ma})", color=text_c, fontsize=11, fontweight="bold")
    ax1.legend(fontsize=8, ncol=5, labelcolor=text_c, facecolor="#0f172a")
    ax1.tick_params(colors=text_c); ax1.spines[:].set_color(grid_c)
    ax1.grid(True, alpha=0.2, color=grid_c)

    ax2 = fig.add_subplot(gs[1, :])
    ax2.set_facecolor("#1e293b")
    ax2.plot(df.index, df["Strat_Cum"], color="#3b82f6", lw=2, label=f"전략 ({total_ret:+.1%})")
    ax2.plot(df.index, df["BH_Cum"], color="#94a3b8", lw=2, ls="--", label=f"Buy & Hold ({bh_ret:+.1%})")
    ax2.axhline(1.0, color="#475569", lw=0.6)
    ax2.set_title("누적 수익률 비교", color=text_c, fontsize=11)
    ax2.legend(fontsize=9, labelcolor=text_c, facecolor="#0f172a")
    ax2.tick_params(colors=text_c); ax2.spines[:].set_color(grid_c)
    ax2.grid(True, alpha=0.2, color=grid_c)

    ax3 = fig.add_subplot(gs[2, 0])
    ax3.set_facecolor("#1e293b")
    ax3.fill_between(df.index, dd * 100, 0, color="#ef4444", alpha=0.5)
    ax3.set_title("낙폭 Drawdown (%)", color=text_c, fontsize=11)
    ax3.tick_params(colors=text_c); ax3.spines[:].set_color(grid_c)
    ax3.grid(True, alpha=0.2, color=grid_c)

    ax4 = fig.add_subplot(gs[2, 1])
    ax4.set_facecolor("#1e293b")
    ax4.axis("off")
    rows = [
        ["전략 총수익률", f"{total_ret:+.1%}"],
        ["B&H 수익률", f"{bh_ret:+.1%}"],
        ["CAGR", f"{cagr:+.2%}"],
        ["Sharpe", f"{sharpe:.2f}"],
        ["MDD", f"{mdd:.1%}"],
        ["승률", f"{win_rate:.1%}"],
        ["손익비", f"{pf:.2f}"],
        ["거래횟수", f"{n_trades}회"],
    ]
    tbl = ax4.table(cellText=rows, colLabels=["지표", "값"], loc="center", bbox=[0, 0, 1, 1])
    tbl.auto_set_font_size(False); tbl.set_fontsize(9)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_facecolor("#0f172a" if r == 0 else "#1e293b")
        cell.set_text_props(color=text_c)
        cell.set_edgecolor(grid_c)
    ax4.set_title("성과 요약", color=text_c, fontsize=11)

    fig.patch.set_facecolor("#0f172a")
    plt.suptitle("백테스트 결과 — MA 크로스오버 전략", color=text_c, fontsize=13, fontweight="bold", y=1.01)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight", facecolor="#0f172a")
    plt.close(fig)
    return {
        "image": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(),
        "metrics": {"cagr": round(cagr, 4), "sharpe": round(sharpe, 2), "mdd": round(mdd, 4),
                    "win_rate": round(win_rate, 4), "profit_factor": round(pf, 2),
                    "n_trades": n_trades, "total_return": round(total_ret, 4), "bh_return": round(bh_ret, 4)},
    }


@app.post("/api/quant/portfolio")
def quant_portfolio(req: PortfolioRequest) -> dict[str, object]:
    """포트폴리오 최적화 — 효율적 프론티어 + Sharpe 극대화 (Day57·76·77 대응)"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    configure_matplotlib_korean_font(plt)

    tickers = ["KOSPI", "S&P500", "국채10Y", "금(Gold)", "BTC"]
    mu_ann = np.array([0.10, 0.12, 0.04, 0.07, 0.30])
    vol_ann = np.array([0.18, 0.17, 0.06, 0.15, 0.70])
    corr = np.array([
        [1.00, 0.75, 0.10, 0.10, 0.20],
        [0.75, 1.00, 0.05, 0.05, 0.25],
        [0.10, 0.05, 1.00, 0.20, 0.00],
        [0.10, 0.05, 0.20, 1.00, 0.05],
        [0.20, 0.25, 0.00, 0.05, 1.00],
    ])
    cov = np.outer(vol_ann, vol_ann) * corr
    n = len(tickers)
    rng = np.random.default_rng(42)
    rf = req.risk_free

    port_rets, port_vols, port_sharpes = [], [], []
    all_weights = []
    for _ in range(req.n_simulations):
        w = rng.random(n); w /= w.sum()
        r = float(w @ mu_ann)
        v = float(np.sqrt(w @ cov @ w))
        port_rets.append(r); port_vols.append(v)
        port_sharpes.append((r - rf) / v)
        all_weights.append(w)

    port_rets = np.array(port_rets)
    port_vols = np.array(port_vols)
    port_sharpes = np.array(port_sharpes)
    all_weights = np.array(all_weights)

    best_i = int(np.argmax(port_sharpes))
    best_w = all_weights[best_i]

    # Risk-parity weights (equal risk contribution approx)
    inv_vol = 1 / vol_ann; rp_w = inv_vol / inv_vol.sum()
    rp_r = float(rp_w @ mu_ann); rp_v = float(np.sqrt(rp_w @ cov @ rp_w))

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor="#0f172a")
    text_c = "#e2e8f0"; grid_c = "#1e293b"

    ax = axes[0]; ax.set_facecolor("#1e293b")
    sc = ax.scatter(port_vols * 100, port_rets * 100, c=port_sharpes, cmap="RdYlGn",
                    s=4, alpha=0.6)
    ax.scatter(port_vols[best_i] * 100, port_rets[best_i] * 100,
               marker="*", color="#fbbf24", s=300, zorder=10, label=f"최적(Sharpe={port_sharpes[best_i]:.2f})")
    ax.scatter(rp_v * 100, rp_r * 100, marker="D", color="#22d3ee", s=120, zorder=10, label="Risk-Parity")
    for i, tk in enumerate(tickers):
        ax.scatter(vol_ann[i] * 100, mu_ann[i] * 100, marker="o", s=80, zorder=10)
        ax.annotate(tk, (vol_ann[i] * 100, mu_ann[i] * 100), textcoords="offset points",
                    xytext=(5, 3), color=text_c, fontsize=8)
    cbar = plt.colorbar(sc, ax=ax); cbar.set_label("Sharpe Ratio", color=text_c)
    cbar.ax.yaxis.set_tick_params(color=text_c)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=text_c)
    ax.set_xlabel("리스크 (변동성 %)", color=text_c); ax.set_ylabel("기대수익률 (%)", color=text_c)
    ax.set_title("효율적 프론티어", color=text_c, fontsize=12, fontweight="bold")
    ax.legend(fontsize=8, labelcolor=text_c, facecolor="#0f172a")
    ax.tick_params(colors=text_c); ax.spines[:].set_color(grid_c)
    ax.grid(True, alpha=0.2, color=grid_c)

    ax2 = axes[1]; ax2.set_facecolor("#1e293b")
    colors = ["#3b82f6", "#22c55e", "#f97316", "#fbbf24", "#a78bfa"]
    bars = ax2.bar(tickers, best_w * 100, color=colors, alpha=0.85, edgecolor=grid_c)
    for bar, val in zip(bars, best_w):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 f"{val:.1%}", ha="center", va="bottom", color=text_c, fontsize=9, fontweight="bold")
    ax2.set_title(f"최적 포트폴리오 비중 (Sharpe={port_sharpes[best_i]:.2f})", color=text_c, fontsize=12, fontweight="bold")
    ax2.set_ylabel("비중 (%)", color=text_c)
    ax2.tick_params(colors=text_c); ax2.spines[:].set_color(grid_c)
    ax2.set_facecolor("#1e293b"); ax2.grid(True, alpha=0.2, color=grid_c, axis="y")

    fig.patch.set_facecolor("#0f172a")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight", facecolor="#0f172a")
    plt.close(fig)

    return {
        "image": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(),
        "optimal_weights": {tk: round(float(w), 4) for tk, w in zip(tickers, best_w)},
        "optimal_return": round(float(port_rets[best_i]), 4),
        "optimal_vol": round(float(port_vols[best_i]), 4),
        "optimal_sharpe": round(float(port_sharpes[best_i]), 4),
        "riskparity_weights": {tk: round(float(w), 4) for tk, w in zip(tickers, rp_w)},
    }


@app.post("/api/quant/financial-knowledge")
def quant_financial_knowledge(req: FinancialKnowledgeRequest) -> dict[str, object]:
    """모듈 8 — 금융상품 이해와 자산배분방법론 5일 커리큘럼 점검/실습."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    configure_matplotlib_korean_font(plt)

    coverage = [
        {
            "day": "Day 052",
            "topic": "주식/ETF 상품",
            "document": "docs/37.md",
            "coverage": 0.96,
            "web_status": "보완됨",
            "items": ["주식/ETF 개요", "ETF 운용 전략", "성과 비교"],
        },
        {
            "day": "Day 053",
            "topic": "채권 상품",
            "document": "docs/37.md",
            "coverage": 0.88,
            "web_status": "보완됨",
            "items": ["채권 개요", "듀레이션", "수익률 곡선", "운용 전략"],
        },
        {
            "day": "Day 054",
            "topic": "파생상품",
            "document": "docs/38.md",
            "coverage": 0.86,
            "web_status": "보완됨",
            "items": ["선물", "옵션", "스왑", "헤징 전략"],
        },
        {
            "day": "Day 055",
            "topic": "포트폴리오 이론",
            "document": "docs/39.md",
            "coverage": 0.94,
            "web_status": "기존+보완",
            "items": ["MPT", "성과분석", "MDD", "Sharpe", "Sortino"],
        },
        {
            "day": "Day 056",
            "topic": "자산배분 모델",
            "document": "docs/40.md",
            "coverage": 0.92,
            "web_status": "기존+보완",
            "items": ["평균분산", "블랙-리터만", "Risk-Parity", "사례 분석"],
        },
    ]

    rng = np.random.default_rng(7)
    n_days = 252
    asset_names = ["주식/ETF", "채권", "원자재", "현금"]
    mu = np.array([0.10, 0.04, 0.06, 0.025])
    vol = np.array([0.19, 0.07, 0.16, 0.01])
    corr = np.array([
        [1.00, -0.10, 0.25, 0.00],
        [-0.10, 1.00, 0.05, 0.00],
        [0.25, 0.05, 1.00, 0.00],
        [0.00, 0.00, 0.00, 1.00],
    ])
    cov = np.outer(vol, vol) * corr
    daily_mean = mu / 252
    daily_cov = cov / 252
    returns = rng.multivariate_normal(daily_mean, daily_cov, n_days)
    curves = np.cumprod(1 + returns, axis=0)

    inv_vol = 1 / vol
    risk_parity_w = inv_vol / inv_vol.sum()
    sixty_forty_w = np.array([0.60, 0.35, 0.00, 0.05])
    market_w = np.array([0.50, 0.30, 0.15, 0.05])
    investor_view = np.array([0.005, 0.000, 0.006, 0.000])
    black_litterman_return = (mu * 0.75) + ((mu + investor_view) * 0.25)

    port_rets, port_vols, sharpes, weights = [], [], [], []
    for _ in range(req.n_simulations):
        w = rng.random(len(asset_names))
        w = w / w.sum()
        r = float(w @ mu)
        v = float(np.sqrt(w.T @ cov @ w))
        s = (r - req.risk_free) / v
        port_rets.append(r)
        port_vols.append(v)
        sharpes.append(s)
        weights.append(w)

    port_rets = np.array(port_rets)
    port_vols = np.array(port_vols)
    sharpes = np.array(sharpes)
    weights = np.array(weights)
    best_i = int(np.argmax(sharpes))
    mean_variance_w = weights[best_i]
    black_litterman_w = black_litterman_return / black_litterman_return.sum()

    def metrics(w: np.ndarray) -> dict[str, float]:
        portfolio_daily = returns @ w
        cumulative = np.cumprod(1 + portfolio_daily)
        cagr = float(cumulative[-1] ** (252 / len(cumulative)) - 1)
        annual_vol = float(np.std(portfolio_daily) * np.sqrt(252))
        mdd = float(np.min(cumulative / np.maximum.accumulate(cumulative) - 1))
        downside = portfolio_daily[portfolio_daily < 0]
        downside_vol = float(np.std(downside) * np.sqrt(252)) if len(downside) else annual_vol
        sharpe = float((cagr - req.risk_free) / annual_vol) if annual_vol else 0.0
        sortino = float((cagr - req.risk_free) / downside_vol) if downside_vol else 0.0
        return {
            "cagr": round(cagr, 4),
            "volatility": round(annual_vol, 4),
            "mdd": round(mdd, 4),
            "sharpe": round(sharpe, 3),
            "sortino": round(sortino, 3),
        }

    strategies = {
        "60/40 사례": sixty_forty_w,
        "평균분산": mean_variance_w,
        "블랙-리터만": black_litterman_w,
        "Risk-Parity": risk_parity_w,
    }

    strategy_payload = {
        name: {
            "weights": {asset: round(float(weight), 4) for asset, weight in zip(asset_names, w)},
            "metrics": metrics(w),
        }
        for name, w in strategies.items()
    }

    spots = np.linspace(70, 130, 121)
    call = np.maximum(spots - 100, 0) - 5
    put = np.maximum(100 - spots, 0) - 4
    straddle = call + put
    tenors = ["3M", "2Y", "5Y", "10Y", "30Y"]
    yields = np.array([4.6, 4.3, 4.0, 4.1, 4.25])

    text_c = "#e2e8f0"; grid_c = "#334155"
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), facecolor="#0f172a")

    ax = axes[0, 0]; ax.set_facecolor("#1e293b")
    for i, name in enumerate(asset_names):
        ax.plot(curves[:, i] * 100, label=name, linewidth=1.4)
    ax.set_title("금융상품 이해: 자산군별 누적 성과", color=text_c, fontweight="bold")
    ax.set_ylabel("기준가", color=text_c)
    ax.legend(fontsize=8, labelcolor=text_c, facecolor="#0f172a")
    ax.tick_params(colors=text_c); ax.grid(True, alpha=0.2, color=grid_c)
    ax.spines[:].set_color(grid_c)

    ax = axes[0, 1]; ax.set_facecolor("#1e293b")
    sc = ax.scatter(port_vols * 100, port_rets * 100, c=sharpes, cmap="viridis", s=5, alpha=0.55)
    ax.scatter(port_vols[best_i] * 100, port_rets[best_i] * 100, marker="*", s=260, color="#fbbf24", label="평균분산")
    rp_r = float(risk_parity_w @ mu); rp_v = float(np.sqrt(risk_parity_w.T @ cov @ risk_parity_w))
    ax.scatter(rp_v * 100, rp_r * 100, marker="D", s=110, color="#22c55e", label="Risk-Parity")
    ax.set_title("자산배분방법론: 효율적 투자선", color=text_c, fontweight="bold")
    ax.set_xlabel("변동성 (%)", color=text_c); ax.set_ylabel("기대수익률 (%)", color=text_c)
    ax.legend(fontsize=8, labelcolor=text_c, facecolor="#0f172a")
    ax.tick_params(colors=text_c); ax.grid(True, alpha=0.2, color=grid_c)
    ax.spines[:].set_color(grid_c)
    cbar = plt.colorbar(sc, ax=ax); cbar.set_label("Sharpe", color=text_c)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=text_c)

    ax = axes[1, 0]; ax.set_facecolor("#1e293b")
    x = np.arange(len(asset_names))
    width = 0.2
    for offset, (name, w) in zip([-1.5, -0.5, 0.5, 1.5], strategies.items()):
        ax.bar(x + offset * width, w * 100, width=width, label=name)
    ax.set_xticks(x); ax.set_xticklabels(asset_names, color=text_c)
    ax.set_title("자산배분 모델별 비중 비교", color=text_c, fontweight="bold")
    ax.set_ylabel("비중 (%)", color=text_c)
    ax.legend(fontsize=8, labelcolor=text_c, facecolor="#0f172a")
    ax.tick_params(colors=text_c); ax.grid(True, alpha=0.2, color=grid_c, axis="y")
    ax.spines[:].set_color(grid_c)

    ax = axes[1, 1]; ax.set_facecolor("#1e293b")
    ax.plot(spots, call, label="콜 매수", color="#3b82f6")
    ax.plot(spots, put, label="풋 매수", color="#ef4444")
    ax.plot(spots, straddle, label="스트래들", color="#a855f7")
    ax2 = ax.twinx()
    ax2.plot(np.arange(len(tenors)), yields, marker="o", color="#22c55e", label="채권 수익률곡선")
    ax2.set_ylabel("금리 (%)", color="#22c55e")
    ax2.tick_params(colors="#22c55e")
    ax2.set_xticks(np.arange(len(tenors)))
    ax2.set_xticklabels(tenors, color=text_c)
    ax.axhline(0, color="#94a3b8", linewidth=0.8)
    ax.set_title("파생상품 손익 + 채권 곡선 예시", color=text_c, fontweight="bold")
    ax.set_xlabel("기초자산 가격 / 만기", color=text_c); ax.set_ylabel("옵션 손익", color=text_c)
    ax.legend(fontsize=8, labelcolor=text_c, facecolor="#0f172a", loc="upper left")
    ax.tick_params(colors=text_c); ax.grid(True, alpha=0.2, color=grid_c)
    ax.spines[:].set_color(grid_c)

    fig.suptitle("퀀트를 위한 금융 필수 지식 — 웹앱 반영 점검", color=text_c, fontsize=15, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight", facecolor="#0f172a")
    plt.close(fig)

    diagnostics = [
        {"area": "문서 커리큘럼", "status": "충분", "note": "37~40.md가 Day 052~056의 5일 과정을 모두 포함합니다."},
        {"area": "기존 웹앱", "status": "부분 반영", "note": "포트폴리오 최적화와 리스크 분석은 있었지만 금융상품별 통합 화면은 부족했습니다."},
        {"area": "보완 웹앱", "status": "반영", "note": "주식/ETF, 채권, 파생상품, 포트폴리오 이론, 자산배분 모델을 한 화면에서 확인합니다."},
    ]

    return {
        "image": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(),
        "coverage": coverage,
        "diagnostics": diagnostics,
        "strategies": strategy_payload,
        "curriculum": [
            {"day": "Day 052", "title": "주식/ETF 상품 이해", "practice": "ETF 성과 비교"},
            {"day": "Day 053", "title": "채권 상품 이해", "practice": "수익률 곡선·듀레이션"},
            {"day": "Day 054", "title": "파생상품 이해", "practice": "옵션 손익 시뮬레이션"},
            {"day": "Day 055", "title": "포트폴리오 이론 및 성과 분석", "practice": "CAGR·MDD·Sharpe"},
            {"day": "Day 056", "title": "자산배분 모델 및 사례 분석", "practice": "평균분산·블랙리터만·Risk-Parity 비교"},
        ],
    }


@app.post("/api/quant/risk")
def quant_risk(req: RiskRequest) -> dict[str, object]:
    """VaR / CVaR 리스크 분석 (Day39·55 대응)"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    configure_matplotlib_korean_font(plt)

    rng = np.random.default_rng(42)
    mu, sigma = 0.0004, 0.012
    daily_ret = rng.normal(mu, sigma, req.n_scenarios).astype(float)

    alpha = 1 - req.confidence
    var_pct = float(np.percentile(daily_ret, alpha * 100))
    cvar_pct = float(daily_ret[daily_ret <= var_pct].mean())
    var_amt = abs(var_pct) * req.portfolio_value
    cvar_amt = abs(cvar_pct) * req.portfolio_value

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor="#0f172a")
    text_c = "#e2e8f0"; grid_c = "#1e293b"

    ax = axes[0]; ax.set_facecolor("#1e293b")
    ax.hist(daily_ret * 100, bins=80, color="#3b82f6", alpha=0.75, edgecolor="none", label="수익률 분포")
    ax.axvline(var_pct * 100, color="#f97316", lw=2, linestyle="--", label=f"VaR ({req.confidence:.0%}): {var_pct:.2%}")
    ax.axvline(cvar_pct * 100, color="#ef4444", lw=2, linestyle="-", label=f"CVaR: {cvar_pct:.2%}")
    ax.fill_betweenx([0, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 500],
                     daily_ret.min() * 100, var_pct * 100, color="#ef4444", alpha=0.15)
    ax.set_xlabel("일간 수익률 (%)", color=text_c); ax.set_ylabel("빈도", color=text_c)
    ax.set_title(f"수익률 분포 & VaR/CVaR ({req.confidence:.0%} 신뢰수준)", color=text_c, fontsize=11, fontweight="bold")
    ax.legend(fontsize=8, labelcolor=text_c, facecolor="#0f172a")
    ax.tick_params(colors=text_c); ax.spines[:].set_color(grid_c)
    ax.grid(True, alpha=0.2, color=grid_c)

    ax2 = axes[1]; ax2.set_facecolor("#1e293b")
    labels = ["VaR 예상 손실", "CVaR 예상 손실", "포트폴리오 가치"]
    values = [var_amt / 1e6, cvar_amt / 1e6, req.portfolio_value / 1e6]
    colors2 = ["#f97316", "#ef4444", "#22c55e"]
    bars = ax2.barh(labels, values, color=colors2, alpha=0.85, edgecolor=grid_c)
    for bar, val in zip(bars, values):
        ax2.text(val + req.portfolio_value / 1e6 * 0.01, bar.get_y() + bar.get_height() / 2,
                 f"{val:.1f}M", va="center", color=text_c, fontsize=10, fontweight="bold")
    ax2.set_xlabel("금액 (백만원)", color=text_c)
    ax2.set_title("리스크 금액 비교", color=text_c, fontsize=11, fontweight="bold")
    ax2.tick_params(colors=text_c); ax2.spines[:].set_color(grid_c)
    ax2.set_facecolor("#1e293b"); ax2.grid(True, alpha=0.2, color=grid_c, axis="x")

    fig.patch.set_facecolor("#0f172a")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight", facecolor="#0f172a")
    plt.close(fig)

    return {
        "image": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(),
        "var_pct": round(var_pct, 6),
        "cvar_pct": round(cvar_pct, 6),
        "var_amount": round(var_amt, 0),
        "cvar_amount": round(cvar_amt, 0),
        "confidence": req.confidence,
        "portfolio_value": req.portfolio_value,
    }


@app.post("/api/quant/pipeline")
def quant_pipeline(req: PipelineRequest) -> dict[str, object]:
    """퀀트 실전 4단계 파이프라인 시각화 (Day43·61 대응)"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import TimeSeriesSplit
    configure_matplotlib_korean_font(plt)
    from sklearn.metrics import accuracy_score

    rng = np.random.default_rng(42)
    n = 1260
    daily_r = rng.normal(0.0003, 0.015, n)
    prices = pd.Series(
        100 * np.exp(np.cumsum(daily_r)),
        index=pd.date_range("2020-01-01", periods=n, freq="B"),
    )

    df = pd.DataFrame({"Close": prices})
    df["MA_fast"] = df["Close"].rolling(req.fast_ma).mean()
    df["MA_slow"] = df["Close"].rolling(req.slow_ma).mean()
    df["RSI"] = _calc_rsi(df["Close"])
    df["BB_upper"] = df["Close"].rolling(20).mean() + 2 * df["Close"].rolling(20).std()
    df["BB_lower"] = df["Close"].rolling(20).mean() - 2 * df["Close"].rolling(20).std()
    df["BB_pct"] = (df["Close"] - df["BB_lower"]) / (df["BB_upper"] - df["BB_lower"])
    df["MACD"] = df["Close"].ewm(span=12).mean() - df["Close"].ewm(span=26).mean()
    df["ATR"] = (df["Close"].rolling(14).max() - df["Close"].rolling(14).min())
    df["Signal"] = (df["MA_fast"] > df["MA_slow"]).astype(float)
    df["Position"] = df["Signal"].shift(1).fillna(0)
    df["Ret"] = df["Close"].pct_change()
    df["Strat_Ret"] = df["Position"] * df["Ret"]
    df["Strat_Cum"] = (1 + df["Strat_Ret"]).cumprod()
    df["BH_Cum"] = (1 + df["Ret"]).cumprod()
    df = df.dropna()

    features = ["MA_fast", "MA_slow", "RSI", "BB_pct", "MACD", "ATR"]
    target = (df["Ret"].shift(-1) > 0).astype(int)
    feat_df = df[features].iloc[:-1]
    tgt = target.iloc[:-1]
    tscv = TimeSeriesSplit(n_splits=3)
    accs = []
    for tr_i, te_i in tscv.split(feat_df):
        rf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
        rf.fit(feat_df.iloc[tr_i], tgt.iloc[tr_i])
        accs.append(accuracy_score(tgt.iloc[te_i], rf.predict(feat_df.iloc[te_i])))
    ml_acc = float(np.mean(accs))

    ret = df["Strat_Ret"]
    n_years = len(ret) / 252
    cum = df["Strat_Cum"]
    cagr = float(cum.iloc[-1] ** (1 / n_years) - 1) if n_years > 0 else 0
    excess = ret - 0.03 / 252
    sharpe = float(excess.mean() / excess.std() * np.sqrt(252)) if excess.std() > 0 else 0
    rolling_max = cum.cummax()
    mdd = float(((cum - rolling_max) / rolling_max).min())

    fig = plt.figure(figsize=(15, 10), facecolor="#0f172a")
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)
    text_c = "#e2e8f0"; grid_c = "#1e293b"

    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor("#1e293b")
    ax1.plot(df.index, df["Close"], color="#64748b", lw=0.8, label="주가")
    ax1.plot(df.index, df["MA_fast"], color="#3b82f6", lw=1.5, label=f"MA{req.fast_ma}")
    ax1.plot(df.index, df["MA_slow"], color="#f97316", lw=1.5, label=f"MA{req.slow_ma}")
    ax1.fill_between(df.index, df["BB_upper"], df["BB_lower"], alpha=0.07, color="#8b5cf6")
    ax1.set_title(f"1단계+2단계: 주가 & 기술지표 — {req.ticker}", color=text_c, fontsize=11, fontweight="bold")
    ax1.legend(fontsize=8, ncol=4, labelcolor=text_c, facecolor="#0f172a")
    ax1.tick_params(colors=text_c); ax1.spines[:].set_color(grid_c)
    ax1.grid(True, alpha=0.2, color=grid_c)

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor("#1e293b")
    ax2.plot(df.index, df["Strat_Cum"], color="#3b82f6", lw=2, label=f"전략")
    ax2.plot(df.index, df["BH_Cum"], color="#94a3b8", lw=2, ls="--", label="Buy&Hold")
    ax2.set_title(f"3단계: 백테스트 | CAGR {cagr:+.1%} | Sharpe {sharpe:.2f} | MDD {mdd:.1%}",
                  color=text_c, fontsize=10, fontweight="bold")
    ax2.legend(fontsize=8, labelcolor=text_c, facecolor="#0f172a")
    ax2.tick_params(colors=text_c); ax2.spines[:].set_color(grid_c)
    ax2.grid(True, alpha=0.2, color=grid_c)

    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor("#1e293b")
    fi = rf.feature_importances_
    sorted_idx = np.argsort(fi)
    bars = ax3.barh([features[i] for i in sorted_idx], fi[sorted_idx],
                    color=["#3b82f6", "#22c55e", "#f97316", "#a78bfa", "#f472b6", "#fbbf24"][::-1],
                    alpha=0.85, edgecolor=grid_c)
    ax3.set_title(f"4단계: ML 특징 중요도 | 방향 정확도 {ml_acc:.1%}", color=text_c, fontsize=10, fontweight="bold")
    ax3.tick_params(colors=text_c); ax3.spines[:].set_color(grid_c)
    ax3.grid(True, alpha=0.2, color=grid_c, axis="x")

    fig.patch.set_facecolor("#0f172a")
    plt.suptitle(f"퀀트 실전 4단계 파이프라인 — {req.ticker}", color=text_c, fontsize=13, fontweight="bold", y=1.01)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight", facecolor="#0f172a")
    plt.close(fig)

    return {
        "image": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(),
        "metrics": {"cagr": round(cagr, 4), "sharpe": round(sharpe, 2), "mdd": round(mdd, 4), "ml_accuracy": round(ml_acc, 4)},
        "ticker": req.ticker,
    }


def _calc_rsi(series: "pd.Series", period: int = 14) -> "pd.Series":
    import pandas as pd
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, 1e-9)
    return 100 - (100 / (1 + rs))


# ── 산업 경쟁력 분석 ─────────────────────────────────────────────────────────

class PorterRequest(BaseModel):
    industry: str = "반도체"
    scores: dict[str, float] = {
        "경쟁강도":       8.0,
        "신규진입 위협":  6.0,
        "대체재 위협":    4.0,
        "구매자 교섭력":  5.0,
        "공급자 교섭력":  7.0,
    }

class SectorRequest(BaseModel):
    tickers: list[str] = ["SOXX", "XLE", "XLF", "XLV", "XLK", "XLI"]
    period:  str       = "1y"

class PeerRequest(BaseModel):
    tickers: dict[str, str] = {
        "삼성전자": "005930.KS",
        "SK하이닉스": "000660.KS",
        "엔비디아": "NVDA",
        "인텔": "INTC",
    }

class LifecycleRequest(BaseModel):
    stage:    str = "성장기"   # 도입기 성장기 성숙기 쇠퇴기
    industry: str = "전기차"


@app.post("/api/industry/porter")
def industry_porter(req: PorterRequest) -> dict[str, object]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import numpy as np
    import io, base64
    configure_matplotlib_korean_font(plt)

    DARK, SURF, BORDER, TEXT, MUTED = "#0f172a","#1e293b","#334155","#e2e8f0","#64748b"
    ACCENT = "#3b82f6"
    C_HIGH  = "#ef4444"   # 위협 강함
    C_MED   = "#f59e0b"
    C_LOW   = "#22c55e"   # 위협 약함

    forces = list(req.scores.keys())
    values = [max(0.0, min(10.0, float(v))) for v in req.scores.values()]
    N = len(forces)

    def force_color(v):
        if v >= 7: return C_HIGH
        if v >= 4: return C_MED
        return C_LOW

    fig = plt.figure(figsize=(14, 8), facecolor=DARK)
    gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.35,
                            left=0.05, right=0.97, top=0.88, bottom=0.1)

    # ── Panel 1: Radar (polar) ──────────────────────────────────────────────
    ax_r = fig.add_subplot(gs[0, 0], polar=True, facecolor=SURF)
    angles = [n / N * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    vals_plot = values + values[:1]

    ax_r.set_theta_offset(np.pi / 2)
    ax_r.set_theta_direction(-1)
    ax_r.set_ylim(0, 10)
    ax_r.set_yticks([2, 4, 6, 8, 10])
    ax_r.set_yticklabels(["2","4","6","8","10"], color=MUTED, fontsize=7)
    ax_r.set_xticks(angles[:-1])
    ax_r.set_xticklabels(forces, color=TEXT, fontsize=9)
    ax_r.spines["polar"].set_color(BORDER)
    ax_r.tick_params(colors=MUTED)
    ax_r.grid(color=BORDER, linewidth=0.8)

    # 배경 zone 색칠 (위험 등급)
    for thresh, col in [(10, "#ef444411"), (7, "#f59e0b11"), (4, "#22c55e11")]:
        zone = [thresh] * N + [thresh]
        ax_r.fill(angles, zone, color=col)

    ax_r.plot(angles, vals_plot, color=ACCENT, lw=2.2, zorder=3)
    ax_r.fill(angles, vals_plot, color=ACCENT, alpha=0.25, zorder=2)
    for a, v in zip(angles[:-1], values):
        ax_r.plot(a, v, "o", color=force_color(v), ms=8, zorder=4)
        ax_r.text(a, v + 0.8, f"{v:.1f}", ha="center", va="center",
                  fontsize=8, color=TEXT, fontweight="bold")

    ax_r.set_title(f"Porter 5 Forces\n{req.industry} 산업",
                   color=TEXT, fontsize=11, fontweight="bold", pad=18)

    # ── Panel 2: 수평 바 + 해석 ─────────────────────────────────────────────
    ax_b = fig.add_subplot(gs[0, 1], facecolor=SURF)
    bars = ax_b.barh(forces, values, color=[force_color(v) for v in values],
                     height=0.5, zorder=2)
    ax_b.set_xlim(0, 10)
    ax_b.axvline(4, color=MUTED, lw=0.8, ls="--", alpha=0.5)
    ax_b.axvline(7, color=MUTED, lw=0.8, ls="--", alpha=0.5)
    ax_b.text(2, -0.8, "약함", ha="center", color=C_LOW, fontsize=8)
    ax_b.text(5.5, -0.8, "보통", ha="center", color=C_MED, fontsize=8)
    ax_b.text(8.5, -0.8, "강함", ha="center", color=C_HIGH, fontsize=8)

    INTERP = {
        "경쟁강도":      {(7,10):"경쟁사 많음 → 가격경쟁↑·수익성↓", (4,7):"과점 구조 → 안정적", (0,4):"독점적 지위"},
        "신규진입 위협": {(7,10):"진입장벽 낮음 → 점유율 위협", (4,7):"중간 진입장벽", (0,4):"특허·규제·규모 장벽↑"},
        "대체재 위협":   {(7,10):"대체재 다수 → 가격결정력↓", (4,7):"부분 대체 가능", (0,4):"대체재 없음"},
        "구매자 교섭력": {(7,10):"구매자 협상력↑ → 마진압박", (4,7):"균형 협상", (0,4):"공급자 우위"},
        "공급자 교섭력": {(7,10):"원재료 공급 불안정·비용↑", (4,7):"복수 공급선 확보", (0,4):"공급 안정"},
    }

    for i, (bar, force, val) in enumerate(zip(bars, forces, values)):
        ax_b.text(val + 0.15, bar.get_y() + bar.get_height()/2,
                  f"{val:.1f}", va="center", fontsize=9,
                  color=TEXT, fontweight="bold")
        for (lo, hi), msg in INTERP.get(force, {}).items():
            if lo <= val <= hi:
                ax_b.text(10.2, bar.get_y() + bar.get_height()/2,
                          msg, va="center", fontsize=7, color=MUTED)
                break

    ax_b.set_xlabel("위협 강도 (0 = 낮음, 10 = 높음)", color=MUTED, fontsize=8)
    ax_b.tick_params(colors=TEXT, labelsize=9)
    ax_b.spines[:].set_color(BORDER)
    ax_b.set_title("5 Forces 위협 강도 분석", color=TEXT, fontsize=11,
                   fontweight="bold", pad=10)
    ax_b.set_xlim(0, 16)   # 오른쪽 텍스트 공간

    # 종합 점수
    avg = sum(values) / N
    grade = "고위험" if avg >= 7 else "중위험" if avg >= 4 else "저위험"
    grade_col = C_HIGH if avg >= 7 else C_MED if avg >= 4 else C_LOW
    fig.suptitle(
        f"산업 경쟁력 분석  |  {req.industry}  |  종합 위협 지수: {avg:.1f}/10  [{grade}]",
        color=TEXT, fontsize=12, fontweight="bold", y=0.97)
    fig.text(0.5, 0.01,
             "■ 녹색: 약함(0-4)  ■ 주황: 보통(4-7)  ■ 빨강: 강함(7-10)",
             ha="center", fontsize=8, color=MUTED)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, facecolor=DARK, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    img = "data:image/png;base64," + base64.b64encode(buf.read()).decode()

    result = {f: {"score": v, "level": "강함" if v>=7 else "보통" if v>=4 else "약함"}
              for f, v in zip(forces, values)}
    return {"image": img, "industry": req.industry,
            "avg_score": round(avg, 2), "grade": grade, "forces": result}


SECTOR_LABELS = {
    "SOXX": "반도체 (SOXX)", "XLE": "에너지 (XLE)", "XLF": "금융 (XLF)",
    "XLV":  "헬스케어 (XLV)", "XLK": "기술 (XLK)",  "XLI": "산업재 (XLI)",
    "XLY":  "소비재경기 (XLY)","XLP": "소비재필수 (XLP)","XLB": "소재 (XLB)",
    "XLRE": "부동산 (XLRE)",  "XLU": "유틸리티 (XLU)","IBB": "바이오 (IBB)",
}

@app.post("/api/industry/sector")
def industry_sector(req: SectorRequest) -> dict[str, object]:
    import yfinance as yf
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import numpy as np
    import pandas as pd
    import io, base64
    configure_matplotlib_korean_font(plt)

    DARK, SURF, BORDER, TEXT, MUTED = "#0f172a","#1e293b","#334155","#e2e8f0","#64748b"
    COLORS = ["#3b82f6","#22c55e","#f59e0b","#ef4444","#a855f7",
              "#06b6d4","#f97316","#84cc16","#ec4899","#14b8a6","#8b5cf6","#fb923c"]

    raw: dict[str, pd.Series] = {}
    for t in req.tickers:
        try:
            df = yf.download(t, period=req.period, progress=False, auto_adjust=True)
            if df.empty: continue
            s = df["Close"]
            if isinstance(s, pd.DataFrame): s = s.iloc[:, 0]
            s = s.dropna()
            if len(s) > 5: raw[t] = s
        except Exception:
            pass

    if not raw:
        raise HTTPException(status_code=503, detail="데이터를 가져올 수 없습니다.")

    fig = plt.figure(figsize=(14, 10), facecolor=DARK)
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.32,
                            left=0.07, right=0.97, top=0.92, bottom=0.07)

    # Panel 1: 정규화 수익률
    ax1 = fig.add_subplot(gs[0, :], facecolor=SURF)
    for i, (t, s) in enumerate(raw.items()):
        norm = (s / s.iloc[0] - 1) * 100
        ax1.plot(norm.index, norm.values, color=COLORS[i % len(COLORS)],
                 lw=1.8, label=SECTOR_LABELS.get(t, t))
    ax1.axhline(0, color=MUTED, lw=0.8, ls="--")
    ax1.set_title("섹터 ETF 정규화 누적 수익률 (%)", color=TEXT, fontsize=10, pad=6)
    ax1.tick_params(colors=TEXT, labelsize=7)
    ax1.spines[:].set_color(BORDER)
    ax1.legend(fontsize=7, facecolor=SURF, labelcolor=TEXT,
               ncol=4, loc="upper left", framealpha=0.7)
    ax1.tick_params(axis="x", rotation=30)
    for lbl in ax1.get_xticklabels(): lbl.set_fontsize(6)

    # Panel 2: 기간 수익률 바
    ax2 = fig.add_subplot(gs[1, 0], facecolor=SURF)
    names, returns, cols = [], [], []
    for i, (t, s) in enumerate(raw.items()):
        r = (s.iloc[-1] / s.iloc[0] - 1) * 100
        names.append(SECTOR_LABELS.get(t, t))
        returns.append(r)
        cols.append(COLORS[i % len(COLORS)])
    order = sorted(range(len(returns)), key=lambda x: returns[x], reverse=True)
    names_s  = [names[i] for i in order]
    returns_s = [returns[i] for i in order]
    cols_s   = [cols[i] for i in order]
    bars = ax2.barh(names_s, returns_s, color=cols_s, height=0.6)
    ax2.axvline(0, color=MUTED, lw=0.8)
    for bar, v in zip(bars, returns_s):
        ax2.text(v + (0.3 if v >= 0 else -0.3), bar.get_y() + bar.get_height()/2,
                 f"{v:+.1f}%", va="center", ha="left" if v >= 0 else "right",
                 fontsize=7, color=TEXT)
    ax2.set_title(f"기간 수익률 순위 ({req.period})", color=TEXT, fontsize=10, pad=6)
    ax2.tick_params(colors=TEXT, labelsize=7)
    ax2.spines[:].set_color(BORDER)

    # Panel 3: 변동성 vs 수익률 (리스크-리턴 산점도)
    ax3 = fig.add_subplot(gs[1, 1], facecolor=SURF)
    for i, (t, s) in enumerate(raw.items()):
        ret  = (s.iloc[-1] / s.iloc[0] - 1) * 100
        vol  = s.pct_change().std() * (252**0.5) * 100
        ax3.scatter(vol, ret, color=COLORS[i % len(COLORS)], s=100, zorder=3)
        ax3.text(vol + 0.3, ret, SECTOR_LABELS.get(t, t).split("(")[0].strip(),
                 fontsize=6.5, color=TEXT)
    ax3.axhline(0, color=MUTED, lw=0.8, ls="--")
    ax3.set_xlabel("연환산 변동성 (%)", color=MUTED, fontsize=8)
    ax3.set_ylabel(f"수익률 ({req.period}) %", color=MUTED, fontsize=8)
    ax3.set_title("리스크-리턴 산점도", color=TEXT, fontsize=10, pad=6)
    ax3.tick_params(colors=TEXT, labelsize=7)
    ax3.spines[:].set_color(BORDER)
    ax3.grid(color=BORDER, lw=0.5, alpha=0.5)

    fig.suptitle(f"섹터 주가 비교 분석  |  {req.period}",
                 color=TEXT, fontsize=12, fontweight="bold", y=0.97)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, facecolor=DARK, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    img = "data:image/png;base64," + base64.b64encode(buf.read()).decode()

    summary = {}
    for t, s in raw.items():
        summary[SECTOR_LABELS.get(t, t)] = {
            "return_pct": round((s.iloc[-1]/s.iloc[0]-1)*100, 2),
            "annual_vol":  round(s.pct_change().std()*(252**0.5)*100, 2),
        }
    return {"image": img, "summary": summary}


@app.post("/api/industry/peer")
def industry_peer(req: PeerRequest) -> dict[str, object]:
    import math

    import yfinance as yf

    if not req.tickers:
        raise HTTPException(status_code=400, detail="비교할 종목을 1개 이상 입력하세요.")
    if len(req.tickers) > 12:
        raise HTTPException(status_code=400, detail="Peer Comparison은 최대 12개 종목까지 지원합니다.")

    def as_float(value):
        if value is None:
            return None
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        if math.isnan(number) or math.isinf(number):
            return None
        return number

    rows: list[dict[str, object]] = []
    for name, ticker in req.tickers.items():
        label = (name or ticker).strip()[:40]
        symbol = (ticker or "").strip().upper()
        if not symbol:
            continue
        try:
            info = yf.Ticker(symbol).info
        except Exception as exc:
            rows.append({
                "company": label,
                "ticker": symbol,
                "error": f"데이터 수신 실패: {exc}",
            })
            continue

        market_cap = as_float(info.get("marketCap"))
        revenue_growth = as_float(info.get("revenueGrowth"))
        operating_margin = as_float(info.get("operatingMargins"))
        debt_to_equity = as_float(info.get("debtToEquity"))
        roe = as_float(info.get("returnOnEquity"))
        per = as_float(info.get("trailingPE"))
        pbr = as_float(info.get("priceToBook"))

        rows.append({
            "company": label,
            "ticker": symbol,
            "market_cap_krw_100m": round(market_cap / 1e8, 0) if market_cap is not None else None,
            "revenue_growth_pct": round(revenue_growth * 100, 1) if revenue_growth is not None else None,
            "operating_margin_pct": round(operating_margin * 100, 1) if operating_margin is not None else None,
            "per": round(per, 1) if per is not None else None,
            "pbr": round(pbr, 2) if pbr is not None else None,
            "debt_to_equity_pct": round(debt_to_equity, 1) if debt_to_equity is not None else None,
            "roe_pct": round(roe * 100, 1) if roe is not None else None,
            "currency": info.get("currency"),
            "sector": info.get("sector"),
        })

    if not rows:
        raise HTTPException(status_code=400, detail="유효한 종목 코드가 없습니다.")

    valid_rows = [r for r in rows if not r.get("error")]
    leader = None
    if valid_rows:
        leader = max(
            valid_rows,
            key=lambda r: (
                r.get("operating_margin_pct") if r.get("operating_margin_pct") is not None else -999,
                r.get("roe_pct") if r.get("roe_pct") is not None else -999,
            ),
        ).get("company")

    return {
        "rows": rows,
        "leader": leader,
        "notes": [
            "동종 기업 여부를 먼저 확인한 뒤 멀티플 차이를 해석하세요.",
            "PER/PBR은 성장률, 수익성, 재무건전성과 함께 봐야 합니다.",
            "Yahoo Finance 항목 누락 시 일부 값은 빈칸으로 표시됩니다.",
        ],
    }


LIFECYCLE_DATA = {
    "도입기": {
        "idx": 0, "color": "#3b82f6",
        "chars": ["매출 낮음·손실 가능", "높은 R&D 비용", "선도자 이점 확보 기회"],
        "strategy": ["성장주 투자", "VC/초기 투자", "기술 모멘텀 추종"],
        "examples": ["양자컴퓨터", "뇌-컴퓨터 인터페이스", "핵융합"],
    },
    "성장기": {
        "idx": 1, "color": "#22c55e",
        "chars": ["매출 급증", "경쟁자 진입 시작", "규모의 경제 달성"],
        "strategy": ["성장주 비중 확대", "시장점유율 1위 기업 주목", "PEG 지표 활용"],
        "examples": ["AI 반도체", "전기차", "클라우드"],
    },
    "성숙기": {
        "idx": 2, "color": "#f59e0b",
        "chars": ["성장 둔화", "가격경쟁 심화", "배당·자사주 매입 증가"],
        "strategy": ["가치주·배당주 투자", "PER·PBR 저평가 선별", "FCF 중심 분석"],
        "examples": ["스마트폰", "자동차", "은행"],
    },
    "쇠퇴기": {
        "idx": 3, "color": "#ef4444",
        "chars": ["매출 감소", "구조조정·M&A", "대체재에 시장 잠식"],
        "strategy": ["Short 전략 고려", "방어주 비중 축소", "Exit 타이밍 관리"],
        "examples": ["인쇄매체", "유선전화", "DVD 렌탈"],
    },
}

@app.post("/api/industry/lifecycle")
def industry_lifecycle(req: LifecycleRequest) -> dict[str, object]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    import io, base64
    configure_matplotlib_korean_font(plt)

    DARK, SURF, BORDER, TEXT, MUTED = "#0f172a","#1e293b","#334155","#e2e8f0","#64748b"

    stage_info = LIFECYCLE_DATA.get(req.stage, LIFECYCLE_DATA["성장기"])
    cur_idx    = stage_info["idx"]

    # S-curve (logistic)
    x = np.linspace(-6, 10, 400)
    y = 100 / (1 + np.exp(-x * 0.9))          # 도입~성숙
    decline = np.linspace(0, 1, 100)
    x_full  = np.concatenate([x, x[-1] + decline * 4])
    y_full  = np.concatenate([y, y[-1] - decline * 35])  # 쇠퇴

    # 각 단계 x 범위
    stage_x = [(-6, -1.5), (-1.5, 3), (3, 7), (7, x_full[-1])]
    stage_colors = [d["color"] for d in LIFECYCLE_DATA.values()]
    stage_names  = list(LIFECYCLE_DATA.keys())

    fig, (ax_main, ax_info) = plt.subplots(1, 2, figsize=(14, 7),
                                           gridspec_kw={"width_ratios": [3, 2]},
                                           facecolor=DARK)

    # ── 메인: S-curve ────────────────────────────────────────────────────────
    ax_main.set_facecolor(SURF)
    for i, ((x0, x1), col, name) in enumerate(zip(stage_x, stage_colors, stage_names)):
        mask = (x_full >= x0) & (x_full <= x1)
        alpha = 0.9 if i == cur_idx else 0.35
        lw    = 3.5 if i == cur_idx else 1.5
        ax_main.plot(x_full[mask], y_full[mask], color=col, lw=lw, alpha=alpha, zorder=3)
        mid_x = (x0 + x1) / 2
        mid_y = np.interp(mid_x, x_full, y_full)
        ax_main.text(mid_x, mid_y + (8 if i != 3 else -8), name,
                     ha="center", fontsize=10, color=col,
                     fontweight="bold" if i == cur_idx else "normal",
                     bbox=dict(boxstyle="round,pad=0.3",
                               facecolor=SURF if i != cur_idx else col + "33",
                               edgecolor=col, linewidth=1.5 if i == cur_idx else 0.8))
        # 단계 구분선
        if i < 3:
            ax_main.axvline(x1, color=BORDER, lw=1, ls=":", alpha=0.7)

    # 현재 위치 표시
    cur_x0, cur_x1 = stage_x[cur_idx]
    cur_mid = (cur_x0 + cur_x1) / 2
    cur_y   = np.interp(cur_mid, x_full, y_full)
    ax_main.scatter([cur_mid], [cur_y], color=stage_info["color"],
                    s=200, zorder=5, edgecolors=TEXT, linewidths=1.5)
    ax_main.annotate(f"▶ {req.industry}\n({req.stage})",
                     xy=(cur_mid, cur_y), xytext=(cur_mid + 0.5, cur_y - 18),
                     fontsize=9, color=stage_info["color"], fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color=stage_info["color"], lw=1.5))

    ax_main.set_xlabel("시간 →", color=MUTED, fontsize=10)
    ax_main.set_ylabel("시장 규모 / 매출", color=MUTED, fontsize=10)
    ax_main.set_title("산업 생애주기 (Industry Life Cycle)", color=TEXT,
                      fontsize=11, fontweight="bold", pad=10)
    ax_main.tick_params(colors=MUTED, labelsize=7)
    ax_main.set_xticklabels([])
    ax_main.spines[:].set_color(BORDER)
    ax_main.set_ylim(-5, 115)

    # ── 사이드: 단계별 특성표 ────────────────────────────────────────────────
    ax_info.set_facecolor(DARK)
    ax_info.axis("off")

    y_pos = 0.97
    ax_info.text(0.5, y_pos, f"{req.industry}  |  {req.stage}", ha="center",
                 fontsize=12, fontweight="bold", color=stage_info["color"],
                 transform=ax_info.transAxes)
    y_pos -= 0.08

    sections = [
        ("특징", stage_info["chars"], "#e2e8f0"),
        ("투자 전략", stage_info["strategy"], "#3b82f6"),
        ("예시 산업", stage_info["examples"], "#a855f7"),
    ]
    for title, items, col in sections:
        ax_info.text(0.05, y_pos, title, fontsize=9, fontweight="bold",
                     color=col, transform=ax_info.transAxes)
        y_pos -= 0.06
        for item in items:
            ax_info.text(0.08, y_pos, f"• {item}", fontsize=8.5, color=TEXT,
                         transform=ax_info.transAxes)
            y_pos -= 0.065
        y_pos -= 0.02

    # 4단계 요약 타임라인
    y_pos -= 0.02
    ax_info.text(0.5, y_pos, "── 4단계 흐름 ──", ha="center",
                 fontsize=8, color=MUTED, transform=ax_info.transAxes)
    y_pos -= 0.065
    for i, (name, data) in enumerate(LIFECYCLE_DATA.items()):
        marker = "●" if i == cur_idx else "○"
        weight = "bold" if i == cur_idx else "normal"
        ax_info.text(0.1 + i * 0.22, y_pos, f"{marker}\n{name}", ha="center",
                     fontsize=8, color=data["color"], fontweight=weight,
                     transform=ax_info.transAxes)

    fig.suptitle("산업 생애주기 분석  |  단계별 투자 전략",
                 color=TEXT, fontsize=12, fontweight="bold", y=0.99)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, facecolor=DARK, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    img = "data:image/png;base64," + base64.b64encode(buf.read()).decode()

    return {"image": img, "stage": req.stage, "industry": req.industry,
            "characteristics": stage_info["chars"],
            "strategies": stage_info["strategy"]}


# ── 거시경제현황 1: yfinance 실시간 ──────────────────────────────────────────

class MacroRealtimeRequest(BaseModel):
    tickers: list[str] = ["^TNX", "CL=F", "^GSPC", "^KS11", "GC=F", "EURUSD=X"]
    period:  str       = "1y"   # 1mo 3mo 6mo 1y 2y 5y

TICKER_LABELS = {
    "^TNX":     "미국 10년물 금리",
    "CL=F":     "WTI 유가",
    "^GSPC":    "S&P 500",
    "^KS11":    "KOSPI",
    "GC=F":     "금 (Gold)",
    "EURUSD=X": "EUR/USD",
    "BTC-USD":  "Bitcoin",
    "^IRX":     "미국 단기금리(3M)",
    "^VIX":     "VIX 공포지수",
    "DX-Y.NYB": "달러 인덱스",
}

@app.post("/api/macro/realtime")
def macro_realtime(req: MacroRealtimeRequest) -> dict[str, object]:
    import yfinance as yf
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import numpy as np
    import pandas as pd
    import io, base64
    configure_matplotlib_korean_font(plt)

    DARK   = "#0f172a"
    SURF   = "#1e293b"
    BORDER = "#334155"
    TEXT   = "#e2e8f0"
    MUTED  = "#64748b"
    COLORS = ["#3b82f6","#22c55e","#f59e0b","#ef4444","#a855f7","#06b6d4","#f97316","#84cc16"]

    if not req.tickers:
        raise HTTPException(status_code=400, detail="최소 1개 종목을 선택하세요.")

    # ── 데이터 fetch ──────────────────────────────────────────────────────────
    raw: dict[str, pd.Series] = {}
    fetch_error: str | None = None
    for t in req.tickers:
        try:
            df = yf.download(t, period=req.period, progress=False, auto_adjust=True)
            if df.empty:
                continue
            close = df["Close"]
            if isinstance(close, pd.DataFrame):
                close = close.iloc[:, 0]
            close = close.dropna()
            if len(close) > 0:
                raw[t] = close
        except Exception as e:
            fetch_error = str(e)

    # ── 실시간 데이터 없을 때 GBM 시뮬레이션으로 폴백 ──────────────────────────
    is_simulated = False
    if not raw:
        is_simulated = True
        rng_fb = np.random.default_rng(42)
        n_days = {"1mo": 22, "3mo": 66, "6mo": 132, "1y": 252,
                  "2y": 504, "5y": 1260}.get(req.period, 252)
        BASE = {
            "^TNX": (4.20, 0.0, 0.40), "CL=F": (78.0, 0.03, 0.35),
            "^GSPC": (4800, 0.08, 0.17), "^KS11": (2650, 0.06, 0.18),
            "GC=F": (2000, 0.05, 0.14), "EURUSD=X": (1.08, -0.01, 0.07),
            "BTC-USD": (45000, 0.20, 0.70), "^IRX": (5.25, 0.0, 0.15),
            "^VIX": (18.0, 0.0, 0.80), "DX-Y.NYB": (104.0, 0.01, 0.06),
        }
        dt = 1 / 252
        for t in req.tickers:
            s0, mu, sigma = BASE.get(t, (100, 0.05, 0.20))
            shocks = rng_fb.standard_normal(n_days)
            log_r  = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks
            vals   = s0 * np.exp(np.cumsum(log_r))
            idx    = pd.date_range(end=pd.Timestamp.today(), periods=n_days, freq="B")
            raw[t] = pd.Series(vals, index=idx)

    labels_used = [TICKER_LABELS.get(t, t) for t in raw]

    # ── 정규화 수익률 ─────────────────────────────────────────────────────────
    norm: dict[str, pd.Series] = {}
    for t, s in raw.items():
        norm[t] = (s / s.iloc[0] - 1) * 100

    # ── 공통 날짜로 상관관계 DataFrame ────────────────────────────────────────
    combined = pd.DataFrame({TICKER_LABELS.get(t, t): s for t, s in raw.items()})
    combined = combined.dropna()
    corr = combined.pct_change().dropna().corr()

    # ── Figure ────────────────────────────────────────────────────────────────
    n = len(raw)
    fig = plt.figure(figsize=(14, 11), facecolor=DARK)
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35,
                            left=0.07, right=0.97, top=0.93, bottom=0.07)

    # Panel 1: 원시 가격 추세
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(SURF)
    for i, (t, s) in enumerate(raw.items()):
        ax2_ = ax1.twinx() if i > 0 else ax1
        col  = COLORS[i % len(COLORS)]
        lbl  = TICKER_LABELS.get(t, t)
        if i == 0:
            ax1.plot(s.index, s.values, color=col, lw=1.5, label=lbl)
        # 정규화 차트가 더 유용하므로 여기선 첫 종목만 왼쪽 축에 표시
    ax1.tick_params(colors=TEXT, labelsize=7)
    ax1.set_title("가격 추이 (첫 번째 종목 기준)", color=TEXT, fontsize=9, pad=6)
    ax1.spines[:].set_color(BORDER)
    ax1.set_xlabel("")
    ax1.tick_params(axis='x', rotation=30)
    for label in ax1.get_xticklabels(): label.set_fontsize(6)

    # Panel 2: 정규화 수익률 (누적 %)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(SURF)
    for i, (t, s) in enumerate(norm.items()):
        ax2.plot(s.index, s.values, color=COLORS[i % len(COLORS)],
                 lw=1.5, label=TICKER_LABELS.get(t, t))
    ax2.axhline(0, color=MUTED, lw=0.8, ls="--")
    ax2.set_title("정규화 누적 수익률 (%)", color=TEXT, fontsize=9, pad=6)
    ax2.tick_params(colors=TEXT, labelsize=7)
    ax2.spines[:].set_color(BORDER)
    ax2.legend(fontsize=6, facecolor=SURF, labelcolor=TEXT,
               loc="upper left", framealpha=0.7)
    ax2.tick_params(axis='x', rotation=30)
    for label in ax2.get_xticklabels(): label.set_fontsize(6)

    # Panel 3: 상관관계 히트맵
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(SURF)
    if len(corr) > 1:
        cmat = corr.values
        im = ax3.imshow(cmat, cmap="RdYlGn", vmin=-1, vmax=1, aspect="auto")
        ax3.set_xticks(range(len(corr.columns)))
        ax3.set_yticks(range(len(corr.columns)))
        ax3.set_xticklabels(corr.columns, rotation=45, ha="right",
                            fontsize=7, color=TEXT)
        ax3.set_yticklabels(corr.columns, fontsize=7, color=TEXT)
        for ii in range(len(cmat)):
            for jj in range(len(cmat)):
                v = cmat[ii, jj]
                ax3.text(jj, ii, f"{v:.2f}", ha="center", va="center",
                         fontsize=7, color="white" if abs(v) > 0.5 else TEXT)
        plt.colorbar(im, ax=ax3, fraction=0.04, pad=0.02).ax.tick_params(
            labelcolor=TEXT, labelsize=7)
    else:
        ax3.text(0.5, 0.5, "2개 이상 선택 시\n상관관계 표시", ha="center",
                 va="center", color=MUTED, transform=ax3.transAxes, fontsize=9)
    ax3.set_title("수익률 상관관계 히트맵", color=TEXT, fontsize=9, pad=6)
    ax3.spines[:].set_color(BORDER)

    # Panel 4: 최근 수익률 바 차트 (1M / 3M / 기간 전체)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(SURF)
    period_returns = {}
    for t, s in raw.items():
        lbl = TICKER_LABELS.get(t, t)
        period_returns[lbl] = (s.iloc[-1] / s.iloc[0] - 1) * 100
    names  = list(period_returns.keys())
    values = list(period_returns.values())
    bar_colors = [COLORS[i % len(COLORS)] for i in range(len(names))]
    bars = ax4.barh(names, values, color=bar_colors, height=0.55)
    ax4.axvline(0, color=MUTED, lw=0.8)
    for bar, v in zip(bars, values):
        ax4.text(v + (0.5 if v >= 0 else -0.5), bar.get_y() + bar.get_height()/2,
                 f"{v:+.1f}%", va="center", ha="left" if v >= 0 else "right",
                 fontsize=7, color=TEXT)
    ax4.set_title(f"기간 전체 수익률 ({req.period})", color=TEXT, fontsize=9, pad=6)
    ax4.tick_params(colors=TEXT, labelsize=7)
    ax4.spines[:].set_color(BORDER)

    title_suffix = "  [시뮬레이션 — 실시간 연결 불가]" if is_simulated else "  (Yahoo Finance)"
    fig.suptitle(f"거시경제현황 — 실시간 데이터{title_suffix}", color=TEXT,
                 fontsize=12, fontweight="bold", y=0.97)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, facecolor=DARK)
    plt.close(fig)
    buf.seek(0)
    img_b64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode()

    # ── 요약 통계 ─────────────────────────────────────────────────────────────
    summary = {}
    for t, s in raw.items():
        lbl = TICKER_LABELS.get(t, t)
        ret  = (s.iloc[-1] / s.iloc[0] - 1) * 100
        vol  = s.pct_change().std() * (252 ** 0.5) * 100
        summary[lbl] = {
            "current": round(float(s.iloc[-1]), 4),
            "return_pct": round(ret, 2),
            "annual_vol_pct": round(vol, 2),
        }

    return {"image": img_b64, "summary": summary, "period": req.period,
            "n_tickers": len(raw),
            "is_simulated": is_simulated,
            "warning": "Yahoo Finance 요청 한도 초과로 시뮬레이션 데이터를 표시합니다. 잠시 후 다시 시도하세요." if is_simulated else None}


# ── 거시경제현황 2: GBM 시뮬레이션 대시보드 ──────────────────────────────────

class MacroSimRequest(BaseModel):
    n_days:    int   = 252
    seed:      int   = 42

@app.post("/api/macro/simulation")
def macro_simulation(req: MacroSimRequest) -> dict[str, object]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import numpy as np
    import io, base64
    configure_matplotlib_korean_font(plt)

    DARK   = "#0f172a"
    SURF   = "#1e293b"
    BORDER = "#334155"
    TEXT   = "#e2e8f0"
    MUTED  = "#64748b"
    COLORS = ["#3b82f6","#f59e0b","#ef4444","#22c55e","#a855f7","#06b6d4"]

    rng = np.random.default_rng(req.seed)
    T   = max(60, min(req.n_days, 1260))
    dt  = 1 / 252

    def gbm(s0, mu, sigma, n, rng):
        shocks = rng.standard_normal(n)
        log_r  = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks
        return s0 * np.exp(np.cumsum(log_r))

    indicators = {
        "기준금리 (%)" :   {"s0": 3.50,  "mu":  0.05, "sigma": 0.08,  "fmt": ".2f"},
        "CPI (전년비 %)":  {"s0": 3.20,  "mu":  0.02, "sigma": 0.12,  "fmt": ".2f"},
        "WTI 유가 ($)":    {"s0": 78.0,  "mu":  0.03, "sigma": 0.30,  "fmt": ".1f"},
        "USD/KRW":         {"s0": 1320,  "mu": -0.01, "sigma": 0.07,  "fmt": ".0f"},
        "KOSPI":           {"s0": 2650,  "mu":  0.06, "sigma": 0.18,  "fmt": ".0f"},
        "S&P 500":         {"s0": 5200,  "mu":  0.08, "sigma": 0.16,  "fmt": ".0f"},
    }

    # macro regime: 경기 사이클 phase 추가 (상승/둔화/침체/회복)
    phase_len  = T // 4
    phases     = ["상승기", "과열기", "침체기", "회복기"]
    phase_muls = [1.0, 0.5, -0.5, 1.2]

    series_dict = {}
    for name, cfg in indicators.items():
        mu_adj = cfg["mu"]
        vals = []
        for ph_i, mul in enumerate(phase_muls):
            seg = gbm(cfg["s0"] if not vals else vals[-1],
                      mu_adj * mul, cfg["sigma"],
                      min(phase_len, T - len(vals)), rng)
            vals.extend(seg.tolist())
            if len(vals) >= T:
                break
        series_dict[name] = np.array(vals[:T])

    days = np.arange(T)

    # ── Figure ────────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(14, 12), facecolor=DARK)
    gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35,
                            left=0.08, right=0.97, top=0.93, bottom=0.05)

    names_list = list(series_dict.keys())
    for idx, (name, vals) in enumerate(series_dict.items()):
        row, col = divmod(idx, 2)
        ax = fig.add_subplot(gs[row, col])
        ax.set_facecolor(SURF)
        color = COLORS[idx]
        cfg   = indicators[name]

        ax.plot(days, vals, color=color, lw=1.5)
        ax.fill_between(days, vals, vals[0], alpha=0.12, color=color)

        # 경기국면 배경
        for ph_i, (ph_name, mul) in enumerate(zip(phases, phase_muls)):
            x0 = ph_i * phase_len
            x1 = min((ph_i + 1) * phase_len, T)
            bg = "#22c55e22" if mul > 0.8 else "#f59e0b22" if mul > 0 else "#ef444422"
            ax.axvspan(x0, x1, color=bg, alpha=0.4)
            ax.text((x0 + x1) / 2, ax.get_ylim()[0], ph_name,
                    ha="center", va="bottom", fontsize=6, color=MUTED)

        cur  = vals[-1]
        chg  = (cur / vals[0] - 1) * 100
        sign = "+" if chg >= 0 else ""
        ax.set_title(f"{name}  현재: {cur:{cfg['fmt']}}  ({sign}{chg:.1f}%)",
                     color=TEXT, fontsize=8.5, pad=5)
        ax.tick_params(colors=TEXT, labelsize=7)
        ax.spines[:].set_color(BORDER)
        ax.set_xlim(0, T)

        # 최고/최저 표시
        hi, lo = np.argmax(vals), np.argmin(vals)
        ax.annotate(f"고: {vals[hi]:{cfg['fmt']}}",
                    xy=(hi, vals[hi]), xytext=(5, 5), textcoords="offset points",
                    fontsize=6, color="#22c55e", arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.5))
        ax.annotate(f"저: {vals[lo]:{cfg['fmt']}}",
                    xy=(lo, vals[lo]), xytext=(5, -12), textcoords="offset points",
                    fontsize=6, color="#ef4444", arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.5))

    # 경기국면 범례 (우측 상단)
    from matplotlib.patches import Patch
    legend_els = [
        Patch(facecolor="#22c55e44", label="상승기"),
        Patch(facecolor="#f59e0b44", label="과열기"),
        Patch(facecolor="#ef444444", label="침체기"),
        Patch(facecolor="#22c55e44", label="회복기"),
    ]
    fig.legend(handles=legend_els, loc="upper right", fontsize=7,
               facecolor=SURF, labelcolor=TEXT, framealpha=0.8, ncol=4,
               bbox_to_anchor=(0.97, 0.995))

    fig.suptitle(f"거시경제 시뮬레이션 대시보드 — {T}거래일 GBM 시뮬레이션",
                 color=TEXT, fontsize=12, fontweight="bold", y=0.975)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, facecolor=DARK)
    plt.close(fig)
    buf.seek(0)
    img_b64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode()

    summary = {name: {"start": round(float(v[0]), 2),
                      "end":   round(float(v[-1]), 2),
                      "chg_pct": round((v[-1]/v[0]-1)*100, 2)}
               for name, v in series_dict.items()}

    return {"image": img_b64, "summary": summary, "n_days": T}


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
