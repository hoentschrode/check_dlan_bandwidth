import urllib2


class MockInfo:
    """
    Mocked response info object (for accessing headers)
    """
    def __init__(self, headers):
        self._headers = headers

    def getheader(self, key):
        return self._headers.get(key)


class MockResponse:
    """
    Mocked response object
    """
    def __init__(self, resp_data, code=200, msg="Ok", headers=None):
        self._resp_data = resp_data
        self._code = code
        self._msg = msg
        self.headers = headers

    def read(self):
        if 400 <= self._code <= 499:
            raise urllib2.HTTPError('/', self._code, 'HTTP-error', hdrs=None, fp=None)
        if 500 <= self._code <= 599:
            raise urllib2.URLError('faked url error reason')
        return self._resp_data

    def getcode(self):
        return self._code

    def info(self):
        return MockInfo(self.headers)
