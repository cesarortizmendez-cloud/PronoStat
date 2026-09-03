import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'datos/index.html')


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
