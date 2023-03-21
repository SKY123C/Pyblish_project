
def set_order(order=0):
    def wrapper1(func, order=order):
        def wrapper2(*args):
            func(*args)
        wrapper2.order = order
        return wrapper2
    return wrapper1


class BaseControll(object):
    pass


