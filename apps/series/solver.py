"""
Series de tiempo (análisis) — lógica pura numpy/scipy.
Referencias: Hyndman & Athanasopoulos (FPP), Box-Jenkins, Enders.

  • Descomposición clásica por medias móviles (aditiva / multiplicativa) + fuerzas de
    tendencia y estacionalidad (Hyndman).
  • ACF y PACF con bandas de confianza (±1,96/√n).
  • Estacionariedad: prueba ADF (Dickey-Fuller aumentada) y KPSS, con valores críticos
    estándar y una herramienta de diferenciación (regular y estacional).
"""
import math
import numpy as np
from scipy import stats as sps


def _clean(y):
    y = np.asarray([v for v in y if v is not None], dtype=float)
    return y[~np.isnan(y)]


# --------------------------------------------------------------------------- #
#  Descomposición clásica
# --------------------------------------------------------------------------- #
def _cma(y, m):
    """Media móvil centrada de orden m (2×m si m es par)."""
    n = len(y)
    tr = np.full(n, np.nan)
    h = m // 2
    if m % 2 == 0:
        for t in range(h, n - h):
            tr[t] = (0.5 * y[t - h] + np.sum(y[t - h + 1:t + h]) + 0.5 * y[t + h]) / m
    else:
        for t in range(h, n - h):
            tr[t] = np.mean(y[t - h:t + h + 1])
    return tr


def descomponer(y, m, modelo="add"):
    y = _clean(y)
    n = len(y)
    if m < 2:
        raise ValueError("El período estacional m debe ser ≥ 2.")
    if n < 2 * m:
        raise ValueError(f"Se requieren al menos 2 ciclos completos (≥ {2*m} datos).")
    if modelo == "mul" and np.any(y <= 0):
        raise ValueError("La descomposición multiplicativa requiere valores > 0.")

    trend = _cma(y, m)
    detr = (y - trend) if modelo == "add" else (y / trend)

    seas_avg = np.array([np.nanmean(detr[fase::m]) for fase in range(m)])
    if modelo == "add":
        seas_avg = seas_avg - np.nanmean(seas_avg)
    else:
        seas_avg = seas_avg / np.nanmean(seas_avg)
    seasonal = seas_avg[np.arange(n) % m]

    resid = (y - trend - seasonal) if modelo == "add" else (y / (trend * seasonal))

    def var(a):
        a = a[~np.isnan(a)]
        return float(np.var(a)) if a.size else 0.0
    tr_r = trend + resid if modelo == "add" else None
    F_t = max(0.0, 1 - var(resid) / var((trend + resid) if modelo == "add" else (y / seasonal))) if var(resid) else 1.0
    F_s = max(0.0, 1 - var(resid) / var((seasonal + resid) if modelo == "add" else (y / trend))) if var(resid) else 1.0

    idx = list(range(1, n + 1))
    j2n = lambda a: [None if (isinstance(v, float) and np.isnan(v)) else float(v) for v in a]
    return {
        "modelo": modelo, "m": m, "n": n, "t": idx,
        "observado": j2n(y), "tendencia": j2n(trend),
        "estacional": j2n(seasonal), "residuo": j2n(resid),
        "indices_estacionales": [float(v) for v in seas_avg],
        "fuerza_tendencia": float(F_t), "fuerza_estacional": float(F_s),
        "interpretacion": _interp_desc(modelo, m, F_t, F_s, seas_avg),
    }


def _interp_desc(modelo, m, F_t, F_s, seas):
    it = [f"Descomposición {'aditiva (Y = T + S + R)' if modelo=='add' else 'multiplicativa (Y = T · S · R)'} con período m = {m}."]
    it.append(f"Fuerza de la tendencia F_T = {F_t:.2f} y de la estacionalidad F_S = {F_s:.2f} "
              "(0 = ausente, cercano a 1 = fuerte).")
    hi = int(np.argmax(seas)) + 1; lo = int(np.argmin(seas)) + 1
    it.append(f"El índice estacional más alto es la fase {hi} y el más bajo la fase {lo}: "
              f"{'suman/restan al nivel' if modelo=='add' else 'multiplican el nivel'} de forma sistemática cada ciclo.")
    it.append("El residuo debería verse sin patrón; si aún muestra estructura, el período m o el tipo de modelo pueden no ser los adecuados.")
    return it


# --------------------------------------------------------------------------- #
#  ACF y PACF
# --------------------------------------------------------------------------- #
def acf_pacf(y, nlags=None):
    y = _clean(y)
    n = len(y)
    if nlags is None:
        nlags = min(int(10 * math.log10(n)) + 1, n // 2)
    nlags = int(min(nlags, n - 1))
    ybar = np.mean(y)
    c0 = np.sum((y - ybar) ** 2)
    acf = [1.0]
    for k in range(1, nlags + 1):
        acf.append(float(np.sum((y[k:] - ybar) * (y[:-k] - ybar)) / c0))

    # PACF por Durbin-Levinson
    phi = np.zeros((nlags + 1, nlags + 1))
    pacf = [1.0]
    if nlags >= 1:
        phi[1][1] = acf[1]; pacf.append(acf[1])
        for k in range(2, nlags + 1):
            num = acf[k] - sum(phi[k - 1][j] * acf[k - j] for j in range(1, k))
            den = 1 - sum(phi[k - 1][j] * acf[j] for j in range(1, k))
            phi[k][k] = num / den if den != 0 else 0.0
            for j in range(1, k):
                phi[k][j] = phi[k - 1][j] - phi[k][k] * phi[k - 1][k - j]
            pacf.append(float(phi[k][k]))

    banda = 1.96 / math.sqrt(n)
    return {"n": n, "nlags": nlags, "acf": acf, "pacf": pacf, "banda": banda,
            "interpretacion": _interp_acf(acf, pacf, banda)}


def _interp_acf(acf, pacf, banda):
    sig_acf = [k for k in range(1, len(acf)) if abs(acf[k]) > banda]
    sig_pacf = [k for k in range(1, len(pacf)) if abs(pacf[k]) > banda]
    it = [f"Bandas de significancia ±{banda:.3f} (±1,96/√n): fuera de ellas, la autocorrelación es significativa."]
    if sig_acf and sig_acf[0] == 1 and len(sig_acf) > 3 and acf[1] > 0.5:
        it.append("La ACF decae lentamente: indicio de serie NO estacionaria (posible tendencia); considera diferenciar.")
    it.append(f"Rezagos significativos — ACF: {sig_acf[:8] if sig_acf else 'ninguno'} · PACF: {sig_pacf[:8] if sig_pacf else 'ninguno'}.")
    it.append("Guía Box-Jenkins: ACF que corta en q y PACF que decae → MA(q); PACF que corta en p y ACF que decae → AR(p); "
              "ambas decaen → ARMA. Picos en múltiplos de m sugieren estacionalidad.")
    return it


# --------------------------------------------------------------------------- #
#  Estacionariedad: ADF y KPSS
# --------------------------------------------------------------------------- #
_ADF_CV = {"c": {"1%": -3.4336, "5%": -2.8621, "10%": -2.5671},
           "ct": {"1%": -3.9638, "5%": -3.4126, "10%": -3.1279},
           "n": {"1%": -2.5666, "5%": -1.9411, "10%": -1.6172}}
_KPSS_CV = {"c": {"10%": 0.347, "5%": 0.463, "1%": 0.739},
            "ct": {"10%": 0.119, "5%": 0.146, "1%": 0.216}}


def _ols(Y, X):
    b = np.linalg.lstsq(X, Y, rcond=None)[0]
    r = Y - X @ b
    n, k = X.shape
    ssr = float(r @ r)
    sigma2 = ssr / (n - k)
    cov = sigma2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    return b, se, ssr, n, k


def adf(y, reg="c", maxlag=None):
    y = _clean(y)
    n = len(y)
    dy = np.diff(y)
    if maxlag is None:
        maxlag = int(np.ceil(12 * (n / 100.0) ** 0.25))
    maxlag = int(max(0, min(maxlag, n // 2 - 3)))

    def build(p, start):
        ts = np.arange(start, n)
        Y = dy[ts - 1]
        parts = []
        if reg in ("c", "ct"):
            parts.append(np.ones(len(ts)))
        if reg == "ct":
            parts.append(ts.astype(float))
        parts.append(y[ts - 1])
        gidx = len(parts) - 1
        for i in range(1, p + 1):
            parts.append(dy[ts - 1 - i])
        return Y, np.column_stack(parts), gidx

    # 1) selección de rezagos por AIC sobre una MUESTRA COMÚN (mismo nobs para todos)
    start_common = maxlag + 1
    best = None
    for p in range(0, maxlag + 1):
        Y, X, gidx = build(p, start_common)
        if X.shape[0] <= X.shape[1] + 1:
            break
        b, se, ssr, nobs, k = _ols(Y, X)
        aic = nobs * math.log(ssr / nobs) + 2 * k
        if best is None or aic < best[0]:
            best = (aic, p)
    usedlag = best[1] if best else 0
    # 2) reajuste final con el máximo de datos para ese número de rezagos
    Y, X, gidx = build(usedlag, usedlag + 1)
    b, se, ssr, nobs, k = _ols(Y, X)
    tstat = float(b[gidx] / se[gidx])
    cv = _ADF_CV[reg]
    if tstat < cv["1%"]:
        dec = "1%"
    elif tstat < cv["5%"]:
        dec = "5%"
    elif tstat < cv["10%"]:
        dec = "10%"
    else:
        dec = None
    estac = dec is not None
    it = [f"ADF: estadístico = {tstat:.3f} (rezagos usados = {usedlag}, n efectivo = {nobs}).",
          f"Valores críticos — 1%: {cv['1%']}, 5%: {cv['5%']}, 10%: {cv['10%']}.",
          (f"Se RECHAZA la hipótesis nula de raíz unitaria al {dec}: hay evidencia de que la serie es ESTACIONARIA."
           if estac else
           "NO se rechaza la hipótesis nula de raíz unitaria: la serie parece NO estacionaria (considera diferenciar).")]
    return {"prueba": "ADF", "H0": "raíz unitaria (no estacionaria)", "estadistico": float(tstat),
            "usedlag": usedlag, "nobs": nobs, "cv": cv, "rechaza_al": dec,
            "estacionaria": estac, "interpretacion": it}


def kpss(y, reg="c"):
    y = _clean(y)
    n = len(y)
    t = np.arange(1, n + 1)
    X = np.column_stack([np.ones(n), t.astype(float)]) if reg == "ct" else np.ones((n, 1))
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ b
    S = np.cumsum(resid)
    l = int(4 * (n / 100.0) ** 0.25)
    s2 = np.sum(resid ** 2) / n
    for j in range(1, l + 1):
        w = 1 - j / (l + 1)
        s2 += 2 * w * np.sum(resid[j:] * resid[:-j]) / n
    eta = float(np.sum(S ** 2) / (n ** 2 * s2))
    cv = _KPSS_CV[reg]
    if eta > cv["1%"]:
        dec = "1%"
    elif eta > cv["5%"]:
        dec = "5%"
    elif eta > cv["10%"]:
        dec = "10%"
    else:
        dec = None
    estac = dec is None
    it = [f"KPSS: estadístico = {eta:.3f} (ancho de banda l = {l}).",
          f"Valores críticos — 10%: {cv['10%']}, 5%: {cv['5%']}, 1%: {cv['1%']}.",
          ("NO se rechaza la hipótesis nula de estacionariedad: la serie parece ESTACIONARIA."
           if estac else
           f"Se RECHAZA la estacionariedad al {dec}: la serie parece NO estacionaria (considera diferenciar).")]
    return {"prueba": "KPSS", "H0": "estacionaria", "estadistico": eta, "l": l, "cv": cv,
            "rechaza_al": dec, "estacionaria": estac, "interpretacion": it}


def estacionariedad(y, reg="c", d=0, D=0, m=12):
    """Aplica diferenciación regular (d) y estacional (D) y corre ADF + KPSS."""
    y0 = _clean(y)
    y = y0.copy()
    hist = []
    for _ in range(int(D)):
        if len(y) <= m:
            raise ValueError("Serie demasiado corta para la diferenciación estacional.")
        y = y[m:] - y[:-m]
        hist.append(f"estacional (lag {m})")
    for _ in range(int(d)):
        y = np.diff(y)
        hist.append("regular")
    if len(y) < 8:
        raise ValueError("La serie diferenciada quedó demasiado corta.")
    a = adf(y, reg)
    k = kpss(y, "ct" if reg == "ct" else "c")
    concl = ("ambas pruebas coinciden en ESTACIONARIA" if (a["estacionaria"] and k["estacionaria"])
             else "ambas coinciden en NO estacionaria" if (not a["estacionaria"] and not k["estacionaria"])
             else "las pruebas discrepan (evidencia mixta)")
    it = [f"Diferenciación aplicada: d = {d}, D = {D} (m = {m}). {'· '.join(hist) if hist else 'ninguna (serie original)'}.",
          f"ADF → {'estacionaria' if a['estacionaria'] else 'no estacionaria'}; "
          f"KPSS → {'estacionaria' if k['estacionaria'] else 'no estacionaria'}: {concl}.",
          "Recomendación: aumenta d si ADF no rechaza y KPSS rechaza; usa diferenciación estacional (D) si hay estacionalidad marcada."]
    return {"d": int(d), "D": int(D), "m": m, "n": len(y),
            "serie_diferenciada": [float(v) for v in y],
            "adf": a, "kpss": k, "interpretacion": it}
