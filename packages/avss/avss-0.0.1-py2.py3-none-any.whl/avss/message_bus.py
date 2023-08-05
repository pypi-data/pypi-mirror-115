from typing import List
from queue import Queue


class Message:
    pass

class ClientDoneMessage:
    def __init__(self, id: int):
        self.id = id

class MessageBus:

    _messages = Queue()

    @classmethod
    def put(cls, message: Message):
        cls._messages.put(message)

    @classmethod
    def get(cls):
        if not cls._messages.empty():
            return cls._messages.get_nowait()
        return None
