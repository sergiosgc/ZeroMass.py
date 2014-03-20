from collections import namedtuple

class HTTPHeader(namedtuple('HTTPHeader', 'name value')):
    __slots__ = ()
    def __str__(self):
        return '%s: %s' % self.name, self.value
    @staticmethod
    def fromString(header):
        name, value = str(header).split(':', 1)
        return HTTPHeader(name=name, value=value)


