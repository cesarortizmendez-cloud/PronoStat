import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from . import solver
from . import datasets as catalogo_ds


def index(request):
    return render(request, 'datos/index.html')


@require_GET
def examples_api(request):
    """Catálogo de ejemplos (metadatos, sin filas)."""
    return JsonResponse({'datasets': catalogo_ds.catalogo()})


@require_GET
def example_api(request):
    """Un dataset de ejemplo completo por id."""
    ds = catalogo_ds.obtener(request.GET.get('id', ''))
    if not ds:
        return JsonResponse({'error': 'Ejemplo no encontrado.'}, status=404)
    return JsonResponse({'id': ds['id'], 'nombre': ds['nombre'], 'm': ds.get('m', 12),
                         'columns': ds['columns'], 'rows': ds['rows']})


def _body(request):
    return json.loads(request.body.decode('utf-8') or '{}')


@csrf_exempt
@require_POST
def analyze_api(request):
    try:
        p = _body(request)
        columns = p['columns']
        rows = p['rows']
        if not rows:
            return JsonResponse({'error': 'El archivo/hoja no contiene filas.'}, status=400)
        return JsonResponse(solver.analyze(columns, rows))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def clean_api(request):
    try:
        p = _body(request)
        result = solver.clean(p['columns'], p['rows'], p.get('options', {}))
        if not result['rows']:
            return JsonResponse({'error': 'La limpieza dejó 0 filas. Revisa la política de nulos.'}, status=400)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
