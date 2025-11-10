# nuevo archivo: health endpoint simple
from django.http import JsonResponse

def health(request):
    """
    Health check endpoint para evidencias (200 OK).
    """
    return JsonResponse({"status": "ok"})