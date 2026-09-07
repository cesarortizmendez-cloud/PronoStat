# -*- coding: utf-8 -*-
"""
PronoStat · Módulo 4 — Ajuste de distribuciones de probabilidad continuas.

Ajusta por máxima verosimilitud (MLE) un conjunto de distribuciones continuas
a una serie de datos, aplica pruebas de bondad de ajuste con sus valores p
(Kolmogorov–Smirnov, Cramér–von Mises, chi-cuadrado) y criterios de información
(AIC/AICc/BIC), y las ordena de mejor a peor. Incluye además una batería de
pruebas de normalidad, datos para gráficos (histograma + PDF, Q–Q) y una
calculadora de probabilidades sobre la distribución ajustada.

Implementación con numpy/scipy (sin statsmodels) para caber en Vercel.
"""
import warnings
import numpy as np
from scipy import stats

# ---------------------------------------------------------------------------
# Catálogo de distribuciones continuas: (nombre scipy, etiqueta, [nombres param])
# El nº de parámetros libres = len(nombres) (incluye loc y escala).
# ---------------------------------------------------------------------------
_DISTS = [
    ('norm',        'Normal',                  ['μ (media)', 'σ (desv.)']),
    ('lognorm',     'Log-normal',              ['s (forma)', 'loc', 'escala']),
    ('expon',       'Exponencial',             ['loc', 'escala (1/λ)']),
    ('gamma',       'Gamma',                   ['α (forma)', 'loc', 'θ (escala)']),
    ('weibull_min', 'Weibull',                 ['k (forma)', 'loc', 'λ (escala)']),
    ('logistic',    'Logística',               ['μ (ubic.)', 's (escala)']),
    ('gumbel_r',    'Gumbel (valor extremo)',  ['μ (ubic.)', 'β (escala)']),
    ('triang',      'Triangular',              ['c (moda rel.)', 'a (mín.)', 'ancho']),
    ('uniform',     'Uniforme',                ['a (mín.)', 'ancho']),
    ('t',           't de Student',            ['ν (g.l.)', 'loc', 'escala']),
]
_POS_ONLY = {'lognorm', 'expon', 'gamma', 'weibull_min'}  # soporte en (0, ∞)


def _clean(values):
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    return x


def _fmt_params(name, params):
    labels = dict(_DISTS)  # no: dict of name->label; rebuild param names
    pnames = {d[0]: d[2] for d in _DISTS}[name]
    return ' · '.join(f'{pn} = {p:.4g}' for pn, p in zip(pnames, params))


def _fit_one(name, label, pnames, x, n):
    """Ajusta una distribución y calcula métricas de bondad de ajuste."""
    dist = getattr(stats, name)
    # Para distribuciones con soporte positivo, fijamos loc=0 si los datos
    # son positivos (evita ajustes inestables y es lo habitual en la práctica).
    try:
        if name in _POS_ONLY and x.min() > 0:
            params = dist.fit(x, floc=0)
        else:
            params = dist.fit(x)
    except Exception:
        params = dist.fit(x)
    params = tuple(float(p) for p in params)
    k = len(params)

    logpdf = dist.logpdf(x, *params)
    if not np.all(np.isfinite(logpdf)):
        raise ValueError('log-verosimilitud no finita')
    ll = float(np.sum(logpdf))

    aic = 2 * k - 2 * ll
    aicc = aic + (2 * k * (k + 1) / (n - k - 1)) if n - k - 1 > 0 else float('nan')
    bic = k * np.log(n) - 2 * ll

    ks_s, ks_p = _ks_gof(dist, params, x, n)
    try:
        cvm = stats.cramervonmises(x, name, args=params)
        cvm_s, cvm_p = float(cvm.statistic), float(cvm.pvalue)
    except Exception:
        cvm_s, cvm_p = float('nan'), float('nan')

    chi2_s, chi2_df, chi2_p = _chi2_gof(dist, params, x, n, k)

    return {
        'dist': name, 'label': label,
        'params': list(params),
        'params_fmt': ' · '.join(f'{pn} = {p:.4g}' for pn, p in zip(pnames, params)),
        'k': k, 'loglik': ll,
        'aic': aic, 'aicc': aicc, 'bic': bic,
        'ks_stat': ks_s, 'ks_p': ks_p,
        'cvm_stat': cvm_s, 'cvm_p': cvm_p,
        'chi2_stat': chi2_s, 'chi2_df': chi2_df, 'chi2_p': chi2_p,
    }


def _chi2_gof(dist, params, x, n, k):
    """Chi-cuadrado de bondad de ajuste con clases equiprobables."""
    m = max(5, int(np.ceil(2 * n ** 0.4)))          # nº de clases (regla práctica)
    m = min(m, max(5, n // 5))                       # ≥5 esperados por clase
    if m < 3:
        return float('nan'), 0, float('nan')
    qs = np.linspace(0, 1, m + 1)[1:-1]
    edges = dist.ppf(qs, *params)
    edges = np.concatenate(([-np.inf], edges, [np.inf]))
    obs, _ = np.histogram(x, bins=edges)
    exp = np.full(m, n / m)
    chi2 = float(np.sum((obs - exp) ** 2 / exp))
    df = max(1, m - 1 - k)
    p = float(stats.chi2.sf(chi2, df))
    return chi2, df, p


def _ks_gof(dist, params, x, n):
    """Kolmogorov–Smirnov de bondad de ajuste, calculado a mano.

    Evita stats.kstest(x, nombre, args=...), cuya firma interna cambia entre
    versiones de scipy (en algunas de Vercel lanza el error de ndtr con 3
    argumentos). Aquí se evalúa la CDF de la distribución ya ajustada.
    """
    try:
        xs = np.sort(x)
        cdf = np.asarray(dist.cdf(xs, *params), dtype=float)
        cdf = np.clip(cdf, 0.0, 1.0)
        d_plus = float(np.max(np.arange(1, n + 1) / n - cdf))
        d_minus = float(np.max(cdf - np.arange(0, n) / n))
        D = max(d_plus, d_minus)
        p = float(stats.kstwobign.sf(D * float(np.sqrt(n))))
        return D, float(min(1.0, max(0.0, p)))
    except Exception:
        return float('nan'), float('nan')


def fit_all(values, bins='auto'):
    x = _clean(values)
    n = int(x.size)
    if n < 8:
        raise ValueError('Se requieren al menos 8 datos válidos para ajustar distribuciones.')

    resultados = []
    for name, label, pnames in _DISTS:
        try:
            resultados.append(_fit_one(name, label, pnames, x, n))
        except Exception:
            continue
    if not resultados:
        raise ValueError('No fue posible ajustar ninguna distribución a estos datos.')

    resultados.sort(key=lambda r: r['aic'])
    best = resultados[0]
    for i, r in enumerate(resultados):
        r['best'] = (i == 0)
        r['delta_aic'] = r['aic'] - best['aic']

    # --- datos para gráfico: histograma (densidad) + curvas PDF ---
    nb = _nbins(x, bins)
    counts, edges = np.histogram(x, bins=nb, density=True)
    centers = (edges[:-1] + edges[1:]) / 2

    lo, hi = float(x.min()), float(x.max())
    pad = 0.05 * (hi - lo if hi > lo else 1.0)
    xs = np.linspace(lo - pad, hi + pad, 220)
    pdfs = {}
    for r in resultados:
        dist = getattr(stats, r['dist'])
        y = dist.pdf(xs, *r['params'])
        y = np.where(np.isfinite(y), y, 0.0)
        pdfs[r['label']] = [round(float(v), 6) for v in y]

    # --- Q–Q plot de la mejor distribución ---
    xs_sorted = np.sort(x)
    pp = (np.arange(1, n + 1) - 0.5) / n
    theo = getattr(stats, best['dist']).ppf(pp, *best['params'])
    finite = np.isfinite(theo)
    qq = {
        'best_label': best['label'],
        'theo': [round(float(v), 6) for v in theo[finite]],
        'sample': [round(float(v), 6) for v in xs_sorted[finite]],
    }
    tmin = float(np.nanmin(theo[finite])); tmax = float(np.nanmax(theo[finite]))
    qq['line'] = [[tmin, tmin], [tmax, tmax]]

    resumen = _resumen(x, n)
    return {
        'n': n,
        'resumen': resumen,
        'ranking': resultados,
        'mejor': best['label'],
        'chart': {
            'x': [round(float(v), 6) for v in xs],
            'hist': {
                'centers': [round(float(v), 6) for v in centers],
                'density': [round(float(v), 6) for v in counts],
                'width': float(edges[1] - edges[0]),
            },
            'pdfs': pdfs,
        },
        'qq': qq,
        'interpretacion': _interp(resultados, resumen, n),
    }


def _nbins(x, bins):
    n = x.size
    if isinstance(bins, (int, float)) and not isinstance(bins, bool):
        return max(3, int(bins))
    return max(5, min(40, int(np.ceil(np.log2(n) + 1))))  # Sturges


def _resumen(x, n):
    return {
        'media': float(np.mean(x)),
        'desv': float(np.std(x, ddof=1)),
        'min': float(np.min(x)), 'max': float(np.max(x)),
        'asimetria': float(stats.skew(x)),
        'curtosis': float(stats.kurtosis(x)),  # exceso (0 ≈ normal)
    }


def _interp(ranking, resumen, n):
    out = []
    best = ranking[0]
    out.append(f'La distribución que mejor ajusta (menor AIC) es la '
               f'<b>{best["label"]}</b>, con parámetros {best["params_fmt"]}.')
    ks_ok = (best['ks_p'] >= 0.05)
    out.append(
        f'Prueba de Kolmogorov–Smirnov: p = {best["ks_p"]:.3f} → '
        + ('<b>no se rechaza</b> el ajuste: los datos son compatibles con la '
           f'distribución {best["label"]} (p ≥ 0,05).'
           if ks_ok else
           '<b>se rechaza</b> el ajuste (p &lt; 0,05): esta distribución no describe '
           'bien los datos, aunque sea la mejor del conjunto.'))
    if len(ranking) > 1:
        seg = ranking[1]
        out.append(f'La segunda mejor es la <b>{seg["label"]}</b> (ΔAIC = '
                   f'{seg["delta_aic"]:.1f}). Una ΔAIC &lt; 2 indica que ambas son '
                   'prácticamente equivalentes; &gt; 10, que la segunda es claramente peor.')
    a = resumen['asimetria']
    forma = ('aproximadamente simétrica' if abs(a) < 0.5 else
             ('con asimetría positiva (cola a la derecha)' if a > 0 else
              'con asimetría negativa (cola a la izquierda)'))
    out.append(f'Los datos son {forma} (asimetría = {a:.2f}) y su curtosis en '
               f'exceso es {resumen["curtosis"]:.2f} (0 ≈ normal).')
    out.append('Nota educativa: los valores p de KS/CvM son aproximados cuando los '
               'parámetros se estiman de los mismos datos; úsalos junto al AIC y a la '
               'inspección visual del histograma y del gráfico Q–Q.')
    return out


# ---------------------------------------------------------------------------
# Batería de pruebas de normalidad
# ---------------------------------------------------------------------------
def normalidad(values):
    x = _clean(values)
    n = int(x.size)
    if n < 8:
        raise ValueError('Se requieren al menos 8 datos válidos.')
    mu = float(np.mean(x)); sd = float(np.std(x, ddof=1))
    pruebas = []

    # Cada prueba va en su propio try/except: si una falla (p. ej. por diferencias
    # entre versiones de scipy), las demás se calculan igual. KS y Jarque-Bera se
    # calculan a mano con primitivas estables, evitando firmas que cambian de versión.
    if 3 <= n <= 5000:
        try:
            r = stats.shapiro(x)
            pruebas.append(_pt('Shapiro–Wilk', float(r.statistic), float(r.pvalue), 'W'))
        except Exception:
            pass
    try:
        r = stats.normaltest(x)
        pruebas.append(_pt("D'Agostino–Pearson (K²)", float(r.statistic), float(r.pvalue), 'K²'))
    except Exception:
        pass
    try:                                                # Jarque–Bera (cálculo directo)
        S = float(stats.skew(x)); Kx = float(stats.kurtosis(x))     # curtosis en exceso
        jb = n / 6.0 * (S ** 2 + (Kx ** 2) / 4.0)
        pruebas.append(_pt('Jarque–Bera', float(jb), float(stats.chi2.sf(jb, 2)), 'JB'))
    except Exception:
        pass
    try:                                                # Kolmogorov–Smirnov vs normal (manual)
        if sd > 0:
            xs = np.sort(x)
            cdf = stats.norm.cdf((xs - mu) / sd)
            d_plus = float(np.max(np.arange(1, n + 1) / n - cdf))
            d_minus = float(np.max(cdf - np.arange(0, n) / n))
            D = max(d_plus, d_minus)
            pks = float(stats.kstwobign.sf(D * float(np.sqrt(n))))
            pruebas.append(_pt('Kolmogorov–Smirnov', D, float(min(1.0, max(0.0, pks))), 'D'))
    except Exception:
        pass

    # Anderson–Darling (usa valores críticos, no p directo). Defensivo ante
    # cambios de API entre versiones de scipy.
    anderson = None
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            ad = stats.anderson(x, dist='norm')
        sl = list(ad.significance_level)
        idx = sl.index(5.0) if 5.0 in sl else 2
        ad_crit = float(ad.critical_values[idx])
        ad_rechaza = float(ad.statistic) > ad_crit
        anderson = {
            'stat': float(ad.statistic), 'critico_5': ad_crit,
            'rechaza': bool(ad_rechaza),
            'texto': ('A² = %.3f > %.3f (crítico 5%%) → se rechaza normalidad'
                      % (ad.statistic, ad_crit)) if ad_rechaza else
                     ('A² = %.3f ≤ %.3f (crítico 5%%) → no se rechaza normalidad'
                      % (ad.statistic, ad_crit)),
        }
    except Exception:
        anderson = None

    ad_rechaza = bool(anderson and anderson['rechaza'])
    n_rechazos = sum(1 for t in pruebas if t['p'] < 0.05) + (1 if ad_rechaza else 0)
    total = len(pruebas) + (1 if anderson else 0)
    if total == 0:
        return {'n': n, 'pruebas': [], 'anderson': None,
                'skew': float(stats.skew(x)), 'kurt': float(stats.kurtosis(x)), 'normal': None,
                'veredicto': 'No se pudo calcular ninguna prueba de normalidad en este entorno; '
                             'usa el histograma y el gráfico Q–Q para evaluar la normalidad visualmente.'}
    normal = n_rechazos == 0
    veredicto = ('Todas las pruebas son compatibles con normalidad (ningún p &lt; 0,05): '
                 'es razonable asumir que los datos provienen de una distribución normal.'
                 if normal else
                 f'{n_rechazos} de {total} pruebas rechazan la normalidad (p &lt; 0,05): '
                 'los datos probablemente <b>no</b> son normales; revisa el histograma, el '
                 'Q–Q y considera otra distribución del ranking.')

    return {
        'n': n, 'pruebas': pruebas, 'anderson': anderson,
        'skew': float(stats.skew(x)), 'kurt': float(stats.kurtosis(x)),
        'normal': normal, 'veredicto': veredicto,
    }


def _pt(nombre, stat, p, simbolo):
    return {'nombre': nombre, 'stat': stat, 'p': p, 'simbolo': simbolo,
            'rechaza': bool(p < 0.05)}


# ---------------------------------------------------------------------------
# Calculadora de probabilidades sobre una distribución ajustada
# ---------------------------------------------------------------------------
def prob_calc(dist, params, modo, a=None, b=None, p=None):
    d = getattr(stats, dist)
    par = tuple(float(v) for v in params)
    res = {'dist': dist, 'modo': modo}
    if modo == 'menor':          # P(X < a)
        res['prob'] = float(d.cdf(float(a), *par)); res['expr'] = f'P(X < {a})'
    elif modo == 'mayor':        # P(X > a)
        res['prob'] = float(d.sf(float(a), *par)); res['expr'] = f'P(X > {a})'
    elif modo == 'entre':        # P(a < X < b)
        lo, hi = sorted([float(a), float(b)])
        res['prob'] = float(d.cdf(hi, *par) - d.cdf(lo, *par))
        res['expr'] = f'P({lo} < X < {hi})'
    elif modo == 'cuantil':      # x tal que P(X < x) = p
        res['x'] = float(d.ppf(float(p), *par)); res['expr'] = f'x tal que P(X < x) = {p}'
        res['prob'] = float(p)
    else:
        raise ValueError('modo inválido')
    return res


# ---------------------------------------------------------------------------
# Análisis de los errores (residuos) del ajuste de una distribución
# ---------------------------------------------------------------------------
def residuos(values, dist, params):
    """Analiza los residuos del ajuste de una distribución seleccionada.

    Definición educativa de residuo: diferencia entre la frecuencia acumulada
    EMPÍRICA de cada dato (posición de graficación de Hazen, (i-0,5)/n) y la
    frecuencia acumulada TEÓRICA que predice la distribución ajustada,
    e_i = F_emp(x_(i)) − F_teo(x_(i)). Es la misma cantidad que mide la prueba
    de Kolmogorov–Smirnov; si el ajuste es bueno, los residuos son pequeños y
    se reparten alrededor de cero sin patrón.
    """
    x = _clean(values)
    n = int(x.size)
    if n < 8:
        raise ValueError('Se requieren al menos 8 datos válidos.')

    label = {d[0]: d[1] for d in _DISTS}.get(dist, dist)
    d = getattr(stats, dist)
    par = tuple(float(v) for v in params)

    xs = np.sort(x)
    F_emp = (np.arange(1, n + 1) - 0.5) / n            # posición de Hazen
    F_teo = np.asarray(d.cdf(xs, *par), dtype=float)
    F_teo = np.clip(F_teo, 0.0, 1.0)
    e = F_emp - F_teo                                  # residuos (P–P)

    # KS a partir de los mismos residuos (coherente con el ranking)
    D_plus = float(np.max(np.arange(1, n + 1) / n - F_teo))
    D_minus = float(np.max(F_teo - np.arange(0, n) / n))
    D = max(D_plus, D_minus)
    ks_p = float(min(1.0, max(0.0, stats.kstwobign.sf(D * float(np.sqrt(n))))))

    media = float(np.mean(e))
    desv = float(np.std(e, ddof=1)) if n > 1 else 0.0
    max_abs = float(np.max(np.abs(e)))
    rmse = float(np.sqrt(np.mean(e ** 2)))
    sesgo = float(stats.skew(e)) if desv > 0 else 0.0

    # histograma de los residuos
    nb = max(5, min(30, int(np.ceil(np.log2(n) + 1))))
    counts, edges = np.histogram(e, bins=nb)
    centers = (edges[:-1] + edges[1:]) / 2

    # residuo en función del valor (para detectar patrones sistemáticos)
    resid_xy = {
        'x': [round(float(v), 6) for v in xs],
        'e': [round(float(v), 6) for v in e],
    }
    # P–P: teórica (eje x) vs empírica (eje y), con recta de 45°
    pp = {
        'teo': [round(float(v), 6) for v in F_teo],
        'emp': [round(float(v), 6) for v in F_emp],
        'line': [[0.0, 0.0], [1.0, 1.0]],
    }

    interp = []
    interp.append(f'Se analizan los residuos del ajuste de la distribución '
                  f'<b>{label}</b>. Cada residuo es la distancia vertical entre la '
                  'frecuencia acumulada observada y la que predice el modelo.')
    signo = 'ligeramente positivo' if media > 1e-4 else (
            'ligeramente negativo' if media < -1e-4 else 'prácticamente nulo')
    interp.append(f'La media de los residuos es {media:.4f} ({signo}) y su desviación '
                  f'estándar {desv:.4f}. Una media cercana a 0 indica que el modelo no '
                  'sobre- ni subestima sistemáticamente la acumulación de probabilidad.')
    interp.append(f'El mayor residuo en valor absoluto es {max_abs:.4f}; coincide con el '
                  f'estadístico D de Kolmogorov–Smirnov (D = {D:.4f}, p = {ks_p:.3f}). '
                  + ('Como p ≥ 0,05, no hay evidencia para rechazar el ajuste.'
                     if ks_p >= 0.05 else
                     'Como p &lt; 0,05, el ajuste se rechaza: revisa el patrón de residuos '
                     'y prueba otra distribución del ranking.'))
    interp.append(f'La raíz del error cuadrático medio (RMSE) de los residuos es {rmse:.4f}. '
                  'En el gráfico de residuos frente al valor, una nube sin tendencia (banda '
                  'horizontal alrededor de 0) confirma un buen ajuste; una curva en “U” o en '
                  '“S” señala que la forma de la distribución no es la adecuada.')
    forma_h = ('aproximadamente simétrico' if abs(sesgo) < 0.5 else
               ('con cola a la derecha' if sesgo > 0 else 'con cola a la izquierda'))
    interp.append(f'El histograma de los residuos es {forma_h} (asimetría = {sesgo:.2f}); '
                  'idealmente debería concentrarse cerca de 0 y ser aproximadamente simétrico.')

    return {
        'dist': dist, 'label': label, 'n': n,
        'pp': pp,
        'resid': resid_xy,
        'hist': {
            'centers': [round(float(v), 6) for v in centers],
            'counts': [int(c) for c in counts],
            'width': float(edges[1] - edges[0]),
        },
        'stats': {
            'media': media, 'desv': desv, 'max_abs': max_abs,
            'rmse': rmse, 'sesgo': sesgo, 'ks_D': D, 'ks_p': ks_p,
        },
        'interpretacion': interp,
    }
