from zm.HTTPHeader import HTTPHeader

class HTTPMessage(object):
    def __init__(self,headers = None, body = None, protocolVersion = '1.1'):
        self.protocolVersion = protocolVersion
        self.headers = {}
        if headers is not None:
            for header in headers:
                self.addHeader(header)

        if body is None:
            self.body = b''
        else:
            self.body = body

    def addHTTPHeader(self, header):
        if header.name not in self.headers:
            self.headers[header.name] = []
        self.headers[header.name].append(header.value)

    def addHeader(self, headerOrName, value = None):
        if value is None:
            if isinstance(headerOrName, str):
                return self.addHTTPHeader(HTTPHeader.fromString(headerOrName))
            else:
                return self.addHTTPHeader(headerOrName)
        else:
            return self.addHTTPHeader(HTTPHeader(name=headerOrName, value=value))

    def containsHeader(self, name):
        return name in self.headers

    def getAllHeaders(self):
        return (HTTPHeader(name=name, value=value) for name,valueArray in self.headers.iteritems() for value in valueArray)

    def getHeader(self, name):
        return self.getFirstHeader(name)

    def getFirstHeader(self, name):
        if name not in self.headers or len(self.headers[name]) == 0:
            raise Exception("Header %s does not exist" % name)
        return self.headers[name][0]

    def getHeaders(self, name):
        if name not in self.headers:
            raise Exception("Header %s does not exist" % name)
        return (HTTPHeader(name=name, value=value) for value in self.headers[name])
    
    def getLastHeader(self, name):
        if name not in self.headers or len(self.headers[name]) == 0:
            raise Exception("Header %s does not exist" % name)
        return self.headers[name][len(self.headers[name]) - 1]

    def getProtocolVersion(self):
        return self.protocolVersion

    def headerIterator(self, name=None):
        if name is None:
            return self.getAllHeaders()
        else:
            return self.getHeaders(name)

    def removeHeader(self, headerOrName, value=None):
        if value is None:
            if isinstance(headerOrName, str):
                name = headerOrName
                if name not in self.headers or len(self.headers[name]) == 0:
                    raise Exception("Header %s does not exist" % name)
                if len(self.headers[name]) != 1:
                    raise Exception("removeHeader called with just a header name (%s), but there are multiple headers named %s" % name, name)
                del self.headers[name]
            else:
                name = headerOrName.name
                if name not in self.headers:
                    raise Exception("Header %s does not exist" % name)
                try:
                    self.headers[name].remove(headerOrName)
                except Exception as e:
                    raise Exception("Header %s does not exist" % name, e)
        else:
            self.removeHeader(HTTPHeader(name=headerOrName, value=value))

    def removeHeaders(self, name):
        if name not in self.headers or len(self.headers[name]) == 0:
            raise Exception("Header %s does not exist" % name)
        del self.headers[name]

    def setHeader(self, headerOrName, value=None):
        if value is None and isinstance(headerOrName, str):
            return self.setHeader(HTTPHeader.fromString(headerOrName))
        if value is not None:
            return self.setHeader(HTTPHeader(name=headerOrName, value=value))
        header = headerOrName
        if header.name not in self.headers or len(self.headers[header.name]) == 0:
            return self.addHeader(header)
        self.headers[header.name][0] = header.value

    def setHeaders(self, headers):
        self.headers = {}
        for header in headers:
            self.addHeader(header)
    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        if not isinstance(body, bytes):
            raise AttributeError
        self._body = body
