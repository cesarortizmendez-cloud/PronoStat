import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'intermitente/index.html')


def _b(request):
    return json.loads(request.body.decode('utf-8') or '{}')


@csrf_exempt
@require_POST
def run_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.run(
            p['y'], p.get('metodo', 'sba'), float(p.get('alpha', 0.1)),
            float(p.get('beta', 0.1)), int(p.get('h', 6)), bool(p.get('optimizar', False))))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def comparar_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.comparar(p['y'], float(p.get('alpha', 0.1)),
                                             float(p.get('beta', 0.1)), bool(p.get('optimizar', True))))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
