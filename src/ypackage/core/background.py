from threading import Thread, Timer


def do_background(func, args=(), kwargs={}):
    return Thread(target=func, args=args, kwargs=kwargs).start()


def do_delayed(func, duration, args=(), kwargs={}):
    return Timer(duration, func, args, kwargs).start()


def background(func):

    def inner(*args, **kwargs):
        do_background(func, args=args, kwargs=kwargs)

    return inner


def delayed(duration):
    def background(func):

        def inner(*args, **kwargs):
            do_delayed(func, duration, args=args, kwargs=kwargs)

        return inner
    return background
