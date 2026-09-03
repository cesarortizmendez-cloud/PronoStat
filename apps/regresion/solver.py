"""
Ajuste de modelos (regresión bivariada) — lógica pura.
Modelos: lineal, exponencial, logarítmico y polinómico.
Devuelve coeficientes, R², R² ajustado, RMSE, residuos, curva ajustada y ecuación.
"""
import math
import numpy as np
from scipy.optimize import curve_fit


def _prep(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = ~(np.isnan(x) | np.isnan(y))
    x, y = x[m], y[m]
    if x.size < 3:
        raise ValueError("Se requieren al menos 3 pares (x, y) válidos.")
    return x, y


def _metrics(y, yhat, n_params):
    n = y.size
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    k = n_params - 1  # nº de predictores
    if n - k - 1 > 0 and not math.isnan(r2):
        adj = 1 - (1 - r2) * (n - 1) / (n - k - 1)
    else:
        adj = float("nan")
    rmse = math.sqrt(ss_res / n)
    mae = float(np.mean(np.abs(y - yhat)))
    return {"r2": r2, "r2_adj": adj, "rmse": rmse, "mae": mae,
            "ss_res": ss_res, "ss_tot": ss_tot}


def _grid(x, n=120):
    return np.linspace(float(np.min(x)), float(np.max(x)), n)


def fit(x, y, model="lineal", degree=2, predict_x=None):
    x, y = _prep(x, y)
    n = x.size
    gx = _grid(x)

    if model == "lineal":
        c = np.polyfit(x, y, 1)          # [b, a]  -> y = a + b x
        b, a = float(c[0]), float(c[1])
        yhat = np.polyval(c, x)
        gy = np.polyval(c, gx)
        params = {"a (intercepto)": a, "b (pendiente)": b}
        eq = f"y = {a:.4g} + {b:.4g}·x"
        npar = 2
        predf = lambda v: a + b * v

    elif model == "polinómico":
        d = max(2, int(degree))
        if n <= d:
            raise ValueError(f"Grado {d} requiere más de {d} puntos.")
        c = np.polyfit(x, y, d)
        yhat = np.polyval(c, x)
        gy = np.polyval(c, gx)
        coeffs = list(c[::-1])           # c0, c1, ...
        params = {f"c{i}": float(v) for i, v in enumerate(coeffs)}
        terms = " + ".join([f"{v:.4g}·x^{i}" if i else f"{v:.4g}" for i, v in enumerate(coeffs)])
        eq = "y = " + terms
        npar = d + 1
        predf = lambda v: float(np.polyval(c, v))

    elif model == "exponencial":
        if np.any(y <= 0):
            raise ValueError("El modelo exponencial requiere y > 0 en todos los puntos.")
        # p0 desde ajuste log-lineal: ln y = ln a + b x
        lc = np.polyfit(x, np.log(y), 1)
        p0 = [math.exp(lc[1]), lc[0]]
        f = lambda t, a, b: a * np.exp(b * t)
        popt, _ = curve_fit(f, x, y, p0=p0, maxfev=10000)
        a, b = float(popt[0]), float(popt[1])
        yhat = f(x, a, b)
        gy = f(gx, a, b)
        params = {"a": a, "b (tasa)": b}
        eq = f"y = {a:.4g}·e^({b:.4g}·x)"
        npar = 2
        predf = lambda v: a * math.exp(b * v)

    elif model == "logarítmico":
        if np.any(x <= 0):
            raise ValueError("El modelo logarítmico requiere x > 0 en todos los puntos.")
        lx = np.log(x)
        c = np.polyfit(lx, y, 1)         # y = a + b ln x
        b, a = float(c[0]), float(c[1])
        yhat = a + b * np.log(x)
        gy = a + b * np.log(gx)
        params = {"a (intercepto)": a, "b": b}
        eq = f"y = {a:.4g} + {b:.4g}·ln(x)"
        npar = 2
        predf = lambda v: a + b * math.log(v)

    else:
        raise ValueError(f"Modelo desconocido: {model}")

    met = _metrics(y, yhat, npar)
    resid = (y - yhat)

    # ------------------- Interpretación automática -------------------
    interp = []
    r2 = met["r2"]
    if r2 == r2:  # no es NaN
        if r2 >= 0.9:
            cal = "excelente"
        elif r2 >= 0.7:
            cal = "bueno"
        elif r2 >= 0.5:
            cal = "moderado"
        else:
            cal = "débil"
        interp.append(f"El modelo {model} explica el {r2*100:.1f}% de la variabilidad de Y "
                      f"(R² = {r2:.3f}); la calidad del ajuste es {cal}.")
    interp.append(f"Ecuación ajustada: {eq}")
    if model == "lineal":
        b = params.get("b (pendiente)", float('nan'))
        interp.append(f"Pendiente b = {b:.3g}: por cada aumento de 1 unidad en X, Y varía en promedio {b:+.3g} unidades.")
    elif model == "exponencial":
        b = params.get("b (tasa)", float('nan'))
        tendencia = "crece" if b > 0 else "decrece"
        interp.append(f"Tasa b = {b:.3g}: Y {tendencia} exponencialmente; al subir X en 1, Y se multiplica por e^{b:.3g} ≈ {math.exp(b):.3g}.")
    elif model == "logarítmico":
        b = params.get("b", float('nan'))
        interp.append(f"Coeficiente b = {b:.3g}: Y cambia {b:.3g} unidades por cada aumento de 1 en ln(X); es un crecimiento que se desacelera.")
    elif model == "polinómico":
        interp.append("El polinomio captura la curvatura de la relación. Cuidado con grados altos: pueden sobreajustar (compara con el R² ajustado).")
    interp.append(f"RMSE = {met['rmse']:.3g} (en unidades de Y): magnitud media de los residuos, es decir cuánto se aleja típicamente la predicción del valor real.")
    if met["r2_adj"] == met["r2_adj"]:
        interp.append(f"R² ajustado = {met['r2_adj']:.3f}: penaliza el número de parámetros; es el indicador adecuado para comparar modelos de distinta complejidad.")

    predictions = None
    if predict_x:
        predictions = []
        for v in predict_x:
            try:
                predictions.append({"x": float(v), "y": float(predf(float(v)))})
            except Exception:
                predictions.append({"x": float(v), "y": None})

    return {
        "model": model,
        "equation": eq,
        "params": params,
        "metrics": met,
        "n": int(n),
        "points": {"x": [float(v) for v in x], "y": [float(v) for v in y]},
        "curve": {"x": [float(v) for v in gx], "y": [float(v) for v in gy]},
        "fitted": [float(v) for v in yhat],
        "residuals": [float(v) for v in resid],
        "predictions": predictions,
        "interpretacion": interp,
    }


def compare(x, y, models=None, degree=2):
    """Ajusta varios modelos y los ordena por R² ajustado (o R²)."""
    models = models or ["lineal", "exponencial", "logarítmico", "polinómico"]
    out = []
    for m in models:
        try:
            r = fit(x, y, m, degree)
            out.append({"model": m, "equation": r["equation"],
                        "r2": r["metrics"]["r2"], "r2_adj": r["metrics"]["r2_adj"],
                        "rmse": r["metrics"]["rmse"], "mae": r["metrics"]["mae"], "ok": True})
        except Exception as e:
            out.append({"model": m, "ok": False, "error": str(e)})
    ok = [r for r in out if r["ok"]]
    key = lambda r: (r["r2_adj"] if r["r2_adj"] == r["r2_adj"] else r["r2"])
    ok.sort(key=key, reverse=True)
    best = ok[0]["model"] if ok else None
    interp = []
    if best:
        b = ok[0]
        interp.append(f"El mejor ajuste es el modelo «{best}» (R² ajustado = {b['r2_adj']:.3f}, RMSE = {b['rmse']:.3g}).")
        interp.append("El ranking usa el R² ajustado porque equilibra bondad de ajuste y simplicidad. "
                      "Antes de decidir, verifica también que los residuos no muestren un patrón claro.")
    else:
        interp.append("Ningún modelo pudo ajustarse a estos datos; revisa los requisitos (exponencial: Y>0; logarítmico: X>0).")
    return {"ranking": out, "best": best, "interpretacion": interp}
