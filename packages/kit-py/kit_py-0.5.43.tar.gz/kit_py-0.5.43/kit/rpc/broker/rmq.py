# -*- coding: utf-8 -*-
from kit.rpc.store import get_store
from .base import Broker


class RMQBroker(Broker):

    def __init__(self, queue, backend_store=None, middlewares=None):
        super().__init__(queue, backend_store, middlewares)
        self.backend_store = backend_store or self._get_default_store()

    def send(self, message):
        self.backend_store.send(self.queue, message)

    def consume(self, *args, **kwargs):
        return self.backend_store.consume(self.queue, *args, **kwargs)

    @staticmethod
    def _get_default_store():
        return get_store()

    def __repr__(self):
        return f"<RMQBroker {self.queue}>"
