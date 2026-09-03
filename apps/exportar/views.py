import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import builder

XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def _xlsx(data, filename):
    resp = HttpResponse(data, content_type=XLSX)
    resp['Content-Disposition'] = f'attachment; filename="{filename}"'
    return resp


def _body(request):
    return json.loads(request.body.decode('utf-8') or '{}')


@csrf_exempt
@require_POST
def dataset(request):
    try:
        p = _body(request)
        data = builder.build_dataset(p['columns'], p['rows'], p.get('source', 'dataset'))
        return _xlsx(data, 'pronostat_dataset.xlsx')
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def descriptiva(request):
    try:
        p = _body(request)
        data = builder.build_descriptiva(p['columna'], p['resultado'])
        return _xlsx(data, f"descriptiva_{p['columna']}.xlsx")
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def regresion(request):
    try:
        p = _body(request)
        data = builder.build_regresion(p.get('ctx', {}), p['resultado'])
        return _xlsx(data, f"regresion_{p['resultado'].get('model','modelo')}.xlsx")
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)


@csrf_exempt
@require_POST
def pronostico(request):
    try:
        p = _body(request)
        data = builder.build_pronostico(p.get('ctx', {}), p['resultado'])
        return _xlsx(data, f"pronostico_{p['resultado'].get('model','modelo')}.xlsx")
    except Exception as e:
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=400)
