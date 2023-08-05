from abc import ABC, abstractclassmethod
import threading

from avss.app_factory import AppFactory
from avss.message_bus import MessageBus, Message, ClientDoneMessage
from avss.settings import get_logger
from avss.parser import HttpParser

logger = get_logger()


class Connection(threading.Thread, ABC):

    def __init__(self, con, addr):
        self.con = con
        self.addr = addr
        self.id = addr[1]
        self._running = threading.Event()
        super().__init__(daemon=True)

    def run(self):
        self._running.set()
        self.do_run()

    def close(self):
        self._running.clear()
        self.con.close()
        MessageBus.put(ClientDoneMessage(self.id))

    def is_running(self):
        return self._running.is_set()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.id == self.id

    @abstractclassmethod
    def do_run(self):
        pass


class HttpConnection(Connection):

    def do_run(self):
        while self.is_running():
            # Receive message & parse Http Request
            msg = self.con.recv(2048)
            http_request = HttpParser.parse(msg.decode())

            # Find the correct app to serve with the given request.
            app = AppFactory.get_app(http_request)
            http_response = app(http_request)

            # Send the response to client.
            self.con.send(http_response.as_bytes())
            logger.debug(http_response.as_string())
            self.close()


class HttpsConnection(Connection):

    def do_run(self):
        pass