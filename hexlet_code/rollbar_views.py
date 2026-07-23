from django.shortcuts import render
import rollbar
import sys


def handler404(request, exception):
    """Обработчик 404 ошибок с отправкой в Rollbar"""
    # Отправляем ошибку в Rollbar
    rollbar.report_exc_info(
        exc_info=sys.exc_info(),
        request=request,
        extra_data={'status_code': 404}
    )
    return render(request, '404.html', status=404)