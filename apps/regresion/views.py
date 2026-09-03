import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'regresion/index.html')


@csrf_exempt
@require_POST
def solve_api(request):
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.fit(
            p['x'], p['y'], p.get('model', 'lineal'),
            int(p.get('degree', 2)), p.get('predict_x')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def compare_api(request):
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.compare(p['x'], p['y'], p.get('models'), int(p.get('degree', 2))))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
