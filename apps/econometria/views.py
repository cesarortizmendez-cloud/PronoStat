import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'econometria/index.html')


@csrf_exempt
@require_POST
def ols_api(request):
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.ols(
            p['Y'], p['Xcols'], p['xnames'],
            p.get('yname', 'Y'), p.get('form', 'nivel'), int(p.get('conf', 95))))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
