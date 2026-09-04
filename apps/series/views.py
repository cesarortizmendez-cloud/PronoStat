import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'series/index.html')


def _b(request):
    return json.loads(request.body.decode('utf-8') or '{}')


@csrf_exempt
@require_POST
def descomponer_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.descomponer(p['y'], int(p.get('m', 12)), p.get('modelo', 'add')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def acf_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.acf_pacf(p['y'], p.get('nlags')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def estacionariedad_api(request):
    try:
        p = _b(request)
        return JsonResponse(solver.estacionariedad(
            p['y'], p.get('reg', 'c'), int(p.get('d', 0)), int(p.get('D', 0)), int(p.get('m', 12))))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
