"""
Muestreo — técnicas, extracción de muestras, tamaño de muestra, asignación y estimación.
Lógica pura (numpy + scipy). Referencias: Cochran, Scheaffer/Mendenhall/Ott, Lohr; INEI.

Incluye:
  • Extracción de muestras desde un conjunto de datos:
      - Aleatorio simple (MAS)      - Sistemático (k = N/n)     - Estratificado (asignación proporcional)
  • Tamaño de muestra para media y proporción, con corrección por población finita (fpc).
  • Asignación en muestreo estratificado: proporcional y óptima de Neyman.
  • Estimación basada en el diseño:
      - MAS: media, total y sus IC con fpc.
      - Estratificado: media y total ponderados con su varianza.
"""
import math
import numpy as np
from scipy import stats as sps


def _z(conf):
    return float(sps.norm.ppf(1 - (1 - conf / 100) / 2))


def _num(rows, col):
    out = []
    for r in rows:
        v = r.get(col)
        try:
            fv = float(v)
            if not math.isnan(fv):
                out.append(fv)
        except (TypeError, ValueError):
            pass
    return np.array(out, dtype=float)


def _resumen(arr):
    if arr.size == 0:
        return None
    return {"n": int(arr.size), "media": float(np.mean(arr)),
            "sd": float(np.std(arr, ddof=1)) if arr.size > 1 else 0.0,
            "min": float(np.min(arr)), "max": float(np.max(arr))}


# --------------------------------------------------------------------------- #
#  Extracción de una muestra desde el dataset
# --------------------------------------------------------------------------- #
def extraer(rows, metodo="mas", n=30, estrato_col=None, var=None, seed=None):
    N = len(rows)
    if N == 0:
        raise ValueError("El conjunto de datos está vacío.")
    n = int(n)
    if n < 1 or n > N:
        raise ValueError(f"El tamaño de muestra debe estar entre 1 y N = {N}.")
    rng = np.random.default_rng(seed)
    alloc = None

    if metodo == "mas":
        idx = sorted(rng.choice(N, size=n, replace=False).tolist())

    elif metodo == "sistematico":
        k = N // n
        if k < 1:
            k = 1
        inicio = int(rng.integers(0, k))
        idx = [(inicio + i * k) for i in range(n) if inicio + i * k < N]
        alloc = {"k": k, "inicio": inicio + 1}  # 1-indexado para mostrar

    elif metodo == "estratificado":
        if not estrato_col:
            raise ValueError("El muestreo estratificado requiere una columna de estrato.")
        grupos = {}
        for i, r in enumerate(rows):
            key = "∅" if r.get(estrato_col) in (None, "") else str(r.get(estrato_col))
            grupos.setdefault(key, []).append(i)
        # asignación proporcional
        alloc = []
        idx = []
        nombres = list(grupos.keys())
        base = {name: n * len(grupos[name]) / N for name in nombres}
        nh = {name: int(math.floor(base[name])) for name in nombres}
        # repartir el resto por mayor parte fraccionaria
        resto = n - sum(nh.values())
        fracs = sorted(nombres, key=lambda nm: base[nm] - nh[nm], reverse=True)
        for j in range(resto):
            nh[fracs[j % len(fracs)]] += 1
        for name in nombres:
            Nh = len(grupos[name])
            take = min(nh[name], Nh)
            sel = rng.choice(grupos[name], size=take, replace=False).tolist() if take > 0 else []
            idx.extend(sel)
            alloc.append({"estrato": name, "N_h": Nh, "n_h": take,
                          "peso": round(Nh / N, 4), "fraccion": round(take / Nh, 4) if Nh else 0})
        idx = sorted(idx)
    else:
        raise ValueError(f"Método de muestreo desconocido: {metodo}")

    muestra = [rows[i] for i in idx]
    comparacion = None
    if var:
        pob = _num(rows, var)
        mue = _num(muestra, var)
        rp, rm = _resumen(pob), _resumen(mue)
        if rp and rm:
            err = rm["media"] - rp["media"]
            comparacion = {"variable": var, "poblacion": rp, "muestra": rm,
                           "error_muestral": err,
                           "error_relativo_pct": (abs(err) / rp["media"] * 100) if rp["media"] else float("nan")}

    return {"metodo": metodo, "N": N, "n": len(idx),
            "indices": [i + 1 for i in idx],  # 1-indexado
            "muestra": muestra[:200],          # límite para no saturar
            "muestra_completa_n": len(muestra),
            "asignacion": alloc, "comparacion": comparacion,
            "interpretacion": _interp_extraer(metodo, N, len(idx), estrato_col, comparacion, alloc)}


def _interp_extraer(metodo, N, n, estrato_col, comp, alloc):
    nombres = {"mas": "aleatorio simple", "sistematico": "sistemático", "estratificado": "estratificado"}
    it = [f"Se extrajo una muestra {nombres.get(metodo, metodo)} de n = {n} unidades de una población de N = {N} "
          f"(fracción de muestreo f = n/N = {n/N:.3f})."]
    if metodo == "sistematico" and alloc:
        it.append(f"Intervalo de selección k = N/n = {alloc['k']}; arranque aleatorio en la posición {alloc['inicio']}, "
                  "y luego cada k-ésima unidad.")
    if metodo == "estratificado":
        it.append(f"Asignación PROPORCIONAL por «{estrato_col}»: cada estrato aporta unidades en proporción a su tamaño (n_h = n·N_h/N).")
    if comp:
        it.append(f"Para «{comp['variable']}», la media poblacional es {comp['poblacion']['media']:.4g} y la de la muestra "
                  f"{comp['muestra']['media']:.4g}: el error de muestreo es {comp['error_muestral']:+.4g} "
                  f"({comp['error_relativo_pct']:.2f}% relativo). Muestras más grandes reducen este error.")
    return it


# --------------------------------------------------------------------------- #
#  Tamaño de muestra (con población finita)
# --------------------------------------------------------------------------- #
def tam_media(E, sigma, conf=95, N=None):
    if E <= 0 or sigma <= 0:
        raise ValueError("E y σ deben ser positivos.")
    z = _z(conf)
    n0 = (z * sigma / E) ** 2
    n = math.ceil(n0)
    n_fin = math.ceil(n0 / (1 + (n0 - 1) / N)) if N and N > 0 else None
    it = [f"Para estimar la media con error ±{E:g} y {conf}% de confianza (σ = {sigma:g}) se requieren n = {n} unidades.",
          f"Fórmula MAS: n₀ = (z·σ/E)² = ({z:.3f}·{sigma:g}/{E:g})² = {n0:.2f}."]
    if n_fin:
        it.append(f"Con población finita N = {N}, la corrección da n = {n_fin} (n = n₀/(1+(n₀−1)/N)).")
    return {"tipo": "media", "z": z, "n0": n0, "n": n, "n_finita": n_fin, "N": N,
            "E": E, "sigma": sigma, "conf": conf, "interpretacion": it}


def tam_prop(E, p=0.5, conf=95, N=None):
    if E <= 0 or not (0 < p < 1):
        raise ValueError("E > 0 y 0 < p < 1.")
    z = _z(conf)
    n0 = z * z * p * (1 - p) / (E * E)
    n = math.ceil(n0)
    n_fin = math.ceil((N * z * z * p * (1 - p)) / (E * E * (N - 1) + z * z * p * (1 - p))) if N and N > 1 else None
    it = [f"Para estimar una proporción con error ±{E*100:g}% y {conf}% de confianza se requieren n = {n} unidades.",
          f"Fórmula MAS: n₀ = z²·p(1−p)/E² = {z:.3f}²·{p:g}·{1-p:g}/{E:g}² = {n0:.2f}"
          + (" (p = 0,5 = escenario conservador)." if abs(p - 0.5) < 1e-9 else ".")]
    if n_fin:
        it.append(f"Con población finita N = {N}, basta n = {n_fin}.")
    return {"tipo": "proporcion", "z": z, "n0": n0, "n": n, "n_finita": n_fin, "N": N,
            "E": E, "p": p, "conf": conf, "interpretacion": it}


# --------------------------------------------------------------------------- #
#  Asignación estratificada (proporcional y Neyman)
# --------------------------------------------------------------------------- #
def asignacion(n, estratos):
    """estratos = [{nombre, N_h, S_h?}]. Devuelve asignación proporcional y de Neyman."""
    n = int(n)
    Ntot = sum(e["N_h"] for e in estratos)
    if Ntot <= 0:
        raise ValueError("La suma de los tamaños de estrato debe ser positiva.")
    tiene_S = all(e.get("S_h") not in (None, "") for e in estratos)
    sumNS = sum(e["N_h"] * float(e["S_h"]) for e in estratos) if tiene_S else None
    filas = []
    for e in estratos:
        Nh = e["N_h"]
        prop = n * Nh / Ntot
        ney = (n * Nh * float(e["S_h"]) / sumNS) if tiene_S else None
        filas.append({"estrato": e["nombre"], "N_h": Nh, "peso": round(Nh / Ntot, 4),
                      "S_h": float(e["S_h"]) if tiene_S else None,
                      "n_proporcional": int(round(prop)),
                      "n_neyman": int(round(ney)) if ney is not None else None})
    it = [f"Muestra total n = {n} repartida entre {len(estratos)} estratos (N = {Ntot}).",
          "Asignación PROPORCIONAL: n_h = n·(N_h/N); cada estrato aporta según su tamaño."]
    if tiene_S:
        it.append("Asignación de NEYMAN (óptima): n_h = n·(N_h·S_h)/Σ(N_h·S_h); da más muestra a los estratos "
                  "más grandes y más variables, minimizando la varianza del estimador.")
    else:
        it.append("Para la asignación óptima de Neyman ingresa además la desviación S_h de cada estrato.")
    return {"n": n, "N": Ntot, "tiene_S": tiene_S, "filas": filas, "interpretacion": it}


# --------------------------------------------------------------------------- #
#  Estimación basada en el diseño
# --------------------------------------------------------------------------- #
def estimar_srs(values, N=None, conf=95):
    x = np.array([v for v in values if v is not None], dtype=float)
    x = x[~np.isnan(x)]
    n = int(x.size)
    if n < 2:
        raise ValueError("Se requieren al menos 2 datos en la muestra.")
    media = float(np.mean(x)); s = float(np.std(x, ddof=1))
    fpc = math.sqrt((N - n) / (N - 1)) if N and N > n else 1.0
    se = s / math.sqrt(n) * fpc
    t = float(sps.t.ppf(1 - (1 - conf / 100) / 2, n - 1))
    margen = t * se
    ic = [media - margen, media + margen]
    total = N * media if N else None
    ic_total = [N * ic[0], N * ic[1]] if N else None
    it = [f"Estimación MAS: la media poblacional se estima en {media:.4g}; con {conf}% de confianza está entre "
          f"{ic[0]:.4g} y {ic[1]:.4g} (n = {n}, s = {s:.4g})."]
    if N:
        it.append(f"El total poblacional se estima en {total:.4g} (= N·x̄), con IC [{ic_total[0]:.4g}, {ic_total[1]:.4g}].")
        it.append(f"Se aplicó corrección por población finita (N = {N}): factor {fpc:.4f}.")
    return {"tipo": "srs", "n": n, "N": N, "media": media, "s": s, "error_std": se,
            "margen": margen, "ic": ic, "total": total, "ic_total": ic_total,
            "fpc": fpc if fpc < 1 else None, "conf": conf, "interpretacion": it}


def estimar_estratificado(estratos, conf=95):
    """estratos = [{nombre, N_h, n_h, media_h, s_h}]."""
    Ntot = sum(e["N_h"] for e in estratos)
    if Ntot <= 0:
        raise ValueError("N total debe ser positivo.")
    media_st = 0.0; var_st = 0.0
    for e in estratos:
        Wh = e["N_h"] / Ntot
        media_st += Wh * e["media_h"]
        nh, Nh, sh = e["n_h"], e["N_h"], e["s_h"]
        if nh and nh > 0:
            var_st += (Wh ** 2) * (sh ** 2 / nh) * (1 - nh / Nh)
    se = math.sqrt(var_st)
    z = _z(conf)
    margen = z * se
    ic = [media_st - margen, media_st + margen]
    total = Ntot * media_st
    it = [f"Estimador estratificado: media = Σ W_h·x̄_h = {media_st:.4g} (W_h = N_h/N).",
          f"Error estándar = {se:.4g}; con {conf}% de confianza, la media está entre {ic[0]:.4g} y {ic[1]:.4g}.",
          f"El total poblacional se estima en {total:.4g}. La estratificación reduce la varianza cuando los estratos "
          "son internamente homogéneos."]
    return {"tipo": "estratificado", "N": Ntot, "media": media_st, "error_std": se,
            "margen": margen, "ic": ic, "total": total, "conf": conf, "interpretacion": it}
