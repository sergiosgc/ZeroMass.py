from zm.HTTPMessage import HTTPMessage
from urllib.parse import urlparse

class HTTPRequest(HTTPMessage):
    def __init__(self, url, method, headers = None, body = None, protocolVersion = '1.1'):
        self.url = url
        self.method = method.upper()
        super(HTTPRequest, self).__init__(headers=headers, body=body, protocolVersion=protocolVersion)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if isinstance(value, str):
            value = urlparse(value)
        self._url = value

    @property
    def scheme(self):
        return self.url.scheme

    @property
    def netloc(self):
        return self.url.netloc

    @property
    def path(self):
        return self.url.path

    @property
    def params(self):
        return self.url.params

    @property
    def query(self):
        return self.url.query

    @property
    def fragment(self):
        return self.url.fragment

    @property
    def username(self):
        return self.url.username

    @property
    def password(self):
        return self.url.password

    @property
    def hostname(self):
        return self.url.hostname

    @property
    def port(self):
        return self.url.port
