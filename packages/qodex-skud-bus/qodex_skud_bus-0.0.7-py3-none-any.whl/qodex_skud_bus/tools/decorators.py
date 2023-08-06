from qodex_skud_bus.tools.exceptions import UnknownPoint
from traceback import format_exc


def point_operating(func):
    """ Декоратор, оборачивающий выполнение всех работ с точками доступа """
    def wrapper(*args, **kwargs):
        try:
            try:
                point_name = kwargs['point_name_str']
            except KeyError:
                point_name = args[1]
            func_name = locals()['func'].__name__
            point_state = func(*args, **kwargs)
            return {'status': True, 'point_name': point_name,
                    'func_name': func_name, 'point_state': point_state}
        except UnknownPoint:
            return {'status': False, 'info': format_exc()}
    return wrapper
