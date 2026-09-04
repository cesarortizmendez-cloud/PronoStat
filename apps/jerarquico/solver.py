"""
Pronósticos jerárquicos — reconciliación de series que suman a un total.
Métodos: bottom-up (de abajo hacia arriba) y top-down (proporciones históricas).
Reutiliza apps.pronostico.solver. Referencia: Hyndman FPP cap. jerárquico.
"""
import numpy as np
from apps.pronostico import solver as P


def run(series, modelo="holt", h=6, m=12, holdout=0, conf=95):
    """series = [{name, values}] de nivel inferior (hojas). El total = suma."""
    if len(series) < 2:
        raise ValueError("Se necesitan al menos 2 series de nivel inferior.")
    # alinear longitudes
    n = min(len(s["values"]) for s in series)
    mats = np.array([[float(v) for v in s["values"][-n:]] for s in series])  # (k, n)
    total = mats.sum(axis=0)
    nombres = [s["name"] for s in series]

    # --- Bottom-up: pronosticar cada hoja y sumar ---
    fc_hojas = []
    for i, nm in enumerate(nombres):
        r = P.run(list(mats[i]), modelo, h=h, m=m, holdout=0, conf=conf)
        fc_hojas.append(np.array(r["forecast"]))
    fc_hojas = np.array(fc_hojas)                       # (k, h)
    total_bu = fc_hojas.sum(axis=0)

    # --- Top-down: pronosticar el total y repartir por proporción histórica ---
    rt = P.run(list(total), modelo, h=h, m=m, holdout=0, conf=conf)
    total_td = np.array(rt["forecast"])
    prop = mats.sum(axis=1) / total.sum()               # proporción histórica de cada hoja
    fc_hojas_td = np.outer(prop, total_td)              # (k, h)

    interp = [
        f"Jerarquía de {len(nombres)} series que suman a un total, pronosticadas con «{P._LABELS.get(modelo, modelo)}».",
        "BOTTOM-UP: se pronostica cada hoja y se suman → el total es coherente con las partes; bueno si las hojas son predecibles.",
        "TOP-DOWN: se pronostica el total y se reparte por la proporción histórica de cada hoja "
        f"({', '.join(f'{nombres[i]}={prop[i]*100:.0f}%' for i in range(len(nombres)))}); bueno si el total es más estable que las hojas.",
        "Ambos producen pronósticos COHERENTES (las hojas suman el total). La elección depende de en qué nivel el patrón es más claro.",
    ]
    return {"modelo": modelo, "label": P._LABELS.get(modelo, modelo), "h": h, "n": int(n),
            "nombres": nombres, "proporciones": [float(x) for x in prop],
            "total_hist": [float(x) for x in total],
            "total_bottom_up": [float(x) for x in total_bu],
            "total_top_down": [float(x) for x in total_td],
            "hojas_bottom_up": [[float(x) for x in row] for row in fc_hojas],
            "hojas_top_down": [[float(x) for x in row] for row in fc_hojas_td],
            "interpretacion": interp}
