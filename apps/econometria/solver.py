"""
Econometría — Modelo de Regresión Lineal Múltiple por Mínimos Cuadrados Ordinarios (MCO/OLS).
Lógica pura (numpy + scipy). Referencias: Gujarati & Porter, Wooldridge, Greene.

Estima  Y = β0 + β1·X1 + … + βk·Xk + u  y entrega inferencia completa
(errores estándar, t, p, IC), bondad de ajuste (R², R² ajustado, F, AIC, BIC) y
diagnósticos de los supuestos de Gauss-Markov:
  • Multicolinealidad: VIF (factor de inflación de la varianza)
  • Autocorrelación:   Durbin-Watson
  • Heterocedasticidad: Breusch-Pagan (LM = n·R²aux)
  • Normalidad de u:   Jarque-Bera

Formas funcionales: nivel-nivel, log-log (elasticidades), log-nivel (semilog), nivel-log.
"""
import math
import numpy as np
from scipy import stats as sps


def _prep_matrix(Y, Xcols, form):
    y = np.asarray(Y, dtype=float)
    X = np.array(Xcols, dtype=float).T if Xcols else np.empty((len(y), 0))
    m = ~np.isnan(y)
    for j in range(X.shape[1]):
        m &= ~np.isnan(X[:, j])
    y, X = y[m], X[m]
    logY = form in ("loglog", "loglin")
    logX = form in ("loglog", "linlog")
    if logY:
        if np.any(y <= 0):
            raise ValueError("La forma logarítmica en Y requiere Y > 0 en todas las observaciones.")
        y = np.log(y)
    if logX and X.shape[1]:
        if np.any(X <= 0):
            raise ValueError("La forma logarítmica en X requiere X > 0 en todas las observaciones.")
        X = np.log(X)
    return y, X, logY, logX


def _ols_core(y, X):
    """Devuelve beta, residuos, XtX_inv sobre matriz de diseño CON intercepto."""
    n = y.size
    Xd = np.column_stack([np.ones(n), X]) if X.shape[1] else np.ones((n, 1))
    XtX = Xd.T @ Xd
    try:
        XtX_inv = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        raise ValueError("Multicolinealidad perfecta: X'X es singular. Elimina variables redundantes.")
    beta = XtX_inv @ Xd.T @ y
    resid = y - Xd @ beta
    return beta, resid, XtX_inv, Xd


def _r2(y, resid):
    sst = float(np.sum((y - np.mean(y)) ** 2))
    ssr = float(np.sum(resid ** 2))
    return (1 - ssr / sst if sst > 0 else float("nan")), ssr, sst


def _vif(X, names):
    """VIF de cada regresor: 1/(1-R²_j) regresando X_j sobre los demás."""
    k = X.shape[1]
    if k < 2:
        return None
    out = []
    for j in range(k):
        yj = X[:, j]
        others = np.delete(X, j, axis=1)
        Xd = np.column_stack([np.ones(len(yj)), others])
        try:
            b = np.linalg.lstsq(Xd, yj, rcond=None)[0]
            r = yj - Xd @ b
            r2j, _, _ = _r2(yj, r)
            vif = 1.0 / (1.0 - r2j) if r2j < 1 else float("inf")
        except Exception:
            vif = float("nan")
        out.append({"var": names[j], "vif": float(vif), "r2": float(r2j)})
    return out


def _breusch_pagan(resid, Xd):
    """LM = n·R² de la regresión auxiliar de e² sobre los regresores."""
    n = resid.size
    e2 = resid ** 2
    try:
        b = np.linalg.lstsq(Xd, e2, rcond=None)[0]
        r = e2 - Xd @ b
        r2, _, _ = _r2(e2, r)
        k = Xd.shape[1] - 1
        lm = n * r2
        p = float(sps.chi2.sf(lm, k)) if k > 0 else float("nan")
        return {"LM": float(lm), "gl": k, "p": p, "r2_aux": float(r2)}
    except Exception:
        return None


def _durbin_watson(resid):
    d = np.diff(resid)
    return float(np.sum(d ** 2) / np.sum(resid ** 2)) if np.sum(resid ** 2) > 0 else float("nan")


def _jarque_bera(resid):
    n = resid.size
    s = float(sps.skew(resid))
    k = float(sps.kurtosis(resid, fisher=True))  # exceso
    jb = n / 6.0 * (s ** 2 + (k ** 2) / 4.0)
    p = float(sps.chi2.sf(jb, 2))
    return {"JB": float(jb), "asimetria": s, "curtosis": k, "p": p}


_FORM_LABEL = {
    "nivel": "Nivel-Nivel", "loglog": "Log-Log (elasticidades)",
    "loglin": "Log-Nivel (semilogarítmico)", "linlog": "Nivel-Log",
}


def ols(Y, Xcols, xnames, yname="Y", form="nivel", conf=95):
    if not Xcols:
        raise ValueError("Selecciona al menos una variable explicativa (X).")
    y, X, logY, logX = _prep_matrix(Y, Xcols, form)
    n = y.size
    k = X.shape[1]
    if n <= k + 1:
        raise ValueError(f"Se necesitan más observaciones (n={n}) que parámetros (k+1={k+1}).")

    beta, resid, XtX_inv, Xd = _ols_core(y, X)
    r2, ssr, sst = _r2(y, resid)
    df = n - k - 1
    sigma2 = ssr / df
    se_reg = math.sqrt(sigma2)
    se = np.sqrt(np.diag(sigma2 * XtX_inv))
    tvals = beta / se
    pvals = 2 * sps.t.sf(np.abs(tvals), df)
    tcrit = float(sps.t.ppf(1 - (1 - conf / 100) / 2, df))

    labels = ["(Intercepto)"] + list(xnames)
    xlab = [(f"ln({nm})" if logX else nm) for nm in xnames]
    labels_disp = ["(Intercepto)"] + xlab
    coefs = []
    for i, name in enumerate(labels_disp):
        stars = "***" if pvals[i] < 0.01 else ("**" if pvals[i] < 0.05 else ("*" if pvals[i] < 0.10 else ""))
        coefs.append({
            "var": name, "beta": float(beta[i]), "se": float(se[i]),
            "t": float(tvals[i]), "p": float(pvals[i]), "stars": stars,
            "ic": [float(beta[i] - tcrit * se[i]), float(beta[i] + tcrit * se[i])],
        })

    adj = 1 - (1 - r2) * (n - 1) / df
    F = (r2 / k) / ((1 - r2) / df) if r2 < 1 else float("inf")
    pF = float(sps.f.sf(F, k, df)) if np.isfinite(F) else 0.0
    aic = n * math.log(ssr / n) + 2 * (k + 1)
    bic = n * math.log(ssr / n) + (k + 1) * math.log(n)

    ydep = ("ln(" + yname + ")") if logY else yname
    terms = " + ".join(f"{coefs[i+1]['beta']:.4g}·{xlab[i]}" for i in range(k))
    equation = f"{ydep} = {coefs[0]['beta']:.4g} + {terms}"

    fitted = (Xd @ beta)
    diagnostics = {
        "vif": _vif(X, xnames),
        "durbin_watson": _durbin_watson(resid),
        "breusch_pagan": _breusch_pagan(resid, Xd),
        "jarque_bera": _jarque_bera(resid),
    }

    result = {
        "yname": yname, "form": form, "form_label": _FORM_LABEL[form],
        "n": int(n), "k": int(k), "gl": int(df),
        "equation": equation, "logY": logY, "logX": logX,
        "coeficientes": coefs,
        "ajuste": {"r2": float(r2), "r2_adj": float(adj), "F": float(F), "pF": pF,
                   "se_reg": float(se_reg), "aic": float(aic), "bic": float(bic),
                   "conf": conf, "tcrit": tcrit},
        "residuos": [float(v) for v in resid],
        "ajustados": [float(v) for v in fitted],
        "y_obs": [float(v) for v in y],
        "diagnostics": diagnostics,
        "interpretacion": _interpret(coefs, r2, adj, F, pF, form, logY, logX, diagnostics, n, k, conf),
    }
    # Q-Q de residuos (normalidad)
    rs = np.sort(resid)
    p = (np.arange(1, n + 1) - 0.5) / n
    result["qq_resid"] = {"z": [float(v) for v in sps.norm.ppf(p)],
                          "sample": [float(v) for v in rs],
                          "slope": float(np.std(resid, ddof=1)), "intercept": float(np.mean(resid))}
    return result


def _interpret(coefs, r2, adj, F, pF, form, logY, logX, diag, n, k, conf):
    it = []
    it.append(f"El modelo explica el {r2*100:.1f}% de la variabilidad de la variable dependiente "
              f"(R² = {r2:.3f}; R² ajustado = {adj:.3f}).")
    sig = "significativo" if pF < 0.05 else "no significativo"
    it.append(f"Prueba F global: F = {F:.2f} (p = {pF:.4f}). En conjunto, el modelo es {sig} al 5% "
              "(al menos un coeficiente distinto de cero).")
    # significancia individual + interpretación por forma funcional
    signif = [c for c in coefs[1:] if c["p"] < 0.05]
    it.append(f"Coeficientes significativos al 5%: {', '.join(c['var'] for c in signif) if signif else 'ninguno'}. "
              "(*** p<0,01, ** p<0,05, * p<0,10.)")
    ejemplo = coefs[1] if len(coefs) > 1 else None
    if ejemplo:
        b = ejemplo["beta"]; nm = ejemplo["var"]
        if form == "loglog":
            it.append(f"Interpretación (log-log = elasticidad): ante un aumento de 1% en {nm}, la dependiente "
                      f"cambia en promedio {b:.3g}% (manteniendo lo demás constante).")
        elif form == "loglin":
            it.append(f"Interpretación (log-nivel): un aumento de 1 unidad en {nm} cambia la dependiente en "
                      f"aproximadamente {b*100:.2g}% (semielasticidad).")
        elif form == "linlog":
            it.append(f"Interpretación (nivel-log): un aumento de 1% en {nm} cambia la dependiente en "
                      f"aproximadamente {b/100:.3g} unidades.")
        else:
            it.append(f"Interpretación (nivel-nivel): manteniendo lo demás constante, un aumento de 1 unidad en "
                      f"{nm} cambia la dependiente en {b:+.3g} unidades en promedio.")
    # diagnósticos
    vif = diag.get("vif")
    if vif:
        peor = max(vif, key=lambda v: v["vif"] if np.isfinite(v["vif"]) else 1e9)
        if peor["vif"] > 10:
            it.append(f"⚠ Multicolinealidad: VIF de {peor['var']} = {peor['vif']:.1f} (>10). "
                      "Los errores estándar pueden estar inflados; considera quitar o combinar variables.")
        elif peor["vif"] > 5:
            it.append(f"Multicolinealidad moderada: VIF máximo = {peor['vif']:.1f} (entre 5 y 10). Vigila la estabilidad de los coeficientes.")
        else:
            it.append(f"Sin multicolinealidad preocupante (VIF máximo = {peor['vif']:.1f} < 5).")
    dw = diag.get("durbin_watson")
    if dw == dw:
        if dw < 1.5:
            it.append(f"⚠ Durbin-Watson = {dw:.2f} (<1,5): posible autocorrelación positiva de los residuos (relevante en series de tiempo).")
        elif dw > 2.5:
            it.append(f"⚠ Durbin-Watson = {dw:.2f} (>2,5): posible autocorrelación negativa.")
        else:
            it.append(f"Durbin-Watson = {dw:.2f} (≈2): sin evidencia clara de autocorrelación.")
    bp = diag.get("breusch_pagan")
    if bp and bp["p"] == bp["p"]:
        if bp["p"] < 0.05:
            it.append(f"⚠ Heterocedasticidad: Breusch-Pagan p = {bp['p']:.4f} (<0,05). La varianza de los errores no es constante; "
                      "usa errores estándar robustos (White) para la inferencia.")
        else:
            it.append(f"Homocedasticidad razonable: Breusch-Pagan p = {bp['p']:.4f} (≥0,05).")
    jb = diag.get("jarque_bera")
    if jb:
        if jb["p"] < 0.05:
            it.append(f"⚠ Normalidad: Jarque-Bera p = {jb['p']:.4f} (<0,05). Los residuos se apartan de la normal; "
                      "con n grande la inferencia sigue siendo válida por el TCL.")
        else:
            it.append(f"Residuos aproximadamente normales: Jarque-Bera p = {jb['p']:.4f} (≥0,05).")
    return it
