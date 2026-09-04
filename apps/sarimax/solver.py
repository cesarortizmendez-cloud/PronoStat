"""
SARIMAX — Regresión con errores SARIMA (variables exógenas).
Reutiliza el motor CSS del módulo ARIMA. numpy/scipy puro.

Modelo:  yₜ = β'Xₜ + nₜ,   con  nₜ ~ SARIMA(p,d,q)(P,D,Q)ₘ
Se estiman β y los parámetros SARIMA conjuntamente minimizando Σeₜ² (CSS).
El pronóstico requiere valores FUTUROS de las exógenas (o se mantienen en su último valor).
"""
import math
import numpy as np
from scipy import stats as sps
from scipy.optimize import least_squares

from apps.arima import solver as AR


def run(y, X, xnames, order=(1, 0, 0), seasonal=(0, 0, 0, 12), include_c=None,
        h=12, conf=95, holdout=0, x_future=None):
    y = np.asarray([v for v in y], dtype=float)
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    # limpiar filas con NaN
    mask = ~np.isnan(y)
    for j in range(X.shape[1]):
        mask &= ~np.isnan(X[:, j])
    y, X = y[mask], X[mask]
    n = len(y)
    kx = X.shape[1]
    p, d, q = [int(v) for v in order]
    P, D, Q, m = [int(v) for v in seasonal]
    if include_c is None:
        include_c = (d + D == 0)
    if n <= kx + p + q + P * m + Q * m + 8:
        raise ValueError("Serie demasiado corta para el modelo y las exógenas especificadas.")

    def _fit(yy, XX):
        diffpoly = AR._diff_poly(d, D, m)
        nparam = (1 if include_c else 0) + kx + p + P + q + Q

        def resid(prm):
            i = 0
            c = prm[i] if include_c else 0.0
            i += 1 if include_c else 0
            beta = prm[i:i + kx]; i += kx
            phi = prm[i:i + p]; i += p
            PHI = prm[i:i + P]; i += P
            theta = prm[i:i + q]; i += q
            THETA = prm[i:i + Q]; i += Q
            nn = yy - XX @ beta
            A, b = AR._build_polys(phi, PHI, theta, THETA, m, diffpoly)
            e, start = AR._residuals(nn, A, b, c)
            return e[start:]

        x0 = np.zeros(nparam)
        off = 1 if include_c else 0
        if kx:
            try:
                x0[off:off + kx] = np.linalg.lstsq(XX, yy, rcond=None)[0]
            except Exception:
                pass
        sol = least_squares(resid, x0, method="lm", max_nfev=6000)
        prm = sol.x
        i = 0
        c = prm[i] if include_c else 0.0; i += 1 if include_c else 0
        beta = prm[i:i + kx]; i += kx
        phi = prm[i:i + p]; i += p; PHI = prm[i:i + P]; i += P
        theta = prm[i:i + q]; i += q; THETA = prm[i:i + Q]; i += Q
        A, b = AR._build_polys(phi, PHI, theta, THETA, m, diffpoly)
        nn = yy - XX @ beta
        e, start = AR._residuals(nn, A, b, c)
        rv = e[start:]; neff = len(rv); ssr = float(rv @ rv); sig2 = ssr / neff
        return {"prm": prm, "c": c, "beta": beta, "A": A, "b": b, "e": e, "n_series": nn,
                "start": start, "resid": rv, "n_eff": neff, "sigma2": sig2, "ssr": ssr,
                "nparam": nparam, "resid_fn": resid}

    # holdout
    test = None
    if holdout > 0:
        f0 = _fit(y[:-holdout], X[:-holdout])
        Xf = X[-holdout:]
        fc = _forecast_x(y[:-holdout], X[:-holdout], Xf, f0, holdout, conf)[0]
        act = y[-holdout:]; err = act - fc
        with np.errstate(divide="ignore", invalid="ignore"):
            mape = float(np.mean(np.abs(err[act != 0] / act[act != 0])) * 100) if np.any(act != 0) else float("nan")
        test = {"size": holdout, "actual": [float(v) for v in act], "pred": [float(v) for v in fc],
                "MAE": float(np.mean(np.abs(err))), "RMSE": float(math.sqrt(np.mean(err ** 2))), "MAPE": mape}

    f = _fit(y, X)
    # exógenas futuras: dadas por el usuario o último valor mantenido
    if x_future is not None and len(x_future) >= h:
        Xf = np.asarray(x_future, dtype=float)[:h]
        if Xf.ndim == 1:
            Xf = Xf.reshape(-1, 1)
        exo_nota = "exógenas futuras provistas por el usuario"
    else:
        Xf = np.tile(X[-1], (h, 1))
        exo_nota = "exógenas futuras mantenidas en su último valor observado"
    fc, lo, hi = _forecast_x(y, X, Xf, f, h, conf)

    # inferencia de coeficientes (Jacobiano numérico)
    se = np.full(f["nparam"], np.nan)
    if f["n_eff"] > f["nparam"]:
        eps = 1e-5; J = np.zeros((f["n_eff"], f["nparam"])); r0 = f["resid_fn"](f["prm"])
        for k in range(f["nparam"]):
            pp = f["prm"].copy(); pp[k] += eps
            J[:, k] = (f["resid_fn"](pp) - r0) / eps
        try:
            cov = (f["ssr"] / (f["n_eff"] - f["nparam"])) * np.linalg.inv(J.T @ J)
            se = np.sqrt(np.abs(np.diag(cov)))
        except np.linalg.LinAlgError:
            pass

    labels = (["c (constante)"] if include_c else []) + list(xnames)
    labels += [f"φ{i}" for i in range(1, p + 1)] + [f"Φ{i}" for i in range(1, P + 1)]
    labels += [f"θ{i}" for i in range(1, q + 1)] + [f"Θ{i}" for i in range(1, Q + 1)]
    coefs = []
    for i, name in enumerate(labels):
        bb = float(f["prm"][i]); s = float(se[i]) if i < len(se) else float("nan")
        t = bb / s if s == s and s > 0 else float("nan")
        pv = 2 * (1 - sps.norm.cdf(abs(t))) if t == t else float("nan")
        st = ("***" if pv < 0.01 else "**" if pv < 0.05 else "*" if pv < 0.10 else "") if pv == pv else ""
        coefs.append({"var": name, "coef": bb, "se": s, "t": t, "p": pv, "stars": st,
                      "es_exog": (include_c and 0 < i <= kx) or (not include_c and i < kx)})

    neff = f["n_eff"]; kk = f["nparam"] + 1
    ll = -0.5 * neff * (math.log(2 * math.pi) + math.log(f["sigma2"] + 1e-12) + 1)
    aic = -2 * ll + 2 * kk; bic = -2 * ll + kk * math.log(neff)
    nlags = max(4, min(2 * m if m > 1 else 10, neff // 2))
    lb = AR._ljung_box(f["resid"], nlags, p + q + P + Q)
    jb = AR._jarque_bera(f["resid"])
    fitted = [None] * f["start"] + [float(y[t] - f["e"][t]) for t in range(f["start"], n)]
    order_str = f"SARIMAX({p},{d},{q})" + (f"({P},{D},{Q})[{m}]" if (P + D + Q) else "") + f" + {kx} exóg."

    return {"order": [p, d, q], "seasonal": [P, D, Q, m], "order_str": order_str,
            "n": n, "h": h, "xnames": list(xnames), "exo_nota": exo_nota,
            "series": [float(v) for v in y], "fitted": fitted,
            "forecast": [float(v) for v in fc],
            "intervals": {"lower": [float(v) for v in lo], "upper": [float(v) for v in hi], "conf": conf},
            "coeficientes": coefs, "test": test,
            "ajuste": {"aic": aic, "bic": bic, "ll": ll, "sigma": math.sqrt(f["sigma2"]), "n_eff": neff},
            "ljung_box": lb, "jarque_bera": jb,
            "interpretacion": _interp(order_str, coefs, aic, lb, jb, test, exo_nota)}


def _forecast_x(y, X, Xf, f, h, conf):
    """Pronóstico: componente de regresión futura + SARIMA sobre nₜ = yₜ − βXₜ."""
    beta, A, b, c = f["beta"], f["A"], f["b"], f["c"]
    n_hist = y - X @ beta                     # errores estructurales observados
    e_hist = f["e"]
    fc_n, lo_n, hi_n = AR._forecast(n_hist, A, b, c, e_hist, h, f["sigma2"], conf)
    reg_f = Xf @ beta
    return reg_f + fc_n, reg_f + lo_n, reg_f + hi_n


def _interp(order_str, coefs, aic, lb, jb, test, exo_nota):
    it = [f"Modelo {order_str} (regresión con errores SARIMA), estimado por CSS. AIC = {aic:.1f}."]
    exs = [c for c in coefs if c.get("es_exog")]
    sig = [c["var"] for c in exs if c["p"] == c["p"] and c["p"] < 0.05]
    if exs:
        it.append(f"Efecto de las variables exógenas — significativas al 5%: {', '.join(sig) if sig else 'ninguna'}. "
                  "Cada β mide el efecto de la exógena sobre Y controlando por la dinámica temporal.")
    it.append(("✔ Ljung-Box p=%.4g: residuos ≈ ruido blanco (buen modelo)." % lb["p"]) if lb["p"] >= 0.05
              else ("⚠ Ljung-Box p=%.4g: aún queda autocorrelación; ajusta los órdenes SARIMA." % lb["p"]))
    if test:
        it.append(f"Validación (holdout {test['size']}): RMSE = {test['RMSE']:.3g}, MAPE = {test['MAPE']:.2f}%.")
    it.append(f"Pronóstico: {exo_nota}. Para escenarios, entrega tú los valores futuros de las exógenas.")
    return it
