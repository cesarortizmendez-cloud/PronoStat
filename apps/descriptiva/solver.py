"""
Estadística descriptiva (monovariada) — lógica pura.

Resumen numérico + insumos para gráficos avanzados:
histograma, densidad (KDE), curva normal teórica, boxplot, violín (KDE),
Q-Q normal, ECDF y strip/jitter. Soporta SEGMENTACIÓN por una variable de grupo
(boxplots/violines/ECDF comparativos + ANOVA de una vía).
"""
import math
import numpy as np
from scipy import stats as sps


# --------------------------------------------------------------------------- #
#  Utilidades
# --------------------------------------------------------------------------- #
def _clean(values):
    x = np.asarray([v for v in values if v is not None], dtype=float)
    return x[~np.isnan(x)]


def _kde(x, xmin, xmax, npts=80):
    if x.size >= 5 and np.std(x) > 0:
        try:
            k = sps.gaussian_kde(x)
            grid = np.linspace(xmin, xmax, npts)
            return {"x": [float(g) for g in grid], "y": [float(v) for v in k(grid)]}
        except Exception:
            return None
    return None


def _boxplot(x):
    q1, med, q3 = [float(v) for v in np.percentile(x, [25, 50, 75])]
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    xmin, xmax = float(np.min(x)), float(np.max(x))
    outliers = [float(v) for v in x if v < lo or v > hi]
    inside = x[(x >= lo) & (x <= hi)]
    return {
        "min": xmin, "q1": q1, "median": med, "q3": q3, "max": xmax,
        "whisker_lo": float(inside.min()) if inside.size else xmin,
        "whisker_hi": float(inside.max()) if inside.size else xmax,
        "outliers": outliers, "iqr": iqr, "lo": float(lo), "hi": float(hi),
    }


def _ecdf(x):
    xs = np.sort(x)
    n = xs.size
    return {"x": [float(v) for v in xs], "y": [float((i + 1) / n) for i in range(n)]}


def _qq_normal(x):
    xs = np.sort(x)
    n = xs.size
    p = (np.arange(1, n + 1) - 0.5) / n
    z = sps.norm.ppf(p)
    mean, sd = float(np.mean(x)), float(np.std(x, ddof=1))
    return {"z": [float(v) for v in z], "sample": [float(v) for v in xs],
            "slope": sd, "intercept": mean}


def _summary_full(x):
    n = int(x.size)
    mean = float(np.mean(x)); med = float(np.median(x))
    var = float(np.var(x, ddof=1)); sd = math.sqrt(var)
    xmin, xmax = float(np.min(x)), float(np.max(x))
    q1, q3 = [float(v) for v in np.percentile(x, [25, 75])]
    iqr = q3 - q1
    vals, counts = np.unique(x, return_counts=True)
    maxc = counts.max()
    modes = [float(v) for v, c in zip(vals, counts) if c == maxc] if maxc > 1 else []
    skew = float(sps.skew(x, bias=False)) if n > 2 else float("nan")
    kurt = float(sps.kurtosis(x, fisher=True, bias=False)) if n > 3 else float("nan")
    cv = float(sd / mean * 100) if mean != 0 else float("nan")
    se = float(sd / math.sqrt(n))
    tcrit = float(sps.t.ppf(0.975, n - 1)) if n > 1 else float("nan")
    ci = [mean - tcrit * se, mean + tcrit * se]
    return {
        "media": mean, "mediana": med, "moda": modes, "desv_std": sd, "varianza": var,
        "coef_var_pct": cv, "error_std": se, "min": xmin, "max": xmax, "rango": xmax - xmin,
        "q1": q1, "q2": med, "q3": q3, "iqr": iqr, "asimetria": skew, "curtosis": kurt,
        "suma": float(np.sum(x)), "ic95_media": ci, "n": n,
    }


def _summary_light(x):
    return {
        "n": int(x.size), "media": float(np.mean(x)), "mediana": float(np.median(x)),
        "desv_std": float(np.std(x, ddof=1)) if x.size > 1 else 0.0,
        "cv": float(np.std(x, ddof=1) / np.mean(x) * 100) if x.size > 1 and np.mean(x) != 0 else float("nan"),
        "min": float(np.min(x)), "q1": float(np.percentile(x, 25)),
        "q3": float(np.percentile(x, 75)), "max": float(np.max(x)),
    }


# --------------------------------------------------------------------------- #
#  Interpretación (resultados de una variable)
# --------------------------------------------------------------------------- #
def _interpret(s, boxplot, n_out):
    interp = []
    mean, med, sd = s["media"], s["mediana"], s["desv_std"]
    cv, skew, kurt, ci = s["coef_var_pct"], s["asimetria"], s["curtosis"], s["ic95_media"]
    if abs(mean - med) < 0.1 * (sd if sd else 1):
        interp.append(f"La media ({mean:.3g}) y la mediana ({med:.3g}) son similares: la distribución es aproximadamente simétrica.")
    elif mean > med:
        interp.append(f"La media ({mean:.3g}) supera a la mediana ({med:.3g}): valores altos la arrastran hacia arriba (cola derecha).")
    else:
        interp.append(f"La media ({mean:.3g}) es menor que la mediana ({med:.3g}): valores bajos la arrastran hacia abajo (cola izquierda).")
    if not math.isnan(cv):
        disp = "baja" if abs(cv) < 15 else ("moderada" if abs(cv) < 30 else "alta")
        interp.append(f"El coeficiente de variación es {cv:.1f}%: dispersión relativa {disp} (<15% baja, 15–30% moderada, >30% alta).")
    if not math.isnan(skew):
        a = "aproximadamente simétrica" if abs(skew) < 0.5 else ("asimétrica a la derecha" if skew > 0 else "asimétrica a la izquierda")
        interp.append(f"Asimetría {skew:.2f}: distribución {a}.")
    if not math.isnan(kurt):
        k = "leptocúrtica (colas pesadas)" if kurt > 0.5 else ("platicúrtica (colas ligeras)" if kurt < -0.5 else "mesocúrtica (≈ normal)")
        interp.append(f"Curtosis (exceso) {kurt:.2f}: {k}.")
    if n_out:
        interp.append(f"Hay {n_out} valor(es) atípico(s) fuera de [{boxplot['lo']:.3g}, {boxplot['hi']:.3g}] (regla 1.5·IQR). Revisa si son errores o casos legítimos.")
    else:
        interp.append("No se detectaron valores atípicos (regla 1.5·IQR).")
    interp.append(f"Con 95% de confianza, la media poblacional está entre {ci[0]:.3g} y {ci[1]:.3g}.")
    return interp


# --------------------------------------------------------------------------- #
#  Núcleo de una variable
# --------------------------------------------------------------------------- #
def _core(x, bins="auto"):
    n = int(x.size)
    if n < 2:
        raise ValueError("Se requieren al menos 2 datos numéricos válidos.")
    s = _summary_full(x)
    xmin, xmax = s["min"], s["max"]
    nb = min(20, max(5, int(round(math.sqrt(n))))) if bins == "auto" else int(bins)
    counts_h, edges = np.histogram(x, bins=nb)
    hist = {
        "counts": [int(c) for c in counts_h],
        "edges": [float(e) for e in edges],
        "centers": [float((edges[i] + edges[i + 1]) / 2) for i in range(len(edges) - 1)],
        "labels": [f"{edges[i]:.1f}–{edges[i+1]:.1f}" for i in range(len(edges) - 1)],
    }
    box = _boxplot(x)
    density = _kde(x, xmin, xmax)
    # curva normal teórica (misma media/sd), para superponer
    mean, sd = s["media"], s["desv_std"]
    normal = None
    if sd > 0:
        grid = np.linspace(xmin, xmax, 80)
        normal = {"x": [float(g) for g in grid],
                  "y": [float(v) for v in sps.norm.pdf(grid, mean, sd)]}
    box_view = {k: box[k] for k in ("min", "q1", "median", "q3", "max",
                                    "whisker_lo", "whisker_hi", "outliers")}
    n_out = len(box["outliers"])
    return {
        "n": n, "summary": s, "hist": hist, "density": density, "normal": normal,
        "boxplot": box_view, "ecdf": _ecdf(x), "qq": _qq_normal(x) if sd > 0 else None,
        "n_outliers": n_out, "interpretacion": _interpret(s, box, n_out),
    }


def describe(values, bins="auto"):
    return _core(_clean(values), bins)


# --------------------------------------------------------------------------- #
#  Exploración con segmentación por grupos
# --------------------------------------------------------------------------- #
def explore(values, groups=None, bins="auto"):
    # Emparejar valor-grupo y descartar nulos
    if groups is not None and len(groups) == len(values):
        pairs = []
        for v, g in zip(values, groups):
            if v is None:
                continue
            try:
                fv = float(v)
            except (TypeError, ValueError):
                continue
            if math.isnan(fv):
                continue
            pairs.append((fv, "∅" if g is None or g == "" else str(g)))
    else:
        pairs = [(float(v), None) for v in _clean(values)]

    x = np.array([p[0] for p in pairs], dtype=float)
    if x.size < 2:
        raise ValueError("Se requieren al menos 2 datos numéricos válidos.")

    overall = _core(x, bins)
    result = {"n": int(x.size), "overall": overall, "grouped": None}

    if groups is not None and any(p[1] is not None for p in pairs):
        gmap = {}
        for v, g in pairs:
            gmap.setdefault(g, []).append(v)
        groups_out, arrays = [], []
        for name, vals in gmap.items():
            arr = np.array(vals, dtype=float)
            if arr.size < 1:
                continue
            xmn, xmx = float(arr.min()), float(arr.max())
            entry = {
                "name": name, "n": int(arr.size), "summary": _summary_light(arr),
                "values": [float(v) for v in arr],
                "boxplot": {k: _boxplot(arr)[k] for k in
                            ("min", "q1", "median", "q3", "max", "whisker_lo", "whisker_hi", "outliers")}
                if arr.size >= 2 else None,
                "density": _kde(arr, xmn, xmx) if arr.size >= 5 else None,
                "ecdf": _ecdf(arr),
            }
            groups_out.append(entry)
            if arr.size >= 2:
                arrays.append(arr)
        # ordenar grupos por mediana para lectura
        groups_out.sort(key=lambda e: e["summary"]["mediana"])

        anova = None
        if len(arrays) >= 2:
            try:
                F, p = sps.f_oneway(*arrays)
                anova = {"F": float(F), "p": float(p), "k": len(arrays)}
            except Exception:
                anova = None

        # interpretación de la segmentación
        ginterp = []
        meds = {e["name"]: e["summary"]["mediana"] for e in groups_out}
        hi = max(meds, key=meds.get); lo = min(meds, key=meds.get)
        ginterp.append(f"Se comparan {len(groups_out)} grupos. La mediana más alta es «{hi}» ({meds[hi]:.3g}) y la más baja «{lo}» ({meds[lo]:.3g}).")
        if anova:
            sig = "sí" if anova["p"] < 0.05 else "no"
            ginterp.append(f"ANOVA de una vía: F = {anova['F']:.2f}, p = {anova['p']:.4f}. "
                           f"A un 5% de significancia, las medias {'difieren' if anova['p']<0.05 else 'no difieren'} significativamente entre grupos (¿hay diferencia real? {sig}).")
            ginterp.append("Nota: la ANOVA supone normalidad y varianzas similares; contrasta con los boxplots/violines antes de concluir.")

        result["grouped"] = {"groups": groups_out, "anova": anova, "interpretacion": ginterp}

    return result


# =========================================================================== #
#  Tablas de distribución de frecuencias
# =========================================================================== #
def _fmt(v):
    v = float(v)
    return int(v) if v == int(v) else round(v, 4)


def _sturges(n):
    return max(1, int(math.ceil(1 + 3.322 * math.log10(n)))) if n > 1 else 1


def tabla_frecuencias(values, bins="auto", tipo="auto"):
    """Tabla de frecuencias monovariada (categórica, discreta o por intervalos)."""
    no_vac = [v for v in values if v not in (None, "")]
    num_ok = 0
    for v in no_vac:
        try:
            float(v); num_ok += 1
        except (TypeError, ValueError):
            pass
    # variable categórica (texto)
    if no_vac and num_ok < 0.8 * len(no_vac):
        s = [str(v) for v in no_vac]
        n = len(s)
        vals, counts = np.unique(s, return_counts=True)
        clases = list(vals); marcas = [None] * len(vals); fi = counts.astype(float)
        li = ls = None
        tipo = "categórica"
        return _build_freq(tipo, n, clases, marcas, fi, li, ls, bins)

    x = _clean(values)
    n = int(x.size)
    if n < 1:
        raise ValueError("No hay datos numéricos válidos.")
    distintos = np.unique(x)
    if tipo == "auto":
        tipo = "discreta" if len(distintos) <= 12 else "continua"

    if tipo == "discreta":
        vals, counts = np.unique(x, return_counts=True)
        clases = [str(_fmt(v)) for v in vals]
        marcas = [float(v) for v in vals]
        fi = counts.astype(float)
        li = ls = None
    else:
        k = _sturges(n) if bins == "auto" else int(bins)
        counts, edges = np.histogram(x, bins=k)
        fi = counts.astype(float)
        li = [float(edges[i]) for i in range(len(edges) - 1)]
        ls = [float(edges[i + 1]) for i in range(len(edges) - 1)]
        marcas = [float((edges[i] + edges[i + 1]) / 2) for i in range(len(edges) - 1)]
        clases = [f"[{edges[i]:.2f} – {edges[i+1]:.2f}" + (")" if i < len(edges) - 2 else "]") for i in range(len(edges) - 1)]
    return _build_freq(tipo, n, clases, marcas, fi, li, ls, bins)


def _build_freq(tipo, n, clases, marcas, fi, li, ls, bins):
    fi = np.asarray(fi, dtype=float)
    Fi_asc = np.cumsum(fi)
    Fi_desc = np.cumsum(fi[::-1])[::-1]          # frec. acumulada descendente
    hi = fi / n
    Hi_asc = np.cumsum(hi)
    pi = hi * 100
    Pi_asc = np.cumsum(pi)

    filas = []
    for i in range(len(fi)):
        row = {"clase": clases[i], "marca": marcas[i],
               "fi": int(fi[i]), "Fi_asc": int(Fi_asc[i]), "Fi_desc": int(Fi_desc[i]),
               "hi": float(hi[i]), "Hi_asc": float(Hi_asc[i]),
               "pi": float(pi[i]), "Pi_asc": float(Pi_asc[i])}
        if li is not None:
            row["li"] = li[i]; row["ls"] = ls[i]
        filas.append(row)

    idx_modal = int(np.argmax(fi))
    interp = [
        f"Tabla de frecuencias {'por intervalos (continua)' if tipo=='continua' else 'de valores (discreta)'} "
        f"con {len(fi)} clases y n = {n} datos" + (f" (regla de Sturges: k = {len(fi)})." if tipo == 'continua' and bins == 'auto' else "."),
        f"Clase modal (mayor frecuencia): «{clases[idx_modal]}» con fᵢ = {int(fi[idx_modal])} "
        f"({pi[idx_modal]:.1f}% de los datos).",
        "fᵢ = frecuencia absoluta · Fᵢ↑ = acumulada ascendente · Fᵢ↓ = acumulada descendente · "
        "hᵢ = relativa (fᵢ/n) · pᵢ = porcentual (%). Verificación: Σfᵢ = n, Σhᵢ = 1, Σpᵢ = 100%.",
    ]
    return {"tipo": tipo, "n": n, "k": len(fi), "filas": filas,
            "totales": {"fi": n, "hi": 1.0, "pi": 100.0}, "interpretacion": interp}


def _categorizar(values, bins):
    """Devuelve (etiqueta_por_obs, categorias_ordenadas) para una variable."""
    nums, allnum = [], True
    for v in values:
        try:
            nums.append(float(v))
        except (TypeError, ValueError):
            allnum = False
            break
    if allnum and not any(isinstance(v, str) and not v.replace('.', '', 1).replace('-', '', 1).isdigit() for v in values if v not in (None, "")):
        arr = np.array(nums, dtype=float)
        uniq = np.unique(arr)
        if len(uniq) <= 10:
            cats = [str(_fmt(u)) for u in uniq]
            labels = [str(_fmt(v)) for v in arr]
            return labels, cats
        k = _sturges(len(arr)) if bins in (None, "auto") else int(bins)
        counts, edges = np.histogram(arr, bins=k)
        cats = [f"[{edges[i]:.1f}–{edges[i+1]:.1f})" for i in range(len(edges) - 1)]
        idx = np.clip(np.digitize(arr, edges[1:-1]), 0, len(cats) - 1)
        labels = [cats[i] for i in idx]
        return labels, cats
    s = ["∅" if v in (None, "") else str(v) for v in values]
    cats = sorted(set(s))
    return s, cats


def tabla_doble(xvalues, yvalues, xname="X", yname="Y", xbins="auto", ybins="auto"):
    """Tabla de doble entrada (contingencia) para dos variables."""
    if len(xvalues) != len(yvalues):
        raise ValueError("Las dos variables deben tener el mismo número de observaciones.")
    # emparejar y descartar faltantes
    xv, yv = [], []
    for a, b in zip(xvalues, yvalues):
        if a in (None, "") or b in (None, ""):
            continue
        xv.append(a); yv.append(b)
    if len(xv) < 2:
        raise ValueError("No hay suficientes pares válidos.")
    xl, xcats = _categorizar(xv, xbins)
    yl, ycats = _categorizar(yv, ybins)
    n = len(xl)
    xi = {c: i for i, c in enumerate(xcats)}
    yi = {c: i for i, c in enumerate(ycats)}
    M = np.zeros((len(xcats), len(ycats)), dtype=int)
    for a, b in zip(xl, yl):
        M[xi[a], yi[b]] += 1
    row_tot = M.sum(axis=1); col_tot = M.sum(axis=0); total = int(M.sum())

    interp = [
        f"Tabla de doble entrada de «{xname}» (filas: {len(xcats)}) × «{yname}» (columnas: {len(ycats)}), n = {total}.",
        "Cada celda cuenta cuántas observaciones combinan esa fila y esa columna; los márgenes (totales) son las "
        "distribuciones de cada variable por separado.",
    ]
    # celda más frecuente
    fi, fj = np.unravel_index(int(np.argmax(M)), M.shape)
    interp.append(f"Combinación más frecuente: «{xcats[fi]}» × «{ycats[fj]}» con {int(M[fi,fj])} casos "
                  f"({M[fi,fj]/total*100:.1f}%).")
    return {"xname": xname, "yname": yname, "xcats": xcats, "ycats": ycats,
            "matriz": [[int(v) for v in row] for row in M],
            "total_filas": [int(v) for v in row_tot], "total_cols": [int(v) for v in col_tot],
            "total": total, "interpretacion": interp}
