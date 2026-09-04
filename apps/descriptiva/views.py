import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'descriptiva/index.html')


@csrf_exempt
@require_POST
def solve_api(request):
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.describe(p['values'], p.get('bins', 'auto')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def explore_api(request):
    """Descriptiva avanzada con segmentación opcional por grupos."""
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.explore(p['values'], p.get('groups'), p.get('bins', 'auto')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def tabla_api(request):
    """Tabla de distribución de frecuencias (monovariada)."""
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.tabla_frecuencias(p['values'], p.get('bins', 'auto'), p.get('tipo', 'auto')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def tabla_doble_api(request):
    """Tabla de doble entrada (bivariada / contingencia)."""
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.tabla_doble(p['x'], p['y'], p.get('xname', 'X'),
                                               p.get('yname', 'Y'), p.get('xbins', 'auto'), p.get('ybins', 'auto')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
