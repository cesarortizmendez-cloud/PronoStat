import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import solver


def index(request):
    return render(request, 'descriptiva/index.html')


@csrf_exempt
@require_POST
def solve_api(request):
    try:
        p = json.loads(request.body.decode('utf-8') or '{}')
        return JsonResponse(solver.describe(p['values'], p.get('bins', 'auto')))
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
