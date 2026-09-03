"""
Estadística descriptiva (monovariada) — lógica pura.
Resumen numérico + insumos para histograma, boxplot y densidad (KDE gaussiano).
"""
import math
import numpy as np
from scipy import stats as sps


def _clean(values):
    x = np.asarray([v for v in values if v is not None], dtype=float)
    x = x[~np.isnan(x)]
    return x


def describe(values, bins="auto"):
    x = _clean(values)
    n = int(x.size)
    if n < 2:
        raise ValueError("Se requieren al menos 2 datos numéricos válidos.")

    mean = float(np.mean(x))
    med = float(np.median(x))
    var = float(np.var(x, ddof=1))
    sd = math.sqrt(var)
    xmin, xmax = float(np.min(x)), float(np.max(x))
    q1, q3 = np.percentile(x, [25, 75])
    q1, q3 = float(q1), float(q3)
    iqr = q3 - q1

    # Moda(s) por conteo de valores redondeados a la resolución de los datos
    vals, counts = np.unique(x, return_counts=True)
    maxc = counts.max()
    modes = [float(v) for v, c in zip(vals, counts) if c == maxc] if maxc > 1 else []

    skew = float(sps.skew(x, bias=False)) if n > 2 else float("nan")
    kurt = float(sps.kurtosis(x, fisher=True, bias=False)) if n > 3 else float("nan")
    cv = float(sd / mean * 100) if mean != 0 else float("nan")
    se = float(sd / math.sqrt(n))

    # IC 95% para la media (t de Student)
    tcrit = float(sps.t.ppf(0.975, n - 1))
    ci = [mean - tcrit * se, mean + tcrit * se]

    # Outliers por regla 1.5·IQR
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = [float(v) for v in x if v < lo or v > hi]

    # Histograma
    if bins == "auto":
        nb = min(20, max(5, int(round(math.sqrt(n)))))
    else:
        nb = int(bins)
    counts_h, edges = np.histogram(x, bins=nb)
    centers = [float((edges[i] + edges[i + 1]) / 2) for i in range(len(edges) - 1)]
    hist = {
        "counts": [int(c) for c in counts_h],
        "edges": [float(e) for e in edges],
        "centers": centers,
        "labels": [f"{edges[i]:.1f}–{edges[i+1]:.1f}" for i in range(len(edges) - 1)],
    }

    # Densidad (KDE gaussiano) evaluada en una malla
    density = None
    if n >= 5 and sd > 0:
        try:
            kde = sps.gaussian_kde(x)
            grid = np.linspace(xmin, xmax, 80)
            density = {"x": [float(g) for g in grid], "y": [float(d) for d in kde(grid)]}
        except Exception:
            density = None

    boxplot = {
        "min": xmin, "q1": q1, "median": med, "q3": q3, "max": xmax,
        "whisker_lo": float(max(xmin, lo)), "whisker_hi": float(min(xmax, hi)),
        "outliers": outliers,
    }

    return {
        "n": n,
        "summary": {
            "media": mean, "mediana": med, "moda": modes,
            "desv_std": sd, "varianza": var, "coef_var_pct": cv,
            "error_std": se, "min": xmin, "max": xmax, "rango": xmax - xmin,
            "q1": q1, "q2": med, "q3": q3, "iqr": iqr,
            "asimetria": skew, "curtosis": kurt, "suma": float(np.sum(x)),
            "ic95_media": ci,
        },
        "hist": hist,
        "density": density,
        "boxplot": boxplot,
        "n_outliers": len(outliers),
    }
