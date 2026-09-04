import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'arima/index.html')


def _b(request):
    return json.loads(request.body.decode('utf-8') or '{}')


@csrf_exempt
@require_POST
def run_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.run(
            p['y'], tuple(p.get('order', [1, 0, 0])), tuple(p.get('seasonal', [0, 0, 0, 12])),
            p.get('include_c'), int(p.get('h', 12)), int(p.get('conf', 95)), int(p.get('holdout', 0))))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def auto_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.auto(
            p['y'], p.get('d'), int(p.get('D', 0)), int(p.get('m', 12)),
            int(p.get('pmax', 2)), int(p.get('qmax', 2)),
            int(p.get('Pmax', 1)), int(p.get('Qmax', 1)),
            bool(p.get('seasonal', True)), p.get('ic', 'aicc')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def rolling_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.rolling_origin(
            p['y'], tuple(p.get('order', [1, 1, 1])), tuple(p.get('seasonal', [0, 0, 0, 12])),
            p.get('include_c'), int(p.get('h', 1)), p.get('min_train'),
            int(p.get('paso', 1)), p.get('ventana', 'expansiva')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
