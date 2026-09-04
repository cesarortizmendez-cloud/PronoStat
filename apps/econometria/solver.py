"""
Econometría (versión PRO) — Regresión lineal múltiple por MCO/OLS.
Lógica pura (numpy + scipy). Referencias: Gujarati & Porter, Wooldridge, Greene.

Estima  Y = β0 + β1X1 + … + βkXk + u  con:
  • Variables categóricas expandidas a DUMMIES (0/1, base omitida) y términos de INTERACCIÓN.
  • Formas funcionales: nivel-nivel, log-log (elasticidades), log-nivel, nivel-log.
  • Inferencia CLÁSICA y ROBUSTA a heterocedasticidad (White HC1).
  • Coeficientes estandarizados (beta).
  • Bondad de ajuste: R², R² ajustado, F, AIC, BIC, error estándar.
  • Diagnósticos: VIF, número de condición (multicolinealidad); Breusch-Pagan y White
    (heterocedasticidad); Durbin-Watson y Breusch-Godfrey (autocorrelación);
    Jarque-Bera (normalidad); Ramsey RESET (forma funcional).
  • Influencia: apalancamiento (hat), residuos estudentizados y distancia de Cook.
"""
import math
import numpy as np
from scipy import stats as sps

_FORM_LABEL = {
    "nivel": "Nivel-Nivel", "loglog": "Log-Log (elasticidades)",
    "loglin": "Log-Nivel (semilogarítmico)", "linlog": "Nivel-Log",
}


# --------------------------------------------------------------------------- #
#  Construcción de la matriz de diseño (dummies + interacciones + forma funcional)
# --------------------------------------------------------------------------- #
def _build_design(Y, numvars, catvars, interactions, form):
    numvars = numvars or []
    catvars = catvars or []
    interactions = interactions or []
    N = len(Y)
    logY = form in ("loglog", "loglin")
    logX = form in ("loglog", "linlog")

    cols = {}       # nombre -> np.array (float, con nan)
    order = []      # orden de columnas
    numeric_names = []

    # numéricas (con posible log)
    for v in numvars:
        arr = np.array([_f(x) for x in v["values"]], dtype=float)
        nm = v["name"]
        if logX:
            with np.errstate(invalid="ignore", divide="ignore"):
                arr = np.where(arr > 0, np.log(arr), np.nan)
            nm = f"ln({v['name']})"
        cols[nm] = arr
        order.append(nm)
        numeric_names.append((v["name"], nm))

    # categóricas -> dummies (base = primera categoría alfabética)
    for v in catvars:
        vals = ["∅" if x in (None, "") else str(x) for x in v["values"]]
        cats = sorted(set(vals))
        base = cats[0]
        for c in cats[1:]:
            nm = f"{v['name']}={c}"
            cols[nm] = np.array([1.0 if x == c else 0.0 for x in vals])
            order.append(nm)
        cols.setdefault("__base__" + v["name"], base)

    # interacciones (producto de dos columnas ya construidas, por nombre original numérico)
    nummap = {orig: nm for orig, nm in numeric_names}
    for pair in interactions:
        a, b = pair[0], pair[1]
        na, nb = nummap.get(a, a), nummap.get(b, b)
        if na in cols and nb in cols:
            nm = f"{a}×{b}"
            cols[nm] = cols[na] * cols[nb]
            order.append(nm)

    if not order:
        raise ValueError("Selecciona al menos una variable explicativa.")

    y = np.array([_f(x) for x in Y], dtype=float)
    if logY:
        with np.errstate(invalid="ignore", divide="ignore"):
            y = np.where(y > 0, np.log(y), np.nan)

    Xmat = np.column_stack([cols[nm] for nm in order])
    mask = ~np.isnan(y)
    for j in range(Xmat.shape[1]):
        mask &= ~np.isnan(Xmat[:, j])
    y, Xmat = y[mask], Xmat[mask]
    bases = {k[8:]: cols[k] for k in cols if str(k).startswith("__base__")}
    return y, Xmat, order, logY, logX, bases


def _f(x):
    try:
        v = float(x)
        return v
    except (TypeError, ValueError):
        return float("nan")


# --------------------------------------------------------------------------- #
#  Pruebas auxiliares
# --------------------------------------------------------------------------- #
def _r2_resid(y, Xd):
    b = np.linalg.lstsq(Xd, y, rcond=None)[0]
    r = y - Xd @ b
    sst = np.sum((y - np.mean(y)) ** 2)
    return (1 - np.sum(r ** 2) / sst if sst > 0 else 0.0), r, b


def _vif(Z, names):
    k = Z.shape[1]
    if k < 2:
        return None
    out = []
    for j in range(k):
        Xd = np.column_stack([np.ones(len(Z)), np.delete(Z, j, axis=1)])
        r2j, _, _ = _r2_resid(Z[:, j], Xd)
        vif = 1.0 / (1.0 - r2j) if r2j < 1 else float("inf")
        out.append({"var": names[j], "vif": float(vif)})
    return out


def _breusch_pagan(resid, Xd):
    n = resid.size
    r2, _, _ = _r2_resid(resid ** 2, Xd)
    k = Xd.shape[1] - 1
    lm = n * r2
    return {"LM": float(lm), "gl": k, "p": float(sps.chi2.sf(lm, k)) if k > 0 else float("nan")}


def _white(resid, Z):
    """Test de White: e² sobre regresores, sus cuadrados y productos cruzados."""
    n, k = Z.shape
    cols = [Z[:, j] for j in range(k)]
    for j in range(k):
        cols.append(Z[:, j] ** 2)
    for i in range(k):
        for j in range(i + 1, k):
            cols.append(Z[:, i] * Z[:, j])
    aux = np.column_stack(cols)
    # eliminar columnas casi constantes
    keep = [c for c in range(aux.shape[1]) if np.std(aux[:, c]) > 1e-10]
    aux = aux[:, keep] if keep else np.empty((n, 0))
    Xd = np.column_stack([np.ones(n), aux])
    r2, _, _ = _r2_resid(resid ** 2, Xd)
    gl = int(np.linalg.matrix_rank(Xd) - 1)
    lm = n * r2
    return {"LM": float(lm), "gl": gl, "p": float(sps.chi2.sf(lm, gl)) if gl > 0 else float("nan")}


def _durbin_watson(resid):
    return float(np.sum(np.diff(resid) ** 2) / np.sum(resid ** 2)) if np.sum(resid ** 2) > 0 else float("nan")


def _breusch_godfrey(resid, Xd):
    n = resid.size
    lag = np.concatenate([[0.0], resid[:-1]])
    aux = np.column_stack([Xd, lag])
    r2, _, _ = _r2_resid(resid, aux)
    lm = n * r2
    return {"LM": float(lm), "gl": 1, "p": float(sps.chi2.sf(lm, 1))}


def _jarque_bera(resid):
    n = resid.size
    s = float(sps.skew(resid)); k = float(sps.kurtosis(resid, fisher=True))
    jb = n / 6.0 * (s ** 2 + (k ** 2) / 4.0)
    return {"JB": float(jb), "p": float(sps.chi2.sf(jb, 2)), "asimetria": s, "curtosis": k}


def _reset(y, Xd, fitted):
    """Ramsey RESET: añade ŷ² y ŷ³ y prueba su significancia conjunta (F)."""
    n, p = Xd.shape
    ssr_r = float(np.sum((y - Xd @ np.linalg.lstsq(Xd, y, rcond=None)[0]) ** 2))
    z = np.column_stack([fitted ** 2, fitted ** 3])
    aug = np.column_stack([Xd, z])
    if np.linalg.matrix_rank(aug) < aug.shape[1]:
        return None
    r = y - aug @ np.linalg.lstsq(aug, y, rcond=None)[0]
    ssr_u = float(np.sum(r ** 2)); q = 2
    dfden = n - p - q
    if dfden <= 0 or ssr_u <= 0:
        return None
    F = ((ssr_r - ssr_u) / q) / (ssr_u / dfden)
    return {"F": float(F), "gl1": q, "gl2": dfden, "p": float(sps.f.sf(F, q, dfden))}


def _condition_number(Z):
    if Z.shape[1] == 0:
        return float("nan")
    norms = np.linalg.norm(Z, axis=0)
    norms[norms == 0] = 1
    Zs = Z / norms
    Xd = np.column_stack([np.ones(len(Zs)), Zs])
    return float(np.linalg.cond(Xd))


# --------------------------------------------------------------------------- #
#  MCO principal
# --------------------------------------------------------------------------- #
def ols(Y, numvars=None, catvars=None, interactions=None, yname="Y",
        form="nivel", conf=95, robust=False):
    y, Z, xnames, logY, logX, bases = _build_design(Y, numvars, catvars, interactions, form)
    n, k = Z.shape
    if n <= k + 1:
        raise ValueError(f"Se necesitan más observaciones (n={n}) que parámetros (k+1={k+1}).")

    Xd = np.column_stack([np.ones(n), Z])
    p = k + 1
    XtX = Xd.T @ Xd
    try:
        XtX_inv = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        raise ValueError("Multicolinealidad perfecta: X'X singular. Elimina variables redundantes.")
    beta = XtX_inv @ Xd.T @ y
    fitted = Xd @ beta
    resid = y - fitted
    df = n - p
    ssr = float(resid @ resid)
    sst = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1 - ssr / sst if sst > 0 else float("nan")
    adj = 1 - (1 - r2) * (n - 1) / df
    sigma2 = ssr / df
    se_reg = math.sqrt(sigma2)

    # covarianzas clásica y robusta (White HC1)
    cov_cls = sigma2 * XtX_inv
    meat = Xd.T @ (Xd * (resid ** 2)[:, None])
    cov_rob = (n / df) * XtX_inv @ meat @ XtX_inv
    cov = cov_rob if robust else cov_cls
    se = np.sqrt(np.diag(cov))
    tvals = beta / se
    pvals = 2 * sps.t.sf(np.abs(tvals), df)
    tcrit = float(sps.t.ppf(1 - (1 - conf / 100) / 2, df))

    # coeficientes estandarizados
    sdy = float(np.std(y, ddof=1))
    sdz = np.std(Z, axis=0, ddof=1)
    labels = ["(Intercepto)"] + xnames
    coefs = []
    for i, name in enumerate(labels):
        stars = "***" if pvals[i] < 0.01 else ("**" if pvals[i] < 0.05 else ("*" if pvals[i] < 0.10 else ""))
        beta_std = None
        if i > 0 and sdy > 0:
            beta_std = float(beta[i] * sdz[i - 1] / sdy)
        coefs.append({"var": name, "beta": float(beta[i]), "se": float(se[i]),
                      "t": float(tvals[i]), "p": float(pvals[i]), "stars": stars,
                      "beta_std": beta_std,
                      "ic": [float(beta[i] - tcrit * se[i]), float(beta[i] + tcrit * se[i])]})

    F = (r2 / k) / ((1 - r2) / df) if r2 < 1 else float("inf")
    pF = float(sps.f.sf(F, k, df)) if np.isfinite(F) else 0.0
    aic = n * math.log(ssr / n) + 2 * p
    bic = n * math.log(ssr / n) + p * math.log(n)

    ydep = ("ln(" + yname + ")") if logY else yname
    terms = " + ".join(f"{coefs[i+1]['beta']:.4g}·{xnames[i]}" for i in range(k))
    equation = f"{ydep} = {coefs[0]['beta']:.4g} + {terms}"

    # influencia
    hat = np.einsum('ij,jk,ik->i', Xd, XtX_inv, Xd)
    hat = np.clip(hat, 0, 0.9999)
    stud = resid / np.sqrt(sigma2 * (1 - hat))
    cook = (resid ** 2 / (p * sigma2)) * (hat / (1 - hat) ** 2)
    umbral_cook = 4.0 / n
    influyentes = [{"i": int(i + 1), "cook": float(cook[i]), "hat": float(hat[i]), "stud": float(stud[i])}
                   for i in np.argsort(cook)[::-1][:8] if cook[i] > umbral_cook]

    diagnostics = {
        "vif": _vif(Z, xnames),
        "condition_number": _condition_number(Z),
        "durbin_watson": _durbin_watson(resid),
        "breusch_godfrey": _breusch_godfrey(resid, Xd),
        "breusch_pagan": _breusch_pagan(resid, Xd),
        "white": _white(resid, Z),
        "jarque_bera": _jarque_bera(resid),
        "reset": _reset(y, Xd, fitted),
    }

    rs = np.sort(resid)
    pp = (np.arange(1, n + 1) - 0.5) / n

    return {
        "yname": yname, "form": form, "form_label": _FORM_LABEL[form],
        "n": int(n), "k": int(k), "gl": int(df), "robust": bool(robust),
        "equation": equation, "logY": logY, "logX": logX, "xnames": xnames,
        "coeficientes": coefs,
        "ajuste": {"r2": float(r2), "r2_adj": float(adj), "F": float(F), "pF": pF,
                   "se_reg": float(se_reg), "aic": float(aic), "bic": float(bic),
                   "conf": conf, "tcrit": tcrit},
        "residuos": [float(v) for v in resid], "ajustados": [float(v) for v in fitted],
        "y_obs": [float(v) for v in y],
        "cook": [float(v) for v in cook], "hat": [float(v) for v in hat],
        "umbral_cook": umbral_cook, "influyentes": influyentes,
        "diagnostics": diagnostics,
        "qq_resid": {"z": [float(v) for v in sps.norm.ppf(pp)], "sample": [float(v) for v in rs],
                     "slope": float(np.std(resid, ddof=1)), "intercept": float(np.mean(resid))},
        "interpretacion": _interpret(coefs, r2, adj, F, pF, form, robust, diagnostics, influyentes, n),
    }


def _interpret(coefs, r2, adj, F, pF, form, robust, diag, influyentes, n):
    it = [f"El modelo explica el {r2*100:.1f}% de la variabilidad (R² = {r2:.3f}; ajustado = {adj:.3f})."]
    it.append(f"Prueba F global: F = {F:.2f} (p = {pF:.4g}); el modelo es {'significativo' if pF < 0.05 else 'no significativo'} al 5%.")
    if robust:
        it.append("Se muestran errores estándar ROBUSTOS a heterocedasticidad (White HC1): la inferencia (t, p, IC) es válida aunque la varianza de los errores no sea constante.")
    sig = [c['var'] for c in coefs[1:] if c['p'] < 0.05]
    it.append(f"Significativos al 5%: {', '.join(sig) if sig else 'ninguno'} (*** p<0,01, ** p<0,05, * p<0,10).")
    if len(coefs) > 1:
        c = coefs[1]; b = c['beta']; nm = c['var']
        if form == "loglog":
            it.append(f"Elasticidad: 1% más en {nm} cambia la dependiente en {b:.3g}% en promedio (ceteris paribus).")
        elif form == "loglin":
            it.append(f"Semielasticidad: 1 unidad más en {nm} cambia la dependiente en ~{b*100:.2g}%.")
        else:
            it.append(f"1 unidad más en {nm} cambia la dependiente en {b:+.3g} unidades en promedio (ceteris paribus).")
    # multicolinealidad
    cn = diag.get("condition_number")
    if cn == cn:
        it.append(f"Número de condición = {cn:.1f} " + ("(>30: posible multicolinealidad)." if cn > 30 else "(<30: sin multicolinealidad grave)."))
    vif = diag.get("vif")
    if vif:
        peor = max(vif, key=lambda v: v["vif"] if np.isfinite(v["vif"]) else 1e9)
        if peor["vif"] > 10:
            it.append(f"⚠ VIF de {peor['var']} = {peor['vif']:.1f} (>10): multicolinealidad; errores estándar inflados.")
    # heterocedasticidad
    bp, wh = diag.get("breusch_pagan"), diag.get("white")
    if bp:
        if bp["p"] < 0.05:
            it.append(f"⚠ Heterocedasticidad (Breusch-Pagan p = {bp['p']:.4g}" + (f", White p = {wh['p']:.4g}" if wh else "") + "): activa los errores robustos.")
        else:
            it.append(f"Homocedasticidad razonable (Breusch-Pagan p = {bp['p']:.4g}).")
    # forma funcional
    rs = diag.get("reset")
    if rs:
        if rs["p"] < 0.05:
            it.append(f"⚠ Ramsey RESET p = {rs['p']:.4g} (<0,05): posible mala especificación de la forma funcional (faltan términos no lineales o interacciones).")
        else:
            it.append(f"Ramsey RESET p = {rs['p']:.4g}: no hay evidencia de mala especificación funcional.")
    # autocorrelación
    dw = diag.get("durbin_watson")
    if dw == dw and (dw < 1.5 or dw > 2.5):
        it.append(f"⚠ Durbin-Watson = {dw:.2f}: posible autocorrelación (relevante en series de tiempo).")
    # normalidad
    jb = diag.get("jarque_bera")
    if jb and jb["p"] < 0.05:
        it.append(f"⚠ Jarque-Bera p = {jb['p']:.4g}: residuos no normales (con n grande la inferencia sigue válida por el TCL).")
    if influyentes:
        it.append(f"Se detectaron {len(influyentes)} observación(es) influyente(s) (distancia de Cook > 4/n = {4/n:.3g}); "
                  f"la más influyente es la fila {influyentes[0]['i']} (Cook = {influyentes[0]['cook']:.3g}). Revísalas.")
    return it
