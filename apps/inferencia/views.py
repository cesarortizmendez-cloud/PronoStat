import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'inferencia/index.html')


def _body(request):
    return json.loads(request.body.decode('utf-8') or '{}')


@csrf_exempt
@require_POST
def ic_media_api(request):
    try:
        p = _body(request)
        return JsonResponse(solver.ic_media(
            values=p.get('values'), media=p.get('media'), s=p.get('s'),
            sigma=p.get('sigma'), n=p.get('n'), conf=p.get('conf', 95), N=p.get('N')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def ic_prop_api(request):
    try:
        p = _body(request)
        return JsonResponse(solver.ic_proporcion(
            x=p.get('x'), n=p.get('n'), phat=p.get('phat'),
            conf=p.get('conf', 95), N=p.get('N')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def n_media_api(request):
    try:
        p = _body(request)
        return JsonResponse(solver.n_media(
            float(p['E']), float(p['sigma']), p.get('conf', 95), p.get('N')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def n_prop_api(request):
    try:
        p = _body(request)
        return JsonResponse(solver.n_proporcion(
            float(p['E']), float(p.get('phat', 0.5)), p.get('conf', 95), p.get('N')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
