"""
ARIMA / SARIMA — modelado de series de tiempo por Mínimos Cuadrados Condicionales (CSS).
Lógica pura numpy/scipy (sin statsmodels). Referencias: Box-Jenkins, Hyndman & Athanasopoulos.

Modelo SARIMA(p,d,q)(P,D,Q)_m:
    Φ(Bᵐ)φ(B)(1−B)^d(1−Bᵐ)^D yₜ = c + Θ(Bᵐ)θ(B) eₜ

Se estima trabajando sobre la serie en su nivel original: se expande el polinomio AR completo
A(B) = φ(B)Φ(Bᵐ)(1−B)^d(1−Bᵐ)^D y el MA completo b(B) = θ(B)Θ(Bᵐ), y se minimiza Σeₜ² (CSS)
con scipy.optimize.least_squares. Entrega coeficientes con EE/t/p, AIC/BIC, log-verosimilitud,
pronóstico con intervalos (ψ-pesos), diagnóstico de residuos (Ljung-Box, Jarque-Bera, ACF),
validación con origen móvil y selección automática por AIC.
"""
import math
import numpy as np
from scipy import stats as sps
from scipy.optimize import least_squares

Z = {80: 1.2816, 90: 1.6449, 95: 1.9600, 99: 2.5758}


def _clean(y):
    y = np.asarray([v for v in y if v is not None], dtype=float)
    return y[~np.isnan(y)]


# --------------------------------------------------------------------------- #
#  Polinomios
# --------------------------------------------------------------------------- #
def _seasonal_poly(coefs, m, sign):
    """Polinomio 1 (+/-) c1 B^m (+/-) c2 B^2m ... como arreglo de coeficientes."""
    p = np.zeros(len(coefs) * m + 1)
    p[0] = 1.0
    for k, c in enumerate(coefs):
        p[(k + 1) * m] = sign * c
    return p


def _diff_poly(d, D, m):
    reg = np.array([1.0])
    for _ in range(d):
        reg = np.convolve(reg, [1.0, -1.0])
    seas = np.array([1.0])
    unit = np.zeros(m + 1); unit[0] = 1.0; unit[m] = -1.0
    for _ in range(D):
        seas = np.convolve(seas, unit)
    return np.convolve(reg, seas)


def _build_polys(phi, PHI, theta, THETA, m, diffpoly):
    ar_ns = np.r_[1.0, -np.asarray(phi, float)] if len(phi) else np.array([1.0])
    ar_s = _seasonal_poly(PHI, m, -1.0)
    a_poly = np.convolve(ar_ns, ar_s)
    A = np.convolve(a_poly, diffpoly)
    ma_ns = np.r_[1.0, np.asarray(theta, float)] if len(theta) else np.array([1.0])
    ma_s = _seasonal_poly(THETA, m, +1.0)
    b = np.convolve(ma_ns, ma_s)
    return A, b


def _residuals(y, A, b, c):
    n = len(y)
    oA = len(A) - 1
    ob = len(b) - 1
    e = np.zeros(n)
    start = oA
    for t in range(start, n):
        pred = c
        for i in range(1, oA + 1):
            if A[i] != 0:
                pred -= A[i] * y[t - i]
        for j in range(1, ob + 1):
            if b[j] != 0:
                pred += b[j] * e[t - j]
        e[t] = y[t] - pred
    return e, start


# --------------------------------------------------------------------------- #
#  Ajuste CSS
# --------------------------------------------------------------------------- #
def _unpack(params, p, P, q, Q, include_c):
    i = 0
    c = params[i] if include_c else 0.0
    i += 1 if include_c else 0
    phi = params[i:i + p]; i += p
    PHI = params[i:i + P]; i += P
    theta = params[i:i + q]; i += q
    THETA = params[i:i + Q]; i += Q
    return c, phi, PHI, theta, THETA


def fit_css(y, order, seasonal, include_c):
    p, d, q = order
    P, D, Q, m = seasonal
    diffpoly = _diff_poly(d, D, m)
    nparam = (1 if include_c else 0) + p + P + q + Q

    def resid(params):
        c, phi, PHI, theta, THETA = _unpack(params, p, P, q, Q, include_c)
        A, b = _build_polys(phi, PHI, theta, THETA, m, diffpoly)
        e, start = _residuals(y, A, b, c)
        return e[start:]

    x0 = np.zeros(nparam)
    if include_c:
        x0[0] = np.mean(np.diff(y, d) if d else y) if len(y) > d else 0.0
    if nparam == 0:
        params = np.array([])
    else:
        sol = least_squares(resid, x0, method="lm", max_nfev=4000)
        params = sol.x

    c, phi, PHI, theta, THETA = _unpack(params, p, P, q, Q, include_c)
    A, b = _build_polys(phi, PHI, theta, THETA, m, diffpoly)
    e, start = _residuals(y, A, b, c)
    resid_v = e[start:]
    n_eff = len(resid_v)
    ssr = float(resid_v @ resid_v)
    sigma2 = ssr / n_eff
    ll = -0.5 * n_eff * (math.log(2 * math.pi) + math.log(sigma2 + 1e-12) + 1)
    kk = nparam + 1
    aic = -2 * ll + 2 * kk
    bic = -2 * ll + kk * math.log(n_eff)
    aicc = aic + (2 * kk * (kk + 1)) / max(1, (n_eff - kk - 1))

    # errores estándar por Jacobiano numérico
    se = np.full(nparam, float("nan"))
    if nparam > 0 and n_eff > nparam:
        eps = 1e-5
        J = np.zeros((n_eff, nparam))
        r0 = resid(params)
        for k in range(nparam):
            pp = params.copy(); pp[k] += eps
            J[:, k] = (resid(pp) - r0) / eps
        try:
            cov = (ssr / (n_eff - nparam)) * np.linalg.inv(J.T @ J)
            se = np.sqrt(np.abs(np.diag(cov)))
        except np.linalg.LinAlgError:
            pass

    return {"params": params, "c": c, "phi": phi, "PHI": PHI, "theta": theta, "THETA": THETA,
            "A": A, "b": b, "e": e, "start": start, "resid": resid_v, "n_eff": n_eff,
            "sigma2": sigma2, "ll": ll, "aic": aic, "bic": bic, "aicc": aicc,
            "se": se, "nparam": nparam, "diffpoly": diffpoly}


def _psi_weights(A, b, h):
    psi = np.zeros(h); psi[0] = 1.0
    for s in range(1, h):
        v = b[s] if s < len(b) else 0.0
        for i in range(1, min(s, len(A) - 1) + 1):
            v -= A[i] * psi[s - i]
        psi[s] = v
    return psi


def _forecast(y, A, b, c, e, h, sigma2, conf):
    n = len(y)
    oA = len(A) - 1; ob = len(b) - 1
    yf = list(y); ef = list(e)
    for s in range(h):
        t = len(yf)
        pred = c
        for i in range(1, oA + 1):
            if A[i] != 0:
                pred -= A[i] * yf[t - i]
        for j in range(1, ob + 1):
            if b[j] != 0:
                idx = t - j
                pred += b[j] * (ef[idx] if idx < len(ef) else 0.0)
        yf.append(pred); ef.append(0.0)
    fc = np.array(yf[n:])
    psi = _psi_weights(A, b, h)
    var = sigma2 * np.cumsum(psi ** 2)
    z = Z.get(int(conf), 1.96)
    lo = fc - z * np.sqrt(var); hi = fc + z * np.sqrt(var)
    return fc, lo, hi


# --------------------------------------------------------------------------- #
#  Diagnóstico de residuos
# --------------------------------------------------------------------------- #
def _acf(x, nlags):
    x = np.asarray(x); xbar = x.mean(); c0 = np.sum((x - xbar) ** 2)
    return [1.0] + [float(np.sum((x[k:] - xbar) * (x[:-k] - xbar)) / c0) for k in range(1, nlags + 1)]


def _ljung_box(resid, nlags, dof):
    n = len(resid); r = _acf(resid, nlags)
    Q = n * (n + 2) * sum((r[k] ** 2) / (n - k) for k in range(1, nlags + 1))
    df = max(1, nlags - dof)
    return {"Q": float(Q), "gl": df, "p": float(sps.chi2.sf(Q, df)), "nlags": nlags,
            "acf": r, "banda": 1.96 / math.sqrt(n)}


def _jarque_bera(resid):
    n = len(resid); s = float(sps.skew(resid)); k = float(sps.kurtosis(resid, fisher=True))
    jb = n / 6.0 * (s ** 2 + k ** 2 / 4.0)
    return {"JB": float(jb), "p": float(sps.chi2.sf(jb, 2)), "asimetria": s, "curtosis": k}


# --------------------------------------------------------------------------- #
#  API principal
# --------------------------------------------------------------------------- #
def _labels(p, P, q, Q, include_c, m):
    lab = (["c (constante)"] if include_c else [])
    lab += [f"φ{i}" for i in range(1, p + 1)]
    lab += [f"Φ{i} (s{m})" for i in range(1, P + 1)]
    lab += [f"θ{i}" for i in range(1, q + 1)]
    lab += [f"Θ{i} (s{m})" for i in range(1, Q + 1)]
    return lab


def run(y, order=(1, 0, 0), seasonal=(0, 0, 0, 12), include_c=None, h=12, conf=95, holdout=0):
    y = _clean(y)
    p, d, q = [int(v) for v in order]
    P, D, Q, m = [int(v) for v in seasonal]
    if include_c is None:
        include_c = (d + D == 0)
    if y.size < (p + q + P * m + Q * m + d + D * m + 5):
        raise ValueError("Serie demasiado corta para el modelo especificado.")

    test = None
    if holdout > 0:
        if holdout >= y.size - (p + q + 5):
            raise ValueError("Holdout demasiado grande.")
        ytr = y[:-holdout]
        f = fit_css(ytr, (p, d, q), (P, D, Q, m), include_c)
        fc, lo, hi = _forecast(ytr, f["A"], f["b"], f["c"], f["e"], holdout, f["sigma2"], conf)
        act = y[-holdout:]
        err = act - fc
        mae = float(np.mean(np.abs(err))); rmse = float(math.sqrt(np.mean(err ** 2)))
        with np.errstate(divide="ignore", invalid="ignore"):
            mape = float(np.mean(np.abs(err[act != 0] / act[act != 0])) * 100) if np.any(act != 0) else float("nan")
        test = {"size": holdout, "actual": [float(v) for v in act], "pred": [float(v) for v in fc],
                "MAE": mae, "RMSE": rmse, "MAPE": mape}

    f = fit_css(y, (p, d, q), (P, D, Q, m), include_c)
    fc, lo, hi = _forecast(y, f["A"], f["b"], f["c"], f["e"], h, f["sigma2"], conf)

    labels = _labels(p, P, q, Q, include_c, m)
    tcrit = 1.96
    coefs = []
    for i, name in enumerate(labels):
        b_ = float(f["params"][i]); se_ = float(f["se"][i]) if i < len(f["se"]) else float("nan")
        t_ = b_ / se_ if se_ and se_ == se_ and se_ > 0 else float("nan")
        pv = 2 * (1 - sps.norm.cdf(abs(t_))) if t_ == t_ else float("nan")
        st = "***" if pv < 0.01 else ("**" if pv < 0.05 else ("*" if pv < 0.10 else "")) if pv == pv else ""
        coefs.append({"var": name, "coef": b_, "se": se_, "t": t_, "p": pv, "stars": st,
                      "ic": [b_ - tcrit * se_, b_ + tcrit * se_] if se_ == se_ else [None, None]})

    nlags = min(2 * m if m > 1 else 10, f["n_eff"] // 2)
    nlags = max(4, int(nlags))
    lb = _ljung_box(f["resid"], nlags, p + q + P + Q)
    jb = _jarque_bera(f["resid"])

    fitted = [None] * f["start"] + [float(f["e"][t] * 0 + (y[t] - f["e"][t])) for t in range(f["start"], len(y))]

    order_str = f"ARIMA({p},{d},{q})" + (f"({P},{D},{Q})[{m}]" if (P + D + Q) > 0 else "")
    return {
        "order": [p, d, q], "seasonal": [P, D, Q, m], "include_c": include_c,
        "order_str": order_str, "n": int(y.size), "h": h,
        "series": [float(v) for v in y], "fitted": fitted,
        "forecast": [float(v) for v in fc],
        "intervals": {"lower": [float(v) for v in lo], "upper": [float(v) for v in hi], "conf": conf},
        "coeficientes": coefs,
        "ajuste": {"aic": f["aic"], "bic": f["bic"], "aicc": f["aicc"], "ll": f["ll"],
                   "sigma2": f["sigma2"], "sigma": math.sqrt(f["sigma2"]), "n_eff": f["n_eff"]},
        "residuos": [float(v) for v in f["resid"]],
        "ljung_box": lb, "jarque_bera": jb, "test": test,
        "interpretacion": _interpret(order_str, coefs, f, lb, jb, test),
    }


def _interpret(order_str, coefs, f, lb, jb, test):
    it = [f"Modelo estimado: {order_str} por mínimos cuadrados condicionales (CSS). "
          f"AIC = {f['aic']:.1f}, BIC = {f['bic']:.1f}, log-verosim. = {f['ll']:.1f}."]
    sig = [c["var"] for c in coefs if c["p"] == c["p"] and c["p"] < 0.05]
    it.append(f"Coeficientes significativos al 5%: {', '.join(sig) if sig else 'ninguno'}.")
    if lb["p"] < 0.05:
        it.append(f"⚠ Ljung-Box (rezagos {lb['nlags']}): Q = {lb['Q']:.1f}, p = {lb['p']:.4g} (<0,05): los residuos "
                  "AÚN tienen autocorrelación → el modelo no captura toda la estructura; prueba otros órdenes.")
    else:
        it.append(f"Ljung-Box p = {lb['p']:.4g} (≥0,05): los residuos se comportan como ruido blanco (buen ajuste).")
    if jb["p"] < 0.05:
        it.append(f"Jarque-Bera p = {jb['p']:.4g}: residuos no normales; los intervalos son aproximados.")
    else:
        it.append(f"Jarque-Bera p = {jb['p']:.4g}: residuos aproximadamente normales.")
    if test:
        it.append(f"Validación en {test['size']} datos de prueba: RMSE = {test['RMSE']:.3g}, MAPE = {test['MAPE']:.2f}%.")
    it.append("Los intervalos de predicción se ensanchan con el horizonte (ψ-pesos de la representación MA(∞)).")
    return it


# --------------------------------------------------------------------------- #
#  Selección automática (grid por AIC)
# --------------------------------------------------------------------------- #
def auto(y, d=None, D=0, m=12, pmax=2, qmax=2, Pmax=1, Qmax=1, seasonal=True, ic="aicc"):
    y = _clean(y)
    if d is None:
        from apps.series import solver as SS
        d = 0
        try:
            a = SS.adf(y, "c")
            if not a["estacionaria"]:
                d = 1
        except Exception:
            d = 1
    if not seasonal:
        Pmax = Qmax = D = 0
    resultados = []
    best = None
    for p in range(pmax + 1):
        for q in range(qmax + 1):
            for P in range(Pmax + 1):
                for Q in range(Qmax + 1):
                    try:
                        f = fit_css(y, (p, d, q), (P, D, Q, m), include_c=(d + D == 0))
                        val = {"aic": f["aic"], "bic": f["bic"], "aicc": f["aicc"]}[ic]
                        resultados.append({"order": [p, d, q], "seasonal": [P, D, Q, m],
                                           "aic": f["aic"], "bic": f["bic"], "aicc": f["aicc"]})
                        if best is None or val < best[0]:
                            best = (val, (p, d, q), (P, D, Q, m))
                    except Exception:
                        pass
    resultados.sort(key=lambda r: r[ic])
    if not best:
        raise ValueError("No se pudo ajustar ningún modelo.")
    return {"d": d, "criterio": ic, "mejor_order": list(best[1]), "mejor_seasonal": list(best[2]),
            "ranking": resultados[:12],
            "interpretacion": [
                f"Selección automática por {ic.upper()} (menor es mejor). Mejor modelo: "
                f"ARIMA{tuple(best[1])}" + (f"×{tuple(best[2][:3])}[{m}]" if sum(best[2][:3]) else "") + ".",
                f"Se probaron {len(resultados)} combinaciones (d fijado en {d}). "
                "Estímalo en la pestaña de estimación para ver coeficientes y diagnósticos."]}


# --------------------------------------------------------------------------- #
#  Validación con origen móvil (rolling / expanding origin)
# --------------------------------------------------------------------------- #
def rolling_origin(y, order, seasonal, include_c=None, h=1, min_train=None, paso=1, ventana="expansiva"):
    y = _clean(y)
    p, d, q = [int(v) for v in order]
    P, D, Q, m = [int(v) for v in seasonal]
    if include_c is None:
        include_c = (d + D == 0)
    n = len(y)
    if min_train is None:
        min_train = max(int(n * 0.6), 2 * m + p + q + 6)
    errs = []
    origenes = []
    end = min_train
    while end + h <= n:
        tr = y[end - min_train:end] if ventana == "movil" else y[:end]
        try:
            f = fit_css(tr, (p, d, q), (P, D, Q, m), include_c)
            fc, _, _ = _forecast(tr, f["A"], f["b"], f["c"], f["e"], h, f["sigma2"], 95)
            act = y[end:end + h]
            e = act - fc
            errs.append(e)
            origenes.append({"origen": int(end), "rmse": float(math.sqrt(np.mean(e ** 2))),
                             "mae": float(np.mean(np.abs(e)))})
        except Exception:
            pass
        end += paso
    if not errs:
        raise ValueError("No se pudo realizar la validación (serie corta o modelo inestable).")
    allerr = np.concatenate(errs)
    with np.errstate(divide="ignore", invalid="ignore"):
        return {"n_origenes": len(origenes), "h": h, "ventana": ventana, "min_train": min_train,
                "MAE": float(np.mean(np.abs(allerr))), "RMSE": float(math.sqrt(np.mean(allerr ** 2))),
                "origenes": origenes,
                "interpretacion": [
                    f"Validación con origen móvil ({'ventana móvil' if ventana=='movil' else 'ventana expansiva'}), "
                    f"horizonte h = {h}: {len(origenes)} orígenes evaluados.",
                    f"Error promedio fuera de muestra: RMSE = {math.sqrt(np.mean(allerr**2)):.3g}, MAE = {np.mean(np.abs(allerr)):.3g}.",
                    "Es una evaluación más honesta que el ajuste in-sample: simula pronosticar en el tiempo real, reestimando en cada origen."]}
