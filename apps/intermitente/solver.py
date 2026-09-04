"""
Demanda intermitente — Croston, SBA (Syntetos-Boylan) y TSB (Teunter-Syntetos-Babai).
numpy puro. Referencias: Croston (1972), Syntetos & Boylan (2005), Teunter et al. (2011).

Series con muchos ceros (repuestos, baja rotación). Se estima por separado el tamaño de la
demanda y el intervalo entre demandas, y se clasifica el patrón (SBC).
"""
import math
import numpy as np


def _clean(y):
    y = np.asarray([v for v in y if v is not None], dtype=float)
    return y[~np.isnan(y)]


def clasificar(y):
    """Clasificación Syntetos-Boylan-Croston por ADI y CV² de los tamaños."""
    y = _clean(y)
    nz = y[y > 0]
    n_dem = len(nz)
    if n_dem == 0:
        return {"ADI": float("inf"), "CV2": 0.0, "clase": "sin demanda", "n_dem": 0,
                "pct_ceros": 100.0}
    ADI = len(y) / n_dem
    cv2 = float((np.std(nz) / np.mean(nz)) ** 2) if np.mean(nz) > 0 else 0.0
    if ADI < 1.32 and cv2 < 0.49:
        clase = "suave (regular)"
    elif ADI >= 1.32 and cv2 < 0.49:
        clase = "intermitente"
    elif ADI < 1.32 and cv2 >= 0.49:
        clase = "errática"
    else:
        clase = "grumosa (lumpy)"
    return {"ADI": float(ADI), "CV2": cv2, "clase": clase, "n_dem": int(n_dem),
            "pct_ceros": float(np.mean(y == 0) * 100)}


def _croston(y, alpha, variante):
    n = len(y)
    yhat = np.full(n, np.nan)
    z = p = None
    q = 1
    last = np.nan
    for t in range(n):
        if y[t] > 0:
            if z is None:
                z, p = y[t], q
            else:
                z = alpha * y[t] + (1 - alpha) * z
                p = alpha * q + (1 - alpha) * p
            rate = z / p
            if variante == "sba":
                rate *= (1 - alpha / 2)
            last = rate
            q = 1
        else:
            q += 1
        yhat[t] = last
    return yhat, (last if not math.isnan(last) else 0.0)


def _tsb(y, alpha, beta):
    n = len(y)
    yhat = np.full(n, np.nan)
    occ = (y > 0).astype(float)
    prob = float(np.mean(occ)) if n else 0.0
    nz = y[y > 0]
    z = float(np.mean(nz)) if len(nz) else 0.0
    last = prob * z
    for t in range(n):
        prob = alpha * occ[t] + (1 - alpha) * prob
        if y[t] > 0:
            z = beta * y[t] + (1 - beta) * z
        last = prob * z
        yhat[t] = last
    return yhat, last


def _metrics(y, yhat):
    m = ~np.isnan(yhat)
    e = y[m] - yhat[m]
    return {"MAE": float(np.mean(np.abs(e))), "RMSE": float(math.sqrt(np.mean(e ** 2))),
            "sesgo": float(np.mean(e))}


def run(y, metodo="sba", alpha=0.1, beta=0.1, h=6, optimizar=False):
    y = _clean(y)
    if len(y) < 4:
        raise ValueError("Se requieren al menos 4 observaciones.")
    if np.all(y == 0):
        raise ValueError("La serie es toda ceros: no hay demanda que modelar.")

    def fit(a, b):
        if metodo == "tsb":
            return _tsb(y, a, b)
        return _croston(y, a, metodo)

    if optimizar:
        grid = np.arange(0.05, 0.51, 0.05)
        best = None
        for a in grid:
            bs = grid if metodo == "tsb" else [beta]
            for b in bs:
                yh, _ = fit(a, b)
                mm = _metrics(y, yh)
                if best is None or mm["RMSE"] < best[0]:
                    best = (mm["RMSE"], a, b)
        alpha, beta = float(best[1]), float(best[2])

    yhat, rate = fit(alpha, beta)
    met = _metrics(y, yhat)
    clas = clasificar(y)
    forecast = [float(rate)] * h

    nombre = {"croston": "Croston", "sba": "Croston-SBA (corrección de sesgo)", "tsb": "TSB (Teunter-Syntetos-Babai)"}[metodo]
    it = [f"Método {nombre} con α = {alpha:.2f}" + (f", β = {beta:.2f}" if metodo == "tsb" else "") +
          (" (parámetros optimizados por RMSE)." if optimizar else "."),
          f"Patrón de demanda: {clas['clase'].upper()} (ADI = {clas['ADI']:.2f}, CV² = {clas['CV2']:.2f}, "
          f"{clas['pct_ceros']:.0f}% de ceros).",
          f"Pronóstico de tasa por período = {rate:.4g} unidades (la demanda intermitente se pronostica como una tasa constante, no como valores puntuales)."]
    if clas["clase"] == "grumosa (lumpy)":
        it.append("Patrón grumoso: el más difícil de pronosticar; TSB o SBA suelen ser preferibles a Croston clásico.")
    elif clas["clase"] == "suave (regular)":
        it.append("Patrón casi regular: podrías usar también los métodos clásicos del módulo de Pronósticos (SES/Holt).")
    it.append("Guía Syntetos-Boylan: ADI≥1,32 → intermitente/grumosa; CV²≥0,49 → alta variabilidad de tamaños.")

    return {"metodo": metodo, "nombre": nombre, "alpha": alpha, "beta": beta, "h": h,
            "n": len(y), "series": [float(v) for v in y],
            "yhat": [None if np.isnan(v) else float(v) for v in yhat],
            "forecast": forecast, "rate": float(rate),
            "metrics": met, "clasificacion": clas, "interpretacion": it}


def comparar(y, alpha=0.1, beta=0.1, optimizar=True):
    """Corre Croston, SBA y TSB y los ordena por RMSE."""
    y = _clean(y)
    filas = []
    for met in ["croston", "sba", "tsb"]:
        try:
            r = run(y, met, alpha, beta, optimizar=optimizar)
            filas.append({"metodo": met, "nombre": r["nombre"], "alpha": r["alpha"], "beta": r["beta"],
                          "rate": r["rate"], "MAE": r["metrics"]["MAE"], "RMSE": r["metrics"]["RMSE"],
                          "sesgo": r["metrics"]["sesgo"], "ok": True})
        except Exception as e:
            filas.append({"metodo": met, "ok": False, "error": str(e)})
    ok = [f for f in filas if f["ok"]]
    ok.sort(key=lambda f: f["RMSE"])
    best = ok[0]["metodo"] if ok else None
    clas = clasificar(y)
    return {"ranking": filas, "best": best, "clasificacion": clas,
            "interpretacion": [
                f"Patrón: {clas['clase'].upper()} (ADI={clas['ADI']:.2f}, CV²={clas['CV2']:.2f}).",
                f"Mejor método por RMSE: {dict((f['metodo'],f.get('nombre','')) for f in ok).get(best,best)}.",
                "En demanda intermitente el RMSE puro puede engañar (muchos ceros); considera también el sesgo y el costo de sobre/sub-stock."]}
