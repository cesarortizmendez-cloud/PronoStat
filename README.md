# 📊 PronoStat — Versión 1

**Laboratorio educativo de Análisis de Datos, Series de Tiempo y Pronósticos**

Desarrollado por **Dr. César Ortiz Méndez** · Ingeniería Industrial · USACH
🔗 [cv-cesarortiz.vercel.app](https://cv-cesarortiz.vercel.app)

Software hermano de **IO-Lab Pro**: misma arquitectura (Django + apps independientes +
cálculo *stateless* + Vercel + PWA), orientado ahora al **análisis de datos**.

---

## 🎯 ¿Qué es PronoStat?

Una aplicación web que guía al estudiante por un flujo completo de análisis de datos:
importar → describir → modelar → pronosticar → exportar. Cada módulo explica la teoría,
muestra el resultado paso a paso y permite exportar todo a Excel.

El conjunto de datos se carga una vez (en el módulo **Datos**) y queda disponible para
todos los demás módulos durante la sesión del navegador (arquitectura *stateless*: el
dataset vive en el cliente y cada módulo envía las columnas relevantes a su API de cálculo).

## 🗂️ Módulos de la Versión 1

| # | Módulo | Análisis | Contenido |
|---|--------|----------|-----------|
| 1 | **Datos** | Preparación | Importación Excel/CSV · selección de hoja y campos · detección de tipos · limpieza básica (nulos, duplicados, coerción) |
| 2 | **Descriptiva** | Monovariado | Media, mediana, moda, s, s², CV, cuartiles, IQR, asimetría, curtosis, IC 95% · histograma, densidad (KDE), boxplot, ECDF |
| 3 | **Regresión** | Bivariado | Ajuste lineal, exponencial, logarítmico y polinómico · R², R² ajustado, RMSE, MAE · residuos · predicción · comparación |
| 4 | **Pronósticos** | Series | Ingenuo, ingenuo estacional, promedio móvil, SES, Holt, Holt-Winters · métricas MAE/RMSE/MAPE/SMAPE/MASE · intervalos de predicción · comparación de modelos |

Las **14 funciones** de la Versión 1 quedan cubiertas, más exportación completa a Excel en cada módulo.

## 🏗️ Arquitectura (idéntica a IO-Lab Pro)

```
pronostat/
├── pronostat/               # Configuración principal de Django
│   ├── settings.py
│   ├── urls.py              # Enrutador raíz (incluye las apps + rutas PWA)
│   └── wsgi.py              # Callable `app` para Vercel
├── apps/                    # Cada módulo es una app independiente
│   ├── home/                # Catálogo / página de inicio
│   ├── datos/               # 1 · Importación y limpieza
│   │   ├── solver.py         # Lógica pura (tipos, perfilado, limpieza)
│   │   ├── views.py          # index + endpoints JSON
│   │   └── urls.py
│   ├── descriptiva/         # 2 · Estadística descriptiva
│   ├── regresion/           # 3 · Ajuste de modelos
│   ├── pronostico/          # 4 · Pronósticos
│   └── exportar/            # Exportación a Excel (openpyxl)
├── templates/
│   ├── base.html            # Layout: sidebar + topbar + footer
│   └── <app>/index.html     # Interfaz educativa de cada módulo
├── static/
│   ├── css/pronostat.css     # Sistema de diseño
│   ├── js/data-store.js      # Store de datos compartido entre módulos
│   ├── js/pwa-install.js
│   ├── manifest.json + service-worker.js + icons/   # PWA
├── requirements.txt
├── manage.py
└── vercel.json
```

### Patrón de cada módulo (tres capas)

1. **`solver.py`** — matemática pura en Python (numpy/scipy), testeable de forma aislada.
2. **`views.py`** — `index` (renderiza el template) + endpoints JSON (`fetch` desde el cliente).
3. **`templates/<app>/index.html`** — teoría + formulario + resultados + gráficos (Chart.js).

> **Nota de diseño:** los modelos de suavizamiento (SES, Holt, Holt-Winters) están
> implementados a mano con numpy + scipy (recursiones ETS clásicas con optimización de
> parámetros por mínima suma de errores al cuadrado). Esto **evita depender de
> statsmodels**, lo que mantiene el *bundle* liviano para el despliegue serverless en
> Vercel (statsmodels suele exceder el límite de tamaño).

## 🚀 Instalación local

```cmd
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py runserver
```

Abre **http://127.0.0.1:8000**. (No se usan modelos de base de datos, así que no es
necesario correr `migrate`.)

## ☁️ Despliegue en Vercel

1. Sube el proyecto a GitHub.
2. En Vercel → **Add New Project** → selecciona el repo. Detecta `vercel.json` automáticamente.
3. Variables de entorno: `SECRET_KEY` (clave larga aleatoria), `DEBUG=False`,
   `ALLOWED_HOSTS=tu-proyecto.vercel.app`.
4. **Deploy**. En 1–2 min queda en línea.

Rutas PWA para verificar tras el deploy: `/manifest.json`, `/service-worker.js`,
`/static/icons/icon-192.png`.

## ✅ Estado de las pruebas

La matemática de todos los solvers fue verificada con datos de referencia:
detección de tipos y limpieza, estadística descriptiva (incl. atípicos y KDE),
los cuatro modelos de regresión (R² y coeficientes recuperados), los seis métodos de
pronóstico (Holt-Winters recupera exactamente una serie estacional limpia) y los cuatro
exportadores a Excel.

## 🔭 Hoja de ruta

- **Versión 2 — Series avanzadas:** descomposición clásica y STL, ACF/PACF, pruebas ADF/KPSS,
  AR/MA/ARMA/ARIMA, SARIMA, validación con origen móvil, diagnóstico de residuos, selección automática.
- **Versión 3 — Plataforma profesional:** SARIMAX y variables externas, demanda intermitente,
  ensamble de modelos, pronósticos múltiples y jerárquicos, simulación y escenarios,
  informes automáticos, PWA offline avanzada.

## 📄 Autoría

Plataforma desarrollada por el **Dr. César Ortiz Méndez** para sus estudiantes de
Ingeniería Industrial en la Universidad de Santiago de Chile (USACH). Uso educativo.

---

*PronoStat v1.0 — construido con Django, numpy/scipy, JavaScript vanilla y Chart.js.*
