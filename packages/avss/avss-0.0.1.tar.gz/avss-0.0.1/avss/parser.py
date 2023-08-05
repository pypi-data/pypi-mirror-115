from datetime import datetime

from avss.http import HttpRequest, HttpResponse


class HttpParser:

    DEFAULT_VERSION = 'HTTP/1.0'
    DEFAULT_HEADERS = {
        'Content-Type': 'text/html; charset=utf-8',
        'Server': 'avss'
    }

    def parse(data: str):
        try:
            lines = data.splitlines()
            method, path, version = lines[0].split(' ')

            headers = {}
            body_index = None
            for index, line in enumerate(lines[1:]):
                if line == '\r\n':
                    body_index = index
                    break
                if line:
                    key, val = line.split(':', 1)
                    headers[key] = val

            if body_index is not None:
                body = lines[body_index:]
            else:
                body = ''

            return HttpRequest(headers, body, method, path, version)
        except IndexError:
            print(f'ERR {data}')

    @classmethod
    def get_headers(cls, kwargs: dict, data: str):
        headers = dict(cls.DEFAULT_HEADERS)
        headers['Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        headers['Content-Length'] = len(data)
        headers.update(kwargs)
        return headers

    @classmethod
    def make_response(cls, data: str, **kwargs):

        response = HttpResponse(
            version=kwargs.get('version', cls.DEFAULT_VERSION),
            status=kwargs.get('status', 200),
            phrase=kwargs.get('phrase', 'OK'),
            headers=cls.get_headers(kwargs, data),
            body=data
        )

        return response
