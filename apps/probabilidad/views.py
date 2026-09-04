import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'probabilidad/index.html')


@csrf_exempt
@require_POST
def fit_api(request):
    """Ajuste de distribuciones + bondad de ajuste (KS, CvM, chi²), AIC/BIC, Q-Q."""
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.fit_all(p['values'], p.get('bins', 'auto')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def normalidad_api(request):
    """Batería de pruebas de normalidad."""
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.normalidad(p['values']))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def prob_api(request):
    """Calculadora de probabilidades sobre la distribución ajustada."""
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.prob_calc(p['dist'], p['params'], p['modo'],
                                             p.get('a'), p.get('b'), p.get('p')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
