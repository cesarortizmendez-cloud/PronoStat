"""
Módulo Datos — lógica pura (sin Django).
Detección de tipos, perfilado y limpieza básica de un conjunto de datos
recibido como lista de columnas + lista de filas (dicts).
"""
import math
import re
from datetime import datetime

_DATE_PATTERNS = [
    "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y",
    "%Y/%m/%d", "%d/%m/%y", "%Y-%m-%d %H:%M:%S",
]
_BOOL_TRUE = {"true", "verdadero", "sí", "si", "yes"}
_BOOL_FALSE = {"false", "falso", "no"}


def _is_blank(v):
    if v is None:
        return True
    if isinstance(v, float) and math.isnan(v):
        return True
    if isinstance(v, str) and v.strip() == "":
        return True
    return False


def _to_number(v):
    """Intenta convertir a float. Soporta separador de miles y coma decimal simple."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    if not isinstance(v, str):
        return None
    s = v.strip().replace("%", "")
    if s == "":
        return None
    # 1.234,56 -> 1234.56  |  1,234.56 -> 1234.56
    if re.search(r",\d{1,2}$", s) and s.count(",") == 1 and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif s.count(",") == 1 and s.count(".") == 0:
        s = s.replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def _is_date(v):
    if isinstance(v, str):
        for p in _DATE_PATTERNS:
            try:
                datetime.strptime(v.strip(), p)
                return True
            except ValueError:
                continue
    return False


def _detect_type(values):
    """Decide el tipo de una columna a partir de sus valores no vacíos."""
    non_blank = [v for v in values if not _is_blank(v)]
    if not non_blank:
        return "texto"
    n = len(non_blank)
    num = sum(1 for v in non_blank if _to_number(v) is not None)
    if num / n >= 0.85:
        return "numérico"
    dat = sum(1 for v in non_blank if _is_date(v))
    if dat / n >= 0.85:
        return "fecha"
    low = [str(v).strip().lower() for v in non_blank]
    if all(x in _BOOL_TRUE | _BOOL_FALSE for x in low):
        return "booleano"
    return "texto"


def analyze(columns, rows):
    """Perfila el dataset: tipo, faltantes, únicos y muestra por columna."""
    profile = []
    for col in columns:
        vals = [r.get(col) for r in rows]
        non_blank = [v for v in vals if not _is_blank(v)]
        col_type = _detect_type(vals)
        uniq = len({str(v) for v in non_blank})
        sample = [v for v in non_blank[:4]]
        entry = {
            "name": col,
            "type": col_type,
            "n": len(vals),
            "missing": len(vals) - len(non_blank),
            "missing_pct": round(100 * (len(vals) - len(non_blank)) / len(vals), 1) if vals else 0,
            "unique": uniq,
            "sample": sample,
        }
        if col_type == "numérico":
            nums = [_to_number(v) for v in non_blank]
            nums = [x for x in nums if x is not None]
            if nums:
                entry["min"] = min(nums)
                entry["max"] = max(nums)
                entry["mean"] = sum(nums) / len(nums)
        profile.append(entry)

    # Filas duplicadas (comparando la tupla completa)
    seen, dups = set(), 0
    for r in rows:
        key = tuple(str(r.get(c)) for c in columns)
        if key in seen:
            dups += 1
        else:
            seen.add(key)

    return {
        "n_rows": len(rows),
        "n_cols": len(columns),
        "duplicate_rows": dups,
        "columns": profile,
    }


def clean(columns, rows, options):
    """
    Aplica limpieza básica.
    options = {
      keep: [col,...],            # columnas a conservar (por defecto todas)
      coerce_numeric: bool,       # convertir columnas numéricas a float real
      trim_text: bool,            # quitar espacios en textos
      drop_duplicates: bool,
      na_policy: 'keep'|'drop_any'|'drop_all',  # filas con nulos
      types: {col: tipo}          # tipos finales elegidos por el usuario
    }
    """
    keep = options.get("keep") or list(columns)
    keep = [c for c in keep if c in columns]
    types = options.get("types") or {}
    coerce = options.get("coerce_numeric", True)
    trim = options.get("trim_text", True)
    na_policy = options.get("na_policy", "keep")
    drop_dups = options.get("drop_duplicates", False)

    report = {"rows_before": len(rows), "removed_na": 0, "removed_dup": 0,
              "coerced_cells": 0, "cols_kept": keep}

    # 1) proyectar columnas + coerción de tipos + trim
    projected = []
    for r in rows:
        new = {}
        for c in keep:
            v = r.get(c)
            t = types.get(c)
            if _is_blank(v):
                new[c] = None
                continue
            if t == "numérico" and coerce:
                num = _to_number(v)
                if num is not None:
                    if num != v:
                        report["coerced_cells"] += 1
                    new[c] = num
                else:
                    new[c] = None  # no convertible -> nulo
            elif isinstance(v, str) and trim:
                new[c] = v.strip()
            else:
                new[c] = v
        projected.append(new)

    # 2) política de nulos
    if na_policy == "drop_any":
        filtered = [r for r in projected if all(not _is_blank(r[c]) for c in keep)]
        report["removed_na"] = len(projected) - len(filtered)
        projected = filtered
    elif na_policy == "drop_all":
        filtered = [r for r in projected if any(not _is_blank(r[c]) for c in keep)]
        report["removed_na"] = len(projected) - len(filtered)
        projected = filtered

    # 3) duplicados
    if drop_dups:
        seen, out = set(), []
        for r in projected:
            key = tuple(str(r[c]) for c in keep)
            if key in seen:
                continue
            seen.add(key)
            out.append(r)
        report["removed_dup"] = len(projected) - len(out)
        projected = out

    report["rows_after"] = len(projected)
    final_cols = [{"name": c, "type": types.get(c, "texto")} for c in keep]
    return {"columns": final_cols, "rows": projected, "report": report}
