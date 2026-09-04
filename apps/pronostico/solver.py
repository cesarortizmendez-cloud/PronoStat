"""
Pronósticos (series de tiempo) — lógica pura, solo numpy + scipy.

Modelos de tipo ingenuo (líneas base): ingenuo simple, ingenuo estacional,
ingenuo con deriva, media simple, caminata aleatoria (y promedio móvil).
Modelos de suavización (marco ETS): SES, Holt (tendencia lineal), Holt
amortiguado, y Holt-Winters aditivo / multiplicativo, cada uno con y sin
tendencia amortiguada (7 variantes de suavización en total).

Los métodos de suavizamiento se implementan a mano (recursiones ETS clásicas) y
sus parámetros se optimizan con scipy.optimize minimizando la suma de errores al
cuadrado. Esto evita depender de statsmodels (más liviano para desplegar en Vercel).

Incluye métricas MAE/RMSE/MAPE/SMAPE/MASE, intervalos de predicción y comparación.
"""
import math
import numpy as np
from scipy.optimize import minimize

Z = {80: 1.2816, 90: 1.6449, 95: 1.9600, 99: 2.5758}


# --------------------------------------------------------------------------- #
#  Métricas
# --------------------------------------------------------------------------- #
def _safe(a):
    return np.asarray(a, dtype=float)


def metrics(y_true, y_pred, scale=None):
    yt, yp = _safe(y_true), _safe(y_pred)
    err = yt - yp
    ae = np.abs(err)
    mae = float(np.mean(ae))
    rmse = float(math.sqrt(np.mean(err ** 2)))
    with np.errstate(divide="ignore", invalid="ignore"):
        mape = float(np.mean(np.abs(err[yt != 0] / yt[yt != 0])) * 100) if np.any(yt != 0) else float("nan")
        denom = (np.abs(yt) + np.abs(yp))
        smape = float(np.mean(2 * ae[denom != 0] / denom[denom != 0]) * 100) if np.any(denom != 0) else float("nan")
    mase = float(mae / scale) if scale and scale > 0 else float("nan")
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape, "SMAPE": smape, "MASE": mase}


def _mase_scale(train, m=1):
    t = _safe(train)
    if m > 1 and t.size > m:
        d = np.abs(t[m:] - t[:-m])
    else:
        d = np.abs(np.diff(t))
    return float(np.mean(d)) if d.size else float("nan")


# --------------------------------------------------------------------------- #
#  Recursiones ETS (devuelven fitted one-step, nivel/tendencia/estacional finales)
# --------------------------------------------------------------------------- #
def _ets_ses(y, alpha):
    n = y.size
    fitted = np.full(n, np.nan)
    level = y[0]
    for t in range(1, n):
        fitted[t] = level
        level = alpha * y[t] + (1 - alpha) * level
    return fitted, level


def _ets_holt(y, alpha, beta, phi=1.0):
    n = y.size
    fitted = np.full(n, np.nan)
    level = y[0]
    trend = y[1] - y[0]
    for t in range(1, n):
        fitted[t] = level + phi * trend
        prev_level = level
        level = alpha * y[t] + (1 - alpha) * (prev_level + phi * trend)
        trend = beta * (level - prev_level) + (1 - beta) * phi * trend
    return fitted, level, trend


def _ets_hw(y, alpha, beta, gamma, m, seasonal="add", phi=1.0):
    n = y.size
    fitted = np.full(n, np.nan)
    cycle_mean = float(np.mean(y[:m]))
    trend = (float(np.mean(y[m:2 * m])) - cycle_mean) / m
    # El nivel inicial representa el nivel en t=m-1 (justo antes de la primera
    # predicción en t=m); la media del primer ciclo está centrada en (m-1)/2,
    # por lo que hay que avanzarla media longitud de ciclo con la tendencia.
    level = cycle_mean + trend * (m - 1) / 2.0
    # Nivel des-tendenciado en cada posición del primer ciclo (la media del ciclo
    # está en el centro (m-1)/2), para que los índices estacionales iniciales no
    # queden contaminados por la tendencia.
    center = (m - 1) / 2.0
    base = np.array([cycle_mean + trend * (i - center) for i in range(m)])
    if seasonal == "add":
        season = list(y[:m] - base)
    else:
        safe = np.where(base == 0, 1e-8, base)
        season = list(y[:m] / safe)
    s = season[:]  # buffer estacional (índice t-m -> s[t % m] tras avance)
    for t in range(m, n):
        s_tm = s[t % m]
        if seasonal == "add":
            fitted[t] = level + phi * trend + s_tm
            prev_level = level
            level = alpha * (y[t] - s_tm) + (1 - alpha) * (prev_level + phi * trend)
            trend = beta * (level - prev_level) + (1 - beta) * phi * trend
            s[t % m] = gamma * (y[t] - level) + (1 - gamma) * s_tm
        else:
            s_tm = s_tm if s_tm != 0 else 1e-8
            fitted[t] = (level + phi * trend) * s_tm
            prev_level = level
            level = alpha * (y[t] / s_tm) + (1 - alpha) * (prev_level + phi * trend)
            trend = beta * (level - prev_level) + (1 - beta) * phi * trend
            s[t % m] = gamma * (y[t] / level if level != 0 else 1.0) + (1 - gamma) * s_tm
    return fitted, level, trend, s


def _sse(y, fitted):
    mask = ~np.isnan(fitted)
    r = y[mask] - fitted[mask]
    return float(np.sum(r ** 2))


def _optimize(func, x0, bounds):
    best = minimize(func, x0, method="L-BFGS-B", bounds=bounds)
    return best.x


# --------------------------------------------------------------------------- #
#  Modelos: fit sobre `train`, forecast de `h` pasos
# --------------------------------------------------------------------------- #
def m_naive(train, h, m=1, **kw):
    t = _safe(train)
    fitted = np.concatenate([[np.nan], t[:-1]])
    return {"fitted": fitted, "forecast": np.repeat(t[-1], h), "params": {"último_valor": float(t[-1])}}


def m_snaive(train, h, m=12, **kw):
    t = _safe(train)
    if t.size <= m:
        raise ValueError("El ingenuo estacional requiere más datos que un ciclo estacional.")
    fitted = np.concatenate([np.full(m, np.nan), t[:-m]])
    fc = t[-m:][(np.arange(h) % m)]
    return {"fitted": fitted, "forecast": fc, "params": {"periodo": m}}


def m_ma(train, h, window=3, **kw):
    t = _safe(train); k = int(window)
    if k < 1 or k > t.size:
        raise ValueError("Ventana de promedio móvil inválida.")
    fitted = np.full(t.size, np.nan)
    for i in range(k, t.size):
        fitted[i] = np.mean(t[i - k:i])
    return {"fitted": fitted, "forecast": np.repeat(np.mean(t[-k:]), h), "params": {"ventana": k}}


def m_drift(train, h, **kw):
    """Ingenuo con deriva (random walk with drift): último valor + cambio medio por paso."""
    t = _safe(train)
    if t.size < 2:
        raise ValueError("El método con deriva requiere al menos 2 observaciones.")
    drift = float((t[-1] - t[0]) / (t.size - 1))
    fitted = np.concatenate([[np.nan], t[:-1] + drift])  # ŷ_t = y_{t-1} + deriva
    fc = t[-1] + drift * np.arange(1, h + 1)
    return {"fitted": fitted, "forecast": fc,
            "params": {"deriva": drift, "último_valor": float(t[-1])}}


def m_mean(train, h, **kw):
    """Media simple: el pronóstico de todo el futuro es el promedio de la historia."""
    t = _safe(train)
    mu = float(np.mean(t))
    fitted = np.concatenate([[np.nan], np.array([float(np.mean(t[:i])) for i in range(1, t.size)])])
    return {"fitted": fitted, "forecast": np.repeat(mu, h), "params": {"media": mu}}


def m_rw(train, h, **kw):
    """Caminata aleatoria (random walk): Yₜ = Yₜ₋₁ + εₜ. Pronóstico puntual = último valor
    (coincide con el ingenuo); es su formulación estocástica, con intervalos que crecen √h."""
    t = _safe(train)
    fitted = np.concatenate([[np.nan], t[:-1]])
    return {"fitted": fitted, "forecast": np.repeat(t[-1], h),
            "params": {"último_valor": float(t[-1]), "sigma_innov": float(np.std(np.diff(t), ddof=1)) if t.size > 2 else 0.0}}


def m_ses(train, h, alpha=None, **kw):
    t = _safe(train)
    if alpha is None:
        a = _optimize(lambda p: _sse(t, _ets_ses(t, p[0])[0]), [0.3], [(1e-4, 1 - 1e-4)])[0]
    else:
        a = float(alpha)
    fitted, level = _ets_ses(t, a)
    return {"fitted": fitted, "forecast": np.repeat(level, h), "params": {"alpha": float(a)}}


def m_holt(train, h, alpha=None, beta=None, damped=False, **kw):
    t = _safe(train)
    if t.size < 3:
        raise ValueError("Holt requiere al menos 3 observaciones.")
    if damped:
        x = _optimize(lambda p: _sse(t, _ets_holt(t, p[0], p[1], p[2])[0]),
                      [0.3, 0.1, 0.95], [(1e-4, 1 - 1e-4), (1e-4, 1 - 1e-4), (0.8, 1.0)])
        a, b, phi = float(x[0]), float(x[1]), float(x[2])
    else:
        x = _optimize(lambda p: _sse(t, _ets_holt(t, p[0], p[1], 1.0)[0]),
                      [0.3, 0.1], [(1e-4, 1 - 1e-4), (1e-4, 1 - 1e-4)])
        a, b, phi = float(x[0]), float(x[1]), 1.0
    fitted, level, trend = _ets_holt(t, a, b, phi)
    steps = np.arange(1, h + 1)
    damp = np.cumsum(phi ** steps) if damped else steps
    fc = level + damp * trend
    p = {"alpha": a, "beta": b, "amortiguado": bool(damped)}
    if damped:
        p["phi"] = phi
    return {"fitted": fitted, "forecast": fc, "params": p}


def m_hw(train, h, m=12, seasonal="add", trend="add", damped=False, **kw):
    t = _safe(train)
    if t.size < 2 * m:
        raise ValueError(f"Holt-Winters requiere al menos {2*m} observaciones (2 ciclos de m={m}).")
    if seasonal == "mul" and np.any(t <= 0):
        raise ValueError("La estacionalidad multiplicativa requiere y > 0.")

    def obj(p):
        phi = p[3] if damped else 1.0
        fitted, *_ = _ets_hw(t, p[0], p[1], p[2], m, seasonal, phi)
        return _sse(t, fitted)

    if damped:
        x = _optimize(obj, [0.3, 0.05, 0.1, 0.95],
                      [(1e-4, 1 - 1e-4)] * 3 + [(0.8, 1.0)])
        a, b, g, phi = map(float, x)
    else:
        x = _optimize(obj, [0.3, 0.05, 0.1], [(1e-4, 1 - 1e-4)] * 3)
        a, b, g = map(float, x); phi = 1.0

    fitted, level, tr, season = _ets_hw(t, a, b, g, m, seasonal, phi)
    steps = np.arange(1, h + 1)
    damp = np.cumsum(phi ** steps) if damped else steps
    base = level + damp * tr
    seas_idx = [(t.size + i) % m for i in range(h)]
    seas = np.array([season[j] for j in seas_idx])
    fc = base + seas if seasonal == "add" else base * seas
    p = {"alpha": a, "beta": b, "gamma": g, "periodo": m,
         "estacional": seasonal, "amortiguado": bool(damped)}
    if damped:
        p["phi"] = phi
    return {"fitted": fitted, "forecast": fc, "params": p}


# --- Variantes explícitas de suavización (mismas recursiones ETS, config fija) --- #
def m_holt_linear(train, h, **kw):
    kw.pop("damped", None)
    return m_holt(train, h, damped=False, **kw)


def m_holt_damped(train, h, **kw):
    kw.pop("damped", None)
    return m_holt(train, h, damped=True, **kw)


def _hw_variant(train, h, seasonal, damped, **kw):
    kw.pop("seasonal", None); kw.pop("damped", None); kw.pop("trend", None)
    return m_hw(train, h, seasonal=seasonal, damped=damped, **kw)


def m_hw_add(train, h, **kw):       return _hw_variant(train, h, "add", False, **kw)
def m_hw_mul(train, h, **kw):       return _hw_variant(train, h, "mul", False, **kw)
def m_hw_damp_add(train, h, **kw):  return _hw_variant(train, h, "add", True, **kw)
def m_hw_damp_mul(train, h, **kw):  return _hw_variant(train, h, "mul", True, **kw)


_MODELS = {
    # --- Modelos de tipo ingenuo (líneas base / benchmarks) ---
    "ingenuo": m_naive,
    "ingenuo_estacional": m_snaive,
    "deriva": m_drift,
    "media": m_mean,
    "random_walk": m_rw,
    "promedio_movil": m_ma,
    # --- Suavización exponencial (marco ETS) ---
    "ses": m_ses,
    "holt": m_holt_linear,
    "holt_amort": m_holt_damped,
    "hw_aditivo": m_hw_add,
    "hw_multiplicativo": m_hw_mul,
    "hw_amort_aditivo": m_hw_damp_add,
    "hw_amort_multiplicativo": m_hw_damp_mul,
    # --- Alias de compatibilidad (ensamble/jerárquico/múltiple/simulación) ---
    "holt_winters": m_hw_add,
}
_LABELS = {
    "ingenuo": "Ingenuo (Naïve)",
    "ingenuo_estacional": "Ingenuo estacional (Seasonal naïve)",
    "deriva": "Ingenuo con deriva (Drift)",
    "media": "Media simple (Mean)",
    "random_walk": "Caminata aleatoria (Random walk)",
    "promedio_movil": "Promedio móvil",
    "ses": "Suavizamiento exp. simple (SES)",
    "holt": "Holt (tendencia lineal)",
    "holt_amort": "Holt con tendencia amortiguada",
    "hw_aditivo": "Holt-Winters aditivo",
    "hw_multiplicativo": "Holt-Winters multiplicativo",
    "hw_amort_aditivo": "Holt-Winters amortiguado aditivo",
    "hw_amort_multiplicativo": "Holt-Winters amortiguado multiplicativo",
    "holt_winters": "Holt-Winters",
}
_SEASONAL = {"ingenuo_estacional", "holt_winters", "hw_aditivo", "hw_multiplicativo",
             "hw_amort_aditivo", "hw_amort_multiplicativo"}
_NOGROW = {"media", "promedio_movil"}          # intervalos de ancho constante


# --------------------------------------------------------------------------- #
def _resid_sigma(y, fitted):
    mask = ~np.isnan(fitted)
    r = _safe(y)[mask] - _safe(fitted)[mask]
    return float(np.std(r, ddof=1)) if r.size > 1 else 0.0


def _intervals(forecast, sigma, conf=95, grow=True):
    z = Z.get(int(conf), 1.96)
    fc = _safe(forecast)
    steps = np.arange(1, fc.size + 1)
    width = z * sigma * (np.sqrt(steps) if grow else np.ones_like(steps, dtype=float))
    return {"lower": [float(v) for v in (fc - width)],
            "upper": [float(v) for v in (fc + width)], "conf": conf}


# --------------------------------------------------------------------------- #
def run(y, model="ses", h=6, m=12, holdout=0, conf=95, params=None):
    y = _safe([v for v in y if v is not None and not (isinstance(v, float) and math.isnan(v))])
    if y.size < 4:
        raise ValueError("Se requieren al menos 4 observaciones.")
    params = params or {}
    h, holdout = int(h), int(holdout)
    if model not in _MODELS:
        raise ValueError(f"Modelo desconocido: {model}")
    seasonal_model = model in _SEASONAL

    test_metrics = test_pred = test_actual = None
    if holdout > 0:
        if holdout >= y.size - 2:
            raise ValueError("El conjunto de prueba es demasiado grande para los datos disponibles.")
        train, test = y[:-holdout], y[-holdout:]
        res_t = _MODELS[model](train, holdout, m=m, **params)
        test_pred = _safe(res_t["forecast"])
        test_actual = test
        scale = _mase_scale(train, m if seasonal_model else 1)
        test_metrics = metrics(test, test_pred, scale)

    res = _MODELS[model](y, h, m=m, **params)
    fitted = _safe(res["fitted"])
    forecast = _safe(res["forecast"])
    sigma = _resid_sigma(y, fitted)
    mask = ~np.isnan(fitted)
    scale_full = _mase_scale(y, m if seasonal_model else 1)
    insample = metrics(y[mask], fitted[mask], scale_full)
    grow = model not in _NOGROW
    pi = _intervals(forecast, sigma, conf, grow)

    # ------------------- Interpretación automática -------------------
    _desc = {
        "ingenuo": "El pronóstico repite el último valor observado (ŷ = yₜ); sirve como línea base de comparación.",
        "ingenuo_estacional": "El pronóstico repite el valor del mismo periodo del ciclo anterior (m atrás): p. ej. este diciembre = diciembre pasado.",
        "deriva": "Ingenuo con deriva: parte del último valor y le suma el cambio promedio observado en la historia, por lo que la proyección sube o baja de forma constante.",
        "media": "Media simple: todos los valores futuros se pronostican como el promedio de toda la serie histórica; ignora tendencia y estacionalidad.",
        "random_walk": "Caminata aleatoria: modelo estocástico Yₜ = Yₜ₋₁ + εₜ. Su pronóstico puntual coincide con el ingenuo (el último valor), y es la base teórica de por qué la incertidumbre crece con √h.",
        "promedio_movil": "El pronóstico es el promedio de las últimas k observaciones: suaviza el ruido pero no capta tendencia ni estacionalidad.",
        "ses": "Suavizamiento exponencial simple: promedio ponderado que da más peso a lo reciente. Apto para series sin tendencia ni estacionalidad.",
        "holt": "Holt (tendencia lineal): extiende el SES con una componente de tendencia, proyectando un crecimiento o decrecimiento sostenido.",
        "holt_amort": "Holt amortiguado: como Holt, pero la tendencia se aplana (φ<1) hacia el futuro, evitando proyecciones exageradas a largo plazo.",
        "hw_aditivo": "Holt-Winters aditivo: modela nivel, tendencia y una estacionalidad de amplitud constante (se suma al nivel).",
        "hw_multiplicativo": "Holt-Winters multiplicativo: la estacionalidad varía en proporción al nivel de la serie (se multiplica); útil cuando las oscilaciones crecen con el nivel.",
        "hw_amort_aditivo": "Holt-Winters amortiguado aditivo: estacionalidad aditiva con tendencia que se frena con el tiempo.",
        "hw_amort_multiplicativo": "Holt-Winters amortiguado multiplicativo: estacionalidad multiplicativa con tendencia amortiguada.",
        "holt_winters": "Holt-Winters modela nivel, tendencia y estacionalidad: es adecuado cuando la serie repite un patrón cada m periodos.",
    }
    interp = [_desc.get(model, "")]
    p = res["params"]
    if p.get("alpha") == p.get("alpha") and "alpha" in p:
        react = "reacciona rápido a los cambios recientes" if p["alpha"] > 0.5 else "es estable y reacciona con lentitud a los cambios"
        interp.append(f"α (nivel) = {p['alpha']:.3f}: {react}.")
    if "beta" in p and p.get("beta") == p.get("beta"):
        interp.append(f"β (tendencia) = {p['beta']:.3f}: qué tan rápido se actualiza la pendiente de la serie.")
    if "gamma" in p and p.get("gamma") == p.get("gamma"):
        interp.append(f"γ (estacionalidad) = {p['gamma']:.3f}: qué tan rápido se actualiza el patrón estacional.")
    _met = test_metrics or insample
    _origen = "sobre el conjunto de prueba (holdout)" if test_metrics else "sobre el ajuste in-sample"
    if _met["MAPE"] == _met["MAPE"]:
        mp = _met["MAPE"]
        q = "excelente" if mp < 10 else ("buena" if mp < 20 else ("aceptable" if mp < 50 else "pobre"))
        interp.append(f"El MAPE {_origen} es {mp:.1f}%: exactitud {q} (guía: <10% excelente, 10–20% buena, 20–50% aceptable, >50% pobre).")
    if _met["MASE"] == _met["MASE"]:
        cmp_ = "mejor" if _met["MASE"] < 1 else "peor"
        interp.append(f"El MASE es {_met['MASE']:.2f}: el modelo pronostica {cmp_} que el método ingenuo (MASE < 1 significa que lo supera).")
    interp.append(f"Los intervalos al {conf}% se ensanchan con el horizonte porque la incertidumbre crece al alejarse en el tiempo: "
                  f"hay ~{conf}% de probabilidad de que el valor real caiga dentro de la banda.")

    return {
        "model": model, "label": _LABELS[model], "n": int(y.size), "h": h,
        "interpretacion": interp,
        "series": [float(v) for v in y],
        "fitted": [None if np.isnan(v) else float(v) for v in fitted],
        "forecast": [float(v) for v in forecast],
        "intervals": pi, "params": res["params"], "sigma": sigma,
        "insample_metrics": insample, "test_metrics": test_metrics,
        "test": {
            "actual": [float(v) for v in test_actual] if test_actual is not None else None,
            "pred": [float(v) for v in test_pred] if test_pred is not None else None,
            "size": holdout,
        } if holdout > 0 else None,
    }


def compare(y, models=None, h=6, m=12, holdout=6, conf=95, params_map=None):
    y_clean = [v for v in y if v is not None]
    models = models or ["ingenuo", "ingenuo_estacional", "deriva", "media", "random_walk",
                        "promedio_movil", "ses", "holt", "holt_amort",
                        "hw_aditivo", "hw_multiplicativo", "hw_amort_aditivo", "hw_amort_multiplicativo"]
    params_map = params_map or {}
    rows = []
    for mod in models:
        try:
            r = run(y_clean, mod, h=h, m=m, holdout=holdout, conf=conf, params=params_map.get(mod))
            met = r["test_metrics"] or r["insample_metrics"]
            rows.append({"model": mod, "label": _LABELS[mod], "ok": True,
                         "metrics": met, "params": r["params"]})
        except Exception as e:
            rows.append({"model": mod, "label": _LABELS.get(mod, mod), "ok": False, "error": str(e)})
    ok = [r for r in rows if r["ok"] and r["metrics"]["RMSE"] == r["metrics"]["RMSE"]]
    ok.sort(key=lambda r: r["metrics"]["RMSE"])
    best = ok[0]["model"] if ok else None
    interp = []
    if best:
        interp.append(f"El mejor modelo es «{_LABELS[best]}» por tener el menor RMSE "
                      f"({ok[0]['metrics']['RMSE']:.3g}), evaluado en {'el conjunto de prueba' if holdout > 0 else 'el ajuste in-sample'}.")
        interp.append("Compara también MAPE y MASE: un buen modelo suele tener MASE < 1 (supera al método ingenuo). "
                      "El modelo más complejo no siempre es el mejor; prefiere el más simple con error similar.")
    else:
        interp.append("Ningún modelo pudo evaluarse; revisa que la serie tenga suficientes datos (Holt-Winters exige 2 ciclos completos).")
    return {"ranking": rows, "best": best, "criterion": "RMSE (menor es mejor)",
            "interpretacion": interp,
            "evaluated_on": "prueba (holdout)" if holdout > 0 else "ajuste in-sample"}
