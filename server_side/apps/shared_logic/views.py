import os
from django.shortcuts import render
from server_side.apps.shared_logic.loggers import view_status_logger
from django.conf import settings
from django.http import HttpResponse, Http404


@view_status_logger
def download_logs(request):
    return work_logs(request, "application/text charset=utf-8")


@view_status_logger
def watch_logs(request):
    return work_logs(request, "text/plain")


@view_status_logger
def work_logs(request, type_pointer):
    file_path = os.path.join(settings.BASE_DIR, 'logs/dismart_admin.log')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=type_pointer)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

