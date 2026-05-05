"""
QuantPipeline.py — 퀀트 실전 4단계 통합 파이프라인
====================================================
Phase 1~4 전 과정을 하나의 스크립트로 실행

실행:
    python QuantPipeline.py

4단계 파이프라인:
    1단계: 데이터 수집 & 정리  (yfinance / 시뮬레이션 fallback)
    2단계: 기술적 지표 계산    (MA, RSI, 볼린저밴드, MACD, ATR)
    3단계: 백테스트            (CAGR, Sharpe, MDD, 승률, 손익비)
    4단계: ML 방향 예측        (RandomForest + 시계열 교차검증)

DOC/Chapter16.md 에서 상세 설명을 확인하세요.
"""

from __future__ import annotations

import warnings
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

matplotlib.use("Agg")
warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────────────────────
# 0. 설정
# ──────────────────────────────────────────────────────────────

TICKER      = "SPY"         # 분석 대상 (변경 가능: QQQ, AAPL, 005930.KS)
START_DATE  = "2015-01-01"
MA_FAST     = 20
MA_SLOW     = 60
RISK_FREE   = 0.03          # 무위험 수익률 (연)
CAPITAL     = 10_000_000    # 초기 자본 (원/달러)


# ──────────────────────────────────────────────────────────────
# 1단계: 데이터 수집 & 정리
# ──────────────────────────────────────────────────────────────

def load_data(ticker: str, start: str) -> pd.DataFrame:
    """
    yfinance로 데이터 수집.
    yfinance 미설치 시 GBM 시뮬레이션으로 fallback.
    """
    try:
        import yfinance as yf
        df = yf.download(ticker, start=start, progress=False, auto_adjust=True)
        if df.empty:
            raise ValueError("빈 데이터")
        # yfinance 멀티인덱스 정리
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        print(f"  ✅ yfinance: {ticker} ({len(df)}일)")
        return df
    except Exception as e:
        print(f"  ⚠️  yfinance 실패 ({e}) → GBM 시뮬레이션 사용")
        return _simulate_ohlcv(n=2520, start=start)   # 약 10년


def _simulate_ohlcv(n: int = 2520, start: str = "2015-01-01") -> pd.DataFrame:
    """기하 브라운 운동(GBM)으로 OHLCV 시뮬레이션"""
    rng = np.random.default_rng(42)
    dt  = 1 / 252
    mu, sigma = 0.10, 0.18   # 연간 수익률·변동성

    log_rets = rng.normal((mu - 0.5 * sigma**2) * dt, sigma * np.sqrt(dt), n)
    closes   = 100.0 * np.exp(np.cumsum(log_rets))
    closes   = np.insert(closes, 0, 100.0)[:-1]

    intra_vol = sigma * np.sqrt(dt) * 0.5
    highs  = closes * (1 + abs(rng.normal(0, intra_vol, n)))
    lows   = closes * (1 - abs(rng.normal(0, intra_vol, n)))
    opens  = closes * (1 + rng.normal(0, intra_vol / 2, n))
    vols   = rng.integers(1_000_000, 10_000_000, n).astype(float)

    idx = pd.date_range(start, periods=n, freq="B")
    return pd.DataFrame(
        {"Open": opens, "High": highs, "Low": lows, "Close": closes, "Volume": vols},
        index=idx,
    )


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """결측치 제거 & 수익률 계산"""
    df = df.copy().dropna()
    close = df["Close"]

    df["Daily_Return"] = close.pct_change()
    df["Log_Return"]   = np.log(close / close.shift(1))
    df["Cum_Return"]   = (1 + df["Daily_Return"]).cumprod() - 1

    annual_ret = df["Daily_Return"].mean() * 252
    annual_vol = df["Daily_Return"].std()  * np.sqrt(252)

    print(f"  기간      : {df.index[0].date()} ~ {df.index[-1].date()}  ({len(df)}일)")
    print(f"  연간 수익률: {annual_ret:+.2%}")
    print(f"  연간 변동성: {annual_vol:.2%}")
    return df


# ──────────────────────────────────────────────────────────────
# 2단계: 기술적 지표 계산
# ──────────────────────────────────────────────────────────────

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """MA, RSI, 볼린저밴드, MACD, ATR 추가"""
    df  = df.copy()
    c   = df["Close"]

    # ── 이동평균선 ─────────────────────────────────────────────
    for w in [5, 20, 60, 120]:
        df[f"MA{w}"] = c.rolling(w).mean()

    # ── RSI ────────────────────────────────────────────────────
    delta = c.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    df["RSI"] = 100 - 100 / (1 + gain / loss)

    # ── 볼린저 밴드 ────────────────────────────────────────────
    ma20 = c.rolling(20).mean()
    std20 = c.rolling(20).std()
    df["BB_mid"] = ma20
    df["BB_up"]  = ma20 + 2 * std20
    df["BB_dn"]  = ma20 - 2 * std20
    df["BB_pct"] = (c - df["BB_dn"]) / (4 * std20).replace(0, np.nan)  # %B

    # ── MACD ───────────────────────────────────────────────────
    ema12 = c.ewm(span=12, adjust=False).mean()
    ema26 = c.ewm(span=26, adjust=False).mean()
    df["MACD"]      = ema12 - ema26
    df["MACD_sig"]  = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_hist"] = df["MACD"] - df["MACD_sig"]

    # ── ATR (변동성 지표) ─────────────────────────────────────
    hl  = df["High"] - df["Low"]
    hcp = (df["High"] - df["Close"].shift(1)).abs()
    lcp = (df["Low"]  - df["Close"].shift(1)).abs()
    df["ATR"] = pd.concat([hl, hcp, lcp], axis=1).max(axis=1).rolling(14).mean()

    print(f"  지표 추가: MA(5/20/60/120) · RSI · 볼린저밴드 · MACD · ATR")
    return df


# ──────────────────────────────────────────────────────────────
# 3단계: 백테스트
# ──────────────────────────────────────────────────────────────

def run_backtest(df: pd.DataFrame, fast: int = MA_FAST, slow: int = MA_SLOW) -> pd.DataFrame:
    """MA 크로스오버 전략 백테스트"""
    df = df.copy()
    df["Signal"]   = (df[f"MA{fast}"] > df[f"MA{slow}"]).astype(int)
    df["Position"] = df["Signal"].shift(1).fillna(0)   # 미래 누수 방지

    df["Strategy_Ret"] = df["Position"] * df["Daily_Return"]
    df["BH_Ret"]       = df["Daily_Return"]

    df["Strategy_Cum"] = (1 + df["Strategy_Ret"]).cumprod()
    df["BH_Cum"]       = (1 + df["BH_Ret"]).cumprod()
    return df.dropna()


def calc_metrics(df: pd.DataFrame) -> dict:
    """핵심 성과 지표 계산"""
    strat = df["Strategy_Ret"]
    bh    = df["BH_Ret"]
    cum_s = df["Strategy_Cum"]
    cum_b = df["BH_Cum"]
    n_yr  = len(strat) / 252

    def cagr(cum):
        return float(cum.iloc[-1] ** (1 / n_yr) - 1) if n_yr > 0 else 0.0

    def sharpe(rets):
        excess = rets - RISK_FREE / 252
        return float(excess.mean() / excess.std() * np.sqrt(252)) if excess.std() > 0 else 0.0

    def mdd(cum):
        return float((cum / cum.cummax() - 1).min())

    def win_rate(rets):
        active = rets[rets != 0]
        return float((active > 0).mean()) if len(active) > 0 else 0.0

    def profit_factor(rets):
        wins   = rets[rets > 0].sum()
        losses = rets[rets < 0].abs().sum()
        return float(wins / losses) if losses > 0 else float("inf")

    return {
        "cagr_s":    cagr(cum_s),    "cagr_bh":    cagr(cum_b),
        "sharpe_s":  sharpe(strat),  "sharpe_bh":  sharpe(bh),
        "mdd_s":     mdd(cum_s),     "mdd_bh":     mdd(cum_b),
        "win_rate":  win_rate(strat),
        "pf":        profit_factor(strat),
        "total_s":   float(cum_s.iloc[-1] - 1),
        "total_bh":  float(cum_b.iloc[-1] - 1),
        "n_trades":  int(df["Signal"].diff().abs().sum()),
    }


def print_metrics(m: dict) -> None:
    print(f"\n{'지표':22s} {'전략':>12s} {'Buy & Hold':>12s}")
    print("-" * 50)
    rows = [
        ("총 수익률",    f"{m['total_s']:>12.2%}",  f"{m['total_bh']:>12.2%}"),
        ("CAGR",        f"{m['cagr_s']:>12.2%}",   f"{m['cagr_bh']:>12.2%}"),
        ("Sharpe Ratio",f"{m['sharpe_s']:>12.2f}", f"{m['sharpe_bh']:>12.2f}"),
        ("MDD",         f"{m['mdd_s']:>12.2%}",    f"{m['mdd_bh']:>12.2%}"),
        ("승률",         f"{m['win_rate']:>12.2%}",  ""),
        ("손익비",       f"{m['pf']:>12.2f}",        ""),
        ("총 거래 횟수", f"{m['n_trades']:>12}회",   ""),
    ]
    for label, vs, vb in rows:
        print(f"  {label:20s} {vs} {vb}")
    print("-" * 50)
    print(f"\n🎯 합격 기준 체크")
    print(f"   Sharpe > 1.0: {'✅ 합격' if m['sharpe_s'] > 1.0 else '⚠️ 미달'}  ({m['sharpe_s']:.2f})")
    print(f"   MDD > -15%:   {'✅ 합격' if m['mdd_s'] > -0.15 else '⚠️ 미달'}  ({m['mdd_s']:.2%})")


# ──────────────────────────────────────────────────────────────
# 4단계: ML 방향 예측 (RandomForest)
# ──────────────────────────────────────────────────────────────

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """기술 지표 → ML 피처 변환"""
    c    = df["Close"]
    feat = pd.DataFrame(index=df.index)

    # 가격 모멘텀
    for n in [1, 3, 5, 10, 20, 60]:
        feat[f"ret_{n}d"] = c.pct_change(n)

    # 이동평균 비율
    for s, l in [(5, 20), (20, 60), (60, 120)]:
        feat[f"ma_ratio_{s}_{l}"] = (
            c.rolling(s).mean() / c.rolling(l).mean() - 1
        )

    # 보조 지표 (이미 df에 있음)
    feat["rsi"]     = df["RSI"]
    feat["bb_pct"]  = df["BB_pct"]
    feat["macd"]    = df["MACD"]
    feat["macd_sig"]= df["MACD_sig"]
    feat["atr_pct"] = df["ATR"] / c

    # 거래량 비율
    feat["vol_ratio"] = (
        df["Volume"] / df["Volume"].rolling(20).mean()
    )

    # 변동성
    feat["vol_20"] = c.pct_change().rolling(20).std()

    # 타깃: 다음날 수익률 양수=1, 음수=0
    feat["target"] = (c.pct_change().shift(-1) > 0).astype(int)

    return feat.dropna()


def run_ml(feat: pd.DataFrame) -> dict:
    """RandomForest + 시계열 교차검증"""
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import TimeSeriesSplit
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score

    X = feat.drop("target", axis=1)
    y = feat["target"]

    tscv   = TimeSeriesSplit(n_splits=5)
    scaler = StandardScaler()
    model  = RandomForestClassifier(
        n_estimators=200, max_depth=5, min_samples_leaf=10,
        random_state=42, n_jobs=-1,
    )
    scores = []

    for tr_idx, te_idx in tscv.split(X):
        X_tr, X_te = X.iloc[tr_idx], X.iloc[te_idx]
        y_tr, y_te = y.iloc[tr_idx], y.iloc[te_idx]

        X_tr_s = scaler.fit_transform(X_tr)
        X_te_s = scaler.transform(X_te)

        model.fit(X_tr_s, y_tr)
        scores.append(accuracy_score(y_te, model.predict(X_te_s)))

    # 전체 데이터로 재학습 → 피처 중요도
    model.fit(scaler.fit_transform(X), y)
    importance = pd.Series(
        model.feature_importances_, index=X.columns
    ).sort_values(ascending=False)

    return {
        "scores":     scores,
        "mean_acc":   float(np.mean(scores)),
        "std_acc":    float(np.std(scores)),
        "importance": importance,
        "model":      model,
        "scaler":     scaler,
        "features":   X.columns.tolist(),
    }


# ──────────────────────────────────────────────────────────────
# 시각화 — 4단계 통합 대시보드
# ──────────────────────────────────────────────────────────────

def plot_dashboard(df: pd.DataFrame, metrics: dict, ml: dict) -> None:
    """4개 패널 통합 대시보드"""
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle(
        f"퀀트 실전 파이프라인 — {TICKER}  (MA{MA_FAST}/MA{MA_SLOW})",
        fontsize=14, fontweight="bold", y=1.01,
    )
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

    close = df["Close"]

    # ── 1. 주가 + MA + 신호 ──────────────────────────────────
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.plot(df.index, close,          color="#94a3b8", lw=1,   label="종가")
    ax1.plot(df.index, df[f"MA{MA_FAST}"], color="#2563eb", lw=1.5, label=f"MA{MA_FAST}")
    ax1.plot(df.index, df[f"MA{MA_SLOW}"], color="#f97316", lw=1.5, label=f"MA{MA_SLOW}")

    buy_mask  = (df["Signal"] == 1) & (df["Signal"].shift(1) == 0)
    sell_mask = (df["Signal"] == 0) & (df["Signal"].shift(1) == 1)
    ax1.scatter(df.index[buy_mask],  close[buy_mask],  marker="^", color="#16a34a", s=50, zorder=5)
    ax1.scatter(df.index[sell_mask], close[sell_mask], marker="v", color="#dc2626", s=50, zorder=5)
    ax1.set_title(f"{TICKER} 주가 & 이동평균 (MA 크로스오버 신호)")
    ax1.legend(fontsize=8, ncol=4)
    ax1.grid(True, alpha=0.3)

    # ── 2. RSI ───────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.plot(df.index, df["RSI"], color="#7c3aed", lw=1)
    ax2.axhline(70, color="#dc2626", lw=1, ls="--", label="과매수(70)")
    ax2.axhline(30, color="#16a34a", lw=1, ls="--", label="과매도(30)")
    ax2.fill_between(df.index, df["RSI"], 70, where=(df["RSI"] > 70), color="#dc2626", alpha=0.2)
    ax2.fill_between(df.index, df["RSI"], 30, where=(df["RSI"] < 30), color="#16a34a", alpha=0.2)
    ax2.set_ylim(0, 100)
    ax2.set_title("RSI")
    ax2.legend(fontsize=7)
    ax2.grid(True, alpha=0.3)

    # ── 3. 누적 수익률 ────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, :2])
    ax3.plot(df.index, df["Strategy_Cum"], color="#2563eb", lw=2, label="전략")
    ax3.plot(df.index, df["BH_Cum"],       color="#94a3b8", lw=2, ls="--", label="Buy & Hold")
    ax3.axhline(1.0, color="#475569", lw=0.8, ls=":")
    ax3.set_title("누적 수익률 비교")
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)

    # ── 4. 낙폭 ─────────────────────────────────────────────
    drawdown = df["Strategy_Cum"] / df["Strategy_Cum"].cummax() - 1
    ax4 = fig.add_subplot(gs[1, 2])
    ax4.fill_between(df.index, drawdown * 100, 0, color="#dc2626", alpha=0.4)
    ax4.axhline(-15, color="#f97316", lw=1, ls="--", label="기준: -15%")
    ax4.set_title("낙폭 (Drawdown %)")
    ax4.legend(fontsize=7)
    ax4.grid(True, alpha=0.3)

    # ── 5. 성과 요약 테이블 ───────────────────────────────────
    ax5 = fig.add_subplot(gs[2, :2])
    ax5.axis("off")
    table_data = [
        ["총 수익률",     f"{metrics['total_s']:+.1%}",  f"{metrics['total_bh']:+.1%}"],
        ["CAGR",         f"{metrics['cagr_s']:+.2%}",   f"{metrics['cagr_bh']:+.2%}"],
        ["Sharpe Ratio", f"{metrics['sharpe_s']:.2f}", f"{metrics['sharpe_bh']:.2f}"],
        ["MDD",          f"{metrics['mdd_s']:.1%}",    f"{metrics['mdd_bh']:.1%}"],
        ["승률",          f"{metrics['win_rate']:.1%}",  ""],
        ["총 거래",       f"{metrics['n_trades']}회",    ""],
    ]
    table = ax5.table(
        cellText=table_data,
        colLabels=["지표", "전략", "Buy & Hold"],
        cellLoc="center", loc="center", bbox=[0, 0, 1, 1],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    ax5.set_title("성과 요약")

    # ── 6. ML 피처 중요도 ─────────────────────────────────────
    ax6 = fig.add_subplot(gs[2, 2])
    top_feat = ml["importance"].head(8)
    ax6.barh(range(len(top_feat)), top_feat.values, color="#2563eb", alpha=0.8)
    ax6.set_yticks(range(len(top_feat)))
    ax6.set_yticklabels(top_feat.index, fontsize=7)
    ax6.invert_yaxis()
    ax6.set_title(f"ML 피처 중요도 (CV 정확도: {ml['mean_acc']:.2%})")
    ax6.grid(True, alpha=0.3, axis="x")

    plt.savefig("quant_pipeline_result.png", dpi=130, bbox_inches="tight")
    print("✅ 차트 저장: quant_pipeline_result.png")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────
# 메인 실행
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    DIVIDER = "=" * 60

    print(DIVIDER)
    print(f"  퀀트 실전 4단계 파이프라인 — {TICKER}")
    print(DIVIDER)

    # ─── 1단계: 데이터 ────────────────────────────────────────
    print("\n🟦 1단계: 데이터 수집 & 정리")
    df = load_data(TICKER, START_DATE)
    df = clean_data(df)

    # ─── 2단계: 지표 ──────────────────────────────────────────
    print("\n🟩 2단계: 기술적 지표 계산")
    df = add_indicators(df)

    # ─── 3단계: 백테스트 ──────────────────────────────────────
    print("\n🟨 3단계: 백테스트")
    df = run_backtest(df)
    metrics = calc_metrics(df)
    print_metrics(metrics)

    # ─── 4단계: ML ────────────────────────────────────────────
    print("\n🟥 4단계: ML 방향 예측 (RandomForest)")
    try:
        feat = build_features(df)
        print(f"  피처: {feat.shape[1]-1}개  |  샘플: {feat.shape[0]}개")
        ml = run_ml(feat)
        print(f"  시계열 CV 정확도: {ml['mean_acc']:.2%} ± {ml['std_acc']:.2%}")
        print("  상위 5개 중요 피처:")
        for fname, fval in ml["importance"].head(5).items():
            bar = "█" * int(fval * 50)
            print(f"    {fname:22s}: {fval:.3f}  {bar}")
    except ImportError:
        print("  ⚠️  scikit-learn 미설치 → pip install scikit-learn")
        ml = {
            "mean_acc": 0.0, "std_acc": 0.0,
            "importance": pd.Series(dtype=float),
        }

    # ─── 시각화 ───────────────────────────────────────────────
    print("\n📊 대시보드 생성 중...")
    plot_dashboard(df, metrics, ml)

    # ─── 자동매매 골격 안내 ───────────────────────────────────
    print(f"\n{DIVIDER}")
    print("  💰 실전 자동매매 연결 방법 (DOC/Chapter16.md 참고)")
    print(DIVIDER)
    print("""
  국내:  pip install mojito2       → 한국투자증권 KIS API
  국내:  PyQt5 + 키움OpenAPI+      → 키움증권 (Windows)
  해외:  pip install alpaca-py     → Alpaca (미국, 무료 모의투자)
  해외:  pip install ib_insync     → Interactive Brokers (글로벌)
  알림:  pip install python-telegram-bot → 텔레그램 매매 알림

  예시:
    from alpaca.trading.client import TradingClient
    broker = TradingClient(API_KEY, SECRET_KEY, paper=True)
    account = broker.get_account()
    print(f"포트폴리오: ${account.portfolio_value}")
""")
    print("✅ 파이프라인 완료! quant_pipeline_result.png 를 확인하세요.")
