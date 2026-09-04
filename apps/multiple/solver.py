"""
Pronósticos múltiples — aplica un modelo a MUCHAS series a la vez (procesamiento por lotes).
Reutiliza apps.pronostico.solver.
"""
import numpy as np
from apps.pronostico import solver as P


def run(series, modelo="ses", h=6, m=12, holdout=0, conf=95):
    """series = [{name, values}]. Devuelve pronóstico + métrica por cada serie."""
    filas = []
    for s in series:
        try:
            y = [v for v in s["values"] if v is not None]
            r = P.run(y, modelo, h=h, m=m, holdout=holdout, conf=conf)
            met = r["test_metrics"] or r["insample_metrics"]
            filas.append({"name": s["name"], "ok": True,
                          "n": r["n"], "forecast": r["forecast"],
                          "lower": r["intervals"]["lower"], "upper": r["intervals"]["upper"],
                          "series": r["series"],
                          "RMSE": met["RMSE"], "MAPE": met["MAPE"], "MASE": met["MASE"],
                          "params": r["params"]})
        except Exception as e:
            filas.append({"name": s["name"], "ok": False, "error": str(e)})

    ok = [f for f in filas if f["ok"]]
    if not ok:
        raise ValueError("Ninguna serie pudo pronosticarse con el modelo elegido.")
    mapes = [f["MAPE"] for f in ok if f["MAPE"] == f["MAPE"]]
    interp = [
        f"Se pronosticaron {len(ok)} series con el modelo «{P._LABELS.get(modelo, modelo)}» a {h} períodos.",
        (f"MAPE promedio entre series: {np.mean(mapes):.1f}% (mín {np.min(mapes):.1f}%, máx {np.max(mapes):.1f}%). "
         if mapes else "") + "Revisa las series con mayor error: pueden requerir otro modelo o más datos.",
        "Este módulo automatiza el pronóstico masivo (una cartera de productos, sucursales, SKUs), aplicando el mismo método a todas.",
    ]
    return {"modelo": modelo, "label": P._LABELS.get(modelo, modelo), "h": h,
            "series": filas, "n_ok": len(ok), "interpretacion": interp}
