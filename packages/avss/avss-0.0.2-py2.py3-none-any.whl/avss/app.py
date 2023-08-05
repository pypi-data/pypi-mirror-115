from avss.http import HttpRequest, HttpResponse
from avss.parser import HttpParser


def default_main(self, http_request: HttpRequest) -> HttpResponse:
    return HttpParser.make_response('<h1>Hello World</h1>')
