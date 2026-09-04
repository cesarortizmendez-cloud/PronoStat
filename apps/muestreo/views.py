import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'muestreo/index.html')


def _b(request):
    return json.loads(request.body.decode('utf-8') or '{}')


@csrf_exempt
@require_POST
def extraer_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.extraer(
            p['rows'], p.get('metodo', 'mas'), int(p.get('n', 30)),
            p.get('estrato_col'), p.get('var'), p.get('seed')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def tam_media_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.tam_media(float(p['E']), float(p['sigma']), p.get('conf', 95), p.get('N')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def tam_prop_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.tam_prop(float(p['E']), float(p.get('p', 0.5)), p.get('conf', 95), p.get('N')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def asignacion_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.asignacion(int(p['n']), p['estratos']))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def estimar_srs_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.estimar_srs(p['values'], p.get('N'), p.get('conf', 95)))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def estimar_estr_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.estimar_estratificado(p['estratos'], p.get('conf', 95)))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
