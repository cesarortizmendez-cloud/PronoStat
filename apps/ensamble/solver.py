"""
Ensamble de modelos — combina pronósticos de varios modelos base.
Reutiliza apps.pronostico.solver. Referencias: Bates & Granger (1969), Hyndman FPP.

Estrategias: media simple, mediana y ponderación por el inverso del error (RMSE) en holdout.
La combinación suele reducir el error y la varianza respecto a cualquier modelo individual.
"""
import math
import numpy as np
from apps.pronostico import solver as P


def run(y, modelos=None, h=6, m=12, holdout=6, conf=95):
    y = [v for v in y if v is not None]
    modelos = modelos or ["ingenuo", "promedio_movil", "ses", "holt", "holt_winters"]
    base = []
    for mod in modelos:
        try:
            r = P.run(y, mod, h=h, m=m, holdout=holdout, conf=conf)
            met = r["test_metrics"] or r["insample_metrics"]
            base.append({"model": mod, "label": P._LABELS[mod], "forecast": r["forecast"],
                         "rmse": met["RMSE"], "mae": met["MAE"], "mape": met["MAPE"],
                         "test_pred": r["test"]["pred"] if r.get("test") else None,
                         "ok": True})
        except Exception as e:
            base.append({"model": mod, "label": P._LABELS.get(mod, mod), "ok": False, "error": str(e)})

    ok = [b for b in base if b["ok"] and b["rmse"] == b["rmse"] and b["rmse"] > 0]
    if len(ok) < 2:
        raise ValueError("Se necesitan al menos 2 modelos válidos para ensamblar.")

    F = np.array([b["forecast"] for b in ok])            # (n_modelos, h)
    # pesos por inverso del RMSE
    w = np.array([1.0 / b["rmse"] for b in ok]); w = w / w.sum()
    ens_media = F.mean(axis=0)
    ens_mediana = np.median(F, axis=0)
    ens_pond = (F * w[:, None]).sum(axis=0)

    # error del ensamble en holdout (si hay predicciones de prueba)
    ens_test_metrics = None
    if holdout > 0 and all(b["test_pred"] is not None for b in ok):
        T = np.array([b["test_pred"] for b in ok])
        actual = np.array(P.run(y, ok[0]["model"], h=h, m=m, holdout=holdout)["test"]["actual"])
        combos = {"media": T.mean(axis=0), "mediana": np.median(T, axis=0), "ponderado": (T * w[:, None]).sum(axis=0)}
        ens_test_metrics = {}
        for name, pred in combos.items():
            e = actual - pred
            ens_test_metrics[name] = {"RMSE": float(math.sqrt(np.mean(e ** 2))),
                                      "MAE": float(np.mean(np.abs(e)))}

    # ranking de individuales + ensambles
    tabla = [{"modelo": b["label"], "peso": float(w[i]), "rmse": b["rmse"], "mae": b["mae"], "mape": b["mape"], "tipo": "individual"} for i, b in enumerate(ok)]
    if ens_test_metrics:
        for nm, mt in ens_test_metrics.items():
            tabla.append({"modelo": f"Ensamble ({nm})", "peso": None, "rmse": mt["RMSE"], "mae": mt["MAE"], "mape": None, "tipo": "ensamble"})
    tabla.sort(key=lambda r: r["rmse"])
    mejor = tabla[0]

    interp = [
        f"Se ensamblaron {len(ok)} modelos. Los pesos por inverso del RMSE dan más importancia a los modelos "
        f"más precisos en el conjunto de prueba.",
        f"Pesos: " + ", ".join(f"{b['label']} = {w[i]:.2f}" for i, b in enumerate(ok)) + ".",
    ]
    if ens_test_metrics:
        best_ind = min((t for t in tabla if t["tipo"] == "individual"), key=lambda t: t["rmse"])
        best_ens = min((t for t in tabla if t["tipo"] == "ensamble"), key=lambda t: t["rmse"])
        if best_ens["rmse"] <= best_ind["rmse"]:
            interp.append(f"✔ El mejor ensamble ({best_ens['modelo']}, RMSE={best_ens['rmse']:.3g}) iguala o supera al "
                          f"mejor modelo individual ({best_ind['modelo']}, RMSE={best_ind['rmse']:.3g}): la combinación ayudó.")
        else:
            interp.append(f"En este caso el mejor individual ({best_ind['modelo']}) superó al ensamble; ocurre cuando un modelo domina claramente.")
    interp.append("Regla práctica (Bates-Granger): combinar modelos diversos reduce el riesgo de elegir uno malo y suele bajar la varianza del error.")

    return {"h": h, "n": len(y), "modelos": [b["label"] for b in ok],
            "pesos": [float(x) for x in w],
            "series": [float(v) for v in y],
            "forecasts_individuales": [{"label": b["label"], "forecast": b["forecast"]} for b in ok],
            "ensamble_media": [float(x) for x in ens_media],
            "ensamble_mediana": [float(x) for x in ens_mediana],
            "ensamble_ponderado": [float(x) for x in ens_pond],
            "tabla": tabla, "mejor": mejor, "interpretacion": interp}
