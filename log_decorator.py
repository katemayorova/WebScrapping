import datetime


def log_decorator_factory(log_file_name):
    def log_decorator(func):
        def log_func(*args, **kwargs):
            timestamp = datetime.datetime.now()
            result = func(*args, **kwargs)
            with open(log_file_name, 'w', encoding='utf-8') as log_file:
                print(f'{timestamp} Вызвана функция {func.__name__}, '
                      f'параметры: {[*args, *kwargs.values()]}, '
                      f'результат: {result}',
                      file=log_file)
            return result
        return log_func
    return log_decorator
