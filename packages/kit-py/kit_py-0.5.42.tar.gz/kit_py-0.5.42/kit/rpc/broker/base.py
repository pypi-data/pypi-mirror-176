# -*- coding: utf-8 -*-


class Broker:

    def __init__(self, queue, backend_store=None, middlewares=None):
        self.backend_store = backend_store
        self.queue = queue
        self.middlewares = []
        self.job = None

        if middlewares:
            for middleware in middlewares:
                self.add_middleware(middleware)

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)

    def send(self, message):
        """
        如果当前Broker是Job的to_broker, 则必须实现此方法
        """

    def consume(self, *args, **kwargs):
        """
        如果当前Broker是Job的from_broker, 则必须实现此方法
        """

    def before_emit(self, signal, *args, **kwargs):
        signal = "before_" + signal
        for middleware in self.middlewares:
            if hasattr(middleware, signal):
                getattr(middleware, signal)(self, *args, **kwargs)

    def after_emit(self, signal, *args, **kwargs):
        signal = "after_" + signal
        for middleware in self.middlewares:
            if hasattr(middleware, signal):
                getattr(middleware, signal)(self, *args, **kwargs)

    def __repr__(self):
        return f"<Broker {self.queue}>"
