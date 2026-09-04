import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'jerarquico/index.html')


@csrf_exempt
@require_POST
def run_api(request):
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.run(p['series'], p.get('modelo', 'holt'), int(p.get('h', 6)),
                                       int(p.get('m', 12)), int(p.get('holdout', 0)), int(p.get('conf', 95))))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
