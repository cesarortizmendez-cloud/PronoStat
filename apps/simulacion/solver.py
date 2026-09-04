"""
Simulación y escenarios — Monte Carlo de trayectorias futuras.
Ajusta un modelo base (apps.pronostico.solver), obtiene el pronóstico puntual y la σ de
residuos, y simula N trayectorias acumulando shocks (normales o por bootstrap de residuos).
Entrega abanico de percentiles, escenarios y probabilidad de superar un umbral.
"""
import math
import numpy as np
from apps.pronostico import solver as P


def run(y, modelo="holt", h=12, m=12, n_sim=1000, dist="normal", umbral=None, conf=95, seed=None):
    y = [v for v in y if v is not None]
    r = P.run(y, modelo, h=h, m=m, holdout=0, conf=conf)
    pf = np.array(r["forecast"], dtype=float)
    sigma = r["sigma"]
    resid = np.array(r["series"], dtype=float)
    fitted = np.array([v for v in r["fitted"] if v is not None], dtype=float)
    # residuos observados para bootstrap
    k = min(len(fitted), len(resid))
    res_obs = resid[-k:] - fitted[-k:] if k > 0 else np.array([0.0])
    res_obs = res_obs[~np.isnan(res_obs)]
    if res_obs.size < 2:
        res_obs = np.random.default_rng(0).normal(0, sigma, 50)

    rng = np.random.default_rng(seed)
    n_sim = int(min(max(n_sim, 100), 5000))
    paths = np.zeros((n_sim, h))
    for i in range(n_sim):
        if dist == "bootstrap":
            shocks = rng.choice(res_obs, size=h, replace=True)
        else:
            shocks = rng.normal(0, sigma, h)
        err = np.cumsum(shocks)           # error acumulado (crece con el horizonte)
        paths[i] = pf + err

    pct = {p: [float(v) for v in np.percentile(paths, p, axis=0)] for p in (5, 25, 50, 75, 95)}
    media = [float(v) for v in paths.mean(axis=0)]

    # escenarios (en el horizonte final)
    final = paths[:, -1]
    escenarios = {
        "optimista_p90": float(np.percentile(final, 90)),
        "esperado_media": float(np.mean(final)),
        "pesimista_p10": float(np.percentile(final, 10)),
    }
    prob = None
    if umbral is not None:
        prob = {
            "umbral": float(umbral),
            "p_supera_final": float(np.mean(final > umbral) * 100),
            "p_supera_algun": float(np.mean(np.any(paths > umbral, axis=1)) * 100),
        }

    interp = [
        f"Simulación Monte Carlo de {n_sim} trayectorias a {h} períodos con el modelo «{P._LABELS.get(modelo, modelo)}» "
        f"(shocks {'por bootstrap de residuos' if dist=='bootstrap' else 'normales'}, σ = {sigma:.3g}).",
        f"Escenarios en t+{h}: pesimista (P10) = {escenarios['pesimista_p10']:.3g}, "
        f"esperado = {escenarios['esperado_media']:.3g}, optimista (P90) = {escenarios['optimista_p90']:.3g}.",
        "El abanico (P5–P95) muestra el rango de resultados plausibles: se ensancha con el horizonte porque la incertidumbre se acumula.",
    ]
    if prob:
        interp.append(f"Probabilidad de superar {umbral:g}: {prob['p_supera_final']:.1f}% en t+{h}, "
                      f"{prob['p_supera_algun']:.1f}% en algún período del horizonte.")
    interp.append("Útil para gestión de riesgo y planificación de escenarios (¿cuánto stock/capacidad ante el peor caso razonable?).")

    return {"modelo": modelo, "label": P._LABELS.get(modelo, modelo), "h": h, "n": len(y),
            "n_sim": n_sim, "dist": dist, "sigma": sigma,
            "series": [float(v) for v in y], "pronostico": [float(v) for v in pf],
            "percentiles": pct, "media_sim": media,
            "escenarios": escenarios, "probabilidad": prob,
            "muestras": [[float(v) for v in paths[i]] for i in range(min(30, n_sim))],
            "interpretacion": interp}
