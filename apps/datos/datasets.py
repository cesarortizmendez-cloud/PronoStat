"""
Catálogo de datasets de ejemplo de PronoStat (generado automáticamente).

Datos ILUSTRATIVOS con fines educativos, calibrados a órdenes de magnitud reales de
Chile por rubro (Cochilco, Subturismo/Sernatur, CNE/Coordinador Eléctrico, SII/BCCh).
No son cifras oficiales. Regenerar con scripts_gen/generar_datasets.py.
"""

DATASETS = [
 {
  "id": "supermercado",
  "nombre": "Ventas de supermercado",
  "sector": "Retail",
  "periodo": "mensual",
  "m": 12,
  "caracteristicas": [
   "tendencia",
   "estacionalidad",
   "ruido",
   "multivariado"
  ],
  "descripcion": "Ventas mensuales (CLP millones) con alza sostenida y estacionalidad marcada (peak de diciembre y marzo escolar). Incluye gasto en publicidad, ticket promedio y temperatura: ideal para Holt-Winters, regresión (publicidad→ventas) y descriptiva.",
  "columns": [
   {
    "name": "periodo",
    "type": "fecha"
   },
   {
    "name": "ventas_mm",
    "type": "numérico"
   },
   {
    "name": "gasto_pub_mm",
    "type": "numérico"
   },
   {
    "name": "ticket_prom_clp",
    "type": "numérico"
   },
   {
    "name": "temp_media_c",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "periodo": "2021-01",
    "ventas_mm": 1672.0,
    "gasto_pub_mm": 85.1,
    "ticket_prom_clp": 18149,
    "temp_media_c": 27.7
   },
   {
    "periodo": "2021-02",
    "ventas_mm": 1657.2,
    "gasto_pub_mm": 91.77,
    "ticket_prom_clp": 17902,
    "temp_media_c": 26.0
   },
   {
    "periodo": "2021-03",
    "ventas_mm": 2020.9,
    "gasto_pub_mm": 111.82,
    "ticket_prom_clp": 17981,
    "temp_media_c": 22.3
   },
   {
    "periodo": "2021-04",
    "ventas_mm": 1823.7,
    "gasto_pub_mm": 101.46,
    "ticket_prom_clp": 17724,
    "temp_media_c": 17.4
   },
   {
    "periodo": "2021-05",
    "ventas_mm": 1778.9,
    "gasto_pub_mm": 98.99,
    "ticket_prom_clp": 17560,
    "temp_media_c": 12.9
   },
   {
    "periodo": "2021-06",
    "ventas_mm": 1856.8,
    "gasto_pub_mm": 101.26,
    "ticket_prom_clp": 17893,
    "temp_media_c": 9.3
   },
   {
    "periodo": "2021-07",
    "ventas_mm": 1943.9,
    "gasto_pub_mm": 99.36,
    "ticket_prom_clp": 18293,
    "temp_media_c": 8.8
   },
   {
    "periodo": "2021-08",
    "ventas_mm": 1798.8,
    "gasto_pub_mm": 95.27,
    "ticket_prom_clp": 18320,
    "temp_media_c": 9.0
   },
   {
    "periodo": "2021-09",
    "ventas_mm": 2030.7,
    "gasto_pub_mm": 101.0,
    "ticket_prom_clp": 18179,
    "temp_media_c": 13.3
   },
   {
    "periodo": "2021-10",
    "ventas_mm": 1890.7,
    "gasto_pub_mm": 107.88,
    "ticket_prom_clp": 18253,
    "temp_media_c": 17.2
   },
   {
    "periodo": "2021-11",
    "ventas_mm": 2090.9,
    "gasto_pub_mm": 104.73,
    "ticket_prom_clp": 18421,
    "temp_media_c": 22.1
   },
   {
    "periodo": "2021-12",
    "ventas_mm": 2606.3,
    "gasto_pub_mm": 142.94,
    "ticket_prom_clp": 17882,
    "temp_media_c": 26.7
   },
   {
    "periodo": "2022-01",
    "ventas_mm": 1942.5,
    "gasto_pub_mm": 111.68,
    "ticket_prom_clp": 18319,
    "temp_media_c": 29.7
   },
   {
    "periodo": "2022-02",
    "ventas_mm": 1693.2,
    "gasto_pub_mm": 96.48,
    "ticket_prom_clp": 18133,
    "temp_media_c": 26.9
   },
   {
    "periodo": "2022-03",
    "ventas_mm": 2139.6,
    "gasto_pub_mm": 122.33,
    "ticket_prom_clp": 18025,
    "temp_media_c": 22.7
   },
   {
    "periodo": "2022-04",
    "ventas_mm": 1881.6,
    "gasto_pub_mm": 100.24,
    "ticket_prom_clp": 17832,
    "temp_media_c": 16.8
   },
   {
    "periodo": "2022-05",
    "ventas_mm": 1856.4,
    "gasto_pub_mm": 101.88,
    "ticket_prom_clp": 18280,
    "temp_media_c": 13.4
   },
   {
    "periodo": "2022-06",
    "ventas_mm": 1924.2,
    "gasto_pub_mm": 97.35,
    "ticket_prom_clp": 18067,
    "temp_media_c": 9.0
   },
   {
    "periodo": "2022-07",
    "ventas_mm": 2148.4,
    "gasto_pub_mm": 117.23,
    "ticket_prom_clp": 18382,
    "temp_media_c": 7.1
   },
   {
    "periodo": "2022-08",
    "ventas_mm": 1962.6,
    "gasto_pub_mm": 116.78,
    "ticket_prom_clp": 18250,
    "temp_media_c": 8.4
   },
   {
    "periodo": "2022-09",
    "ventas_mm": 2188.6,
    "gasto_pub_mm": 113.21,
    "ticket_prom_clp": 18436,
    "temp_media_c": 12.0
   },
   {
    "periodo": "2022-10",
    "ventas_mm": 2050.0,
    "gasto_pub_mm": 106.3,
    "ticket_prom_clp": 18297,
    "temp_media_c": 16.6
   },
   {
    "periodo": "2022-11",
    "ventas_mm": 2145.3,
    "gasto_pub_mm": 120.59,
    "ticket_prom_clp": 17883,
    "temp_media_c": 23.0
   },
   {
    "periodo": "2022-12",
    "ventas_mm": 2572.5,
    "gasto_pub_mm": 134.51,
    "ticket_prom_clp": 18906,
    "temp_media_c": 25.3
   },
   {
    "periodo": "2023-01",
    "ventas_mm": 1894.7,
    "gasto_pub_mm": 100.69,
    "ticket_prom_clp": 18162,
    "temp_media_c": 27.7
   },
   {
    "periodo": "2023-02",
    "ventas_mm": 1722.6,
    "gasto_pub_mm": 110.64,
    "ticket_prom_clp": 18361,
    "temp_media_c": 26.1
   },
   {
    "periodo": "2023-03",
    "ventas_mm": 2367.2,
    "gasto_pub_mm": 119.66,
    "ticket_prom_clp": 18605,
    "temp_media_c": 22.6
   },
   {
    "periodo": "2023-04",
    "ventas_mm": 2070.9,
    "gasto_pub_mm": 106.96,
    "ticket_prom_clp": 17930,
    "temp_media_c": 18.3
   },
   {
    "periodo": "2023-05",
    "ventas_mm": 2017.4,
    "gasto_pub_mm": 111.32,
    "ticket_prom_clp": 18944,
    "temp_media_c": 12.1
   },
   {
    "periodo": "2023-06",
    "ventas_mm": 2037.3,
    "gasto_pub_mm": 121.23,
    "ticket_prom_clp": 18669,
    "temp_media_c": 9.4
   },
   {
    "periodo": "2023-07",
    "ventas_mm": 2198.9,
    "gasto_pub_mm": 111.16,
    "ticket_prom_clp": 18840,
    "temp_media_c": 7.2
   },
   {
    "periodo": "2023-08",
    "ventas_mm": 2120.9,
    "gasto_pub_mm": 115.8,
    "ticket_prom_clp": 19012,
    "temp_media_c": 9.8
   },
   {
    "periodo": "2023-09",
    "ventas_mm": 2195.8,
    "gasto_pub_mm": 104.43,
    "ticket_prom_clp": 18357,
    "temp_media_c": 11.8
   },
   {
    "periodo": "2023-10",
    "ventas_mm": 2188.0,
    "gasto_pub_mm": 113.55,
    "ticket_prom_clp": 19185,
    "temp_media_c": 16.5
   },
   {
    "periodo": "2023-11",
    "ventas_mm": 2371.5,
    "gasto_pub_mm": 115.48,
    "ticket_prom_clp": 18069,
    "temp_media_c": 23.8
   },
   {
    "periodo": "2023-12",
    "ventas_mm": 2976.5,
    "gasto_pub_mm": 141.52,
    "ticket_prom_clp": 18764,
    "temp_media_c": 25.2
   },
   {
    "periodo": "2024-01",
    "ventas_mm": 1964.2,
    "gasto_pub_mm": 123.85,
    "ticket_prom_clp": 18874,
    "temp_media_c": 28.6
   },
   {
    "periodo": "2024-02",
    "ventas_mm": 1918.1,
    "gasto_pub_mm": 103.02,
    "ticket_prom_clp": 18702,
    "temp_media_c": 26.3
   },
   {
    "periodo": "2024-03",
    "ventas_mm": 2392.0,
    "gasto_pub_mm": 132.73,
    "ticket_prom_clp": 18431,
    "temp_media_c": 21.9
   },
   {
    "periodo": "2024-04",
    "ventas_mm": 2123.7,
    "gasto_pub_mm": 121.83,
    "ticket_prom_clp": 19000,
    "temp_media_c": 15.9
   },
   {
    "periodo": "2024-05",
    "ventas_mm": 2153.6,
    "gasto_pub_mm": 123.99,
    "ticket_prom_clp": 18605,
    "temp_media_c": 14.5
   },
   {
    "periodo": "2024-06",
    "ventas_mm": 2377.4,
    "gasto_pub_mm": 126.44,
    "ticket_prom_clp": 19052,
    "temp_media_c": 8.2
   },
   {
    "periodo": "2024-07",
    "ventas_mm": 2188.1,
    "gasto_pub_mm": 124.54,
    "ticket_prom_clp": 19035,
    "temp_media_c": 8.5
   },
   {
    "periodo": "2024-08",
    "ventas_mm": 2145.6,
    "gasto_pub_mm": 114.07,
    "ticket_prom_clp": 18473,
    "temp_media_c": 9.8
   },
   {
    "periodo": "2024-09",
    "ventas_mm": 2420.6,
    "gasto_pub_mm": 125.45,
    "ticket_prom_clp": 19425,
    "temp_media_c": 12.2
   },
   {
    "periodo": "2024-10",
    "ventas_mm": 2320.7,
    "gasto_pub_mm": 130.61,
    "ticket_prom_clp": 18788,
    "temp_media_c": 17.9
   },
   {
    "periodo": "2024-11",
    "ventas_mm": 2486.8,
    "gasto_pub_mm": 134.93,
    "ticket_prom_clp": 18945,
    "temp_media_c": 23.3
   },
   {
    "periodo": "2024-12",
    "ventas_mm": 2686.2,
    "gasto_pub_mm": 148.96,
    "ticket_prom_clp": 18930,
    "temp_media_c": 26.6
   }
  ]
 },
 {
  "id": "cobre",
  "nombre": "Producción y precio del cobre",
  "sector": "Minería",
  "periodo": "mensual",
  "m": 12,
  "caracteristicas": [
   "ciclo",
   "tendencia",
   "ruido",
   "multivariado"
  ],
  "descripcion": "Producción nacional de cobre (miles de toneladas/mes, ~450 kton) y precio (US$/lb, ~4,2). Muestra un componente cíclico plurianual ligado al precio; útil para estudiar ciclo vs. estacionalidad y regresión precio→producción.",
  "columns": [
   {
    "name": "periodo",
    "type": "fecha"
   },
   {
    "name": "produccion_kton",
    "type": "numérico"
   },
   {
    "name": "precio_usd_lb",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "periodo": "2021-01",
    "produccion_kton": 441.3,
    "precio_usd_lb": 4.482
   },
   {
    "periodo": "2021-02",
    "produccion_kton": 446.5,
    "precio_usd_lb": 4.429
   },
   {
    "periodo": "2021-03",
    "produccion_kton": 445.9,
    "precio_usd_lb": 4.648
   },
   {
    "periodo": "2021-04",
    "produccion_kton": 465.2,
    "precio_usd_lb": 4.679
   },
   {
    "periodo": "2021-05",
    "produccion_kton": 470.8,
    "precio_usd_lb": 4.728
   },
   {
    "periodo": "2021-06",
    "produccion_kton": 464.1,
    "precio_usd_lb": 4.711
   },
   {
    "periodo": "2021-07",
    "produccion_kton": 464.4,
    "precio_usd_lb": 4.752
   },
   {
    "periodo": "2021-08",
    "produccion_kton": 473.7,
    "precio_usd_lb": 4.697
   },
   {
    "periodo": "2021-09",
    "produccion_kton": 486.0,
    "precio_usd_lb": 4.577
   },
   {
    "periodo": "2021-10",
    "produccion_kton": 475.6,
    "precio_usd_lb": 4.515
   },
   {
    "periodo": "2021-11",
    "produccion_kton": 487.6,
    "precio_usd_lb": 4.302
   },
   {
    "periodo": "2021-12",
    "produccion_kton": 478.2,
    "precio_usd_lb": 4.285
   },
   {
    "periodo": "2022-01",
    "produccion_kton": 454.6,
    "precio_usd_lb": 4.116
   },
   {
    "periodo": "2022-02",
    "produccion_kton": 447.7,
    "precio_usd_lb": 3.963
   },
   {
    "periodo": "2022-03",
    "produccion_kton": 452.9,
    "precio_usd_lb": 3.891
   },
   {
    "periodo": "2022-04",
    "produccion_kton": 457.4,
    "precio_usd_lb": 3.796
   },
   {
    "periodo": "2022-05",
    "produccion_kton": 460.9,
    "precio_usd_lb": 3.737
   },
   {
    "periodo": "2022-06",
    "produccion_kton": 436.7,
    "precio_usd_lb": 3.624
   },
   {
    "periodo": "2022-07",
    "produccion_kton": 423.8,
    "precio_usd_lb": 3.616
   },
   {
    "periodo": "2022-08",
    "produccion_kton": 440.0,
    "precio_usd_lb": 3.735
   },
   {
    "periodo": "2022-09",
    "produccion_kton": 450.6,
    "precio_usd_lb": 3.72
   },
   {
    "periodo": "2022-10",
    "produccion_kton": 451.0,
    "precio_usd_lb": 3.525
   },
   {
    "periodo": "2022-11",
    "produccion_kton": 435.3,
    "precio_usd_lb": 3.727
   },
   {
    "periodo": "2022-12",
    "produccion_kton": 431.0,
    "precio_usd_lb": 3.901
   },
   {
    "periodo": "2023-01",
    "produccion_kton": 433.3,
    "precio_usd_lb": 3.893
   },
   {
    "periodo": "2023-02",
    "produccion_kton": 421.3,
    "precio_usd_lb": 3.822
   },
   {
    "periodo": "2023-03",
    "produccion_kton": 415.1,
    "precio_usd_lb": 4.076
   },
   {
    "periodo": "2023-04",
    "produccion_kton": 425.3,
    "precio_usd_lb": 4.028
   },
   {
    "periodo": "2023-05",
    "produccion_kton": 427.1,
    "precio_usd_lb": 4.278
   },
   {
    "periodo": "2023-06",
    "produccion_kton": 430.6,
    "precio_usd_lb": 4.351
   },
   {
    "periodo": "2023-07",
    "produccion_kton": 420.0,
    "precio_usd_lb": 4.461
   },
   {
    "periodo": "2023-08",
    "produccion_kton": 441.5,
    "precio_usd_lb": 4.455
   },
   {
    "periodo": "2023-09",
    "produccion_kton": 452.6,
    "precio_usd_lb": 4.794
   },
   {
    "periodo": "2023-10",
    "produccion_kton": 458.1,
    "precio_usd_lb": 4.552
   },
   {
    "periodo": "2023-11",
    "produccion_kton": 457.4,
    "precio_usd_lb": 4.554
   },
   {
    "periodo": "2023-12",
    "produccion_kton": 445.4,
    "precio_usd_lb": 4.751
   },
   {
    "periodo": "2024-01",
    "produccion_kton": 454.5,
    "precio_usd_lb": 4.623
   },
   {
    "periodo": "2024-02",
    "produccion_kton": 444.2,
    "precio_usd_lb": 4.532
   },
   {
    "periodo": "2024-03",
    "produccion_kton": 479.3,
    "precio_usd_lb": 4.572
   },
   {
    "periodo": "2024-04",
    "produccion_kton": 488.3,
    "precio_usd_lb": 4.608
   },
   {
    "periodo": "2024-05",
    "produccion_kton": 481.6,
    "precio_usd_lb": 4.425
   },
   {
    "periodo": "2024-06",
    "produccion_kton": 476.0,
    "precio_usd_lb": 4.24
   },
   {
    "periodo": "2024-07",
    "produccion_kton": 471.4,
    "precio_usd_lb": 4.242
   },
   {
    "periodo": "2024-08",
    "produccion_kton": 478.6,
    "precio_usd_lb": 4.142
   },
   {
    "periodo": "2024-09",
    "produccion_kton": 502.3,
    "precio_usd_lb": 3.943
   },
   {
    "periodo": "2024-10",
    "produccion_kton": 488.6,
    "precio_usd_lb": 3.727
   },
   {
    "periodo": "2024-11",
    "produccion_kton": 506.3,
    "precio_usd_lb": 3.83
   },
   {
    "periodo": "2024-12",
    "produccion_kton": 481.6,
    "precio_usd_lb": 3.686
   },
   {
    "periodo": "2025-01",
    "produccion_kton": 465.7,
    "precio_usd_lb": 3.58
   },
   {
    "periodo": "2025-02",
    "produccion_kton": 464.3,
    "precio_usd_lb": 3.531
   },
   {
    "periodo": "2025-03",
    "produccion_kton": 470.6,
    "precio_usd_lb": 3.547
   },
   {
    "periodo": "2025-04",
    "produccion_kton": 469.0,
    "precio_usd_lb": 3.613
   },
   {
    "periodo": "2025-05",
    "produccion_kton": 457.9,
    "precio_usd_lb": 3.903
   },
   {
    "periodo": "2025-06",
    "produccion_kton": 448.5,
    "precio_usd_lb": 3.752
   },
   {
    "periodo": "2025-07",
    "produccion_kton": 432.7,
    "precio_usd_lb": 3.731
   },
   {
    "periodo": "2025-08",
    "produccion_kton": 451.1,
    "precio_usd_lb": 4.04
   },
   {
    "periodo": "2025-09",
    "produccion_kton": 438.6,
    "precio_usd_lb": 4.155
   },
   {
    "periodo": "2025-10",
    "produccion_kton": 434.4,
    "precio_usd_lb": 3.993
   },
   {
    "periodo": "2025-11",
    "produccion_kton": 428.0,
    "precio_usd_lb": 4.165
   },
   {
    "periodo": "2025-12",
    "produccion_kton": 430.5,
    "precio_usd_lb": 4.41
   }
  ]
 },
 {
  "id": "turismo",
  "nombre": "Llegada de turistas extranjeros",
  "sector": "Turismo",
  "periodo": "mensual",
  "m": 12,
  "caracteristicas": [
   "estacionalidad fuerte",
   "tendencia",
   "ciclo",
   "shock"
  ],
  "descripcion": "Llegadas mensuales de turistas (miles), con peak de verano austral (enero–febrero) y valle invernal. Incluye un shock (caída y recuperación) para practicar el manejo de eventos atípicos y quiebres.",
  "columns": [
   {
    "name": "periodo",
    "type": "fecha"
   },
   {
    "name": "turistas_miles",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "periodo": "2019-01",
    "turistas_miles": 781.9
   },
   {
    "periodo": "2019-02",
    "turistas_miles": 610.4
   },
   {
    "periodo": "2019-03",
    "turistas_miles": 422.4
   },
   {
    "periodo": "2019-04",
    "turistas_miles": 276.6
   },
   {
    "periodo": "2019-05",
    "turistas_miles": 203.5
   },
   {
    "periodo": "2019-06",
    "turistas_miles": 207.5
   },
   {
    "periodo": "2019-07",
    "turistas_miles": 362.8
   },
   {
    "periodo": "2019-08",
    "turistas_miles": 255.3
   },
   {
    "periodo": "2019-09",
    "turistas_miles": 392.1
   },
   {
    "periodo": "2019-10",
    "turistas_miles": 417.1
   },
   {
    "periodo": "2019-11",
    "turistas_miles": 503.3
   },
   {
    "periodo": "2019-12",
    "turistas_miles": 584.4
   },
   {
    "periodo": "2020-01",
    "turistas_miles": 903.1
   },
   {
    "periodo": "2020-02",
    "turistas_miles": 677.8
   },
   {
    "periodo": "2020-03",
    "turistas_miles": 442.0
   },
   {
    "periodo": "2020-04",
    "turistas_miles": 317.8
   },
   {
    "periodo": "2020-05",
    "turistas_miles": 231.1
   },
   {
    "periodo": "2020-06",
    "turistas_miles": 248.5
   },
   {
    "periodo": "2020-07",
    "turistas_miles": 377.0
   },
   {
    "periodo": "2020-08",
    "turistas_miles": 299.4
   },
   {
    "periodo": "2020-09",
    "turistas_miles": 461.2
   },
   {
    "periodo": "2020-10",
    "turistas_miles": 440.3
   },
   {
    "periodo": "2020-11",
    "turistas_miles": 515.9
   },
   {
    "periodo": "2020-12",
    "turistas_miles": 650.8
   },
   {
    "periodo": "2021-01",
    "turistas_miles": 1050.5
   },
   {
    "periodo": "2021-02",
    "turistas_miles": 736.8
   },
   {
    "periodo": "2021-03",
    "turistas_miles": 89.9
   },
   {
    "periodo": "2021-04",
    "turistas_miles": 54.5
   },
   {
    "periodo": "2021-05",
    "turistas_miles": 46.3
   },
   {
    "periodo": "2021-06",
    "turistas_miles": 46.4
   },
   {
    "periodo": "2021-07",
    "turistas_miles": 78.5
   },
   {
    "periodo": "2021-08",
    "turistas_miles": 59.3
   },
   {
    "periodo": "2021-09",
    "turistas_miles": 88.2
   },
   {
    "periodo": "2021-10",
    "turistas_miles": 91.2
   },
   {
    "periodo": "2021-11",
    "turistas_miles": 158.6
   },
   {
    "periodo": "2021-12",
    "turistas_miles": 235.1
   },
   {
    "periodo": "2022-01",
    "turistas_miles": 390.8
   },
   {
    "periodo": "2022-02",
    "turistas_miles": 408.9
   },
   {
    "periodo": "2022-03",
    "turistas_miles": 289.1
   },
   {
    "periodo": "2022-04",
    "turistas_miles": 253.5
   },
   {
    "periodo": "2022-05",
    "turistas_miles": 212.9
   },
   {
    "periodo": "2022-06",
    "turistas_miles": 217.8
   },
   {
    "periodo": "2022-07",
    "turistas_miles": 403.1
   },
   {
    "periodo": "2022-08",
    "turistas_miles": 346.0
   },
   {
    "periodo": "2022-09",
    "turistas_miles": 498.9
   },
   {
    "periodo": "2022-10",
    "turistas_miles": 565.9
   },
   {
    "periodo": "2022-11",
    "turistas_miles": 666.3
   },
   {
    "periodo": "2022-12",
    "turistas_miles": 757.1
   },
   {
    "periodo": "2023-01",
    "turistas_miles": 1335.7
   },
   {
    "periodo": "2023-02",
    "turistas_miles": 877.9
   },
   {
    "periodo": "2023-03",
    "turistas_miles": 592.5
   },
   {
    "periodo": "2023-04",
    "turistas_miles": 426.6
   },
   {
    "periodo": "2023-05",
    "turistas_miles": 327.7
   },
   {
    "periodo": "2023-06",
    "turistas_miles": 292.1
   },
   {
    "periodo": "2023-07",
    "turistas_miles": 490.0
   },
   {
    "periodo": "2023-08",
    "turistas_miles": 390.9
   },
   {
    "periodo": "2023-09",
    "turistas_miles": 546.5
   },
   {
    "periodo": "2023-10",
    "turistas_miles": 581.7
   },
   {
    "periodo": "2023-11",
    "turistas_miles": 682.7
   },
   {
    "periodo": "2023-12",
    "turistas_miles": 841.8
   },
   {
    "periodo": "2024-01",
    "turistas_miles": 1302.7
   },
   {
    "periodo": "2024-02",
    "turistas_miles": 1067.0
   },
   {
    "periodo": "2024-03",
    "turistas_miles": 694.3
   },
   {
    "periodo": "2024-04",
    "turistas_miles": 455.0
   },
   {
    "periodo": "2024-05",
    "turistas_miles": 332.4
   },
   {
    "periodo": "2024-06",
    "turistas_miles": 338.9
   },
   {
    "periodo": "2024-07",
    "turistas_miles": 556.1
   },
   {
    "periodo": "2024-08",
    "turistas_miles": 429.1
   },
   {
    "periodo": "2024-09",
    "turistas_miles": 677.5
   },
   {
    "periodo": "2024-10",
    "turistas_miles": 618.5
   },
   {
    "periodo": "2024-11",
    "turistas_miles": 680.3
   },
   {
    "periodo": "2024-12",
    "turistas_miles": 924.4
   }
  ]
 },
 {
  "id": "electricidad",
  "nombre": "Demanda eléctrica nacional (SEN)",
  "sector": "Energía",
  "periodo": "mensual",
  "m": 12,
  "caracteristicas": [
   "tendencia",
   "estacionalidad bimodal",
   "ruido"
  ],
  "descripcion": "Demanda eléctrica del Sistema Eléctrico Nacional (GWh/mes, ~6.500). Estacionalidad bimodal: peaks de invierno (calefacción) y de verano (refrigeración). Buen caso para descomponer y comparar modelos.",
  "columns": [
   {
    "name": "periodo",
    "type": "fecha"
   },
   {
    "name": "demanda_gwh",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "periodo": "2022-01",
    "demanda_gwh": 6728.0
   },
   {
    "periodo": "2022-02",
    "demanda_gwh": 6572.5
   },
   {
    "periodo": "2022-03",
    "demanda_gwh": 6246.7
   },
   {
    "periodo": "2022-04",
    "demanda_gwh": 6040.0
   },
   {
    "periodo": "2022-05",
    "demanda_gwh": 6387.8
   },
   {
    "periodo": "2022-06",
    "demanda_gwh": 7062.7
   },
   {
    "periodo": "2022-07",
    "demanda_gwh": 7288.3
   },
   {
    "periodo": "2022-08",
    "demanda_gwh": 6678.4
   },
   {
    "periodo": "2022-09",
    "demanda_gwh": 6175.6
   },
   {
    "periodo": "2022-10",
    "demanda_gwh": 6353.1
   },
   {
    "periodo": "2022-11",
    "demanda_gwh": 6487.4
   },
   {
    "periodo": "2022-12",
    "demanda_gwh": 6787.3
   },
   {
    "periodo": "2023-01",
    "demanda_gwh": 6892.0
   },
   {
    "periodo": "2023-02",
    "demanda_gwh": 6692.2
   },
   {
    "periodo": "2023-03",
    "demanda_gwh": 6511.0
   },
   {
    "periodo": "2023-04",
    "demanda_gwh": 6153.6
   },
   {
    "periodo": "2023-05",
    "demanda_gwh": 6373.2
   },
   {
    "periodo": "2023-06",
    "demanda_gwh": 7085.7
   },
   {
    "periodo": "2023-07",
    "demanda_gwh": 7369.7
   },
   {
    "periodo": "2023-08",
    "demanda_gwh": 7174.2
   },
   {
    "periodo": "2023-09",
    "demanda_gwh": 6679.9
   },
   {
    "periodo": "2023-10",
    "demanda_gwh": 6434.9
   },
   {
    "periodo": "2023-11",
    "demanda_gwh": 6663.9
   },
   {
    "periodo": "2023-12",
    "demanda_gwh": 7078.2
   },
   {
    "periodo": "2024-01",
    "demanda_gwh": 7040.2
   },
   {
    "periodo": "2024-02",
    "demanda_gwh": 6836.2
   },
   {
    "periodo": "2024-03",
    "demanda_gwh": 6625.8
   },
   {
    "periodo": "2024-04",
    "demanda_gwh": 6412.8
   },
   {
    "periodo": "2024-05",
    "demanda_gwh": 6914.7
   },
   {
    "periodo": "2024-06",
    "demanda_gwh": 7374.3
   },
   {
    "periodo": "2024-07",
    "demanda_gwh": 7716.4
   },
   {
    "periodo": "2024-08",
    "demanda_gwh": 7257.9
   },
   {
    "periodo": "2024-09",
    "demanda_gwh": 6754.1
   },
   {
    "periodo": "2024-10",
    "demanda_gwh": 6648.9
   },
   {
    "periodo": "2024-11",
    "demanda_gwh": 6859.5
   },
   {
    "periodo": "2024-12",
    "demanda_gwh": 7179.2
   },
   {
    "periodo": "2025-01",
    "demanda_gwh": 7249.1
   },
   {
    "periodo": "2025-02",
    "demanda_gwh": 7287.6
   },
   {
    "periodo": "2025-03",
    "demanda_gwh": 6968.9
   },
   {
    "periodo": "2025-04",
    "demanda_gwh": 6533.0
   },
   {
    "periodo": "2025-05",
    "demanda_gwh": 6951.5
   },
   {
    "periodo": "2025-06",
    "demanda_gwh": 7497.8
   },
   {
    "periodo": "2025-07",
    "demanda_gwh": 7790.3
   },
   {
    "periodo": "2025-08",
    "demanda_gwh": 7381.3
   },
   {
    "periodo": "2025-09",
    "demanda_gwh": 6965.1
   },
   {
    "periodo": "2025-10",
    "demanda_gwh": 7064.8
   },
   {
    "periodo": "2025-11",
    "demanda_gwh": 7147.6
   },
   {
    "periodo": "2025-12",
    "demanda_gwh": 7375.0
   }
  ]
 },
 {
  "id": "salmon",
  "nombre": "Exportaciones de salmón",
  "sector": "Acuicultura",
  "periodo": "mensual",
  "m": 12,
  "caracteristicas": [
   "tendencia",
   "estacionalidad",
   "ruido"
  ],
  "descripcion": "Toneladas mensuales exportadas de salmón (~62.000 ton), con crecimiento sostenido y mayor demanda hacia fin de año. Adecuado para Holt y Holt-Winters.",
  "columns": [
   {
    "name": "periodo",
    "type": "fecha"
   },
   {
    "name": "export_ton",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "periodo": "2022-01",
    "export_ton": 54872
   },
   {
    "periodo": "2022-02",
    "export_ton": 57900
   },
   {
    "periodo": "2022-03",
    "export_ton": 62671
   },
   {
    "periodo": "2022-04",
    "export_ton": 61831
   },
   {
    "periodo": "2022-05",
    "export_ton": 63115
   },
   {
    "periodo": "2022-06",
    "export_ton": 59348
   },
   {
    "periodo": "2022-07",
    "export_ton": 60580
   },
   {
    "periodo": "2022-08",
    "export_ton": 60144
   },
   {
    "periodo": "2022-09",
    "export_ton": 68928
   },
   {
    "periodo": "2022-10",
    "export_ton": 67017
   },
   {
    "periodo": "2022-11",
    "export_ton": 69078
   },
   {
    "periodo": "2022-12",
    "export_ton": 65602
   },
   {
    "periodo": "2023-01",
    "export_ton": 56733
   },
   {
    "periodo": "2023-02",
    "export_ton": 60529
   },
   {
    "periodo": "2023-03",
    "export_ton": 62425
   },
   {
    "periodo": "2023-04",
    "export_ton": 63282
   },
   {
    "periodo": "2023-05",
    "export_ton": 66195
   },
   {
    "periodo": "2023-06",
    "export_ton": 65925
   },
   {
    "periodo": "2023-07",
    "export_ton": 64973
   },
   {
    "periodo": "2023-08",
    "export_ton": 65335
   },
   {
    "periodo": "2023-09",
    "export_ton": 66435
   },
   {
    "periodo": "2023-10",
    "export_ton": 69401
   },
   {
    "periodo": "2023-11",
    "export_ton": 73581
   },
   {
    "periodo": "2023-12",
    "export_ton": 65945
   },
   {
    "periodo": "2024-01",
    "export_ton": 61038
   },
   {
    "periodo": "2024-02",
    "export_ton": 62867
   },
   {
    "periodo": "2024-03",
    "export_ton": 66442
   },
   {
    "periodo": "2024-04",
    "export_ton": 67145
   },
   {
    "periodo": "2024-05",
    "export_ton": 73308
   },
   {
    "periodo": "2024-06",
    "export_ton": 69717
   },
   {
    "periodo": "2024-07",
    "export_ton": 66454
   },
   {
    "periodo": "2024-08",
    "export_ton": 66144
   },
   {
    "periodo": "2024-09",
    "export_ton": 71366
   },
   {
    "periodo": "2024-10",
    "export_ton": 75921
   },
   {
    "periodo": "2024-11",
    "export_ton": 74777
   },
   {
    "periodo": "2024-12",
    "export_ton": 67514
   },
   {
    "periodo": "2025-01",
    "export_ton": 62505
   },
   {
    "periodo": "2025-02",
    "export_ton": 66383
   },
   {
    "periodo": "2025-03",
    "export_ton": 72118
   },
   {
    "periodo": "2025-04",
    "export_ton": 71846
   },
   {
    "periodo": "2025-05",
    "export_ton": 72837
   },
   {
    "periodo": "2025-06",
    "export_ton": 74393
   },
   {
    "periodo": "2025-07",
    "export_ton": 74329
   },
   {
    "periodo": "2025-08",
    "export_ton": 71827
   },
   {
    "periodo": "2025-09",
    "export_ton": 75998
   },
   {
    "periodo": "2025-10",
    "export_ton": 73819
   },
   {
    "periodo": "2025-11",
    "export_ton": 75207
   },
   {
    "periodo": "2025-12",
    "export_ton": 77169
   }
  ]
 },
 {
  "id": "temperatura",
  "nombre": "Temperatura media de Santiago",
  "sector": "Clima",
  "periodo": "mensual",
  "m": 12,
  "caracteristicas": [
   "estacionalidad pura",
   "sin tendencia",
   "ruido bajo"
  ],
  "descripcion": "Temperatura media mensual (°C) en Santiago: estacionalidad sinusoidal casi pura, sin tendencia. El caso más didáctico para entender la componente estacional y la descomposición.",
  "columns": [
   {
    "name": "periodo",
    "type": "fecha"
   },
   {
    "name": "temp_media_c",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "periodo": "2020-01",
    "temp_media_c": 26.6
   },
   {
    "periodo": "2020-02",
    "temp_media_c": 26.3
   },
   {
    "periodo": "2020-03",
    "temp_media_c": 22.7
   },
   {
    "periodo": "2020-04",
    "temp_media_c": 18.0
   },
   {
    "periodo": "2020-05",
    "temp_media_c": 11.8
   },
   {
    "periodo": "2020-06",
    "temp_media_c": 9.1
   },
   {
    "periodo": "2020-07",
    "temp_media_c": 7.4
   },
   {
    "periodo": "2020-08",
    "temp_media_c": 9.7
   },
   {
    "periodo": "2020-09",
    "temp_media_c": 12.1
   },
   {
    "periodo": "2020-10",
    "temp_media_c": 16.8
   },
   {
    "periodo": "2020-11",
    "temp_media_c": 22.8
   },
   {
    "periodo": "2020-12",
    "temp_media_c": 25.6
   },
   {
    "periodo": "2021-01",
    "temp_media_c": 26.7
   },
   {
    "periodo": "2021-02",
    "temp_media_c": 26.7
   },
   {
    "periodo": "2021-03",
    "temp_media_c": 22.8
   },
   {
    "periodo": "2021-04",
    "temp_media_c": 15.6
   },
   {
    "periodo": "2021-05",
    "temp_media_c": 11.9
   },
   {
    "periodo": "2021-06",
    "temp_media_c": 8.2
   },
   {
    "periodo": "2021-07",
    "temp_media_c": 7.9
   },
   {
    "periodo": "2021-08",
    "temp_media_c": 9.7
   },
   {
    "periodo": "2021-09",
    "temp_media_c": 13.7
   },
   {
    "periodo": "2021-10",
    "temp_media_c": 17.9
   },
   {
    "periodo": "2021-11",
    "temp_media_c": 21.8
   },
   {
    "periodo": "2021-12",
    "temp_media_c": 25.5
   },
   {
    "periodo": "2022-01",
    "temp_media_c": 26.9
   },
   {
    "periodo": "2022-02",
    "temp_media_c": 26.5
   },
   {
    "periodo": "2022-03",
    "temp_media_c": 23.3
   },
   {
    "periodo": "2022-04",
    "temp_media_c": 16.3
   },
   {
    "periodo": "2022-05",
    "temp_media_c": 12.9
   },
   {
    "periodo": "2022-06",
    "temp_media_c": 9.4
   },
   {
    "periodo": "2022-07",
    "temp_media_c": 7.7
   },
   {
    "periodo": "2022-08",
    "temp_media_c": 10.8
   },
   {
    "periodo": "2022-09",
    "temp_media_c": 12.8
   },
   {
    "periodo": "2022-10",
    "temp_media_c": 17.5
   },
   {
    "periodo": "2022-11",
    "temp_media_c": 22.9
   },
   {
    "periodo": "2022-12",
    "temp_media_c": 25.8
   },
   {
    "periodo": "2023-01",
    "temp_media_c": 26.8
   },
   {
    "periodo": "2023-02",
    "temp_media_c": 26.4
   },
   {
    "periodo": "2023-03",
    "temp_media_c": 23.2
   },
   {
    "periodo": "2023-04",
    "temp_media_c": 17.4
   },
   {
    "periodo": "2023-05",
    "temp_media_c": 13.1
   },
   {
    "periodo": "2023-06",
    "temp_media_c": 8.6
   },
   {
    "periodo": "2023-07",
    "temp_media_c": 8.5
   },
   {
    "periodo": "2023-08",
    "temp_media_c": 9.0
   },
   {
    "periodo": "2023-09",
    "temp_media_c": 12.8
   },
   {
    "periodo": "2023-10",
    "temp_media_c": 18.0
   },
   {
    "periodo": "2023-11",
    "temp_media_c": 21.7
   },
   {
    "periodo": "2023-12",
    "temp_media_c": 26.1
   },
   {
    "periodo": "2024-01",
    "temp_media_c": 28.6
   },
   {
    "periodo": "2024-02",
    "temp_media_c": 26.2
   },
   {
    "periodo": "2024-03",
    "temp_media_c": 23.3
   },
   {
    "periodo": "2024-04",
    "temp_media_c": 18.0
   },
   {
    "periodo": "2024-05",
    "temp_media_c": 11.4
   },
   {
    "periodo": "2024-06",
    "temp_media_c": 9.3
   },
   {
    "periodo": "2024-07",
    "temp_media_c": 6.8
   },
   {
    "periodo": "2024-08",
    "temp_media_c": 9.0
   },
   {
    "periodo": "2024-09",
    "temp_media_c": 12.3
   },
   {
    "periodo": "2024-10",
    "temp_media_c": 17.5
   },
   {
    "periodo": "2024-11",
    "temp_media_c": 22.5
   },
   {
    "periodo": "2024-12",
    "temp_media_c": 26.3
   },
   {
    "periodo": "2025-01",
    "temp_media_c": 27.2
   },
   {
    "periodo": "2025-02",
    "temp_media_c": 25.3
   },
   {
    "periodo": "2025-03",
    "temp_media_c": 21.9
   },
   {
    "periodo": "2025-04",
    "temp_media_c": 18.0
   },
   {
    "periodo": "2025-05",
    "temp_media_c": 13.5
   },
   {
    "periodo": "2025-06",
    "temp_media_c": 9.0
   },
   {
    "periodo": "2025-07",
    "temp_media_c": 8.0
   },
   {
    "periodo": "2025-08",
    "temp_media_c": 9.4
   },
   {
    "periodo": "2025-09",
    "temp_media_c": 11.7
   },
   {
    "periodo": "2025-10",
    "temp_media_c": 16.4
   },
   {
    "periodo": "2025-11",
    "temp_media_c": 22.5
   },
   {
    "periodo": "2025-12",
    "temp_media_c": 25.0
   }
  ]
 },
 {
  "id": "metro",
  "nombre": "Pasajeros del Metro de Santiago",
  "sector": "Transporte",
  "periodo": "mensual",
  "m": 12,
  "caracteristicas": [
   "tendencia",
   "estacionalidad",
   "ruido"
  ],
  "descripcion": "Pasajeros mensuales (millones) del Metro. Fuerte caída en febrero (vacaciones) y recuperación en marzo. Bueno para Holt-Winters y para discutir efectos de calendario.",
  "columns": [
   {
    "name": "periodo",
    "type": "fecha"
   },
   {
    "name": "pasajeros_mm",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "periodo": "2022-01",
    "pasajeros_mm": 45.51
   },
   {
    "periodo": "2022-02",
    "pasajeros_mm": 34.43
   },
   {
    "periodo": "2022-03",
    "pasajeros_mm": 54.81
   },
   {
    "periodo": "2022-04",
    "pasajeros_mm": 53.82
   },
   {
    "periodo": "2022-05",
    "pasajeros_mm": 55.93
   },
   {
    "periodo": "2022-06",
    "pasajeros_mm": 53.78
   },
   {
    "periodo": "2022-07",
    "pasajeros_mm": 49.79
   },
   {
    "periodo": "2022-08",
    "pasajeros_mm": 55.98
   },
   {
    "periodo": "2022-09",
    "pasajeros_mm": 54.91
   },
   {
    "periodo": "2022-10",
    "pasajeros_mm": 57.4
   },
   {
    "periodo": "2022-11",
    "pasajeros_mm": 54.29
   },
   {
    "periodo": "2022-12",
    "pasajeros_mm": 50.83
   },
   {
    "periodo": "2023-01",
    "pasajeros_mm": 50.11
   },
   {
    "periodo": "2023-02",
    "pasajeros_mm": 37.08
   },
   {
    "periodo": "2023-03",
    "pasajeros_mm": 59.27
   },
   {
    "periodo": "2023-04",
    "pasajeros_mm": 58.15
   },
   {
    "periodo": "2023-05",
    "pasajeros_mm": 58.99
   },
   {
    "periodo": "2023-06",
    "pasajeros_mm": 57.9
   },
   {
    "periodo": "2023-07",
    "pasajeros_mm": 53.33
   },
   {
    "periodo": "2023-08",
    "pasajeros_mm": 57.98
   },
   {
    "periodo": "2023-09",
    "pasajeros_mm": 53.63
   },
   {
    "periodo": "2023-10",
    "pasajeros_mm": 59.27
   },
   {
    "periodo": "2023-11",
    "pasajeros_mm": 59.26
   },
   {
    "periodo": "2023-12",
    "pasajeros_mm": 51.43
   },
   {
    "periodo": "2024-01",
    "pasajeros_mm": 49.28
   },
   {
    "periodo": "2024-02",
    "pasajeros_mm": 38.39
   },
   {
    "periodo": "2024-03",
    "pasajeros_mm": 60.21
   },
   {
    "periodo": "2024-04",
    "pasajeros_mm": 58.77
   },
   {
    "periodo": "2024-05",
    "pasajeros_mm": 60.86
   },
   {
    "periodo": "2024-06",
    "pasajeros_mm": 58.81
   },
   {
    "periodo": "2024-07",
    "pasajeros_mm": 54.69
   },
   {
    "periodo": "2024-08",
    "pasajeros_mm": 58.96
   },
   {
    "periodo": "2024-09",
    "pasajeros_mm": 55.16
   },
   {
    "periodo": "2024-10",
    "pasajeros_mm": 61.7
   },
   {
    "periodo": "2024-11",
    "pasajeros_mm": 61.17
   },
   {
    "periodo": "2024-12",
    "pasajeros_mm": 52.57
   },
   {
    "periodo": "2025-01",
    "pasajeros_mm": 52.41
   },
   {
    "periodo": "2025-02",
    "pasajeros_mm": 39.33
   },
   {
    "periodo": "2025-03",
    "pasajeros_mm": 61.25
   },
   {
    "periodo": "2025-04",
    "pasajeros_mm": 62.75
   },
   {
    "periodo": "2025-05",
    "pasajeros_mm": 63.61
   },
   {
    "periodo": "2025-06",
    "pasajeros_mm": 60.29
   },
   {
    "periodo": "2025-07",
    "pasajeros_mm": 56.77
   },
   {
    "periodo": "2025-08",
    "pasajeros_mm": 61.19
   },
   {
    "periodo": "2025-09",
    "pasajeros_mm": 59.07
   },
   {
    "periodo": "2025-10",
    "pasajeros_mm": 64.86
   },
   {
    "periodo": "2025-11",
    "pasajeros_mm": 62.74
   },
   {
    "periodo": "2025-12",
    "pasajeros_mm": 58.41
   }
  ]
 },
 {
  "id": "dolar",
  "nombre": "Dólar observado (CLP)",
  "sector": "Financiero",
  "periodo": "mensual",
  "m": 12,
  "caracteristicas": [
   "caminata aleatoria",
   "tendencia estocástica",
   "ruido",
   "sin estacionalidad"
  ],
  "descripcion": "Tipo de cambio peso/dólar (CLP), modelado como caminata aleatoria con deriva. No tiene estacionalidad: es el caso ideal para mostrar por qué el método ingenuo suele ser difícil de superar.",
  "columns": [
   {
    "name": "periodo",
    "type": "fecha"
   },
   {
    "name": "dolar_clp",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "periodo": "2020-01",
    "dolar_clp": 857.9
   },
   {
    "periodo": "2020-02",
    "dolar_clp": 858.3
   },
   {
    "periodo": "2020-03",
    "dolar_clp": 868.9
   },
   {
    "periodo": "2020-04",
    "dolar_clp": 850.9
   },
   {
    "periodo": "2020-05",
    "dolar_clp": 849.7
   },
   {
    "periodo": "2020-06",
    "dolar_clp": 854.6
   },
   {
    "periodo": "2020-07",
    "dolar_clp": 856.4
   },
   {
    "periodo": "2020-08",
    "dolar_clp": 882.9
   },
   {
    "periodo": "2020-09",
    "dolar_clp": 888.5
   },
   {
    "periodo": "2020-10",
    "dolar_clp": 894.8
   },
   {
    "periodo": "2020-11",
    "dolar_clp": 880.8
   },
   {
    "periodo": "2020-12",
    "dolar_clp": 880.4
   },
   {
    "periodo": "2021-01",
    "dolar_clp": 872.9
   },
   {
    "periodo": "2021-02",
    "dolar_clp": 903.0
   },
   {
    "periodo": "2021-03",
    "dolar_clp": 899.9
   },
   {
    "periodo": "2021-04",
    "dolar_clp": 903.2
   },
   {
    "periodo": "2021-05",
    "dolar_clp": 919.7
   },
   {
    "periodo": "2021-06",
    "dolar_clp": 929.5
   },
   {
    "periodo": "2021-07",
    "dolar_clp": 914.5
   },
   {
    "periodo": "2021-08",
    "dolar_clp": 924.0
   },
   {
    "periodo": "2021-09",
    "dolar_clp": 934.5
   },
   {
    "periodo": "2021-10",
    "dolar_clp": 934.2
   },
   {
    "periodo": "2021-11",
    "dolar_clp": 941.7
   },
   {
    "periodo": "2021-12",
    "dolar_clp": 944.8
   },
   {
    "periodo": "2022-01",
    "dolar_clp": 930.1
   },
   {
    "periodo": "2022-02",
    "dolar_clp": 925.2
   },
   {
    "periodo": "2022-03",
    "dolar_clp": 927.4
   },
   {
    "periodo": "2022-04",
    "dolar_clp": 922.2
   },
   {
    "periodo": "2022-05",
    "dolar_clp": 930.6
   },
   {
    "periodo": "2022-06",
    "dolar_clp": 944.5
   },
   {
    "periodo": "2022-07",
    "dolar_clp": 949.7
   },
   {
    "periodo": "2022-08",
    "dolar_clp": 947.1
   },
   {
    "periodo": "2022-09",
    "dolar_clp": 965.4
   },
   {
    "periodo": "2022-10",
    "dolar_clp": 968.9
   },
   {
    "periodo": "2022-11",
    "dolar_clp": 975.1
   },
   {
    "periodo": "2022-12",
    "dolar_clp": 967.8
   },
   {
    "periodo": "2023-01",
    "dolar_clp": 967.1
   },
   {
    "periodo": "2023-02",
    "dolar_clp": 981.0
   },
   {
    "periodo": "2023-03",
    "dolar_clp": 991.8
   },
   {
    "periodo": "2023-04",
    "dolar_clp": 991.5
   },
   {
    "periodo": "2023-05",
    "dolar_clp": 993.5
   },
   {
    "periodo": "2023-06",
    "dolar_clp": 997.8
   },
   {
    "periodo": "2023-07",
    "dolar_clp": 988.4
   },
   {
    "periodo": "2023-08",
    "dolar_clp": 988.0
   },
   {
    "periodo": "2023-09",
    "dolar_clp": 983.8
   },
   {
    "periodo": "2023-10",
    "dolar_clp": 969.1
   },
   {
    "periodo": "2023-11",
    "dolar_clp": 972.8
   },
   {
    "periodo": "2023-12",
    "dolar_clp": 973.0
   },
   {
    "periodo": "2024-01",
    "dolar_clp": 957.3
   },
   {
    "periodo": "2024-02",
    "dolar_clp": 949.7
   },
   {
    "periodo": "2024-03",
    "dolar_clp": 950.5
   },
   {
    "periodo": "2024-04",
    "dolar_clp": 917.7
   },
   {
    "periodo": "2024-05",
    "dolar_clp": 921.8
   },
   {
    "periodo": "2024-06",
    "dolar_clp": 926.9
   },
   {
    "periodo": "2024-07",
    "dolar_clp": 936.6
   },
   {
    "periodo": "2024-08",
    "dolar_clp": 931.4
   },
   {
    "periodo": "2024-09",
    "dolar_clp": 916.2
   },
   {
    "periodo": "2024-10",
    "dolar_clp": 925.6
   },
   {
    "periodo": "2024-11",
    "dolar_clp": 911.0
   },
   {
    "periodo": "2024-12",
    "dolar_clp": 919.4
   },
   {
    "periodo": "2025-01",
    "dolar_clp": 913.2
   },
   {
    "periodo": "2025-02",
    "dolar_clp": 903.0
   },
   {
    "periodo": "2025-03",
    "dolar_clp": 908.4
   },
   {
    "periodo": "2025-04",
    "dolar_clp": 923.8
   },
   {
    "periodo": "2025-05",
    "dolar_clp": 923.8
   },
   {
    "periodo": "2025-06",
    "dolar_clp": 922.7
   },
   {
    "periodo": "2025-07",
    "dolar_clp": 904.4
   },
   {
    "periodo": "2025-08",
    "dolar_clp": 916.3
   },
   {
    "periodo": "2025-09",
    "dolar_clp": 919.0
   },
   {
    "periodo": "2025-10",
    "dolar_clp": 917.7
   },
   {
    "periodo": "2025-11",
    "dolar_clp": 935.3
   },
   {
    "periodo": "2025-12",
    "dolar_clp": 918.4
   }
  ]
 },
 {
  "id": "ipc",
  "nombre": "Inflación mensual (IPC)",
  "sector": "Macroeconomía",
  "periodo": "mensual",
  "m": 12,
  "caracteristicas": [
   "cambio de régimen",
   "ruido",
   "sin estacionalidad clara"
  ],
  "descripcion": "Variación mensual del IPC (%). Presenta un régimen inflacionario alto que luego cede: útil para discutir estacionariedad, quiebres y por qué un promedio simple engaña.",
  "columns": [
   {
    "name": "periodo",
    "type": "fecha"
   },
   {
    "name": "ipc_var_pct",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "periodo": "2021-01",
    "ipc_var_pct": 0.93
   },
   {
    "periodo": "2021-02",
    "ipc_var_pct": 0.99
   },
   {
    "periodo": "2021-03",
    "ipc_var_pct": 0.95
   },
   {
    "periodo": "2021-04",
    "ipc_var_pct": 0.64
   },
   {
    "periodo": "2021-05",
    "ipc_var_pct": 1.02
   },
   {
    "periodo": "2021-06",
    "ipc_var_pct": 0.97
   },
   {
    "periodo": "2021-07",
    "ipc_var_pct": 1.11
   },
   {
    "periodo": "2021-08",
    "ipc_var_pct": 1.24
   },
   {
    "periodo": "2021-09",
    "ipc_var_pct": 0.93
   },
   {
    "periodo": "2021-10",
    "ipc_var_pct": 1.0
   },
   {
    "periodo": "2021-11",
    "ipc_var_pct": 0.98
   },
   {
    "periodo": "2021-12",
    "ipc_var_pct": 0.96
   },
   {
    "periodo": "2022-01",
    "ipc_var_pct": 0.91
   },
   {
    "periodo": "2022-02",
    "ipc_var_pct": 0.98
   },
   {
    "periodo": "2022-03",
    "ipc_var_pct": 1.07
   },
   {
    "periodo": "2022-04",
    "ipc_var_pct": 0.79
   },
   {
    "periodo": "2022-05",
    "ipc_var_pct": 1.17
   },
   {
    "periodo": "2022-06",
    "ipc_var_pct": 0.97
   },
   {
    "periodo": "2022-07",
    "ipc_var_pct": 0.94
   },
   {
    "periodo": "2022-08",
    "ipc_var_pct": 0.56
   },
   {
    "periodo": "2022-09",
    "ipc_var_pct": 0.84
   },
   {
    "periodo": "2022-10",
    "ipc_var_pct": 0.68
   },
   {
    "periodo": "2022-11",
    "ipc_var_pct": 0.87
   },
   {
    "periodo": "2022-12",
    "ipc_var_pct": 0.89
   },
   {
    "periodo": "2023-01",
    "ipc_var_pct": 0.89
   },
   {
    "periodo": "2023-02",
    "ipc_var_pct": 0.68
   },
   {
    "periodo": "2023-03",
    "ipc_var_pct": 0.67
   },
   {
    "periodo": "2023-04",
    "ipc_var_pct": 0.71
   },
   {
    "periodo": "2023-05",
    "ipc_var_pct": 0.33
   },
   {
    "periodo": "2023-06",
    "ipc_var_pct": 0.53
   },
   {
    "periodo": "2023-07",
    "ipc_var_pct": 0.49
   },
   {
    "periodo": "2023-08",
    "ipc_var_pct": 0.61
   },
   {
    "periodo": "2023-09",
    "ipc_var_pct": 0.44
   },
   {
    "periodo": "2023-10",
    "ipc_var_pct": 0.58
   },
   {
    "periodo": "2023-11",
    "ipc_var_pct": 0.43
   },
   {
    "periodo": "2023-12",
    "ipc_var_pct": 0.54
   },
   {
    "periodo": "2024-01",
    "ipc_var_pct": 0.66
   },
   {
    "periodo": "2024-02",
    "ipc_var_pct": 0.57
   },
   {
    "periodo": "2024-03",
    "ipc_var_pct": 0.48
   },
   {
    "periodo": "2024-04",
    "ipc_var_pct": 0.51
   },
   {
    "periodo": "2024-05",
    "ipc_var_pct": 0.3
   },
   {
    "periodo": "2024-06",
    "ipc_var_pct": 0.24
   },
   {
    "periodo": "2024-07",
    "ipc_var_pct": 0.23
   },
   {
    "periodo": "2024-08",
    "ipc_var_pct": 0.38
   },
   {
    "periodo": "2024-09",
    "ipc_var_pct": 0.56
   },
   {
    "periodo": "2024-10",
    "ipc_var_pct": 0.25
   },
   {
    "periodo": "2024-11",
    "ipc_var_pct": 0.42
   },
   {
    "periodo": "2024-12",
    "ipc_var_pct": 0.18
   },
   {
    "periodo": "2025-01",
    "ipc_var_pct": 0.18
   },
   {
    "periodo": "2025-02",
    "ipc_var_pct": 0.47
   },
   {
    "periodo": "2025-03",
    "ipc_var_pct": 0.25
   },
   {
    "periodo": "2025-04",
    "ipc_var_pct": 0.25
   },
   {
    "periodo": "2025-05",
    "ipc_var_pct": 0.63
   },
   {
    "periodo": "2025-06",
    "ipc_var_pct": 0.36
   },
   {
    "periodo": "2025-07",
    "ipc_var_pct": 0.34
   },
   {
    "periodo": "2025-08",
    "ipc_var_pct": 0.32
   },
   {
    "periodo": "2025-09",
    "ipc_var_pct": 0.41
   },
   {
    "periodo": "2025-10",
    "ipc_var_pct": 0.25
   },
   {
    "periodo": "2025-11",
    "ipc_var_pct": 0.36
   },
   {
    "periodo": "2025-12",
    "ipc_var_pct": 0.5
   }
  ]
 },
 {
  "id": "heladeria",
  "nombre": "Ventas de heladería artesanal",
  "sector": "Alimentos",
  "periodo": "mensual",
  "m": 12,
  "caracteristicas": [
   "estacionalidad multiplicativa",
   "tendencia",
   "ruido"
  ],
  "descripcion": "Unidades vendidas por mes: la amplitud estacional crece con el nivel (verano ×2,6 vs. invierno ×0,4). Caso clásico para Holt-Winters MULTIPLICATIVO.",
  "columns": [
   {
    "name": "periodo",
    "type": "fecha"
   },
   {
    "name": "ventas_unid",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "periodo": "2022-01",
    "ventas_unid": 10780
   },
   {
    "periodo": "2022-02",
    "ventas_unid": 9169
   },
   {
    "periodo": "2022-03",
    "ventas_unid": 5786
   },
   {
    "periodo": "2022-04",
    "ventas_unid": 3957
   },
   {
    "periodo": "2022-05",
    "ventas_unid": 2688
   },
   {
    "periodo": "2022-06",
    "ventas_unid": 1968
   },
   {
    "periodo": "2022-07",
    "ventas_unid": 1832
   },
   {
    "periodo": "2022-08",
    "ventas_unid": 1878
   },
   {
    "periodo": "2022-09",
    "ventas_unid": 3220
   },
   {
    "periodo": "2022-10",
    "ventas_unid": 4878
   },
   {
    "periodo": "2022-11",
    "ventas_unid": 7263
   },
   {
    "periodo": "2022-12",
    "ventas_unid": 8654
   },
   {
    "periodo": "2023-01",
    "ventas_unid": 12021
   },
   {
    "periodo": "2023-02",
    "ventas_unid": 10867
   },
   {
    "periodo": "2023-03",
    "ventas_unid": 6793
   },
   {
    "periodo": "2023-04",
    "ventas_unid": 4108
   },
   {
    "periodo": "2023-05",
    "ventas_unid": 2625
   },
   {
    "periodo": "2023-06",
    "ventas_unid": 1992
   },
   {
    "periodo": "2023-07",
    "ventas_unid": 1868
   },
   {
    "periodo": "2023-08",
    "ventas_unid": 2104
   },
   {
    "periodo": "2023-09",
    "ventas_unid": 3166
   },
   {
    "periodo": "2023-10",
    "ventas_unid": 4909
   },
   {
    "periodo": "2023-11",
    "ventas_unid": 7949
   },
   {
    "periodo": "2023-12",
    "ventas_unid": 10254
   },
   {
    "periodo": "2024-01",
    "ventas_unid": 12259
   },
   {
    "periodo": "2024-02",
    "ventas_unid": 11157
   },
   {
    "periodo": "2024-03",
    "ventas_unid": 7054
   },
   {
    "periodo": "2024-04",
    "ventas_unid": 4507
   },
   {
    "periodo": "2024-05",
    "ventas_unid": 2772
   },
   {
    "periodo": "2024-06",
    "ventas_unid": 2170
   },
   {
    "periodo": "2024-07",
    "ventas_unid": 1872
   },
   {
    "periodo": "2024-08",
    "ventas_unid": 2360
   },
   {
    "periodo": "2024-09",
    "ventas_unid": 3494
   },
   {
    "periodo": "2024-10",
    "ventas_unid": 5358
   },
   {
    "periodo": "2024-11",
    "ventas_unid": 7810
   },
   {
    "periodo": "2024-12",
    "ventas_unid": 11172
   },
   {
    "periodo": "2025-01",
    "ventas_unid": 12851
   },
   {
    "periodo": "2025-02",
    "ventas_unid": 12776
   },
   {
    "periodo": "2025-03",
    "ventas_unid": 6789
   },
   {
    "periodo": "2025-04",
    "ventas_unid": 4327
   },
   {
    "periodo": "2025-05",
    "ventas_unid": 3220
   },
   {
    "periodo": "2025-06",
    "ventas_unid": 2257
   },
   {
    "periodo": "2025-07",
    "ventas_unid": 2166
   },
   {
    "periodo": "2025-08",
    "ventas_unid": 2397
   },
   {
    "periodo": "2025-09",
    "ventas_unid": 3421
   },
   {
    "periodo": "2025-10",
    "ventas_unid": 5570
   },
   {
    "periodo": "2025-11",
    "ventas_unid": 8356
   },
   {
    "periodo": "2025-12",
    "ventas_unid": 11413
   }
  ]
 },
 {
  "id": "repuestos",
  "nombre": "Demanda de repuestos (intermitente)",
  "sector": "Inventario",
  "periodo": "mensual",
  "m": 12,
  "caracteristicas": [
   "demanda intermitente",
   "muchos ceros",
   "ruido"
  ],
  "descripcion": "Demanda mensual de un repuesto de baja rotación: mayoría de meses en cero con picos esporádicos. Motiva métodos específicos (Croston) que se abordan en la Versión 3.",
  "columns": [
   {
    "name": "periodo",
    "type": "fecha"
   },
   {
    "name": "demanda_unid",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "periodo": "2021-01",
    "demanda_unid": 0
   },
   {
    "periodo": "2021-02",
    "demanda_unid": 0
   },
   {
    "periodo": "2021-03",
    "demanda_unid": 4
   },
   {
    "periodo": "2021-04",
    "demanda_unid": 0
   },
   {
    "periodo": "2021-05",
    "demanda_unid": 4
   },
   {
    "periodo": "2021-06",
    "demanda_unid": 0
   },
   {
    "periodo": "2021-07",
    "demanda_unid": 0
   },
   {
    "periodo": "2021-08",
    "demanda_unid": 0
   },
   {
    "periodo": "2021-09",
    "demanda_unid": 0
   },
   {
    "periodo": "2021-10",
    "demanda_unid": 1
   },
   {
    "periodo": "2021-11",
    "demanda_unid": 2
   },
   {
    "periodo": "2021-12",
    "demanda_unid": 0
   },
   {
    "periodo": "2022-01",
    "demanda_unid": 0
   },
   {
    "periodo": "2022-02",
    "demanda_unid": 0
   },
   {
    "periodo": "2022-03",
    "demanda_unid": 0
   },
   {
    "periodo": "2022-04",
    "demanda_unid": 2
   },
   {
    "periodo": "2022-05",
    "demanda_unid": 0
   },
   {
    "periodo": "2022-06",
    "demanda_unid": 0
   },
   {
    "periodo": "2022-07",
    "demanda_unid": 0
   },
   {
    "periodo": "2022-08",
    "demanda_unid": 0
   },
   {
    "periodo": "2022-09",
    "demanda_unid": 4
   },
   {
    "periodo": "2022-10",
    "demanda_unid": 0
   },
   {
    "periodo": "2022-11",
    "demanda_unid": 0
   },
   {
    "periodo": "2022-12",
    "demanda_unid": 0
   },
   {
    "periodo": "2023-01",
    "demanda_unid": 0
   },
   {
    "periodo": "2023-02",
    "demanda_unid": 0
   },
   {
    "periodo": "2023-03",
    "demanda_unid": 0
   },
   {
    "periodo": "2023-04",
    "demanda_unid": 0
   },
   {
    "periodo": "2023-05",
    "demanda_unid": 0
   },
   {
    "periodo": "2023-06",
    "demanda_unid": 3
   },
   {
    "periodo": "2023-07",
    "demanda_unid": 0
   },
   {
    "periodo": "2023-08",
    "demanda_unid": 1
   },
   {
    "periodo": "2023-09",
    "demanda_unid": 0
   },
   {
    "periodo": "2023-10",
    "demanda_unid": 0
   },
   {
    "periodo": "2023-11",
    "demanda_unid": 0
   },
   {
    "periodo": "2023-12",
    "demanda_unid": 0
   },
   {
    "periodo": "2024-01",
    "demanda_unid": 3
   },
   {
    "periodo": "2024-02",
    "demanda_unid": 0
   },
   {
    "periodo": "2024-03",
    "demanda_unid": 4
   },
   {
    "periodo": "2024-04",
    "demanda_unid": 0
   },
   {
    "periodo": "2024-05",
    "demanda_unid": 2
   },
   {
    "periodo": "2024-06",
    "demanda_unid": 0
   },
   {
    "periodo": "2024-07",
    "demanda_unid": 0
   },
   {
    "periodo": "2024-08",
    "demanda_unid": 0
   },
   {
    "periodo": "2024-09",
    "demanda_unid": 0
   },
   {
    "periodo": "2024-10",
    "demanda_unid": 0
   },
   {
    "periodo": "2024-11",
    "demanda_unid": 0
   },
   {
    "periodo": "2024-12",
    "demanda_unid": 0
   },
   {
    "periodo": "2025-01",
    "demanda_unid": 0
   },
   {
    "periodo": "2025-02",
    "demanda_unid": 0
   },
   {
    "periodo": "2025-03",
    "demanda_unid": 0
   },
   {
    "periodo": "2025-04",
    "demanda_unid": 0
   },
   {
    "periodo": "2025-05",
    "demanda_unid": 0
   },
   {
    "periodo": "2025-06",
    "demanda_unid": 0
   },
   {
    "periodo": "2025-07",
    "demanda_unid": 0
   },
   {
    "periodo": "2025-08",
    "demanda_unid": 0
   },
   {
    "periodo": "2025-09",
    "demanda_unid": 0
   },
   {
    "periodo": "2025-10",
    "demanda_unid": 0
   },
   {
    "periodo": "2025-11",
    "demanda_unid": 2
   },
   {
    "periodo": "2025-12",
    "demanda_unid": 0
   }
  ]
 },
 {
  "id": "vino",
  "nombre": "Producción de vino (vendimia)",
  "sector": "Agroindustria",
  "periodo": "mensual",
  "m": 12,
  "caracteristicas": [
   "estacionalidad concentrada",
   "tendencia leve",
   "ruido"
  ],
  "descripcion": "Millones de litros producidos por mes, concentrados en la vendimia (marzo–abril) y casi nulos el resto del año. Estacionalidad muy marcada y no sinusoidal.",
  "columns": [
   {
    "name": "periodo",
    "type": "fecha"
   },
   {
    "name": "produccion_millon_l",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "periodo": "2022-01",
    "produccion_millon_l": 0.13
   },
   {
    "periodo": "2022-02",
    "produccion_millon_l": 0.69
   },
   {
    "periodo": "2022-03",
    "produccion_millon_l": 4.66
   },
   {
    "periodo": "2022-04",
    "produccion_millon_l": 5.65
   },
   {
    "periodo": "2022-05",
    "produccion_millon_l": 2.01
   },
   {
    "periodo": "2022-06",
    "produccion_millon_l": 0.52
   },
   {
    "periodo": "2022-07",
    "produccion_millon_l": 0.21
   },
   {
    "periodo": "2022-08",
    "produccion_millon_l": 0.15
   },
   {
    "periodo": "2022-09",
    "produccion_millon_l": 0.15
   },
   {
    "periodo": "2022-10",
    "produccion_millon_l": 0.23
   },
   {
    "periodo": "2022-11",
    "produccion_millon_l": 0.39
   },
   {
    "periodo": "2022-12",
    "produccion_millon_l": 0.43
   },
   {
    "periodo": "2023-01",
    "produccion_millon_l": 0.18
   },
   {
    "periodo": "2023-02",
    "produccion_millon_l": 0.56
   },
   {
    "periodo": "2023-03",
    "produccion_millon_l": 4.94
   },
   {
    "periodo": "2023-04",
    "produccion_millon_l": 5.39
   },
   {
    "periodo": "2023-05",
    "produccion_millon_l": 2.43
   },
   {
    "periodo": "2023-06",
    "produccion_millon_l": 0.57
   },
   {
    "periodo": "2023-07",
    "produccion_millon_l": 0.23
   },
   {
    "periodo": "2023-08",
    "produccion_millon_l": 0.16
   },
   {
    "periodo": "2023-09",
    "produccion_millon_l": 0.17
   },
   {
    "periodo": "2023-10",
    "produccion_millon_l": 0.23
   },
   {
    "periodo": "2023-11",
    "produccion_millon_l": 0.41
   },
   {
    "periodo": "2023-12",
    "produccion_millon_l": 0.41
   },
   {
    "periodo": "2024-01",
    "produccion_millon_l": 0.16
   },
   {
    "periodo": "2024-02",
    "produccion_millon_l": 0.67
   },
   {
    "periodo": "2024-03",
    "produccion_millon_l": 5.5
   },
   {
    "periodo": "2024-04",
    "produccion_millon_l": 5.98
   },
   {
    "periodo": "2024-05",
    "produccion_millon_l": 2.53
   },
   {
    "periodo": "2024-06",
    "produccion_millon_l": 0.49
   },
   {
    "periodo": "2024-07",
    "produccion_millon_l": 0.22
   },
   {
    "periodo": "2024-08",
    "produccion_millon_l": 0.17
   },
   {
    "periodo": "2024-09",
    "produccion_millon_l": 0.17
   },
   {
    "periodo": "2024-10",
    "produccion_millon_l": 0.2
   },
   {
    "periodo": "2024-11",
    "produccion_millon_l": 0.42
   },
   {
    "periodo": "2024-12",
    "produccion_millon_l": 0.47
   },
   {
    "periodo": "2025-01",
    "produccion_millon_l": 0.17
   },
   {
    "periodo": "2025-02",
    "produccion_millon_l": 0.74
   },
   {
    "periodo": "2025-03",
    "produccion_millon_l": 4.75
   },
   {
    "periodo": "2025-04",
    "produccion_millon_l": 5.83
   },
   {
    "periodo": "2025-05",
    "produccion_millon_l": 2.57
   },
   {
    "periodo": "2025-06",
    "produccion_millon_l": 0.6
   },
   {
    "periodo": "2025-07",
    "produccion_millon_l": 0.23
   },
   {
    "periodo": "2025-08",
    "produccion_millon_l": 0.17
   },
   {
    "periodo": "2025-09",
    "produccion_millon_l": 0.17
   },
   {
    "periodo": "2025-10",
    "produccion_millon_l": 0.25
   },
   {
    "periodo": "2025-11",
    "produccion_millon_l": 0.41
   },
   {
    "periodo": "2025-12",
    "produccion_millon_l": 0.49
   }
  ]
 },
 {
  "id": "ecommerce",
  "nombre": "Pedidos diarios de e-commerce",
  "sector": "Comercio digital",
  "periodo": "diario",
  "m": 7,
  "caracteristicas": [
   "estacionalidad semanal",
   "tendencia",
   "ruido",
   "m=7"
  ],
  "descripcion": "Pedidos diarios durante 16 semanas: patrón semanal (peaks de fin de semana) con crecimiento. Ejemplo de estacionalidad NO anual (m=7) para Holt-Winters con período semanal.",
  "columns": [
   {
    "name": "dia",
    "type": "texto"
   },
   {
    "name": "dia_semana",
    "type": "texto"
   },
   {
    "name": "pedidos",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "dia": "D001",
    "dia_semana": "lun",
    "pedidos": 315
   },
   {
    "dia": "D002",
    "dia_semana": "mar",
    "pedidos": 324
   },
   {
    "dia": "D003",
    "dia_semana": "mié",
    "pedidos": 326
   },
   {
    "dia": "D004",
    "dia_semana": "jue",
    "pedidos": 316
   },
   {
    "dia": "D005",
    "dia_semana": "vie",
    "pedidos": 324
   },
   {
    "dia": "D006",
    "dia_semana": "sáb",
    "pedidos": 398
   },
   {
    "dia": "D007",
    "dia_semana": "dom",
    "pedidos": 449
   },
   {
    "dia": "D008",
    "dia_semana": "lun",
    "pedidos": 351
   },
   {
    "dia": "D009",
    "dia_semana": "mar",
    "pedidos": 302
   },
   {
    "dia": "D010",
    "dia_semana": "mié",
    "pedidos": 267
   },
   {
    "dia": "D011",
    "dia_semana": "jue",
    "pedidos": 321
   },
   {
    "dia": "D012",
    "dia_semana": "vie",
    "pedidos": 331
   },
   {
    "dia": "D013",
    "dia_semana": "sáb",
    "pedidos": 416
   },
   {
    "dia": "D014",
    "dia_semana": "dom",
    "pedidos": 446
   },
   {
    "dia": "D015",
    "dia_semana": "lun",
    "pedidos": 360
   },
   {
    "dia": "D016",
    "dia_semana": "mar",
    "pedidos": 327
   },
   {
    "dia": "D017",
    "dia_semana": "mié",
    "pedidos": 292
   },
   {
    "dia": "D018",
    "dia_semana": "jue",
    "pedidos": 325
   },
   {
    "dia": "D019",
    "dia_semana": "vie",
    "pedidos": 340
   },
   {
    "dia": "D020",
    "dia_semana": "sáb",
    "pedidos": 396
   },
   {
    "dia": "D021",
    "dia_semana": "dom",
    "pedidos": 432
   },
   {
    "dia": "D022",
    "dia_semana": "lun",
    "pedidos": 373
   },
   {
    "dia": "D023",
    "dia_semana": "mar",
    "pedidos": 324
   },
   {
    "dia": "D024",
    "dia_semana": "mié",
    "pedidos": 321
   },
   {
    "dia": "D025",
    "dia_semana": "jue",
    "pedidos": 329
   },
   {
    "dia": "D026",
    "dia_semana": "vie",
    "pedidos": 354
   },
   {
    "dia": "D027",
    "dia_semana": "sáb",
    "pedidos": 436
   },
   {
    "dia": "D028",
    "dia_semana": "dom",
    "pedidos": 411
   },
   {
    "dia": "D029",
    "dia_semana": "lun",
    "pedidos": 393
   },
   {
    "dia": "D030",
    "dia_semana": "mar",
    "pedidos": 328
   },
   {
    "dia": "D031",
    "dia_semana": "mié",
    "pedidos": 323
   },
   {
    "dia": "D032",
    "dia_semana": "jue",
    "pedidos": 332
   },
   {
    "dia": "D033",
    "dia_semana": "vie",
    "pedidos": 377
   },
   {
    "dia": "D034",
    "dia_semana": "sáb",
    "pedidos": 457
   },
   {
    "dia": "D035",
    "dia_semana": "dom",
    "pedidos": 502
   },
   {
    "dia": "D036",
    "dia_semana": "lun",
    "pedidos": 422
   },
   {
    "dia": "D037",
    "dia_semana": "mar",
    "pedidos": 342
   },
   {
    "dia": "D038",
    "dia_semana": "mié",
    "pedidos": 348
   },
   {
    "dia": "D039",
    "dia_semana": "jue",
    "pedidos": 359
   },
   {
    "dia": "D040",
    "dia_semana": "vie",
    "pedidos": 355
   },
   {
    "dia": "D041",
    "dia_semana": "sáb",
    "pedidos": 467
   },
   {
    "dia": "D042",
    "dia_semana": "dom",
    "pedidos": 501
   },
   {
    "dia": "D043",
    "dia_semana": "lun",
    "pedidos": 443
   },
   {
    "dia": "D044",
    "dia_semana": "mar",
    "pedidos": 355
   },
   {
    "dia": "D045",
    "dia_semana": "mié",
    "pedidos": 370
   },
   {
    "dia": "D046",
    "dia_semana": "jue",
    "pedidos": 378
   },
   {
    "dia": "D047",
    "dia_semana": "vie",
    "pedidos": 344
   },
   {
    "dia": "D048",
    "dia_semana": "sáb",
    "pedidos": 457
   },
   {
    "dia": "D049",
    "dia_semana": "dom",
    "pedidos": 526
   },
   {
    "dia": "D050",
    "dia_semana": "lun",
    "pedidos": 396
   },
   {
    "dia": "D051",
    "dia_semana": "mar",
    "pedidos": 379
   },
   {
    "dia": "D052",
    "dia_semana": "mié",
    "pedidos": 377
   },
   {
    "dia": "D053",
    "dia_semana": "jue",
    "pedidos": 368
   },
   {
    "dia": "D054",
    "dia_semana": "vie",
    "pedidos": 422
   },
   {
    "dia": "D055",
    "dia_semana": "sáb",
    "pedidos": 527
   },
   {
    "dia": "D056",
    "dia_semana": "dom",
    "pedidos": 523
   },
   {
    "dia": "D057",
    "dia_semana": "lun",
    "pedidos": 438
   },
   {
    "dia": "D058",
    "dia_semana": "mar",
    "pedidos": 383
   },
   {
    "dia": "D059",
    "dia_semana": "mié",
    "pedidos": 369
   },
   {
    "dia": "D060",
    "dia_semana": "jue",
    "pedidos": 353
   },
   {
    "dia": "D061",
    "dia_semana": "vie",
    "pedidos": 401
   },
   {
    "dia": "D062",
    "dia_semana": "sáb",
    "pedidos": 464
   },
   {
    "dia": "D063",
    "dia_semana": "dom",
    "pedidos": 528
   },
   {
    "dia": "D064",
    "dia_semana": "lun",
    "pedidos": 444
   },
   {
    "dia": "D065",
    "dia_semana": "mar",
    "pedidos": 354
   },
   {
    "dia": "D066",
    "dia_semana": "mié",
    "pedidos": 347
   },
   {
    "dia": "D067",
    "dia_semana": "jue",
    "pedidos": 384
   },
   {
    "dia": "D068",
    "dia_semana": "vie",
    "pedidos": 458
   },
   {
    "dia": "D069",
    "dia_semana": "sáb",
    "pedidos": 483
   },
   {
    "dia": "D070",
    "dia_semana": "dom",
    "pedidos": 553
   },
   {
    "dia": "D071",
    "dia_semana": "lun",
    "pedidos": 439
   },
   {
    "dia": "D072",
    "dia_semana": "mar",
    "pedidos": 391
   },
   {
    "dia": "D073",
    "dia_semana": "mié",
    "pedidos": 397
   },
   {
    "dia": "D074",
    "dia_semana": "jue",
    "pedidos": 407
   },
   {
    "dia": "D075",
    "dia_semana": "vie",
    "pedidos": 433
   },
   {
    "dia": "D076",
    "dia_semana": "sáb",
    "pedidos": 544
   },
   {
    "dia": "D077",
    "dia_semana": "dom",
    "pedidos": 579
   },
   {
    "dia": "D078",
    "dia_semana": "lun",
    "pedidos": 420
   },
   {
    "dia": "D079",
    "dia_semana": "mar",
    "pedidos": 416
   },
   {
    "dia": "D080",
    "dia_semana": "mié",
    "pedidos": 386
   },
   {
    "dia": "D081",
    "dia_semana": "jue",
    "pedidos": 419
   },
   {
    "dia": "D082",
    "dia_semana": "vie",
    "pedidos": 452
   },
   {
    "dia": "D083",
    "dia_semana": "sáb",
    "pedidos": 555
   },
   {
    "dia": "D084",
    "dia_semana": "dom",
    "pedidos": 596
   },
   {
    "dia": "D085",
    "dia_semana": "lun",
    "pedidos": 453
   },
   {
    "dia": "D086",
    "dia_semana": "mar",
    "pedidos": 426
   },
   {
    "dia": "D087",
    "dia_semana": "mié",
    "pedidos": 394
   },
   {
    "dia": "D088",
    "dia_semana": "jue",
    "pedidos": 418
   },
   {
    "dia": "D089",
    "dia_semana": "vie",
    "pedidos": 472
   },
   {
    "dia": "D090",
    "dia_semana": "sáb",
    "pedidos": 542
   },
   {
    "dia": "D091",
    "dia_semana": "dom",
    "pedidos": 569
   },
   {
    "dia": "D092",
    "dia_semana": "lun",
    "pedidos": 460
   },
   {
    "dia": "D093",
    "dia_semana": "mar",
    "pedidos": 420
   },
   {
    "dia": "D094",
    "dia_semana": "mié",
    "pedidos": 427
   },
   {
    "dia": "D095",
    "dia_semana": "jue",
    "pedidos": 393
   },
   {
    "dia": "D096",
    "dia_semana": "vie",
    "pedidos": 459
   },
   {
    "dia": "D097",
    "dia_semana": "sáb",
    "pedidos": 496
   },
   {
    "dia": "D098",
    "dia_semana": "dom",
    "pedidos": 581
   },
   {
    "dia": "D099",
    "dia_semana": "lun",
    "pedidos": 514
   },
   {
    "dia": "D100",
    "dia_semana": "mar",
    "pedidos": 424
   },
   {
    "dia": "D101",
    "dia_semana": "mié",
    "pedidos": 389
   },
   {
    "dia": "D102",
    "dia_semana": "jue",
    "pedidos": 430
   },
   {
    "dia": "D103",
    "dia_semana": "vie",
    "pedidos": 486
   },
   {
    "dia": "D104",
    "dia_semana": "sáb",
    "pedidos": 624
   },
   {
    "dia": "D105",
    "dia_semana": "dom",
    "pedidos": 661
   },
   {
    "dia": "D106",
    "dia_semana": "lun",
    "pedidos": 531
   },
   {
    "dia": "D107",
    "dia_semana": "mar",
    "pedidos": 453
   },
   {
    "dia": "D108",
    "dia_semana": "mié",
    "pedidos": 444
   },
   {
    "dia": "D109",
    "dia_semana": "jue",
    "pedidos": 422
   },
   {
    "dia": "D110",
    "dia_semana": "vie",
    "pedidos": 450
   },
   {
    "dia": "D111",
    "dia_semana": "sáb",
    "pedidos": 631
   },
   {
    "dia": "D112",
    "dia_semana": "dom",
    "pedidos": 654
   }
  ]
 },
 {
  "id": "sueldos",
  "nombre": "Sueldos mensuales (muestra)",
  "sector": "Recursos Humanos",
  "periodo": "transversal",
  "m": 0,
  "caracteristicas": [
   "distribución sesgada",
   "asimetría positiva",
   "atípicos"
  ],
  "descripcion": "Muestra de 200 sueldos (CLP): distribución asimétrica a la derecha con algunos valores muy altos. Pensado para estadística descriptiva (media vs. mediana, CV, asimetría y detección de atípicos).",
  "columns": [
   {
    "name": "trabajador",
    "type": "texto"
   },
   {
    "name": "sueldo_clp",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "trabajador": "T001",
    "sueldo_clp": 1053000
   },
   {
    "trabajador": "T002",
    "sueldo_clp": 760000
   },
   {
    "trabajador": "T003",
    "sueldo_clp": 450000
   },
   {
    "trabajador": "T004",
    "sueldo_clp": 396000
   },
   {
    "trabajador": "T005",
    "sueldo_clp": 1087000
   },
   {
    "trabajador": "T006",
    "sueldo_clp": 1169000
   },
   {
    "trabajador": "T007",
    "sueldo_clp": 388000
   },
   {
    "trabajador": "T008",
    "sueldo_clp": 470000
   },
   {
    "trabajador": "T009",
    "sueldo_clp": 646000
   },
   {
    "trabajador": "T010",
    "sueldo_clp": 1053000
   },
   {
    "trabajador": "T011",
    "sueldo_clp": 574000
   },
   {
    "trabajador": "T012",
    "sueldo_clp": 444000
   },
   {
    "trabajador": "T013",
    "sueldo_clp": 1115000
   },
   {
    "trabajador": "T014",
    "sueldo_clp": 917000
   },
   {
    "trabajador": "T015",
    "sueldo_clp": 481000
   },
   {
    "trabajador": "T016",
    "sueldo_clp": 489000
   },
   {
    "trabajador": "T017",
    "sueldo_clp": 1185000
   },
   {
    "trabajador": "T018",
    "sueldo_clp": 358000
   },
   {
    "trabajador": "T019",
    "sueldo_clp": 587000
   },
   {
    "trabajador": "T020",
    "sueldo_clp": 851000
   },
   {
    "trabajador": "T021",
    "sueldo_clp": 738000
   },
   {
    "trabajador": "T022",
    "sueldo_clp": 1082000
   },
   {
    "trabajador": "T023",
    "sueldo_clp": 289000
   },
   {
    "trabajador": "T024",
    "sueldo_clp": 686000
   },
   {
    "trabajador": "T025",
    "sueldo_clp": 791000
   },
   {
    "trabajador": "T026",
    "sueldo_clp": 803000
   },
   {
    "trabajador": "T027",
    "sueldo_clp": 907000
   },
   {
    "trabajador": "T028",
    "sueldo_clp": 379000
   },
   {
    "trabajador": "T029",
    "sueldo_clp": 1401000
   },
   {
    "trabajador": "T030",
    "sueldo_clp": 853000
   },
   {
    "trabajador": "T031",
    "sueldo_clp": 900000
   },
   {
    "trabajador": "T032",
    "sueldo_clp": 510000
   },
   {
    "trabajador": "T033",
    "sueldo_clp": 744000
   },
   {
    "trabajador": "T034",
    "sueldo_clp": 1323000
   },
   {
    "trabajador": "T035",
    "sueldo_clp": 675000
   },
   {
    "trabajador": "T036",
    "sueldo_clp": 750000
   },
   {
    "trabajador": "T037",
    "sueldo_clp": 797000
   },
   {
    "trabajador": "T038",
    "sueldo_clp": 301000
   },
   {
    "trabajador": "T039",
    "sueldo_clp": 624000
   },
   {
    "trabajador": "T040",
    "sueldo_clp": 962000
   },
   {
    "trabajador": "T041",
    "sueldo_clp": 533000
   },
   {
    "trabajador": "T042",
    "sueldo_clp": 666000
   },
   {
    "trabajador": "T043",
    "sueldo_clp": 669000
   },
   {
    "trabajador": "T044",
    "sueldo_clp": 309000
   },
   {
    "trabajador": "T045",
    "sueldo_clp": 1017000
   },
   {
    "trabajador": "T046",
    "sueldo_clp": 346000
   },
   {
    "trabajador": "T047",
    "sueldo_clp": 840000
   },
   {
    "trabajador": "T048",
    "sueldo_clp": 636000
   },
   {
    "trabajador": "T049",
    "sueldo_clp": 573000
   },
   {
    "trabajador": "T050",
    "sueldo_clp": 703000
   },
   {
    "trabajador": "T051",
    "sueldo_clp": 991000
   },
   {
    "trabajador": "T052",
    "sueldo_clp": 1021000
   },
   {
    "trabajador": "T053",
    "sueldo_clp": 548000
   },
   {
    "trabajador": "T054",
    "sueldo_clp": 626000
   },
   {
    "trabajador": "T055",
    "sueldo_clp": 442000
   },
   {
    "trabajador": "T056",
    "sueldo_clp": 327000
   },
   {
    "trabajador": "T057",
    "sueldo_clp": 1094000
   },
   {
    "trabajador": "T058",
    "sueldo_clp": 393000
   },
   {
    "trabajador": "T059",
    "sueldo_clp": 471000
   },
   {
    "trabajador": "T060",
    "sueldo_clp": 822000
   },
   {
    "trabajador": "T061",
    "sueldo_clp": 347000
   },
   {
    "trabajador": "T062",
    "sueldo_clp": 864000
   },
   {
    "trabajador": "T063",
    "sueldo_clp": 446000
   },
   {
    "trabajador": "T064",
    "sueldo_clp": 385000
   },
   {
    "trabajador": "T065",
    "sueldo_clp": 509000
   },
   {
    "trabajador": "T066",
    "sueldo_clp": 444000
   },
   {
    "trabajador": "T067",
    "sueldo_clp": 765000
   },
   {
    "trabajador": "T068",
    "sueldo_clp": 1382000
   },
   {
    "trabajador": "T069",
    "sueldo_clp": 953000
   },
   {
    "trabajador": "T070",
    "sueldo_clp": 858000
   },
   {
    "trabajador": "T071",
    "sueldo_clp": 500000
   },
   {
    "trabajador": "T072",
    "sueldo_clp": 603000
   },
   {
    "trabajador": "T073",
    "sueldo_clp": 712000
   },
   {
    "trabajador": "T074",
    "sueldo_clp": 655000
   },
   {
    "trabajador": "T075",
    "sueldo_clp": 724000
   },
   {
    "trabajador": "T076",
    "sueldo_clp": 369000
   },
   {
    "trabajador": "T077",
    "sueldo_clp": 1623000
   },
   {
    "trabajador": "T078",
    "sueldo_clp": 343000
   },
   {
    "trabajador": "T079",
    "sueldo_clp": 620000
   },
   {
    "trabajador": "T080",
    "sueldo_clp": 1008000
   },
   {
    "trabajador": "T081",
    "sueldo_clp": 459000
   },
   {
    "trabajador": "T082",
    "sueldo_clp": 1125000
   },
   {
    "trabajador": "T083",
    "sueldo_clp": 328000
   },
   {
    "trabajador": "T084",
    "sueldo_clp": 458000
   },
   {
    "trabajador": "T085",
    "sueldo_clp": 205000
   },
   {
    "trabajador": "T086",
    "sueldo_clp": 1113000
   },
   {
    "trabajador": "T087",
    "sueldo_clp": 365000
   },
   {
    "trabajador": "T088",
    "sueldo_clp": 469000
   },
   {
    "trabajador": "T089",
    "sueldo_clp": 971000
   },
   {
    "trabajador": "T090",
    "sueldo_clp": 785000
   },
   {
    "trabajador": "T091",
    "sueldo_clp": 1125000
   },
   {
    "trabajador": "T092",
    "sueldo_clp": 913000
   },
   {
    "trabajador": "T093",
    "sueldo_clp": 1031000
   },
   {
    "trabajador": "T094",
    "sueldo_clp": 519000
   },
   {
    "trabajador": "T095",
    "sueldo_clp": 632000
   },
   {
    "trabajador": "T096",
    "sueldo_clp": 954000
   },
   {
    "trabajador": "T097",
    "sueldo_clp": 961000
   },
   {
    "trabajador": "T098",
    "sueldo_clp": 1058000
   },
   {
    "trabajador": "T099",
    "sueldo_clp": 449000
   },
   {
    "trabajador": "T100",
    "sueldo_clp": 381000
   },
   {
    "trabajador": "T101",
    "sueldo_clp": 352000
   },
   {
    "trabajador": "T102",
    "sueldo_clp": 520000
   },
   {
    "trabajador": "T103",
    "sueldo_clp": 626000
   },
   {
    "trabajador": "T104",
    "sueldo_clp": 363000
   },
   {
    "trabajador": "T105",
    "sueldo_clp": 601000
   },
   {
    "trabajador": "T106",
    "sueldo_clp": 903000
   },
   {
    "trabajador": "T107",
    "sueldo_clp": 1080000
   },
   {
    "trabajador": "T108",
    "sueldo_clp": 491000
   },
   {
    "trabajador": "T109",
    "sueldo_clp": 875000
   },
   {
    "trabajador": "T110",
    "sueldo_clp": 348000
   },
   {
    "trabajador": "T111",
    "sueldo_clp": 474000
   },
   {
    "trabajador": "T112",
    "sueldo_clp": 695000
   },
   {
    "trabajador": "T113",
    "sueldo_clp": 477000
   },
   {
    "trabajador": "T114",
    "sueldo_clp": 446000
   },
   {
    "trabajador": "T115",
    "sueldo_clp": 753000
   },
   {
    "trabajador": "T116",
    "sueldo_clp": 401000
   },
   {
    "trabajador": "T117",
    "sueldo_clp": 696000
   },
   {
    "trabajador": "T118",
    "sueldo_clp": 624000
   },
   {
    "trabajador": "T119",
    "sueldo_clp": 849000
   },
   {
    "trabajador": "T120",
    "sueldo_clp": 960000
   },
   {
    "trabajador": "T121",
    "sueldo_clp": 704000
   },
   {
    "trabajador": "T122",
    "sueldo_clp": 513000
   },
   {
    "trabajador": "T123",
    "sueldo_clp": 1089000
   },
   {
    "trabajador": "T124",
    "sueldo_clp": 726000
   },
   {
    "trabajador": "T125",
    "sueldo_clp": 424000
   },
   {
    "trabajador": "T126",
    "sueldo_clp": 717000
   },
   {
    "trabajador": "T127",
    "sueldo_clp": 484000
   },
   {
    "trabajador": "T128",
    "sueldo_clp": 186000
   },
   {
    "trabajador": "T129",
    "sueldo_clp": 407000
   },
   {
    "trabajador": "T130",
    "sueldo_clp": 544000
   },
   {
    "trabajador": "T131",
    "sueldo_clp": 523000
   },
   {
    "trabajador": "T132",
    "sueldo_clp": 305000
   },
   {
    "trabajador": "T133",
    "sueldo_clp": 552000
   },
   {
    "trabajador": "T134",
    "sueldo_clp": 814000
   },
   {
    "trabajador": "T135",
    "sueldo_clp": 372000
   },
   {
    "trabajador": "T136",
    "sueldo_clp": 748000
   },
   {
    "trabajador": "T137",
    "sueldo_clp": 239000
   },
   {
    "trabajador": "T138",
    "sueldo_clp": 847000
   },
   {
    "trabajador": "T139",
    "sueldo_clp": 495000
   },
   {
    "trabajador": "T140",
    "sueldo_clp": 336000
   },
   {
    "trabajador": "T141",
    "sueldo_clp": 1144000
   },
   {
    "trabajador": "T142",
    "sueldo_clp": 829000
   },
   {
    "trabajador": "T143",
    "sueldo_clp": 1056000
   },
   {
    "trabajador": "T144",
    "sueldo_clp": 767000
   },
   {
    "trabajador": "T145",
    "sueldo_clp": 781000
   },
   {
    "trabajador": "T146",
    "sueldo_clp": 542000
   },
   {
    "trabajador": "T147",
    "sueldo_clp": 811000
   },
   {
    "trabajador": "T148",
    "sueldo_clp": 630000
   },
   {
    "trabajador": "T149",
    "sueldo_clp": 477000
   },
   {
    "trabajador": "T150",
    "sueldo_clp": 597000
   },
   {
    "trabajador": "T151",
    "sueldo_clp": 347000
   },
   {
    "trabajador": "T152",
    "sueldo_clp": 648000
   },
   {
    "trabajador": "T153",
    "sueldo_clp": 817000
   },
   {
    "trabajador": "T154",
    "sueldo_clp": 698000
   },
   {
    "trabajador": "T155",
    "sueldo_clp": 871000
   },
   {
    "trabajador": "T156",
    "sueldo_clp": 562000
   },
   {
    "trabajador": "T157",
    "sueldo_clp": 667000
   },
   {
    "trabajador": "T158",
    "sueldo_clp": 665000
   },
   {
    "trabajador": "T159",
    "sueldo_clp": 1714000
   },
   {
    "trabajador": "T160",
    "sueldo_clp": 343000
   },
   {
    "trabajador": "T161",
    "sueldo_clp": 1791000
   },
   {
    "trabajador": "T162",
    "sueldo_clp": 456000
   },
   {
    "trabajador": "T163",
    "sueldo_clp": 555000
   },
   {
    "trabajador": "T164",
    "sueldo_clp": 753000
   },
   {
    "trabajador": "T165",
    "sueldo_clp": 875000
   },
   {
    "trabajador": "T166",
    "sueldo_clp": 648000
   },
   {
    "trabajador": "T167",
    "sueldo_clp": 733000
   },
   {
    "trabajador": "T168",
    "sueldo_clp": 1311000
   },
   {
    "trabajador": "T169",
    "sueldo_clp": 2388000
   },
   {
    "trabajador": "T170",
    "sueldo_clp": 805000
   },
   {
    "trabajador": "T171",
    "sueldo_clp": 929000
   },
   {
    "trabajador": "T172",
    "sueldo_clp": 626000
   },
   {
    "trabajador": "T173",
    "sueldo_clp": 1498000
   },
   {
    "trabajador": "T174",
    "sueldo_clp": 622000
   },
   {
    "trabajador": "T175",
    "sueldo_clp": 847000
   },
   {
    "trabajador": "T176",
    "sueldo_clp": 392000
   },
   {
    "trabajador": "T177",
    "sueldo_clp": 176000
   },
   {
    "trabajador": "T178",
    "sueldo_clp": 2026000
   },
   {
    "trabajador": "T179",
    "sueldo_clp": 1117000
   },
   {
    "trabajador": "T180",
    "sueldo_clp": 1037000
   },
   {
    "trabajador": "T181",
    "sueldo_clp": 415000
   },
   {
    "trabajador": "T182",
    "sueldo_clp": 294000
   },
   {
    "trabajador": "T183",
    "sueldo_clp": 586000
   },
   {
    "trabajador": "T184",
    "sueldo_clp": 698000
   },
   {
    "trabajador": "T185",
    "sueldo_clp": 942000
   },
   {
    "trabajador": "T186",
    "sueldo_clp": 663000
   },
   {
    "trabajador": "T187",
    "sueldo_clp": 1242000
   },
   {
    "trabajador": "T188",
    "sueldo_clp": 783000
   },
   {
    "trabajador": "T189",
    "sueldo_clp": 768000
   },
   {
    "trabajador": "T190",
    "sueldo_clp": 1172000
   },
   {
    "trabajador": "T191",
    "sueldo_clp": 474000
   },
   {
    "trabajador": "T192",
    "sueldo_clp": 798000
   },
   {
    "trabajador": "T193",
    "sueldo_clp": 501000
   },
   {
    "trabajador": "T194",
    "sueldo_clp": 472000
   },
   {
    "trabajador": "T195",
    "sueldo_clp": 1394000
   },
   {
    "trabajador": "T196",
    "sueldo_clp": 1133000
   },
   {
    "trabajador": "T197",
    "sueldo_clp": 860000
   },
   {
    "trabajador": "T198",
    "sueldo_clp": 1261000
   },
   {
    "trabajador": "T199",
    "sueldo_clp": 795000
   },
   {
    "trabajador": "T200",
    "sueldo_clp": 1289000
   }
  ]
 },
 {
  "id": "viviendas",
  "nombre": "Precio de viviendas vs. superficie",
  "sector": "Inmobiliario",
  "periodo": "transversal",
  "m": 0,
  "caracteristicas": [
   "relación positiva",
   "no lineal",
   "regresión"
  ],
  "descripcion": "Superficie (m²) y precio (UF) de 45 departamentos del Gran Santiago. Relación positiva con curvatura: ideal para comparar ajuste lineal vs. polinómico/exponencial.",
  "columns": [
   {
    "name": "comuna",
    "type": "texto"
   },
   {
    "name": "superficie_m2",
    "type": "numérico"
   },
   {
    "name": "precio_uf",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "comuna": "Maipú",
    "superficie_m2": 47.3,
    "precio_uf": 71
   },
   {
    "comuna": "La Florida",
    "superficie_m2": 89.9,
    "precio_uf": 94
   },
   {
    "comuna": "Ñuñoa",
    "superficie_m2": 128.4,
    "precio_uf": 194
   },
   {
    "comuna": "Providencia",
    "superficie_m2": 75.8,
    "precio_uf": 105
   },
   {
    "comuna": "Las Condes",
    "superficie_m2": 119.5,
    "precio_uf": 320
   },
   {
    "comuna": "Puente Alto",
    "superficie_m2": 119.6,
    "precio_uf": 276
   },
   {
    "comuna": "Santiago",
    "superficie_m2": 86.2,
    "precio_uf": 211
   },
   {
    "comuna": "Vitacura",
    "superficie_m2": 100.2,
    "precio_uf": 115
   },
   {
    "comuna": "Maipú",
    "superficie_m2": 70.9,
    "precio_uf": 28
   },
   {
    "comuna": "La Florida",
    "superficie_m2": 67.7,
    "precio_uf": 20
   },
   {
    "comuna": "Ñuñoa",
    "superficie_m2": 74.1,
    "precio_uf": 106
   },
   {
    "comuna": "Providencia",
    "superficie_m2": 65.4,
    "precio_uf": 185
   },
   {
    "comuna": "Las Condes",
    "superficie_m2": 120.0,
    "precio_uf": 190
   },
   {
    "comuna": "Puente Alto",
    "superficie_m2": 136.0,
    "precio_uf": 357
   },
   {
    "comuna": "Santiago",
    "superficie_m2": 159.7,
    "precio_uf": 295
   },
   {
    "comuna": "Vitacura",
    "superficie_m2": 158.2,
    "precio_uf": 479
   },
   {
    "comuna": "Maipú",
    "superficie_m2": 153.1,
    "precio_uf": 350
   },
   {
    "comuna": "La Florida",
    "superficie_m2": 159.3,
    "precio_uf": 727
   },
   {
    "comuna": "Ñuñoa",
    "superficie_m2": 54.8,
    "precio_uf": 146
   },
   {
    "comuna": "Providencia",
    "superficie_m2": 77.7,
    "precio_uf": 79
   },
   {
    "comuna": "Las Condes",
    "superficie_m2": 164.4,
    "precio_uf": 645
   },
   {
    "comuna": "Puente Alto",
    "superficie_m2": 74.4,
    "precio_uf": 84
   },
   {
    "comuna": "Santiago",
    "superficie_m2": 145.3,
    "precio_uf": 311
   },
   {
    "comuna": "Vitacura",
    "superficie_m2": 149.4,
    "precio_uf": 270
   },
   {
    "comuna": "Maipú",
    "superficie_m2": 155.2,
    "precio_uf": 488
   },
   {
    "comuna": "La Florida",
    "superficie_m2": 153.6,
    "precio_uf": 327
   },
   {
    "comuna": "Ñuñoa",
    "superficie_m2": 130.2,
    "precio_uf": 403
   },
   {
    "comuna": "Providencia",
    "superficie_m2": 108.1,
    "precio_uf": 221
   },
   {
    "comuna": "Las Condes",
    "superficie_m2": 160.1,
    "precio_uf": 471
   },
   {
    "comuna": "Puente Alto",
    "superficie_m2": 73.0,
    "precio_uf": 164
   },
   {
    "comuna": "Santiago",
    "superficie_m2": 143.0,
    "precio_uf": 290
   },
   {
    "comuna": "Vitacura",
    "superficie_m2": 120.2,
    "precio_uf": 20
   },
   {
    "comuna": "Maipú",
    "superficie_m2": 114.0,
    "precio_uf": 244
   },
   {
    "comuna": "La Florida",
    "superficie_m2": 102.5,
    "precio_uf": 206
   },
   {
    "comuna": "Ñuñoa",
    "superficie_m2": 70.7,
    "precio_uf": 156
   },
   {
    "comuna": "Providencia",
    "superficie_m2": 49.2,
    "precio_uf": 99
   },
   {
    "comuna": "Las Condes",
    "superficie_m2": 95.0,
    "precio_uf": 142
   },
   {
    "comuna": "Puente Alto",
    "superficie_m2": 104.0,
    "precio_uf": 248
   },
   {
    "comuna": "Santiago",
    "superficie_m2": 56.6,
    "precio_uf": 20
   },
   {
    "comuna": "Vitacura",
    "superficie_m2": 78.7,
    "precio_uf": 192
   },
   {
    "comuna": "Maipú",
    "superficie_m2": 70.7,
    "precio_uf": 111
   },
   {
    "comuna": "La Florida",
    "superficie_m2": 67.3,
    "precio_uf": 133
   },
   {
    "comuna": "Ñuñoa",
    "superficie_m2": 137.5,
    "precio_uf": 502
   },
   {
    "comuna": "Providencia",
    "superficie_m2": 86.6,
    "precio_uf": 158
   },
   {
    "comuna": "Las Condes",
    "superficie_m2": 135.6,
    "precio_uf": 434
   }
  ]
 },
 {
  "id": "estudio",
  "nombre": "Horas de estudio vs. nota",
  "sector": "Educación",
  "periodo": "transversal",
  "m": 0,
  "caracteristicas": [
   "relación logarítmica",
   "rendimientos decrecientes",
   "regresión"
  ],
  "descripcion": "Horas de estudio y nota final (1–7) de 60 estudiantes. Rendimientos decrecientes: el ajuste logarítmico supera al lineal. Bueno para comparar modelos de regresión.",
  "columns": [
   {
    "name": "estudiante",
    "type": "texto"
   },
   {
    "name": "horas_estudio",
    "type": "numérico"
   },
   {
    "name": "nota",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "estudiante": "E001",
    "horas_estudio": 16.3,
    "nota": 5.8
   },
   {
    "estudiante": "E002",
    "horas_estudio": 24.1,
    "nota": 6.1
   },
   {
    "estudiante": "E003",
    "horas_estudio": 26.3,
    "nota": 5.9
   },
   {
    "estudiante": "E004",
    "horas_estudio": 3.3,
    "nota": 3.6
   },
   {
    "estudiante": "E005",
    "horas_estudio": 8.8,
    "nota": 5.3
   },
   {
    "estudiante": "E006",
    "horas_estudio": 21.2,
    "nota": 5.6
   },
   {
    "estudiante": "E007",
    "horas_estudio": 17.5,
    "nota": 5.2
   },
   {
    "estudiante": "E008",
    "horas_estudio": 23.0,
    "nota": 6.1
   },
   {
    "estudiante": "E009",
    "horas_estudio": 20.4,
    "nota": 6.2
   },
   {
    "estudiante": "E010",
    "horas_estudio": 0.6,
    "nota": 2.7
   },
   {
    "estudiante": "E011",
    "horas_estudio": 20.1,
    "nota": 6.1
   },
   {
    "estudiante": "E012",
    "horas_estudio": 8.6,
    "nota": 4.5
   },
   {
    "estudiante": "E013",
    "horas_estudio": 24.7,
    "nota": 6.2
   },
   {
    "estudiante": "E014",
    "horas_estudio": 19.1,
    "nota": 5.9
   },
   {
    "estudiante": "E015",
    "horas_estudio": 17.7,
    "nota": 6.2
   },
   {
    "estudiante": "E016",
    "horas_estudio": 18.3,
    "nota": 5.9
   },
   {
    "estudiante": "E017",
    "horas_estudio": 7.9,
    "nota": 4.8
   },
   {
    "estudiante": "E018",
    "horas_estudio": 20.0,
    "nota": 5.3
   },
   {
    "estudiante": "E019",
    "horas_estudio": 19.4,
    "nota": 6.2
   },
   {
    "estudiante": "E020",
    "horas_estudio": 22.7,
    "nota": 6.3
   },
   {
    "estudiante": "E021",
    "horas_estudio": 23.1,
    "nota": 5.0
   },
   {
    "estudiante": "E022",
    "horas_estudio": 2.3,
    "nota": 3.2
   },
   {
    "estudiante": "E023",
    "horas_estudio": 1.7,
    "nota": 3.0
   },
   {
    "estudiante": "E024",
    "horas_estudio": 7.9,
    "nota": 4.5
   },
   {
    "estudiante": "E025",
    "horas_estudio": 9.2,
    "nota": 4.2
   },
   {
    "estudiante": "E026",
    "horas_estudio": 24.1,
    "nota": 6.6
   },
   {
    "estudiante": "E027",
    "horas_estudio": 13.0,
    "nota": 5.3
   },
   {
    "estudiante": "E028",
    "horas_estudio": 5.3,
    "nota": 5.1
   },
   {
    "estudiante": "E029",
    "horas_estudio": 9.6,
    "nota": 5.5
   },
   {
    "estudiante": "E030",
    "horas_estudio": 1.4,
    "nota": 2.7
   },
   {
    "estudiante": "E031",
    "horas_estudio": 13.2,
    "nota": 5.2
   },
   {
    "estudiante": "E032",
    "horas_estudio": 24.5,
    "nota": 6.2
   },
   {
    "estudiante": "E033",
    "horas_estudio": 27.0,
    "nota": 6.4
   },
   {
    "estudiante": "E034",
    "horas_estudio": 26.7,
    "nota": 6.5
   },
   {
    "estudiante": "E035",
    "horas_estudio": 25.1,
    "nota": 6.2
   },
   {
    "estudiante": "E036",
    "horas_estudio": 24.7,
    "nota": 6.0
   },
   {
    "estudiante": "E037",
    "horas_estudio": 4.0,
    "nota": 4.0
   },
   {
    "estudiante": "E038",
    "horas_estudio": 13.7,
    "nota": 5.0
   },
   {
    "estudiante": "E039",
    "horas_estudio": 11.7,
    "nota": 5.1
   },
   {
    "estudiante": "E040",
    "horas_estudio": 1.2,
    "nota": 2.4
   },
   {
    "estudiante": "E041",
    "horas_estudio": 2.5,
    "nota": 3.4
   },
   {
    "estudiante": "E042",
    "horas_estudio": 18.4,
    "nota": 5.8
   },
   {
    "estudiante": "E043",
    "horas_estudio": 27.4,
    "nota": 6.0
   },
   {
    "estudiante": "E044",
    "horas_estudio": 26.1,
    "nota": 6.5
   },
   {
    "estudiante": "E045",
    "horas_estudio": 12.5,
    "nota": 5.6
   },
   {
    "estudiante": "E046",
    "horas_estudio": 12.1,
    "nota": 4.9
   },
   {
    "estudiante": "E047",
    "horas_estudio": 1.5,
    "nota": 3.4
   },
   {
    "estudiante": "E048",
    "horas_estudio": 10.3,
    "nota": 5.3
   },
   {
    "estudiante": "E049",
    "horas_estudio": 12.2,
    "nota": 5.1
   },
   {
    "estudiante": "E050",
    "horas_estudio": 15.6,
    "nota": 5.9
   },
   {
    "estudiante": "E051",
    "horas_estudio": 20.3,
    "nota": 6.0
   },
   {
    "estudiante": "E052",
    "horas_estudio": 22.4,
    "nota": 6.8
   },
   {
    "estudiante": "E053",
    "horas_estudio": 0.7,
    "nota": 2.2
   },
   {
    "estudiante": "E054",
    "horas_estudio": 26.4,
    "nota": 6.5
   },
   {
    "estudiante": "E055",
    "horas_estudio": 16.5,
    "nota": 5.6
   },
   {
    "estudiante": "E056",
    "horas_estudio": 6.1,
    "nota": 4.3
   },
   {
    "estudiante": "E057",
    "horas_estudio": 16.6,
    "nota": 4.7
   },
   {
    "estudiante": "E058",
    "horas_estudio": 26.9,
    "nota": 6.7
   },
   {
    "estudiante": "E059",
    "horas_estudio": 23.0,
    "nota": 6.3
   },
   {
    "estudiante": "E060",
    "horas_estudio": 12.6,
    "nota": 5.3
   }
  ]
 },
 {
  "id": "precio_demanda",
  "nombre": "Precio vs. demanda",
  "sector": "Comercio",
  "periodo": "transversal",
  "m": 0,
  "caracteristicas": [
   "relación negativa",
   "exponencial",
   "regresión"
  ],
  "descripcion": "Precio (CLP) y unidades demandadas de un producto: relación negativa decreciente (elasticidad). Caso típico para ajuste exponencial o logarítmico.",
  "columns": [
   {
    "name": "precio_clp",
    "type": "numérico"
   },
   {
    "name": "demanda_unid",
    "type": "numérico"
   }
  ],
  "rows": [
   {
    "precio_clp": 2280,
    "demanda_unid": 738
   },
   {
    "precio_clp": 1400,
    "demanda_unid": 1528
   },
   {
    "precio_clp": 680,
    "demanda_unid": 2807
   },
   {
    "precio_clp": 1690,
    "demanda_unid": 1154
   },
   {
    "precio_clp": 2130,
    "demanda_unid": 731
   },
   {
    "precio_clp": 2280,
    "demanda_unid": 692
   },
   {
    "precio_clp": 550,
    "demanda_unid": 3353
   },
   {
    "precio_clp": 580,
    "demanda_unid": 3208
   },
   {
    "precio_clp": 1280,
    "demanda_unid": 1792
   },
   {
    "precio_clp": 980,
    "demanda_unid": 2188
   },
   {
    "precio_clp": 1480,
    "demanda_unid": 1561
   },
   {
    "precio_clp": 2210,
    "demanda_unid": 759
   },
   {
    "precio_clp": 2180,
    "demanda_unid": 798
   },
   {
    "precio_clp": 1880,
    "demanda_unid": 940
   },
   {
    "precio_clp": 670,
    "demanda_unid": 2998
   },
   {
    "precio_clp": 2310,
    "demanda_unid": 543
   },
   {
    "precio_clp": 940,
    "demanda_unid": 2274
   },
   {
    "precio_clp": 1110,
    "demanda_unid": 1941
   },
   {
    "precio_clp": 640,
    "demanda_unid": 3088
   },
   {
    "precio_clp": 600,
    "demanda_unid": 3178
   },
   {
    "precio_clp": 2320,
    "demanda_unid": 670
   },
   {
    "precio_clp": 2100,
    "demanda_unid": 936
   },
   {
    "precio_clp": 1160,
    "demanda_unid": 1908
   },
   {
    "precio_clp": 2350,
    "demanda_unid": 616
   },
   {
    "precio_clp": 1360,
    "demanda_unid": 1637
   },
   {
    "precio_clp": 2060,
    "demanda_unid": 863
   },
   {
    "precio_clp": 1680,
    "demanda_unid": 1186
   },
   {
    "precio_clp": 940,
    "demanda_unid": 2192
   },
   {
    "precio_clp": 1820,
    "demanda_unid": 1066
   },
   {
    "precio_clp": 1150,
    "demanda_unid": 1940
   },
   {
    "precio_clp": 980,
    "demanda_unid": 2152
   },
   {
    "precio_clp": 970,
    "demanda_unid": 2335
   },
   {
    "precio_clp": 2240,
    "demanda_unid": 747
   },
   {
    "precio_clp": 870,
    "demanda_unid": 2630
   },
   {
    "precio_clp": 1070,
    "demanda_unid": 1981
   },
   {
    "precio_clp": 1090,
    "demanda_unid": 2084
   },
   {
    "precio_clp": 1490,
    "demanda_unid": 1499
   },
   {
    "precio_clp": 920,
    "demanda_unid": 2364
   },
   {
    "precio_clp": 700,
    "demanda_unid": 2859
   },
   {
    "precio_clp": 680,
    "demanda_unid": 3060
   }
  ]
 }
]


def catalogo():
    """Metadatos de todos los ejemplos (sin las filas)."""
    return [{k: v for k, v in d.items() if k != "rows"} | {"n": len(d["rows"])}
            for d in DATASETS]


def obtener(ds_id):
    """Devuelve un dataset completo por id, o None."""
    for d in DATASETS:
        if d["id"] == ds_id:
            return d
    return None
