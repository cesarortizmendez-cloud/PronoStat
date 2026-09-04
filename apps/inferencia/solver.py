"""
Inferencia estadística — estimación por intervalos y tamaño de muestra.
Lógica pura (numpy + scipy). Referencias: Walpole/Myers, Montgomery/Runger,
Triola; formulario coherente con OpenStax/LibreTexts.

Cubre:
  • IC para la media con σ CONOCIDA (Z)          x̄ ± z_{α/2}·σ/√n
  • IC para la media con σ DESCONOCIDA (t)       x̄ ± t_{α/2,n−1}·s/√n
  • IC para una PROPORCIÓN                        Wald, Wilson (score) y Agresti-Coull
  • Corrección por población finita (fpc)         √((N−n)/(N−1))
  • Tamaño de muestra para la media               n = (z_{α/2}·σ/E)²
  • Tamaño de muestra para una proporción         n = z²·p̂(1−p̂)/E²
El Teorema Central del Límite justifica el uso de la normal para x̄ cuando n es grande
(regla práctica n ≥ 30) aun si la población no es normal.
"""
import math
import numpy as np
from scipy import stats as sps


def _z(conf):
    alpha = 1 - conf / 100.0
    return float(sps.norm.ppf(1 - alpha / 2))


def _t(conf, gl):
    alpha = 1 - conf / 100.0
    return float(sps.t.ppf(1 - alpha / 2, gl))


def _clean(values):
    x = np.asarray([v for v in values if v is not None], dtype=float)
    return x[~np.isnan(x)]


# --------------------------------------------------------------------------- #
#  IC para la media
# --------------------------------------------------------------------------- #
def ic_media(values=None, media=None, s=None, sigma=None, n=None,
             conf=95, N=None):
    """
    σ conocida  -> se pasa `sigma`  -> usa Z.
    σ desconocida -> se pasa `s` (o se calcula de los datos) -> usa t (gl=n−1).
    `values` (lista) permite calcular x̄, s y n desde datos.
    `N` (población) aplica corrección por población finita.
    """
    if values is not None:
        x = _clean(values)
        if x.size < 2:
            raise ValueError("Se requieren al menos 2 datos.")
        n = int(x.size)
        media = float(np.mean(x))
        s = float(np.std(x, ddof=1))
    if media is None or n is None or n < 1:
        raise ValueError("Faltan datos: media y n son obligatorios.")

    sigma_known = sigma is not None
    if sigma_known:
        de = float(sigma)
        metodo = "Z (σ conocida)"
        gl = None
        crit = _z(conf)
    else:
        if s is None:
            raise ValueError("Con σ desconocida se necesita la desviación muestral s.")
        de = float(s)
        gl = n - 1
        if n >= 30:
            metodo = "t (σ desconocida; n≥30, por TCL t≈Z)"
        else:
            metodo = "t (σ desconocida)"
        crit = _t(conf, gl)

    se = de / math.sqrt(n)
    fpc = None
    if N and N > n:
        fpc = math.sqrt((N - n) / (N - 1))
        se *= fpc
    margen = crit * se
    ic = [media - margen, media + margen]

    interp = [
        f"Con {conf}% de confianza, la media poblacional (μ) está entre {ic[0]:.4g} y {ic[1]:.4g}.",
        f"Se usó la distribución {'normal (Z)' if sigma_known else 'de Student (t)'} porque "
        + ("σ es conocida." if sigma_known else f"σ es desconocida y se estima con s (gl = {gl})."),
        f"El margen de error es ±{margen:.4g} (valor crítico {crit:.3f} × error estándar {se:.4g}).",
    ]
    if not sigma_known and n < 30:
        interp.append("Con n < 30, la validez del intervalo depende de que la población sea aproximadamente normal.")
    else:
        interp.append("Por el Teorema Central del Límite, la distribución de x̄ es aproximadamente normal para este n.")
    if fpc:
        interp.append(f"Se aplicó corrección por población finita (N = {N}): factor {fpc:.4f}.")

    return {"tipo": "media", "metodo": metodo, "media": media, "s": s, "sigma": sigma,
            "n": n, "gl": gl, "conf": conf, "valor_critico": crit, "error_std": se,
            "margen": margen, "ic": ic, "fpc": fpc, "sigma_known": sigma_known,
            "interpretacion": interp}


# --------------------------------------------------------------------------- #
#  IC para una proporción
# --------------------------------------------------------------------------- #
def ic_proporcion(x=None, n=None, phat=None, conf=95, N=None):
    if n is None or n < 1:
        raise ValueError("n es obligatorio.")
    n = int(n)
    if x is not None:
        x = int(x)
        if x < 0 or x > n:
            raise ValueError("El número de éxitos debe estar entre 0 y n.")
        phat = x / n
    if phat is None:
        raise ValueError("Se requiere el número de éxitos x o la proporción p̂.")
    phat = float(phat)
    z = _z(conf)

    fpc = 1.0
    if N and N > n:
        fpc = math.sqrt((N - n) / (N - 1))

    # Wald
    se_wald = math.sqrt(phat * (1 - phat) / n) * fpc
    wald = [phat - z * se_wald, phat + z * se_wald]

    # Wilson (score) — recomendado
    z2 = z * z
    denom = 1 + z2 / n
    centro = (phat + z2 / (2 * n)) / denom
    half = (z / denom) * math.sqrt(phat * (1 - phat) / n + z2 / (4 * n * n)) * fpc
    wilson = [centro - half, centro + half]

    # Agresti-Coull
    n_ac = n + z2
    p_ac = (x + z2 / 2) / n_ac if x is not None else (phat * n + z2 / 2) / n_ac
    se_ac = math.sqrt(p_ac * (1 - p_ac) / n_ac) * fpc
    agresti = [p_ac - z * se_ac, p_ac + z * se_ac]

    clamp = lambda iv: [max(0.0, iv[0]), min(1.0, iv[1])]
    wald, wilson, agresti = clamp(wald), clamp(wilson), clamp(agresti)

    regla = n * phat >= 5 and n * (1 - phat) >= 5
    interp = [
        f"Proporción muestral p̂ = {phat:.4f} ({phat*100:.2f}%). Con {conf}% de confianza, la proporción "
        f"poblacional está aproximadamente entre {wilson[0]*100:.2f}% y {wilson[1]*100:.2f}% (intervalo de Wilson).",
        f"El margen de error (Wald) es ±{z*se_wald:.4f} ({z*se_wald*100:.2f} puntos porcentuales).",
        ("Se cumple la condición n·p̂ ≥ 5 y n·(1−p̂) ≥ 5: la aproximación normal es adecuada."
         if regla else
         "No se cumple n·p̂ ≥ 5 y n·(1−p̂) ≥ 5: prefiere el intervalo de Wilson o exacto; el de Wald puede ser impreciso."),
        "Wilson y Agresti-Coull son más precisos que Wald con muestras pequeñas o proporciones extremas.",
    ]
    if fpc < 1:
        interp.append(f"Se aplicó corrección por población finita (N = {N}).")

    return {"tipo": "proporcion", "phat": phat, "x": x, "n": n, "conf": conf, "z": z,
            "error_std": se_wald, "margen": z * se_wald,
            "ic_wald": wald, "ic_wilson": wilson, "ic_agresti": agresti,
            "regla_np": regla, "fpc": fpc if fpc < 1 else None, "interpretacion": interp}


# --------------------------------------------------------------------------- #
#  Tamaño de muestra
# --------------------------------------------------------------------------- #
def n_media(E, sigma, conf=95, N=None):
    if E <= 0 or sigma <= 0:
        raise ValueError("El error E y σ deben ser positivos.")
    z = _z(conf)
    n0 = (z * sigma / E) ** 2
    n_inf = math.ceil(n0)
    n_fin = None
    if N and N > 0:
        n_fin = math.ceil(n0 / (1 + (n0 - 1) / N))
    interp = [
        f"Para estimar la media con un error máximo de ±{E:g} y {conf}% de confianza (σ = {sigma:g}), "
        f"se requieren n = {n_inf} observaciones.",
        f"Fórmula: n = (z·σ/E)² = ({z:.3f}·{sigma:g}/{E:g})² = {n0:.2f} → se redondea hacia arriba.",
    ]
    if n_fin:
        interp.append(f"Con población finita N = {N}, basta n = {n_fin} (corrección por población finita).")
    interp.append("Si σ es desconocida, usa una estimación previa (estudio piloto) o el rango/4 como aproximación.")
    return {"tipo": "n_media", "E": E, "sigma": sigma, "conf": conf, "z": z,
            "n0": n0, "n": n_inf, "n_finita": n_fin, "N": N, "interpretacion": interp}


def n_proporcion(E, phat=0.5, conf=95, N=None):
    if E <= 0 or not (0 < phat < 1):
        raise ValueError("E debe ser positivo y p̂ estar entre 0 y 1.")
    z = _z(conf)
    n0 = (z * z * phat * (1 - phat)) / (E * E)
    n_inf = math.ceil(n0)
    n_fin = None
    if N and N > 0:
        n_fin = math.ceil((N * z * z * phat * (1 - phat)) /
                          (E * E * (N - 1) + z * z * phat * (1 - phat)))
    conservador = abs(phat - 0.5) < 1e-9
    interp = [
        f"Para estimar una proporción con un error máximo de ±{E*100:g}% y {conf}% de confianza, "
        f"se requieren n = {n_inf} observaciones.",
        f"Fórmula: n = z²·p̂(1−p̂)/E² = {z:.3f}²·{phat:g}·{1-phat:g}/{E:g}² = {n0:.2f} → se redondea hacia arriba.",
        ("Se usó p̂ = 0,5 (escenario más conservador: máximo tamaño de muestra), apropiado cuando no hay información previa."
         if conservador else
         f"Se usó una estimación previa p̂ = {phat:g}."),
    ]
    if n_fin:
        interp.append(f"Con población finita N = {N}, basta n = {n_fin}.")
    return {"tipo": "n_proporcion", "E": E, "phat": phat, "conf": conf, "z": z,
            "n0": n0, "n": n_inf, "n_finita": n_fin, "N": N, "interpretacion": interp}
