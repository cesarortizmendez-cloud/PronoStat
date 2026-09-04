import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'sarimax/index.html')


@csrf_exempt
@require_POST
def run_api(request):
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.run(
            p['y'], p['X'], p['xnames'], tuple(p.get('order', [1, 0, 0])),
            tuple(p.get('seasonal', [0, 0, 0, 12])), p.get('include_c'),
            int(p.get('h', 12)), int(p.get('conf', 95)), int(p.get('holdout', 0)),
            p.get('x_future')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
