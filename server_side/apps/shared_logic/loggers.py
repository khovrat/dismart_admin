import functools
import logging
from django.http import Http404
from django.shortcuts import render


logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(message)s',
    filename='logs/dismart_admin.log',
)


def view_status_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ex_args = ""
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            logging.exception('~' * 30 + 'Errors happened' + 30 * '~')
            ex_args = e
        else:
            return res
        kwargs['context'] = {'msg': ex_args}
        kwargs['template_name'] = 'errors/error500.html'
        return render(*args, **kwargs)

    return wrapper


def class_status_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            logging.exception('~' * 30 + 'Errors happened' + 30 * '~')
            raise Http404("Query error occurred.", e.args)
        return res

    return wrapper