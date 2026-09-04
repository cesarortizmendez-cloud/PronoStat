"""
Informes automáticos — resumen integral del conjunto de datos (perfilado + hallazgos).
Reutiliza la estadística descriptiva. numpy/scipy.
"""
import math
import numpy as np
from scipy import stats as sps


def _num(rows, col):
    out = []
    for r in rows:
        v = r.get(col)
        try:
            fv = float(v)
            if not math.isnan(fv):
                out.append(fv)
        except (TypeError, ValueError):
            pass
    return np.array(out, dtype=float)


def resumen(columns, rows):
    n = len(rows)
    numcols = [c["name"] for c in columns if c["type"] == "numérico"]
    colinfo = []
    for c in columns:
        vals = [r.get(c["name"]) for r in rows]
        miss = sum(1 for v in vals if v in (None, "") or (isinstance(v, float) and math.isnan(v)))
        entry = {"name": c["name"], "type": c["type"], "faltantes": miss,
                 "faltantes_pct": round(100 * miss / n, 1) if n else 0}
        if c["type"] == "numérico":
            x = _num(rows, c["name"])
            if x.size >= 2:
                q1, q3 = np.percentile(x, [25, 75])
                iqr = q3 - q1
                lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                sd = float(np.std(x, ddof=1)); mean = float(np.mean(x))
                entry["stats"] = {
                    "media": mean, "mediana": float(np.median(x)), "sd": sd,
                    "cv": float(sd / mean * 100) if mean else float("nan"),
                    "min": float(np.min(x)), "max": float(np.max(x)),
                    "asimetria": float(sps.skew(x)) if x.size > 2 else float("nan"),
                    "atipicos": int(np.sum((x < lo) | (x > hi))),
                }
        colinfo.append(entry)

    # correlaciones
    corr = None
    if len(numcols) >= 2:
        M = np.array([_num(rows, c) for c in numcols])
        L = min(len(a) for a in M)
        M = np.array([a[:L] for a in M])
        cm = np.corrcoef(M)
        corr = {"cols": numcols, "matrix": [[float(v) for v in row] for row in cm]}

    # hallazgos
    insights = [f"El conjunto tiene {n} filas y {len(columns)} columnas ({len(numcols)} numéricas)."]
    faltan = [c for c in colinfo if c["faltantes"] > 0]
    if faltan:
        insights.append("Columnas con datos faltantes: " + ", ".join(f"{c['name']} ({c['faltantes_pct']}%)" for c in faltan) + ".")
    else:
        insights.append("No hay datos faltantes.")
    num_stats = [c for c in colinfo if "stats" in c]
    if num_stats:
        mas_disp = max(num_stats, key=lambda c: abs(c["stats"]["cv"]) if c["stats"]["cv"] == c["stats"]["cv"] else -1)
        insights.append(f"Mayor dispersión relativa: {mas_disp['name']} (CV = {mas_disp['stats']['cv']:.1f}%).")
        mas_asim = max(num_stats, key=lambda c: abs(c["stats"]["asimetria"]) if c["stats"]["asimetria"] == c["stats"]["asimetria"] else -1)
        insights.append(f"Más asimétrica: {mas_asim['name']} (asimetría = {mas_asim['stats']['asimetria']:.2f}).")
        con_atip = [c for c in num_stats if c["stats"]["atipicos"] > 0]
        if con_atip:
            insights.append("Con valores atípicos: " + ", ".join(f"{c['name']} ({c['stats']['atipicos']})" for c in con_atip) + ".")
    if corr:
        pares = []
        cs = corr["cols"]; mm = corr["matrix"]
        for i in range(len(cs)):
            for j in range(i + 1, len(cs)):
                pares.append((abs(mm[i][j]), cs[i], cs[j], mm[i][j]))
        pares.sort(reverse=True)
        if pares and pares[0][0] > 0.5:
            a = pares[0]
            insights.append(f"Correlación más fuerte: {a[1]} ↔ {a[2]} (r = {a[3]:.2f}), relación {'positiva' if a[3]>0 else 'negativa'} "
                            f"{'fuerte' if a[0]>0.7 else 'moderada'}.")

    return {"n": n, "n_cols": len(columns), "n_num": len(numcols),
            "columnas": colinfo, "correlaciones": corr, "insights": insights}
