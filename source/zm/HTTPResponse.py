from zm.HTTPMessage import HTTPMessage

class HTTPResponse(HTTPMessage):
    def __init__(self, headers = None, body = None, protocolVersion = '1.1'):
        self.resultCode = 0
        super(HTTPResponse, self).__init__(headers=headers, body=body, protocolVersion=protocolVersion)
