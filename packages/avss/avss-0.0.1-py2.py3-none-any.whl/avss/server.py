from abc import ABC, abstractclassmethod
import socket
import threading
from typing import List
from queue import Queue

from avss.connection import Connection, HttpConnection
from avss.settings import get_logger, get_settings
from avss.message_bus import MessageBus, Message, ClientDoneMessage


logger = get_logger()
settings = get_settings()


class Server(ABC):

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.max_connections = int(settings['settings']['MAX_CONNECTIONS'])

        self._connections: Dict[int, Connection] = {}
        self._pending_connections = Queue()
        self._running = threading.Event()

    @abstractclassmethod
    def do_start(self):
        pass

    @abstractclassmethod
    def do_run(self):
        pass

    @abstractclassmethod
    def do_stop(self):
        pass

    def check_message_bus(self):
        message = MessageBus.get()
        if message is not None:
            if isinstance(message, ClientDoneMessage):
                logger.debug(f'Client {message.id} is done, removing reference con.')
                self._connections.pop(message.id)

    def respond_client(self, con: Connection):
        if len(self._connections) < self.max_connections:
            con.start()
            self._connections[con.id] = con
        else:
            self._pending_connections.put(con)

    def start(self):
        self.do_start()
        self._running.set()
        self.do_run()

    def stop(self):
        self._running.clear()
        self.do_stop()

    def is_running(self):
        return self._running.is_set()


class HttpServer(Server):

    def __init__(self, host='', port=6001):
        super().__init__(host, port)
        self._sock = None
        self._listen_timout = 1

    def do_start(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.settimeout(self._listen_timout)
        self._sock.bind((self.host, self.port))
        logger.info(f'Server listening at {self.host}:{self.port}')

    def do_run(self):
        if self._sock is None:
            logging.error('Cant run server without socket connection.')
            return

        self._sock.listen(0)

        while self.is_running():
            try:
                conn, addr = self._sock.accept()
                logger.debug(f'New connection at {addr}')
                self.respond_client(HttpConnection(conn, addr))
            except socket.timeout:
                self.check_message_bus()

    def do_stop(self):
        pass
