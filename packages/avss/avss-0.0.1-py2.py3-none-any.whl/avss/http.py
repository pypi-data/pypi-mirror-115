from abc import ABC, abstractclassmethod
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class HttpPacket(ABC):
    headers: Dict[str, str]
    body: str

    def as_string(self):
        packet = self.get_header() + '\r\n'
        packet += '\r\n'.join(f'{key}: {val}' for key, val in self.headers.items())
        packet += '\r\n\r\n'
        if self.body:
            packet += self.body
            packet += '\r\n\r\n'

        return packet

    def as_bytes(self):
        return self.as_string().encode('utf-8')

    @abstractclassmethod
    def get_header(self):
        pass


@dataclass
class HttpRequest(HttpPacket):
    method: str
    path: str
    version: str

    def get_header(self):
        return f'{self.method} {self.path} {self.version}'


@dataclass
class HttpResponse(HttpPacket):
    version: str
    status: str
    phrase: str

    def get_header(self):
        return f'{self.version} {self.status} {self.phrase}'
